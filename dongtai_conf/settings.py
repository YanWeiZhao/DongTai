"""
Django settings for dongtai_conf project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
from configparser import ConfigParser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("debug", 'false') == 'true' #or os.getenv('environment', None) in ('TEST',)

# READ CONFIG FILE
config = ConfigParser()
status = config.read(os.path.join(BASE_DIR, 'dongtai_conf/conf/config.ini'))
if len(status) == 0:
    print("config file not exist. stop running")
    exit(0)

def ranstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()`-{}|:?><>?'
    salt = ''
    for i in range(num):
        salt += random.choice(H)
    return salt


# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = config.get('security', 'secret_key')
except Exception as e:
    SECRET_KEY = ranstr(50)
# DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition
TOKEN_EXP_DAY = 14

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'captcha',
    'modeltranslation',
    'django_celery_beat',
    'deploy.commands'
]
DEFAULT_AUTO_FIELD='django.db.models.AutoField'
def get_installed_apps():
    from os import walk, chdir, getcwd
    previous_path = getcwd()
    master = []
    APPS_ROOT_PATH = BASE_DIR
    chdir(APPS_ROOT_PATH)
    for root, directories, files in walk(top=getcwd(), topdown=False):
        for file_ in files:
            if 'apps.py' in file_ and len(
                    list(
                        filter(lambda x: x != '',
                               root.replace(getcwd(), '').split('/')))) == 1:
                app_path = f"{root.replace(BASE_DIR + '/', '').replace('/', '.')}"
                master.append(app_path)
    chdir(previous_path)
    return master
CUSTOM_APPS = get_installed_apps()
INSTALLED_APPS.extend(CUSTOM_APPS)


MODELTRANSLATION_LANGUAGES = ('en', 'zh')
MODELTRANSLATION_DEFAULT_LANGUAGE = 'zh'
REST_FRAMEWORK = {
    'PAGE_SIZE':
        20,
    'DEFAULT_PAGINATION_CLASS': ['django.core.paginator'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_THROTTLE_CLASSES': ('rest_framework.throttling.AnonRateThrottle',
                                 'rest_framework.throttling.UserRateThrottle'),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '6000000/min',
        'user': '6000000/min'
    },
}

basedir = os.path.dirname(os.path.realpath(__file__))
LANGUAGE_CODE = 'zh'
LANGUAGES = (
    ('en', 'English'),
    ('zh', '简体中文'),
)
USE_I18N = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'static/i18n'),
)
USE_L10N = True
MODELTRANSLATION_FALLBACK_LANGUAGES = ('zh', 'en')
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'dongtai_common.common.utils.CSPMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'xff.middleware.XForwardedForMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

XFF_TRUSTED_PROXY_DEPTH = 20

CSRF_COOKIE_NAME = "DTCsrfToken"
CSRF_HEADER_NAME = "HTTP_CSRF_TOKEN"
def safe_execute(default, exception, function, *args):
    try:
        return function(*args)
    except exception:
        return default


CSRF_TRUSTED_ORIGINS = tuple(
    filter(
        lambda x: x != "",
        safe_execute("", BaseException, config.get, "security",
                     "csrf_trust_origins").split(",")))
CSRF_COOKIE_AGE = 60 * 60 * 24

AGENT_UPGRADE_URL = "https://www.huoxian.cn"
CORS_ALLOWED_ORIGINS = [
        'https://dongtai.io',
]

CORS_ORIGIN_REGEX_WHITELIST = [
    r"^https://\w+\.huoxian.cn:(\:\d+)?$",
    r"^https://\w+\.dongtai_common.io:(\:\d+)?$",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'GET',
    'OPTIONS',
    'POST',
    'PUT',
    'DELETE'
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'referer',
    'x-token',
    'user-agent',
    'x-csrftoken',
    'csrf-token',
    'x-requested-with',
    'x_http_method_override'
]

ROOT_URLCONF = 'dongtai_conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '/static/templates')],
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

WSGI_APPLICATION = 'dongtai_conf.wsgi.application'

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 900,
        'ENGINE': 'django.db.backends.mysql',
        'USER': config.get("mysql", 'user'),
        'NAME': config.get("mysql", 'name'),
        'PASSWORD': config.get("mysql", 'password'),
        'HOST': config.get("mysql", 'host'),
        'PORT': config.get("mysql", 'port'),
        'OPTIONS': {
            'init_command':
            'SET max_execution_time=20000;SET NAMES utf8mb4;SET collation_server=utf8mb4_general_ci;SET collation_database=utf8mb4_general_ci; ',
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
        'TEST': {
            'USER': config.get("mysql", 'user'),
            'NAME': config.get("mysql", 'name'),
            'PASSWORD': config.get("mysql", 'password'),
            'HOST': config.get("mysql", 'host'),
            'PORT': config.get("mysql", 'port'),
        }
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}
REDIS_URL = 'redis://:%(password)s@%(host)s:%(port)s/%(db)s' % {
    'password': config.get("redis", 'password'),
    'host': config.get("redis", 'host'),
    'port': config.get("redis", 'port'),
    'db': config.get("redis", 'db'),
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]
AUTH_USER_MODEL = 'dongtai_common.User'
TIME_ZONE = "Asia/Shanghai"
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = "/static/"
CAPTCHA_IMAGE_SIZE = (80, 45)
CAPTCHA_LENGTH = 4
CAPTCHA_TIMEOUT = 1
LOGGING_LEVEL = 'DEBUG' if DEBUG else 'ERROR'
if os.getenv('environment', None) == 'TEST':
    LOGGING_LEVEL = 'INFO'
LOGGING_LEVEL = safe_execute(LOGGING_LEVEL, BaseException, config.get, "other",
                             "logging_level")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            u'{levelname} {asctime} [{module}.{funcName}:{lineno}] {message}',
            'style': '{',
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter"
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'dongtai-webapi': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/webapi.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'dongtai.openapi': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/openapi.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'dongtai-core': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/core.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'celery.apps.worker': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/worker.log',
            'formatter': 'verbose'
        },
        'jsonlog': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/logstash/server.log',
            'formatter': 'json'
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': LOGGING_LEVEL,
        },
        'dongtai-webapi': {
            'handlers': ['console', 'dongtai-webapi'],
            'propagate': True,
            'level': LOGGING_LEVEL,
        },
        'dongtai.openapi': {
            'handlers': ['console', 'dongtai.openapi'],
            'propagate': True,
            'level': LOGGING_LEVEL,
        },
        'dongtai-core': {
            'handlers': ['console', 'dongtai-webapi'],
            'propagate': True,
            'level': LOGGING_LEVEL,
        },
        'django': {
            'handlers': ['console', 'dongtai-webapi'],
            'propagate': True,
            'level': LOGGING_LEVEL,
        },
        'dongtai-engine': {
            'handlers': ['console', 'dongtai-webapi'],
            'propagate': True,
            'level': LOGGING_LEVEL,
        },
        'celery.apps.worker': {
            'handlers': ['console', 'celery.apps.worker'],
            'propagate': True,
            'level': LOGGING_LEVEL,
        },
        'jsonlogger': { # it use to logging to local logstash file
            'handlers': ['jsonlog'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}
REST_PROXY = {
    'HOST': config.get("engine", 'url'),
}

OPENAPI = config.get("apiserver", "url")

# notify
EMAIL_SERVER = config.get('smtp', 'server')
EMAIL_USER = config.get('smtp', 'user')
EMAIL_PASSWORD = config.get('smtp', 'password')
EMAIL_FROM_ADDR = config.get('smtp', 'from_addr')
EMAIL_PORT = config.get('smtp', 'port')
ENABLE_SSL = config.get('smtp', 'ssl') == 'True'
ADMIN_EMAIL = config.get('smtp', 'cc_addr')
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

TEST_RUNNER = 'test.NoDbTestRunner'


#if os.getenv('environment', None) == 'TEST' or os.getenv('REQUESTLOG',
#                                                         None) == 'TRUE':
#    MIDDLEWARE.insert(0, 'apitimelog.middleware.RequestLogMiddleware')


#if os.getenv('environment', None) == 'TEST' or os.getenv('PYTHONAGENT', None) == 'TRUE':
#    MIDDLEWARE.insert(0, 'dongtai_agent_python.middlewares.django_middleware.FireMiddleware')
if os.getenv('environment', None) == 'TEST' or os.getenv('SAVEEYE',
                                                         None) == 'TRUE':
    CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null', )
if os.getenv('environment', 'PROD') in ('TEST', 'DOC') or os.getenv(
        'DOC', None) == 'TRUE':
    from django.utils.translation import gettext_lazy as _
    INSTALLED_APPS.append('drf_spectacular')
    SPECTACULAR_SETTINGS = {
        'TITLE':
        'DongTai WebApi Doc',
        'VERSION':
        "1.1.0",
        'PREPROCESSING_HOOKS':
        ['drf_spectacular.hooks.preprocess_exclude_path_format'],
        'URL_FORMAT_OVERRIDE':
        None,
        'DESCRIPTION':
        _("""Here is the API documentation in dongtai_conf. The corresponding management part API can be found through the relevant tag.

