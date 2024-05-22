# operations/urls.py

from django.urls import path
from .views import add_operation, validate_operation

urlpatterns = [
    path("add/", add_operation, name="add_operation"),
    path("validate/", validate_operation, name="validate_operation"),
]
