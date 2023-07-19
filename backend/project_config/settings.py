import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ok_zcfy2+zuv0jdi$1rr0af(f)_buu!!p4jp8ona-1&u4oz@r+'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # -------- Django --------
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # -------- Libs --------
    'rest_framework',
    # -------- Apps --------
    'clients.apps.ClientsConfig',
    'services.apps.ServicesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'project_config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    },
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGS_DIR = BASE_DIR / 'logs/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'console_formatter': {
            'format': '{style}{levelname}: {filename} | line {lineno} | {funcName}():{reset_styles}\t{message}',
            'style': '{',
        },

        'file_formatter': {
            'format': '{asctime} | {levelname} | {filename} | line {lineno} | {funcName}():\n\t{message}',
            'style': '{',
        }
    },

    'filters': {
        'console_filter': {
            '()': 'project_config.logging_config.ConsoleStyleFilter',
        },
    },

    'handlers': {
        'simple_console_handler': {
            'class': 'logging.StreamHandler',
        },

        'dev_console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_formatter',
            'filters': ['console_filter']
        },

        'dev_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*20,  # 20 MB
            'formatter': 'file_formatter',
            'filename': LOGS_DIR / 'dev' / 'django_optimize_dev.log',
            'backupCount': 5,
        },

        'prod_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*20,  # 20 MB
            'formatter': 'file_formatter',
            'filename': LOGS_DIR / 'prod' / 'django_optimize_prod.log',
            'backupCount': 5,
        },

        'prod_mail_handler': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'WARNING',
            'formatter': 'file_formatter',
        },
    },

    'loggers': {
        'django.db.backends': {
            'handlers': ['simple_console_handler'],
            'level': 'DEBUG',
        },
        
        'dev_main_logger': {
            'level': 'DEBUG',
            'handlers': ['dev_console_handler', 'dev_file_handler'],
        },

        'dev_console_logger': {
            'level': 'DEBUG',
            'handlers': ['dev_console_handler'],
        },

        'prod_logger': {
            'level': 'INFO',
            'handlers': ['prod_file_handler', 'prod_mail_handler']
        },
    }
}

CELERY_BROKER_URL = 'redis://redis:6379/0'
