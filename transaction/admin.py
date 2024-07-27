from django.contrib import admin
from .models import Transaction, Compte, File, Categorie, Alert


admin.site.register(Categorie)
admin.site.register(Compte)
admin.site.register(File)
admin.site.register(Transaction)
admin.site.register(Alert)

