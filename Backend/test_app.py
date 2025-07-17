import unittest
from app import app, db, Sweet

class SweetShopTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Reset database before each test
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_sweet(self):
        sweet_data = {
            "name": "Kaju Katli",
            "category": "Nut-Based",
            "price": 50,
            "quantity": 20
        }
        response = self.client.post('/sweets', json=sweet_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], "Kaju Katli")
        self.assertEqual(data['category'], "Nut-Based")
        self.assertEqual(data['price'], 50)
        self.assertEqual(data['quantity'], 20)

    def test_view_all_sweets(self):
        # Add a couple of sweets to the database first
        sweet1 = Sweet(name="Kaju Katli", category="Nut-Based", price=50, quantity=20)
        sweet2 = Sweet(name="Gulab Jamun", category="Milk-Based", price=30, quantity=10)

        with app.app_context():
            db.session.add_all([sweet1, sweet2])
            db.session.commit()

        # Call the GET endpoint
        response = self.client.get('/sweets')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "Kaju Katli")
        self.assertEqual(data[1]["name"], "Gulab Jamun")