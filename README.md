# PERFUMES3
Proyecto de Sistemas Inteligentes
Documentación del Proyecto PERFUMES
1. Descripción del proyecto
PERFUMES es una aplicación web desarrollada en Python con Flask que funciona como
un asistente inteligente para la recomendación de perfumes. El sistema permite a los
usuarios ingresar descripciones en lenguaje natural (por ejemplo: preferencias de
aromas, sensaciones o género), y a partir de ello genera recomendaciones
personalizadas utilizando inteligencia artificial y una base de datos relacional.
El flujo principal del sistema combina:
• Procesamiento de lenguaje natural mediante la API de OpenAI.
• Extracción automática de filtros (género, notas aromáticas y cantidad de resultados).
• Consulta dinámica a una base de datos SQL Server con perfumes registrados.
• Generación de respuestas explicativas y visuales para el usuario final.
El objetivo principal del proyecto es demostrar la integración de IA generativa con un
sistema web tradicional orientado a la toma de decisiones y recomendaciones
personalizadas.
2. Tecnologías utilizadas
Lenguajes y Frameworks
• Python 3: Lenguaje principal del proyecto.
• Flask: Framework web ligero para la creación del servidor y manejo de rutas.
• HTML / CSS / JavaScript: Para la interfaz de usuario (plantillas Flask).
Inteligencia Artificial
• OpenAI API (GPT-3.5-Turbo):
o Extracción de filtros desde texto en lenguaje natural.
o Generación de recomendaciones breves y explicativas.
Base de Datos
• SQL Server: Base de datos relacional que almacena la información de los perfumes.
• pyodbc: Conector para la comunicación entre Python y SQL Server.
Otras Tecnologías
• Sesiones de Flask: Para mantener el historial de conversación del usuario.
• Entorno virtual (venv): Aislamiento de dependencias del proyecto.
3. Arquitectura del sistema
El sistema sigue una arquitectura cliente-servidor con separación lógica de
responsabilidades:
Componentes principales
1. Cliente (Frontend)
o Interfaz web donde el usuario escribe sus preferencias.
o Muestra recomendaciones en formato de texto y tarjetas visuales de perfumes.
2. Servidor Flask (Backend)
o run.py: Punto de entrada de la aplicación.
o app/__init__.py: Inicialización de la app Flask y registro de Blueprints.
o routes.py: Lógica principal del sistema.
▪ Recepción de la entrada del usuario.
▪ Comunicación con OpenAI.
▪ Construcción dinámica de consultas SQL.
▪ Retorno de resultados en formato JSON.
3. Módulo de Configuración
o config.py: Manejo de variables sensibles (API Key, conexión a BD).
4. Base de Datos SQL Server
o Tabla Perfumes con campos como:
▪ nombre
▪ marca
▪ notas
▪ genero
▪ imagen_url
Flujo de funcionamiento
1. El usuario ingresa una descripción en lenguaje natural.
2. La API de OpenAI extrae filtros estructurados en formato JSON.
3. El backend construye una consulta SQL dinámica basada en esos filtros.
4. Se obtienen perfumes aleatorios que coinciden con los criterios.
5. OpenAI genera una recomendación textual final.
6. El sistema devuelve texto e imágenes al frontend.
4.Evidencias del entrenamiento
El proyecto no entrena un modelo propio, sino que utiliza un modelo preentrenado de
OpenAI (GPT-3.5-Turbo) mediante ingeniería de prompts. Las evidencias del
“entrenamiento” se reflejan en:
• Uso de prompts estructurados para forzar respuestas en formato JSON.
• Ajuste de parámetros como temperature = 0 para respuestas deterministas.
• Validación y limpieza de respuestas del modelo mediante expresiones regulares.
• Contextualización de respuestas usando historial de conversación (memoria corta).
Estas prácticas permiten simular un comportamiento entrenado y controlado, asegurando
respuestas coherentes y útiles sin necesidad de entrenar un modelo desde cero.
