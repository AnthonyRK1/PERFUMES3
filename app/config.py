import os
import pyodbc

class Config:
    # Tu API Key de OpenAI
    OPENAI_API_KEY = ''
    
    # Llave para evitar el RuntimeError de sesiones
    SECRET_KEY = 'qwertyuiop123456789'
    
    # Datos de tu base de datos BB
    SERVER = r"HUAWEI-D15\SQLEXPRESS"  
    DATABASE = "PERFUMES_NUEVA" 
    DRIVER = "ODBC Driver 18 for SQL Server"  

def get_db_connection():
    config = Config()
    conn = pyodbc.connect(
        f"DRIVER={{{config.DRIVER}}};"
        f"SERVER={config.SERVER};"
        f"DATABASE={config.DATABASE};"
        "Trusted_Connection=yes;" 
        "TrustServerCertificate=yes;"
    )
    return conn