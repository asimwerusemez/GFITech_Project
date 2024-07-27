from django.urls import path
from .views import objectif_view, object_add, update_object, delete_object, ajout_montant_objectif

app_name = 'objectif'

urlpatterns = [
    path("", objectif_view, name="objectif_view"),
    path("ajouter", object_add, name="object_add"),
    path("modifier/<int:id>", update_object, name="update_object"),
    path("supprimer/<int:id>", delete_object, name="delete_object"),
    path("ajout_montant_objectif/<int:id>", ajout_montant_objectif, name="ajout_montant_objectif"),
]
