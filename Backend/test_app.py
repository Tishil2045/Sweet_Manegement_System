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

    def test_delete_sweet(self):
        # Add a sweet to delete
        sweet = Sweet(name="Jalebi", category="Sugar-Based", price=25, quantity=15)
        with app.app_context():
            db.session.add(sweet)
            db.session.commit()
            sweet_id = sweet.id

        # Delete the sweet
        response = self.client.delete(f'/sweets/{sweet_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Sweet deleted"})

        # Confirm it no longer exists
        with app.app_context():
            deleted = Sweet.query.get(sweet_id)
            self.assertIsNone(deleted)

    def test_update_sweet(self):
        # First, add a sweet to update
        sweet = Sweet(name="Rasgulla", category="Milk-Based", price=20, quantity=30)
        with app.app_context():
            db.session.add(sweet)
            db.session.commit()
            sweet_id = sweet.id

        # Data to update
        updated_data = {
            "name": "Rasgulla Deluxe",
            "category": "Milk-Based",
            "price": 25,
            "quantity": 50
        }

        # Call the update API
        response = self.client.put(f'/sweets/{sweet_id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertEqual(data['name'], "Rasgulla Deluxe")
        self.assertEqual(data['price'], 25)
        self.assertEqual(data['quantity'], 50)

    def test_search_sweets(self):
        # Add sample sweets
        with app.app_context():
            db.session.add_all([
                Sweet(name="Kaju Katli", category="Nut-Based", price=50, quantity=10),
                Sweet(name="Gulab Jamun", category="Milk-Based", price=30, quantity=15),
                Sweet(name="Gajar Halwa", category="Vegetable-Based", price=40, quantity=20)
            ])
            db.session.commit()

        # Search by partial name
        response = self.client.get('/sweets/search?name=kaju')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Kaju Katli")

        # Search by category
        response = self.client.get('/sweets/search?category=Milk-Based')
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Gulab Jamun")

        # Search by price range
        response = self.client.get('/sweets/search?min_price=35&max_price=55')
        data = response.get_json()
        self.assertEqual(len(data), 2)

    def test_purchase_sweet():
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        client = app.test_client()

        with app.app_context():
            db.create_all()
            sweet = Sweet(name="Kaju Katli", price=50.0, quantity=2, category="Dry Fruit")
            db.session.add(sweet)
            db.session.commit()
            sweet_id = sweet.id

        # Case 1: Successful purchase
        response = client.post(f'/sweets/{sweet_id}/purchase')
        assert response.status_code == 200
        assert response.get_json()['quantity'] == 1

        # Case 2: Out of stock
        with app.app_context():
            sweet = Sweet.query.get(sweet_id)
            sweet.quantity = 0
            db.session.commit()

        response = client.post(f'/sweets/{sweet_id}/purchase')
        assert response.status_code == 400
        assert "Out of stock" in response.get_json()['error']

        # Case 3: Invalid sweet ID
        response = client.post('/sweets/9999/purchase')
        assert response.status_code == 404
        assert "Sweet not found" in response.get_json()['error']

    def test_restock_sweet():
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        client = app.test_client()

        with app.app_context():
            db.create_all()
            sweet = Sweet(name="Barfi", price=40.0, quantity=3, category="Milk")
            db.session.add(sweet)
            db.session.commit()
            sweet_id = sweet.id

        # Case 1: Successful restock
        response = client.post(f'/sweets/{sweet_id}/restock')
        assert response.status_code == 200
        assert response.get_json()['quantity'] == 4

        # Case 2: Invalid sweet ID
        response = client.post('/sweets/9999/restock')
        assert response.status_code == 404
        assert "Sweet not found" in response.get_json()['error']