from app import create_app
import os

app = create_app()
app.secret_key = 'qwertyuiop123456789' # Esta llave es perfecta

if __name__ == '__main__':
    app.run(debug=True) 