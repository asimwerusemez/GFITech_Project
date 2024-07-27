from django.urls import path
from .views import all_expense, generate_user_budget

app_name = "analyseDepense"

urlpatterns = [
    path("", all_expense, name="analyseDepense"),
    path("budget", generate_user_budget, name="budget_generate"),
]
