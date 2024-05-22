# operations/urls.py

from django.urls import path
from .views import AddOperationView, ValidateOperationView

urlpatterns = [
    path("add/", AddOperationView.as_view(), name="add_operation"),
    path("validate/", ValidateOperationView.as_view(), name="validate_operation"),
]
