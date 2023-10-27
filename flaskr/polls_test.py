import unittest
from . import create_app  # Replace with the actual import statement
from unittest.mock import patch
import json


class TestGetPollFunction(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            test_config={
                "TESTING": True,
            }
        )
        self.client = self.app.test_client()

    def test_viewPoll(self):
        # Replace 'your_existing_poll_id' with a valid poll_id from your database
        response = self.client.get("/viewPoll/1")
        data = response.data.decode("utf-8")

        # Assert that the response code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response data contains the expected poll details
        self.assertIn("poll_id", data)
        self.assertIn("title", data)
        self.assertIn("description", data)
        self.assertIn("created_at", data)
        self.assertIn("user_id", data)

    def test_get_nonexistent_poll(self):
        # Replace 'your_nonexistent_poll_id' with a non-existing poll_id
        response = self.client.get("/get_poll/300")

        # Assert that the response code is 200 (OK) - this is application-specific
        # You can customize the response code or message in your Flask route
        self.assertEqual(response.status_code, 200)

        # Assert that the response data indicates that the poll was not found
        self.assertIn("Poll not found.", response.data.decode("utf-8"))

    def test_create_poll_endpoint(self):
        # Simulate a POST request to the /createEndpoint route with sample form data
        response = self.client.post(
            "/createEndpoint",
            data={
                "poll_title": "Sample Poll",
                "poll_description": "Description of the poll",
                "choices[]": ["Choice 1", "Choice 2", "Choice 3"],
            },
        )

        # Assert that the response matches the expected JSON response
        expected_response = jsonify(request.form).get_data(as_text=True)
        self.assertEqual(response.get_data(as_text=True), expected_response)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
