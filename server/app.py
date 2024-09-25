from flask import Flask, jsonify
from flask_cors import CORS  # Importa CORS
import psycopg2

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Habilita CORS para todas las rutas de la API

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        conn = psycopg2.connect(
            dbname="ecommerce_ikfq",
            user="ecommerce_ikfq_user",
            password="Tdkv6RKytsf5d1pACeRJicF8tG2Ec2ON",
            host="dpg-crq0213v2p9s738di0j0-a.frankfurt-postgres.render.com",
            port="5432"
        )
        cur = conn.cursor()

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
