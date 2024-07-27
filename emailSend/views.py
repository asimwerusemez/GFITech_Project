from django.shortcuts import render
from transaction.models import Categorie, Transaction
from .utils import SendMessageEmail
from django.utils.timezone import now
from datetime import timedelta

from django.contrib.auth import get_user_model

# User = get_user_model()


def sendEmailUser(request):
    user = request.user
    transaction = Transaction.objects.filter(utilisateur=user)

    calcDepassement = transaction.montant - transaction.categorie.limite

    subject = f"Depassement dans la categorie {transaction.categorie.nom_categorie} de {calcDepassement} $"
    template = "email/alertEmail.html"
    context = {
        "date": now,
        "email": user.email
    }
    receivers = [user.email]
    if transaction.montant > transaction.categorie.limite:
        # Envoyer l'e-mail
        email_sent = SendMessageEmail(
            subject=subject,
            receivers=[user.email],
            template=template,
            context=context
        )
        if not email_sent:
            print(f"Erreur lors de l'envoi de l'e-mail à {user.email}")

    return render(request, "email/alertEmail.html")




