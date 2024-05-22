# operations/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Operation
from .serializers import OperationSerializer
import requests
from django.conf import settings
from .logs_config import logging


logger = logging.getLogger(__name__)


def get_weather(town: str) -> dict:
    """Get weather data from OpenWeather API"""
    api_key = settings.OPENWEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={town}&appid={api_key}&units=metric"
    response = requests.get(url)
    logger.info(f"Got weather response: {response}")
    if response.status_code == 200:
        logger.info(f"Got weather data: {response.json()}")
        return response.json()
    logger.error(f"Error getting weather data: {response.text}")
    return None


def validate_restrictions(restrictions, arguments):
    """Validate restrictions for an operation"""

    for restriction in restrictions:
        logger.info(f"Validating restriction: {restriction}")
        for key, value in restriction.items():
            if key == "@date":
                if not (value["after"] <= arguments["date"] <= value["before"]):
                    logger.debug(f"Date condition failed: {value}")
                    return False
            elif key == "@level":
                if not (value["lt"] < arguments["level"] < value["gt"]):
                    logger.debug(f"Level condition failed: {value}")
                    return False
            elif key == "@meteo":
                weather = get_weather(arguments["meteo"]["town"])
                logger.info(f"Got weather data: {weather}")
                if weather:
                    temp = weather["main"]["temp"]
                    if not (temp > value["temp"]["gt"]):
                        logger.debug(f"Temperature condition failed: {value}")
                        return False
                    if not (
                        weather["weather"][0]["main"].lower() == value["is"].lower()
                    ):
                        logger.debug(f"Weather condition failed: {value}")
                        return False
                else:
                    return False
            elif key == "@or":
                if not any(validate_restrictions([cond], arguments) for cond in value):
                    logger.debug(f"OR condition failed: {value}")
                    return False
            elif key == "@and":
                if not all(validate_restrictions([cond], arguments) for cond in value):
                    logger.debug(f"AND condition failed: {value}")
                    return False
    return True


class AddOperationView(APIView):
    """Add an operation to the system"""

    def post(self, request):
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            logger.info(f"Adding operation: {validated_data}")
            serializer.save()
            return Response(
                {"status": "success", "operation": validated_data},
                status=status.HTTP_201_CREATED,
            )
        logger.error(f"Error adding operation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateOperationView(APIView):
    """Validate an operation request"""

    def post(self, request):
        data = request.data
        operation_name = data.get("operation_name")
        arguments = data.get("arguments")

        try:
            operation = Operation.objects.get(name=operation_name)
            logger.info(f"Validating operation: {operation_name}")
        except Operation.DoesNotExist:
            logger.error(f"Operation not found: {operation_name}")
            return Response(
                {"status": "denied", "reason": "Operation not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if validate_restrictions(operation.restrictions, arguments):
            logger.info(f"Operation {operation_name} accepted")
            return Response(
                {"status": "accepted", "priority": {"value": operation.priority}},
                status=status.HTTP_200_OK,
            )
        else:
            logger.info(f"Operation {operation_name} denied")
            return Response(
                {"status": "denied", "reason": "Validation failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