There are two authentication methods. You can obtain csrf_token and sessionid through the login process, or access the corresponding API through the user's corresponding Token.

The Token method is recommended here, and users can find it in the Agent installation interface such as -H
  'Authorization: Token {token}', here is the token corresponding to the user, the token method also requires a token like this on the request header."""
          ),
    }
    REST_FRAMEWORK[
        'DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'


if os.getenv('environment', None) == 'TEST' or os.getenv('CPROFILE',
                                                         None) == 'TRUE':
    DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False
    MIDDLEWARE.append(
        'django_cprofile_middleware.middleware.ProfilerMiddleware')

SCA_BASE_URL = config.get('sca', 'base_url')

if os.getenv('environment', None) in ('TEST', 'PROD'):
    SESSION_COOKIE_DOMAIN = config.get('other',
                                            'demo_session_cookie_domain')
    CSRF_COOKIE_DOMAIN = SESSION_COOKIE_DOMAIN
    DOMAIN = config.get('other', 'domain')

try:
    DOMAIN_VUL = config.get('other', 'domain_vul')
except Exception as e:
    DOMAIN_VUL = "localhost"

from urllib.parse import urljoin
#OPENAPI
BUCKET_URL = 'https://oss-cn-beijing.aliyuncs.com'
BUCKET_NAME = 'dongtai'
BUCKET_NAME_BASE_URL = 'agent/' if os.getenv('active.profile',
                                             None) != 'TEST' else 'agent_test/'
VERSION = 'latest'
# CONST
PENDING = 1
VERIFYING = 2
CONFIRMED = 3
IGNORE = 4
SOLVED = 5
ENGINE_URL = config.get("engine", "url")
HEALTH_ENGINE_URL = urljoin(ENGINE_URL, "/api/engine/health")
BASE_ENGINE_URL = config.get("engine", "url") + '/api/engine/run?method_pool_id={id}'
SCA_ENGINE_URL = config.get("engine","url") + '/api/engine/sca?agent_id={agent_id}' \
                            + '&package_path={package_path}&package_signature={package_signature}' \
                            + '&package_name={package_name}&package_algorithm={package_algorithm}'
REPLAY_ENGINE_URL = config.get("engine", "url") + '/api/engine/run?method_pool_id={id}&model=replay'

CELERY_BROKER_URL = 'redis://:%(password)s@%(host)s:%(port)s/%(db)s' % {
    'password': config.get("redis", 'password'),
    'host': config.get("redis", 'host'),
    'port': config.get("redis", 'port'),
    'db': config.get("redis", 'db'),
}
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_EXPIRES = 600
# CELERY_WORKER_LOG_FORMAT = '%(asctime)s [%(module)s %(levelname)s] %(message)s'
# CELERY_WORKER_LOG_FORMAT = '%(message)s'
# CELERY_WORKER_TASK_LOG_FORMAT = '%(task_id)s %(task_name)s %(message)s'
CELERY_WORKER_TASK_LOG_FORMAT = '%(message)s'
# CELERY_WORKER_LOG_FORMAT = '%(asctime)s [%(module)s %(levelname)s] %(message)s'
CELERY_WORKER_LOG_FORMAT = '%(message)s'
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_WORKER_REDIRECT_STDOUTS = True
CELERY_WORKER_REDIRECT_STDOUTS_LEVEL = "ERROR"
# CELERY_WORKER_HIJACK_ROOT_LOGGER = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 5000
# CELERYD_CONCURRENCY = 8
CELERY_IGNORE_RESULT = True

CELERY_TASK_SOFT_TIME_LIMIT = 3600
CELERY_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_ACKS_ON_FAILURE_OR_TIMEOUT = False
DJANGO_CELERY_BEAT_TZ_AWARE = False
from ast import literal_eval

DONGTAI_CELERY_CACHE_PREHEAT = safe_execute(
    True, BaseException, lambda x, y: literal_eval(config.get(x, y)), "other",
    "cache_preheat")
DEFAULT_CIRCUITCONFIG = {
    'SYSTEM': {
        "name":
        "系统配置",
        "metric_group":
        1,
        "interval":
        1,
        "deal":
        1,
        "is_enable":
        1,
        "is_deleted":
        0,
        "targets": [],
        "metrics": [{
            "metric_type": 1,
            "opt": 5,
            "value": 100
        }, {
            "metric_type": 2,
            "opt": 5,
            "value": 100
        }, {
            "metric_type": 3,
            "opt": 5,
            "value": 1000000000
        }]
    },
    'JVM': {
        "name":
        "JVM",
        "metric_group":
        2,
        "interval":
        1,
        "deal":
        1,
        "is_enable":
        1,
        "is_deleted":
        0,
        "targets": [],
        "metrics": [{
            "metric_type": 4,
            "opt": 5,
            "value": 100
        }, {
            "metric_type": 5,
            "opt": 5,
            "value": 1000000000
        }, {
            "metric_type": 6,
            "opt": 5,
            "value": 1000000
        }, {
            "metric_type": 7,
            "opt": 5,
            "value": 1000000
        }, {
            "metric_type": 8,
            "opt": 5,
            "value": 1000000
        }]
    },
    'APPLICATION': {
        "name":
        "应用配置",
        "metric_group":
        3,
        "interval":
        1,
        "deal":
        1,
        "is_enable":
        1,
        "is_deleted":
        0,
        "targets": [],
        "metrics": [{
            "metric_type": 9,
            "opt": 5,
            "value": 10000
        }, {
            "metric_type": 10,
            "opt": 5,
            "value": 100000000
        }]
    }
}

