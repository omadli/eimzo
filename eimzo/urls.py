from .views import download_certificate
from django.urls import path

urlpatterns = [
    path("uploads/<str:filename>", download_certificate, name="download"),
]
