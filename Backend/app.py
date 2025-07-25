from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sweetshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB Model
class Sweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity
        }

# Create DB
with app.app_context():
    db.create_all()
    # TEMP: Add a test sweet if DB is empty
    with app.app_context():
        if not Sweet.query.first():
            test = Sweet(name="Kaju Katli", category="Nut-Based", price=50, quantity=20)
            db.session.add(test)
            db.session.commit()


@app.route("/")
def home():
    return "Sweet Shop API is running."

@app.route('/sweets', methods=['POST'])
def add_sweet():
    data = request.get_json()
    name = data.get('name')
    category = data.get('category')
    price = data.get('price')
    quantity = data.get('quantity')

    # Validation (optional for now)
    if not name or not category or price is None or quantity is None:
        return jsonify({"error": "Missing required fields"}), 400

    # Create sweet
    new_sweet = Sweet(
        name=name,
        category=category,
        price=price,
        quantity=quantity
    )
    db.session.add(new_sweet)
    db.session.commit()

    return jsonify(new_sweet.to_dict()), 201

@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    return jsonify([s.to_dict() for s in sweets]), 200

@app.route('/sweets/<int:sweet_id>', methods=['DELETE'])
def delete_sweet(sweet_id):
    sweet = Sweet.query.get(sweet_id)
    if not sweet:
        return jsonify({"error": "Sweet not found"}), 404

    db.session.delete(sweet)
    db.session.commit()
    return jsonify({"message": "Sweet deleted"}), 200

@app.route('/sweets/<int:sweet_id>', methods=['PUT'])
def update_sweet(sweet_id):
    sweet = Sweet.query.get(sweet_id)
    if not sweet:
        return jsonify({"error": "Sweet not found"}), 404

    data = request.get_json()
    sweet.name = data.get("name", sweet.name)
    sweet.category = data.get("category", sweet.category)
    sweet.price = data.get("price", sweet.price)
    sweet.quantity = data.get("quantity", sweet.quantity)

    db.session.commit()
    return jsonify(sweet.to_dict()), 200

@app.route('/sweets/search', methods=['GET'])
def search_sweets():
    name = request.args.get('name', '').lower()
    category = request.args.get('category', '').lower()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    query = Sweet.query

    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)

    results = query.all()
    return jsonify([s.to_dict() for s in results]), 200

@app.route('/sweets/<int:sweet_id>/purchase', methods=['POST'])
def purchase_sweet(sweet_id):
    sweet = Sweet.query.get(sweet_id)
    if not sweet:
        return jsonify({"error": "Sweet not found"}), 404

    data = request.get_json()
    quantity_to_purchase = data.get('quantity', 0)

    if not isinstance(quantity_to_purchase, int) or quantity_to_purchase <= 0:
        return jsonify({"error": "Invalid purchase quantity"}), 400

    if sweet.quantity < quantity_to_purchase:
        return jsonify({"error": "Not enough stock"}), 400

    sweet.quantity -= quantity_to_purchase
    db.session.commit()

    return jsonify({
        "message": "Purchase successful",
        "remaining_quantity": sweet.quantity,
        "sweet": sweet.to_dict()
    }), 200


@app.route('/sweets/<int:sweet_id>/restock', methods=['POST'])
def restock_sweet(sweet_id):
    sweet = Sweet.query.get(sweet_id)
    if not sweet:
        return jsonify({"error": "Sweet not found"}), 404

    data = request.get_json()
    quantity_to_add = data.get('quantity', 0)

    if not isinstance(quantity_to_add, int) or quantity_to_add <= 0:
        return jsonify({"error": "Invalid restock quantity"}), 400

    sweet.quantity += quantity_to_add
    db.session.commit()

    return jsonify({
        "message": "Restock successful",
        "new_quantity": sweet.quantity,
        "sweet": sweet.to_dict()
    }), 200



if __name__ == '__main__':
    app.run(debug=True)
