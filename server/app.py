from flask import Flask, jsonify
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        # Conectar a la base de datos utilizando la variable de entorno DATABASE_URL
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor()

        # Consultar la tabla
        cur.execute("""
            SELECT 
                id, 
                product_name AS title, 
                description, 
                category, 
                image_url AS image, 
                is_available AS isNew, 
                original_price AS oldPrice, 
                sale_price AS price 
            FROM ecommerce_products;
        """)
        
        rows = cur.fetchall()

        products = []
        for row in rows:
            product = {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "category": row[3],
                "image": row[4],
                "isNew": 1 if row[5] else 0,
                "oldPrice": f"{row[6]:.2f}",
                "price": f"{row[7]:.2f}",
                "calificacion": None
            }
            products.append(product)

        cur.close()
        conn.close()

        return jsonify(products)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
