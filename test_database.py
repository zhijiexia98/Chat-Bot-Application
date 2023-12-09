import unittest
from app import app, db, ChatHistory

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        # Configure the app for testing
        # test database url
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xiazhijie:Shinyway123!@localhost:5432/postgres'
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Initialize the database for testing
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clear all the testing input
        with app.app_context():
            db.drop_all()
            db.create_all()

    def test_message_storing(self):
        # Send a POST request to the API with a test message
        response = self.app.post('/api', json={'message': 'This is a test for database storing functionality'})

        # Check if the response is valid
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)

        # Query the database for the inserted chat history
        with app.app_context():
            chat_history = ChatHistory.query.one()
            self.assertIsNotNone(chat_history)
            self.assertEqual(chat_history.user_message, 'This is a test for database storing functionality')
            # Here we assume the AI response is not empty
            self.assertNotEqual(chat_history.ai_response, '')

    def test_empty_message_handling(self):
        # Capture the initial count of records in the database
        with app.app_context():
            initial_count = ChatHistory.query.count()

        # Send an empty message and expect a 400 response
        response = self.app.post('/api', json={'message': ''})
        self.assertEqual(response.status_code, 400)  # Assuming the app returns 400 for empty messages
        self.assertIn("Empty message received", response.get_json().get("response", ""))

        # Verify that no new records have been added to the database
        with app.app_context():
            new_count = ChatHistory.query.count()
            self.assertEqual(new_count, initial_count)  # The count should remain the same


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
