from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'directory'
BASE_DIR = Path(__file__).parents[1]

DEBUG = False
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'project' / 'templates',
        ],
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


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# Local Settings
# Generate local_settings.py if it does not exist.

try:
    from project.local_settings import *
except ImportError:
    from django.core.management.utils import get_random_secret_key
    from textwrap import dedent

    # Move old file if it does exist but can't be imported.
    try:
        (BASE_DIR / 'project' / 'local_settings.py').rename(BASE_DIR / 'project' / 'local_settings.py.old')
    except FileNotFoundError:
        pass

    with open(BASE_DIR / 'project' / 'local_settings.py', 'w') as f:
        f.write(dedent(f"""\
        from pathlib import Path
        
        # Build paths inside the project like this: BASE_DIR / 'directory'
        BASE_DIR = Path(__file__).parents[1]
        
        # SECURITY WARNING: keep the secret key used in production secret!
        SECRET_KEY = {repr(get_random_secret_key())}
        
        # SECURITY WARNING: don't run with debug turned on in production!
        DEBUG = True
        
        ALLOWED_HOSTS = []
        
        
        # Database
        # https://docs.djangoproject.com/en/1.11/ref/settings/#databases
        
        DATABASES = {{
            'default': {{
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'saffybot',
                'USER': 'postgres',
                'PASSWORD': 'password',
                'HOST': '127.0.0.1',
                'PORT': '5432',
            }}
        }}
        """))

    print("You didn't appear to have a local_settings.py file, so one was generated for you.")
    from project.local_settings import *
