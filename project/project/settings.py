"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')  # Введите свой ключ

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ALLOWED_HOSTS = list(os.getenv('ALLOWED_HOSTS'))  # Установите свой список

# Application definition

INSTALLED_APPS = [
    'django_dump_load_utf8',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'NewsPortal.apps.NewsportalConfig',
    'django_filters',
    'accounts',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_apscheduler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Кэшировать весь сайт целиком
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': os.getenv('POSTGRE_NAME'),
        # 'USER': os.getenv('POSTGRE_USER'),
        # 'PASSWORD': os.getenv('POSTGRE_PASS'),
        # 'HOST': os.getenv('POSTGRE_HOST'),
        # 'PORT': os.getenv('POSTGRE_PORT'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/news'
LOGOUT_REDIRECT_URL = '/news'
ACCOUNT_LOGOUT_REDIRECT_URL = '/news'

ACCOUNT_FORMS = {'signup': 'accounts.forms.CustomSignupForm'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # none, optional, mandatory
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# else:
#     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_SUBJECT_PREFIX = ''
EMAIL_HOST = os.getenv('EMAIL_HOST')  # Укажите свой хост почты
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))  # Укажите свой порт почты
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = 60
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Укажите свой хост юзера
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Укажите свой пароль

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')  # Укажите свой емайл
SERVER_EMAIL = os.getenv('SERVER_EMAIL')  # Укажите свой емайл

SITE_URL = os.getenv('SITE_URL')  # Укажите свою ссылку

ADMINS = os.getenv('ADMINS')  # Укажите свой список администраторов
MANAGERS = os.getenv('MANAGERS')  # Укажите свой список менеджеров

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')  # Укажите свои данные
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIME_ZONE = 'Europe/Moscow'
CELERY_TASK_TIME_LIMIT = 30 * 60

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        'TIMEOUT': 30,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # Фильтрация логов при определённых настройках
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },

    # Определение формата и внешнего вида логов
    'formatters': {
        'console_debug': {
            'format': '[{asctime}] | {levelname} | {message}',
            'style': '{',
        },
        'console_warning_AND_mail_admins': {
            'format': '[{asctime}] | {levelname} | {message} | {pathname}',
            'style': '{',
        },
        'console_error_AND_file_error': {
            'format': '[{asctime}] | {levelname} | {message} | '
                      '{pathname} {exc_info}',
            'style': '{',
        },
        'file_general_AND_file_security': {
            'format': '[{asctime}] | {levelname} | {module} | {message}',
            'style': '{',
        },
    },

    # Обработчики для определения вывода и хранения логов
    'handlers': {
        'console_debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_debug',
            'filters': ['require_debug_true'],
        },
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'console_warning_AND_mail_admins',
            'filters': ['require_debug_true'],
        },
        'console_error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'console_error_AND_file_error',
            'filters': ['require_debug_true'],
        },
        'file_general': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file_general_AND_file_security',
            'filename': 'general.log',
            'filters': ['require_debug_false'],
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'console_error_AND_file_error',
            'filename': 'errors.log',
        },
        'file_security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file_general_AND_file_security',
            'filename': 'security.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'console_warning_AND_mail_admins',
            'filters': ['require_debug_false'],
        },
    },

    # Регистраторы логирования
    'loggers': {
        'django': {
            'handlers': [
                'console_debug',
                'console_warning',
                'console_error',
                'file_general',
            ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['file_security'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
