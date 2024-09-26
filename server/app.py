from flask import Flask, jsonify
import psycopg2
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configura tus credenciales de la base de datos usando variables de entorno
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return None

@app.route('/api/productos', methods=['GET'])
def get_products_api():
    return fetch_products()

def fetch_products():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ecommerce_products;')
        rows = cursor.fetchall()

        products = []
        for row in rows:
            product = {
                "_id": row[0],  # id
                "title": row[1],  # product_name
                "description": row[2],  # description
                "category": row[3],  # category
                "image": row[4],  # image_url
                "isAvailable": row[5],  # is_available
                "oldPrice": str(row[6]),  # original_price como string
                "price": float(row[7]),  # sale_price
                "discount": float(row[8]) if row[8] is not None else None,  # discount
                "rating": 0  # Puedes establecer una lógica para la calificación si es necesario
            }
            products.append(product)

        cursor.close()
        conn.close()

        return jsonify(products)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT')), debug=True)
