from django.urls import path
from .views import import_relev_excel, listeTransaction, gestionCompte, supprimerCompte
from .views import addTransaction, addCategorie, deleteTransaction, updateTransactiom, alertDepensement

app_name = "transaction"

urlpatterns = [
    path("", listeTransaction, name="listeTransaction"),
    path("ajout_file", import_relev_excel, name="add_transaction_by_file"),
    path("ajout_form", addTransaction, name="add_transaction_by_form"),
    path("ajout_categorie", addCategorie, name="addCategorie"),
    path("comptes", gestionCompte, name="comptes"),
    path("supprimerCompte/<int:id>", supprimerCompte, name="supprimer_compte"),
    path("supprimerTransactiom/<int:id>", deleteTransaction, name="deleteTransaction"),
    path("updateTransactiom/<int:id>", updateTransactiom, name="updateTransactiom"),
    
    path("alertDepensement", alertDepensement, name="alertDepensement"),


    # path("task", test_task, name="test_task"),
    # path("task_result/<str:task_id>", test_task_result, name="test_task_result"),
]
