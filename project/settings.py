from pathlib import Path

# Ορισμός του βασικού φακέλου του έργου: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent


# Μυστικό κλειδί - Πρέπει να παραμείνει απόρρητο
SECRET_KEY = 'django-insecure-v-zes40knfo^q5zh890!pl-u)8$dcopk(qky+qb#tt!o+u#vqt'

# Ενεργοποίηση λειτουργίας αποσφαλμάτωσης (Debug)
DEBUG = False

# Λίστα επιτρεπόμενων hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # Λίστα επιτρεπόμενων hosts



# Εγκατεστημένες εφαρμογές
INSTALLED_APPS = [
    'festivalsystem.apps.FestivalsystemConfig', # Εφαρμογή για το σύστημα φεστιβάλ
    'phonenumber_field', # Υποστήριξη αριθμών τηλεφώνου
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware - Διαχείριση αιτήσεων/απαντήσεων
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'  # Ρυθμίσεις διευθύνσεων URL

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Ρυθμίσεις βάσης δεδομένων (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Ρυθμίσεις επικύρωσης κωδικών πρόσβασης
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization - Ρυθμίσεις διεθνοποίησης
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# Στατικά αρχεία
STATIC_URL = 'static/'

# Αρχεία media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Προσαρμοσμένο μοντέλο χρήστη
AUTH_USER_MODEL = 'festivalsystem.User'

# Περιοχή για αριθμούς τηλεφώνου
PHONENUMBER_DEFAULT_REGION = 'IN'