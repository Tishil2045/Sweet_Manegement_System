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