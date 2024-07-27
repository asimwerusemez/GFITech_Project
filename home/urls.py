from django.urls import path
from .views import index, contact, fonctionnalite

app_name = "home"


urlpatterns = [
    path("", index, name="index"),
    path("contact", contact, name="contact"),
    path("fonctionnalite", fonctionnalite, name="fonctionnalite"),
]
