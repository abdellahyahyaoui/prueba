from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import stripe
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilitar CORS
port = int(os.getenv("PORT", 5000))  # Valor por defecto si no se establece en .env
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route("/")
def hello_world():
    return "Hello World!"

# Nueva ruta para obtener los productos
@app.route("/productos", methods=["GET"])
def get_productos():
    productos = [
        {"id": 1, "nombre": "Producto 1", "precio": 100},
        {"id": 2, "nombre": "Producto 2", "precio": 200},
        {"id": 3, "nombre": "Producto 3", "precio": 300},
        {"id": 4, "nombre": "Producto 4", "precio": 400},
        {"id": 5, "nombre": "Producto 5", "precio": 500},
    ]
    return jsonify(productos)

@app.route("/pay", methods=["POST"])
def pay():
    try:
        data = request.get_json()
        items = data.get("items")
        email = data.get("email")

        # Verificar si 'items' y 'email' están presentes
        if not items or not email:
            return jsonify({"message": "Bad Request"}), 400

        # Extraer datos de los ítems
        extracting_items = [{
            'quantity': item['quantity'],
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(item['price'] * 100),  # Convertir a centavos
                'product_data': {
                    'name': item['title'],
                    'description': item['description'],
                    'images': [item['image']],
                },
            },
        } for item in items]

        # Crear la sesión de pago en Stripe
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=extracting_items,
            mode="payment",
            success_url=f"http://localhost:{port}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"http://localhost:{port}/cancel",
            metadata={"email": email},
        )

        return jsonify({
            "message": "Connection is Active",
            "success": True,
            "id": session.id
        })
    except Exception as e:
        print(f"Error: {e}")  # Imprimir el error exacto
        return jsonify({"message": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(port=port)
