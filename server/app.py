import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configura la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para la tabla ecommerce_products
class Product(db.Model):
    __tablename__ = 'ecommerce_products'
    
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    original_price = db.Column(db.Numeric(10, 2), nullable=False)
    sale_price = db.Column(db.Numeric(10, 2), nullable=False)

# Ruta para obtener todos los productos
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([{
            'id': product.id,
            'product_name': product.product_name,
            'description': product.description,
            'category': product.category,
            'image_url': product.image_url,
            'is_available': product.is_available,
            'original_price': str(product.original_price),
            'sale_price': str(product.sale_price)
        } for product in products])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener un producto específico por ID
@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify({
            'id': product.id,
            'product_name': product.product_name,
            'description': product.description,
            'category': product.category,
            'image_url': product.image_url,
            'is_available': product.is_available,
            'original_price': str(product.original_price),
            'sale_price': str(product.sale_price)
        })
    return jsonify({'message': 'Product not found'}), 404

# Ruta para crear un nuevo producto
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(
        product_name=data['product_name'],
        description=data.get('description'),
        category=data.get('category'),
        image_url=data.get('image_url'),
        is_available=data.get('is_available', True),
        original_price=data['original_price'],
        sale_price=data['sale_price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created', 'id': new_product.id}), 201

# Ruta para actualizar un producto
@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get(id)
    if product:
        product.product_name = data.get('product_name', product.product_name)
        product.description = data.get('description', product.description)
        product.category = data.get('category', product.category)
        product.image_url = data.get('image_url', product.image_url)
        product.is_available = data.get('is_available', product.is_available)
        product.original_price = data.get('original_price', product.original_price)
        product.sale_price = data.get('sale_price', product.sale_price)
        
        db.session.commit()
        return jsonify({'message': 'Product updated'})
    return jsonify({'message': 'Product not found'}), 404

# Ruta para eliminar un producto
@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'})
    return jsonify({'message': 'Product not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)
