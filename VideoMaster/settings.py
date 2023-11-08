from pathlib import Path
from decouple import config
from django.contrib import messages
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #added Installs
    "django_celery_results",
    "storages",

    #Custom Django apps
    "video",
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

ROOT_URLCONF = 'VideoMaster.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'VideoMaster.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]
STATIC_ROOT = os.path.join(BASE_DIR,"static_root")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MESSAGE_TAGS = {
    messages.ERROR :'danger'
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# celery Settings
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_RESULT_BACKEND = 'django-db'

#aws settings
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID',cast=str)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY',cast=str)
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME',cast=str)
AWS_QUERYSTRING_AUTH = True
# AWS_QUERYSTRING_EXPIRE = 3600
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'ap-south-1'
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN',cast=str)
AWS_CLOUDFRONT_KEY_ID = config('AWS_CLOUDFRONT_KEY_ID',cast=str)
AWS_CLOUDFRONT_KEY="-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA4cehD0fe/ATR2tH5XKh85PT+hg8M2bW49d2vGs8TqQBw/a2p\nGl7E06H1nzdb3qu58E4RD8/31FnET3Z6UFj6L/wgh8XcYknFuGe24gOGmfHC+wkv\nhz6E9OGQyFK/43GFv1wiVT20qFMqhKYBY3TR1FWls40rADgDVj4T9kHduZCxGKVu\nmNoTYo/NMrzhoIBELY5KpYC3G2M+ZGG1fdUDSaxMlAlpzC0H5U0qT26XCuvxt+uj\ndgXlBH9kkssdN4dUHSlArag2omD2wEqpTop4pZ8AS+M30Z6zDyLd9yoETjCooSel\n5Qg8aodU2Ce+g0jcDxoSkYXqZjO+XiFEndMIfQIDAQABAoIBAQCNsUPBnEAzdy7g\nHdBZtx+SbLJjHYTaCHKIUlR3Baf38t/2RAsREpKBom3MOui76JerWMLaYpDMwn0x\nxU/jpsN0Y81ih+jUAipEnUons0DA0fmko9IhFTpJmFnNbikgqvjd7Atb5Xq//Fl9\nn9TVPtYEZK+17A0leQGXGSRb8mAc+KQY3FE2IV/ebTW6s8T4CZBC0OO4O0QAEDBG\njfATMufXNw6p/sEg8zeEdJyH7/p30sUELijZwNmvAibOj5wWrJdMJ+zZpw4tmvZW\nKANSiYmLlMkREDilELL+mo0IYEo9lzyBZruOyM4iSlpJOLlyfRx+JyUeIuVecEdO\nqdImr02BAoGBAPy7LPobauCHzyKvidYHkxLY1kJhb8ORCFmXmsmtBYEKgSFkSFYH\n1127K1PouulnZErJNtgi27XHhDgS0x/dGRkKi2cXAnehdE4CR+og/hrokBSTrSAq\nM+qSNx/yYTmYCMQWEuA4fz8C8cEWy5kv0SeMGTWdc9YXlMDzDkkWegxdAoGBAOSz\nNtNLx4JgrK9eNh2uIr0YfDaXvWUGwmO9geiA4/SWNDNwjZBhL3AxfQ+q75dOoorJ\nUM58w4YslMKR6sPh4UZnDegE4XaZJUBClI+Yhst9vhGuwTheAV+7FgH1I//JfFAF\nVnUowGfNcs32KSiC9j7iBqzIGhlteimGLiWIkiqhAoGBAOLWBSp+zVC11J5nO6nU\nppb19GkkFzJKzFnNjuqQ1y3ZBcm4vowpAY5pXhwz+P9hA010iDs6HkVrzCqgCsrA\nobQuGKzwpBBH46HYvj9QWYJBVoCBg5QpDOvvTHbqD4WoBcYpocuKKfueYupR0W+u\n0WVTg5Txu3RfOe5suVe0StspAoGAIYAfB9SR5QdERGwIgVCAxjJP/686jxHuZ63a\n2bQHsExQWTijhAK4cDbPmvvvHLroFGxo6dZczcq5/8ZgHVF5LlbqMpKEdFr6me8m\n0+ID3MsOjIiMxTT//oXpM2A1ZcKd8xrVD1Ro2su9hW4JmWWVrKBvWd/18sOWoX6G\nQ/k9cAECgYA66APjjk2d39/bjh/r8gxWj42x3+OqHEVZuMFATyi5k2qHRdGaSejP\nAR7IifRRb76wrbczar0+TwMGZeu26Jw6KZ+7JP26jEMSeoyNUOsokvQuRzjCwxMf\nstFon0LLSioddg6cZUEgakIJqOrAYUOTUFePI+KYwP1FbrTjYqZkEA==\n-----END RSA PRIVATE KEY-----"