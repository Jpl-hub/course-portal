from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env automatically (keeps credentials/config out of code)
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = "demo-secret-key-change-in-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Keep only essentials to avoid generating unwanted tables.
INSTALLED_APPS = [
    "courses",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "course_portal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [],
        },
    },
]

WSGI_APPLICATION = "course_portal.wsgi.application"

# MySQL is shown as the primary data source in this demo.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE", "course_portal"),
        "USER": os.getenv("MYSQL_USER", "root"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD", "example"),
        "HOST": os.getenv("MYSQL_HOST", "localhost"),
        "PORT": os.getenv("MYSQL_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

# Logging removed for a cleaner demo output.
