from django.urls import path
from .views import register_entreprise, register_particulier, login_user, logout_user, choice_profile

app_name = "accounts"

urlpatterns = [
    path('register_entreprise/', register_entreprise, name='register_entreprise'),
    path('register_particulier/', register_particulier, name='register_particulier'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('choix_profile/', choice_profile, name='choice'),
]
