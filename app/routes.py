import json, openai, re
from flask import Blueprint, render_template, request, jsonify, session
from .config import Config, get_db_connection

openai.api_key = Config.OPENAI_API_KEY
main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Inicializamos el historial como lista vacía
    session['chat_history'] = []
    return render_template('index.html')

@main.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('input', '')
    history = session.get('chat_history', [])

    try:
        # PASO 1: EXTRAER FILTROS
        prompt_filtros = f"Usuario: {user_input}. Responde SOLO un JSON con: genero (Hombre/Mujer/Unisex), palabras_clave (lista de notas), cantidad (3)."
        
        res_filtros = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un extractor de datos. Solo respondes JSON puro."},
                {"role": "user", "content": prompt_filtros}
            ],
            temperature=0
        )
        
        content = res_filtros['choices'][0]['message']['content']
        
        # Limpieza de JSON por si la IA agrega texto extra
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            filtros = json.loads(match.group())
        else:
            filtros = {"genero": "Unisex", "palabras_clave": ["fresco"], "cantidad": 3}

        # PASO 2: BÚSQUEDA SQL
        conn = get_db_connection()
        cursor = conn.cursor()
        
        palabras = filtros.get('palabras_clave', ['fresco'])
        genero = filtros.get('genero', 'Unisex')
        cantidad = filtros.get('cantidad', 3)

        # Construcción de la consulta dinámica
        query_parts = " OR ".join(["notas LIKE ?" for _ in palabras])
        sql = f"SELECT TOP (?) nombre, marca, notas, imagen_url FROM Perfumes WHERE ({query_parts}) AND genero = ? ORDER BY NEWID()"
        
        # Parámetros: [cantidad, %nota1%, %nota2%, ..., genero]
        params = [cantidad] + [f"%{p}%" for p in palabras] + [genero]
        
        cursor.execute(sql, params)
        perfumes_sql = cursor.fetchall()
        conn.close()

        # PASO 3: RESPUESTA FINAL
        if perfumes_sql:
            lista_nombres = ", ".join([p[0] for p in perfumes_sql])
            prompt_final = f"El usuario busca: {user_input}. Recomienda estos: {lista_nombres}. Sé breve y usa negritas."
            
            mensajes_chat = [{"role": "system", "content": "Eres un sommelier de perfumes breve."}]
            # Agregamos los últimos 4 mensajes del historial para contexto
            mensajes_chat.extend(history[-4:])
            mensajes_chat.append({"role": "user", "content": prompt_final})

            res_final = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=mensajes_chat
            )
            texto_ia = res_final['choices'][0]['message']['content']

            # Actualizar memoria (Guardamos entrada real del usuario y respuesta de IA)
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": texto_ia})
            session['chat_history'] = history[-6:] # Mantener solo los últimos 6
            session.modified = True # Importante para que Flask guarde la sesión

            # Generar HTML de las tarjetas
            html_cards = '<div class="perfume-grid">'
            for p in perfumes_sql:
                html_cards += f'''
                <div class="perfume-card">
                    <img src="{p[3]}" alt="{p[0]}">
                    <h4>{p[0]}</h4>
                    <span>{p[1]}</span>
                </div>'''
            html_cards += '</div>'

            return jsonify({'response': texto_ia, 'image': html_cards})

        return jsonify({'response': "No encontré coincidencias exactas, ¿intentamos con otras notas?", 'image': ''})

    except Exception as e:
        print(f"ERROR REAL: {e}")
        