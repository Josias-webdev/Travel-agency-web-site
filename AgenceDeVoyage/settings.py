"""
Django settings for AgenceDeVoyage project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from django.urls import reverse_lazy
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%r-#a9_^$9=lkps%z(i2-&f0cy8@hxs54s&lr_p6=5ivc&la$c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ocean-reservation-4ab8dd8a81e5.herokuapp.com']
# ALLOWED_HOSTS = []

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_USE_TLS = True 
# EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST = 'smtp-mail.outlook.com'
# EMAIL_HOST_USER = '63f37e4aab498e'
# EMAIL_HOST_PASSWORD = '4e5b39b2ad6392'
EMAIL_HOST_USER = "joejosiasb@outlook.com"
EMAIL_HOST_PASSWORD = "Joetumberli"
# EMAIL_PORT = '2525'
EMAIL_PORT = '587'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_auto_logout.middleware.auto_logout', # step 1 of logout session
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'AgenceDeVoyage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_auto_logout.context_processors.auto_logout_client', # step 2 of logout session
            ],
        },
    },
]

WSGI_APPLICATION = 'AgenceDeVoyage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'oceanreservation_db',
#         'USER': 'postgres',
#         'PASSWORD': 'admin',
#         'HOST': 'localhost',
#     }
# }

DATABASES = {'default': dj_database_url.config(default='postgres://uc0pqdnpscs1iq:p943c81be09fd163088a80d204b28211b2ac268abd86dc3eaa08ed7227bafb6f2@c6sfjnr30ch74e.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dbglkftcgkc6ni')}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#MEDIA FILES 
MEDIA_URL = "media/"
# MEDIA_ROOT = BASE_DIR/'media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTO_LOGOUT = {'IDLE_TIME': 500,'REDIRECT_TO_LOGIN_IMMEDIATELY': True, 'MESSAGE': 'The session has expired. Please login again to continue.',}

LOGOUT_REDIRECT_URL = reverse_lazy('app/signin')

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

#whitenoise settings

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'