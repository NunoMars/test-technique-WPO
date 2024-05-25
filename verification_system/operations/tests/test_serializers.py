from django.test import TestCase
from rest_framework.exceptions import ValidationError
from operations.serializers import OperationSerializer
from operations.models import Operation


class TestOperationSerializer(TestCase):
    def test_valid_data_happy_path_1(self):
        operation_data = {
            "name": "Addition",
            "value": 10,
            "priority": 1,
            "restrictions": "None",
        }
        expected_data = {
            "id": 1,
            "name": "Addition",
            "priority": 1,
            "restrictions": "None",
        }

        serializer = OperationSerializer(data=operation_data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        self.assertEqual(serializer.data, expected_data)
        self.assertIsInstance(result, Operation)

    def test_valid_data_happy_path_2(self):
        operation_data = {
            "name": "Subtraction",
            "value": -5,
            "priority": 1,  # Ajoutez la valeur de priorité ici
            "restrictions": "None",  # Ajoutez la valeur de restrictions ici
        }
        expected_data = {
            "id": 2,
            "name": "Subtraction",
            "priority": 1,  # Ajoutez la valeur de priorité ici
            "restrictions": "None",  # Ajoutez la valeur de restrictions ici
        }

        serializer = OperationSerializer(data=operation_data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        del serializer.data["id"]
        self.assertEqual(serializer.data, expected_data)
        self.assertIsInstance(result, Operation)

    def test_invalid_data_error_case_null_name(self):
        operation_data = {"name": None, "value": 10}
        exception_message = "This field may not be null."

        serializer = OperationSerializer(data=operation_data)

        with self.assertRaisesMessage(ValidationError, exception_message):
            serializer.is_valid(raise_exception=True)
