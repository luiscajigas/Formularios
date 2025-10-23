import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', '@69094(65^bskx7(u5565rn-_(ra+%t3ou-qkhp=(mxx7rt-)6')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*'] # o reemplaza con tu dominio render.com si quieres más seguridad

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'asistencia',
'solicitudes',

]

MIDDLEWARE = [
'django.middleware.security.SecurityMiddleware',
'whitenoise.middleware.WhiteNoiseMiddleware', # <- Importante para servir estáticos en Render
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'taller_formularios.urls'

TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [BASE_DIR / 'templates'], # si tienes carpetas de plantillas personalizadas
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

WSGI_APPLICATION = 'taller_formularios.wsgi.application'


DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}


AUTH_PASSWORD_VALIDATORS = [
{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'