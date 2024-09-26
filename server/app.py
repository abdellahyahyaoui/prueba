from flask import Flask, jsonify, request
from flask_cors import CORS  # Importar CORS
import psycopg2
import os
import stripe
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar Flask
app = Flask(__name__)

# Configura CORS para permitir tu frontend
CORS(app, resources={r"/api/*": {"origins": "https://prueba-5a9a3.web.app"}})  # Ajusta esto si es necesario

# Configura tus credenciales de la base de datos usando variables de entorno
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Configura la clave secreta de Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

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

@app.route('/api/pay', methods=['POST'])
def pay():
    try:
        data = request.json
        items = data['items']
        email = data['email']

        # Crear una sesión de Stripe Checkout
        line_items = []
        for item in items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',  # Cambia la moneda según sea necesario
                    'product_data': {
                        'name': item['title'],
                        'images': [item['image']],
                    },
                    'unit_amount': int(item['price'] * 100),  # El precio debe estar en centavos
                },
                'quantity': item['quantity'],
            })

        # Crear la sesión de Stripe Checkout
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://tu-frontend-url/success',  # Cambia esto a la URL de éxito de tu frontend
            cancel_url='https://tu-frontend-url/cancel',    # Cambia esto a la URL de cancelación de tu frontend
            customer_email=email,
        )

        return jsonify({'id': checkout_session.id})

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT')), debug=True)
