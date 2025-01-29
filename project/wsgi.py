import os

from django.core.wsgi import get_wsgi_application
# Ορισμός ρυθμίσεων για την WSGI εφαρμογή
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()
