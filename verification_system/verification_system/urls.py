from django.urls import path, include

urlpatterns = [
    path("operations/", include("operations.urls")),
]
