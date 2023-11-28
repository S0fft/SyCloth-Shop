from pathlib import Path

from decouple import config

BASE_DIR: str = Path(__file__).resolve().parent.parent

SECRET_KEY: str = config('SECRET_KEY')

DEBUG: bool = config('DEBUG', cast=bool)

ALLOWED_HOSTS: list[str] = []

DOMAIN_NAME: str = 'http://127.0.0.1:8000'

INSTALLED_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',

    'debug_toolbar',

    'products',
    'orders',
    'users',
]

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF: str = 'base.urls'

TEMPLATES: list[dict[str, any]] = [
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

                'products.context_processors.baskets',
            ],
        },
    },
]

WSGI_APPLICATION: str = 'base.wsgi.application'

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

DATABASES: dict[str, str | bool] = {
    'default': {
        'ENGINE': config('ENGINE'),
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('HOST'),
        'PORT': config('PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
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

LANGUAGE_CODE: str = 'en-en'

TIME_ZONE: str = 'UTC'

USE_I18N: bool = True

USE_L10N: bool = True

USE_TZ: bool = True

STATIC_URL: str = '/static/'

STATICFILES_DIRS: list[str] = [
    BASE_DIR / 'static',
]

MEDIA_URL: str = '/media/'

MEDIA_ROOT: str = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

AUTH_USER_MODEL: str = 'users.User'

LOGIN_URL: str = '/users/login/'

LOGIN_REDIRECT_URL: str = '/'

LOGOUT_REDIRECT_URL: str = '/'

EMAIL_HOST: str = config('EMAIL_HOST')
EMAIL_PORT: str = config('EMAIL_PORT')
EMAIL_HOST_USER: str = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD: str = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL: bool = config('EMAIL_USE_SSL', cast=bool)

AUTHENTICATION_BACKENDS: list[str] = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID: int = 1

SOCIALACCOUNT_PROVIDERS: dict[str, dict[list[str]]] = {
    'github': {
        'SCOPE': [
            'user',
        ],
    }
}

CELERY_BROKER_URL: str = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND: str = 'redis://127.0.0.1:6379'

STRIPE_PUBLIC_KEY: str = config('STRIPE_PUBLIC_KEY')
STRIPE_SECRET: str = config('STRIPE_SECRET')
