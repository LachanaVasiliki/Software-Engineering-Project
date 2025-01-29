from django.contrib import admin
from django.urls import include, path

# Ρυθμίσεις δρομολόγησης URL
urlpatterns = [
    path('admin/', admin.site.urls),  # Διαχειριστικό πάνελ
    path('', include("festivalsystem.urls"))  # Εφαρμογή συστήματος φεστιβάλ
]
