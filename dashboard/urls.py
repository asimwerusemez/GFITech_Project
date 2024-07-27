from django.urls import path
from .views import view_dash, gain_view

app_name = "dashboard"

urlpatterns = [
    path("", view_dash, name="view_dash"),
    path("test", gain_view, name="gain_view"),
]
