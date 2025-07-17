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