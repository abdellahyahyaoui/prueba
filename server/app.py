import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
import MySQLdb.cursors
import stripe

# Cargar las variables desde el archivo .env
load_dotenv()

# Verificar que las variables de entorno se han cargado correctamente
print("MYSQL_USER:", os.environ.get('MYSQL_USER'))
print("MYSQL_PASSWORD:", os.environ.get('MYSQL_PASSWORD'))

app = Flask(__name__)

# Habilita CORS para permitir solicitudes desde otros dominios
CORS(app)

# Configuración de MySQL desde las variables de entorno
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

mysql = MySQL(app)

# Configuración de Stripe desde las variables de entorno
stripe.api_key = os.environ.get('STRIPE_API_KEY')

@app.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API de Ecommerce"})

@app.route('/api/productos', methods=['GET'])
def get_productos():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        cursor.close()
        return jsonify(productos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/productos', methods=['POST'])
def add_productos():
    try:
        datos = request.get_json()
        
        cursor = mysql.connection.cursor()
        for producto in datos:
            cursor.execute('''INSERT INTO productos (_id, title, isNew, oldPrice, price, description, category, image, rating) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                           (producto['_id'], producto['title'], producto['isNew'], producto['oldPrice'], 
                            producto['price'], producto['description'], producto['category'], 
                            producto['image'], producto['rating']))
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'mensaje': 'Productos añadidos exitosamente.'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pay', methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        items = data['items']  # Los items deberían tener id y cantidad
        email = data['email']
        
        # Crear la sesión de checkout en Stripe
        line_items = []
        for item in items:
            line_items.append({
                'price_data': {
                    'currency': 'eur',  # Cambia a tu moneda
                    'product_data': {
                        'name': item['title'],
                        'images': [item['image']],
                    },
                    'unit_amount': int(item['price'] * 100),  # Precio en centavos
                },
                'quantity': item['quantity'],
            })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}',  # Cambia esto a tu URL de éxito
            cancel_url='http://localhost:3000/cancel',  # Cambia esto a tu URL de cancelación
            customer_email=email,
        )

        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
