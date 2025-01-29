import os

from django.core.asgi import get_asgi_application
# Ορισμός ρυθμίσεων για την ASGI εφαρμογή
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_asgi_application()
