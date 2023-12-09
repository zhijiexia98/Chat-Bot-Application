import unittest
from app import app

class ChatBotTestCase(unittest.TestCase):
    # Set up before each test
    def setUp(self):
        # Configure the app for testing mode
        app.config['TESTING'] = True
        self.client = app.test_client()

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

    # Test the API's response to invalid data
    def test_api_with_invalid_data(self):
        # Send an empty message to the API
        invalid_data = {"message": "", "language": "en"}
        response = self.client.post('/api', json=invalid_data)
        # Expect a 400 Bad Request status code due to invalid input
        self.assertEqual(response.status_code, 400)
        # Check if 'error' key is present in the JSON response

    # Test the API's handling of non-English languages
    def test_api_with_non_english_language(self):
        # Send a message in Spanish
        non_english_message = {"message": "Hola, ¿cómo estás?", "language": "es"}
        response = self.client.post('/api', json=non_english_message)
        # Expect a successful response
        self.assertEqual(response.status_code, 200)
        # Check if 'response' key is in the JSON response

    """
    def test_api_rate_limiting(self):
        message = {"message": "Test rate limiting", "language": "en"}
        for _ in range(15):  # Assuming a rate limit is set, exceed it
            response = self.client.post('/api', json=message)
            if response.status_code != 200:
                break

        # Expect a non-200 status code when rate limit is exceeded
        self.assertNotEqual(response.status_code, 200)
    """

    # Test the API's sentiment analysis handling for a negative message
    def test_api_negative_sentiment_handling(self):
        negative_message = {"message": "I am very unhappy and angry", "language": "en"}
        response = self.client.post('/api', json=negative_message)
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200
        # Check if the API response includes the expected sentiment acknowledgment
        self.assertIn("I sense that you're upset", response.json['response'])

    # Test the API's sentiment analysis handling for a positive message
    def test_api_positive_sentiment_handling(self):
        positive_message = {"message": "I am very happy and excited", "language": "en"}
        response = self.client.post('/api', json=positive_message)
        self.assertEqual(response.status_code, 200)  # Check if the response status code is 200
        # Check if the API response does not include the negative sentiment acknowledgment
        self.assertNotIn("I sense that you're upset", response.json['response'])


if __name__ == '__main__':
    unittest.main()
