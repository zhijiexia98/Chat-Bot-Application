import unittest
from app import app, db, ChatHistory

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        # Configure the app for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xiazhijie:Shinyway123!@localhost:5432/xiazhijie'
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Initialize the database for testing
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Ensures that the database is emptied for next test
        with app.app_context():
            db.drop_all()

    def test_message_storing(self):
        # Send a POST request to the API with a test message
        response = self.app.post('/api', json={'message': 'Hello, world!'})

        # Check if the response is valid
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)

        # Query the database for the inserted chat history
        with app.app_context():
            chat_history = ChatHistory.query.one()
            self.assertIsNotNone(chat_history)
            self.assertEqual(chat_history.user_message, 'Hello, world!')
            # Here we assume the AI response is not empty, but in a real test,
            # you might want to mock the OpenAI API response
            self.assertNotEqual(chat_history.ai_response, '')

    def test_empty_message_handling(self):
        response = self.app.post('/api', json={'message': ''})
        self.assertEqual(response.status_code, 400)  # Assuming the app returns 400 for empty messages
        self.assertIn("Empty message received", response.get_json().get("response", ""))
        with app.app_context():
            count = ChatHistory.query.count()
            self.assertEqual(count, 0)  # No new records should be added

    def test_non_english_message_storing(self):
        test_message = '你好，中国！'
        response = self.app.post('/api', json={'message': test_message})
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            chat_history = ChatHistory.query.one()
            self.assertIsNotNone(chat_history)
            self.assertEqual(chat_history.user_message, test_message)


if __name__ == '__main__':
    unittest.main()
