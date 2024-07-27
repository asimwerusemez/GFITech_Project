from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from gfitech import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("home.urls")),
    path("accounts/", include("accounts.urls")),
    path("transaction/", include("transaction.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("objectifs/", include("objectif.urls")),
    path("analyseDepense/", include("analyseDepense.urls"))


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
