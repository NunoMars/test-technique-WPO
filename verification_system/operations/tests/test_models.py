from django.core.exceptions import ValidationError
from django.test import TestCase
from operations.models import Operation


class TestOperationModel(TestCase):
    def test_happy_path_1(self):
        name = "Operation A"
        priority = {"level": 1}
        restrictions = {"time": "day"}

        self._commun_test_case(name, priority, restrictions)

    def test_happy_path_2(self):
        name = "Operation B"
        priority = {"level": 2, "speed": "high"}
        restrictions = {"time": "night", "area": "urban"}

        self._commun_test_case(name, priority, restrictions)

    def _commun_test_case(self, name, priority, restrictions):
        """Common test case for happy path scenarios"""
        operation = Operation(name=name, priority=priority, restrictions=restrictions)
        operation.full_clean()
        self.assertEqual(operation.name, name)
        self.assertEqual(operation.priority, priority)
        self.assertEqual(operation.restrictions, restrictions)

        # Repeat the above pattern for the remaining test cases

    def test_error_case_null_name(self):
        name = None
        priority = {"level": 1}
        restrictions = {"time": "day"}

        with self.assertRaises((ValidationError, TypeError)):
            operation = Operation(
                name=name, priority=priority, restrictions=restrictions
            )
            operation.full_clean()  # This will raise ValidationError for invalid data
