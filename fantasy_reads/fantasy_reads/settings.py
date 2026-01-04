"""
Django settings for fantasy_reads project.
"""

import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad

# Helper para obtener variables de entorno obligatorias
def get_env_variable(var_name: str) -> str:
    """Obtiene la variable de entorno o lanza ImproperlyConfigured si falta."""
    try:
        return os.environ[var_name]
    except KeyError:
        raise ImproperlyConfigured(f"La variable de entorno '{var_name}' no está definida. Defínela y reinicia la aplicación.")

# SECRET_KEY obligatoria (no debe existir hardcodeada)
SECRET_KEY = get_env_variable('SECRET_KEY')

# DEBUG depende de variable de entorno (por defecto False si no está definida)
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('1', 'true', 'yes')

# Configuración de ALLOWED_HOSTS para Render
# Render provee RENDER_EXTERNAL_HOSTNAME en el entorno de ejecución.
render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_host:
    ALLOWED_HOSTS = [render_host, 'localhost', '127.0.0.1']
else:
    # Entorno local o sin host de Render: restringir a localhost por defecto
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reads',  # tu app personalizada
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fantasy_reads.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                BASE_DIR / 'templates', #carpeta global para autenticacion
                BASE_DIR / 'reads' / 'templates' #carpeta con templates de la app
                ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fantasy_reads.wsgi.application'

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseña
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

# Internacionalización
LANGUAGE_CODE = 'es-CL'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Archivos estáticos y media
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'reads' / 'static']

# Ruta donde collectstatic colocará los archivos para servir en producción
# Requerida para despliegues en Render / cualquier servidor WSGI
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# API key para Google Books (obligatoria en variables de entorno)
GOOGLE_BOOKS_API_KEY = get_env_variable('GOOGLE_BOOKS_API_KEY')

#redirecciona al index luego del login y logout
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

