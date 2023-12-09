import unittest
from app import app, db, ChatHistory

class ChatBotTestCase(unittest.TestCase):
    # Set up before each test
    def setUp(self):
        # Configure the app for testing mode
        app.config['TESTING'] = True
        # Use an in-memory SQLite database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.client = app.test_client()  # Create a test client

        with app.app_context():
            db.create_all()  # Create all database tables

    # Tear down after each test
    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Test if the index page loads correctly
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200

    # Test the API response for a standard message
    def test_api_response(self):
        test_message = {"message": "Hello", "language": "en"}
        response = self.client.post('/api', json=test_message)
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200
        self.assertIn('response', response.json)  # Check if 'response' key is in the JSON response

    # Test the API's sentiment analysis handling for a negative message
    def test_api_sentiment_handling(self):
        negative_message = {"message": "I am very unhappy and angry", "language": "en"}
        response = self.client.post('/api', json=negative_message)
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200
        # Check if the API response includes the expected sentiment acknowledgment
        self.assertIn("I sense that you're upset", response.json['response'])

    # Test if a database entry is created after sending a message
    def test_database_entry_creation(self):
        message = {"message": "Testing database entry", "language": "en"}
        self.client.post('/api', json=message)

        with app.app_context():
            # Query the first entry in the ChatHistory table
            entry = ChatHistory.query.first()
            self.assertIsNotNone(entry)  # Check if an entry was created
            # Check if the message in the database matches the one sent
            self.assertEqual(entry.user_message, message['message'])


    # Test the API's response to invalid data
    def test_api_with_invalid_data(self):
        # Send an empty message to the API
        invalid_data = {"message": "", "language": "en"}
        response = self.client.post('/api', json=invalid_data)
        # Expect a 400 Bad Request status code due to invalid input
        self.assertEqual(response.status_code, 400)
        # Check if 'error' key is present in the JSON response
        self.assertIn('error', response.json)

    # Test the API's handling of non-English languages
    def test_api_with_non_english_language(self):
        # Send a message in Spanish
        non_english_message = {"message": "Hola, ¿cómo estás?", "language": "es"}
        response = self.client.post('/api', json=non_english_message)
        # Expect a successful response
        self.assertEqual(response.status_code, 200)
        # Check if 'response' key is in the JSON response
        self.assertIn('response', response.json)

    # Test the API's rate limiting feature
    def test_api_rate_limiting(self):
        # Send multiple requests to test rate limiting
        message = {"message": "Test rate limiting", "language": "en"}
        for _ in range(15):  # Assuming a rate limit is set, exceed it
            response = self.client.post('/api', json=message)
        # Expect a non-200 status code (e.g., 429 Too Many Requests) when rate limit is exceeded
        self.assertNotEqual(response.status_code, 200)

    # Test if multiple database entries are created correctly
    def test_database_multiple_entries(self):
        # Send multiple distinct messages
        messages = [
            {"message": "First message", "language": "en"},
            {"message": "Second message", "language": "en"}
        ]
        for msg in messages:
            self.client.post('/api', json=msg)

        with app.app_context():
            # Count the number of entries in the database
            entries = ChatHistory.query.count()
            # Check if the count matches the number of messages sent
            self.assertEqual(entries, len(messages))


if __name__ == '__main__':
    unittest.main()
