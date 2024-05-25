from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase


class TestAddOperationView(TestCase):
    def test_post_operation(self):
        # Arrange
        client = APIClient()
        url = reverse("add_operation")  # Assuming URL name is 'add-operation'
        payload = {
            "name": "Test",
            "priority": {"value": 1},
            "restrictions": [
                {"@date": {"after": "2024-01-18", "before": "2024-07-15"}},
                {
                    "@or": [
                        {"@level": {"eq": 40}},
                        {
                            "@and": [
                                {"@level": {"lt": 30, "gt": 15}},
                                {"@meteo": {"is": "clear", "temp": {"gt": "15"}}},
                            ]
                        },
                    ]
                },
            ],
        }
        expected_status = status.HTTP_201_CREATED
        expected_response = {
            "operation": "Test",
            "status": "accepted",
            "priority": {"value": 1},
        }

        # Act
        response = client.post(url, payload, format="json")
        # Assert
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(response.json(), expected_response)


class TestValidateOperationView(TestCase):
    def test_post_operation(self):
        # Arrange
        client = APIClient()
        url = reverse("add_operation")  # Assuming URL name is 'add-operation'
        payload = {
            "name": "Test",
            "priority": {"value": 1},
            "restrictions": [
                {"@date": {"after": "2024-01-18", "before": "2024-07-15"}},
                {
                    "@or": [
                        {"@level": {"eq": 40}},
                        {
                            "@and": [
                                {"@level": {"lt": 30, "gt": 15}},
                                {"@meteo": {"is": "clear", "temp": {"gt": "15"}}},
                            ]
                        },
                    ]
                },
            ],
        }

        # Act
        response = client.post(url, payload, format="json")
        url = reverse("validate_operation")
        payload = {
            "operation_name": "Test",
            "arguments": {"level": 40, "meteo": {"town": "Paris"}},
        }
        expected_status = status.HTTP_200_OK
        expected_response = {
            "operation_name": "Test",
            "status": "accepted",
            "priority": {"value": 1},
        }

        # Act
        response = client.post(url, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, expected_status)
        self.assertEqual(response.json(), expected_response)
