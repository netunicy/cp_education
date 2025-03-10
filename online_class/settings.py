import django_heroku
from pathlib import Path
import os
import stripe
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = False

#with open(os.path.join(BASE_DIR,'secret_key.txt')) as f:
    #SECRET_KEY = f.read().strip()
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '2a92df29dgdfhkghjl92lfg44sd4g1gds2f422d8g474d2fghdf26ga6faer4rsttyj')
    
ALLOWED_HOSTS = ['127.0.0.1:8000','localhost','www.cpnetuni.com','cpnetuni.com', 'dimpan-bb7f5a0620d7.herokuapp.com']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'homepage.apps.HomepageConfig',
    'accounts.apps.AccountsConfig',
    'partnership.apps.PartnershipConfig',
    'contact_us.apps.ContactUsConfig',
    'blogs.apps.BlogsConfig',
    'primary.apps.PrimaryConfig',
    'captcha',
    'tinymce',
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

ROOT_URLCONF = 'online_class.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join (BASE_DIR, 'homepage/templates/homepage'),
                os.path.join (BASE_DIR, 'accounts/templates/accounts'),
                os.path.join (BASE_DIR, 'partnership/templates/partnership'),
                os.path.join (BASE_DIR, 'contact_us/templates/contact_us'),
                os.path.join (BASE_DIR, 'blogs/templates/blogs'),
                os.path.join (BASE_DIR, 'primary/templates/primary'),
                 
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

WSGI_APPLICATION = 'online_class.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd48bt70segul3c',
        'USER': 'u7cutb55nc591d',
        'PASSWORD': 'p518aecec04b3dcb9b6e5a784bc8b86ed31eed876839204490c0ec6ed18a977e9',
        'HOST': 'ec2-54-205-238-146.compute-1.amazonaws.com',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c timezone=Europe/Athens',
        }
    }
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

USE_I18N = True

TIME_ZONE = 'Europe/Athens'

USE_TZ = False


# Expire session after 30 minutes of inactivity



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'  # Default είναι τυχαία γράμματα
CAPTCHA_LENGTH = 6  # Μήκος του CAPTCHA
CAPTCHA_IMAGE_SIZE = (200, 50)  # Διαστάσεις εικόνας
CAPTCHA_FONT_SIZE = 36  # Μέγεθος γραμματοσειράς
CAPTCHA_TIMEOUT = 5  # Διάρκεια ισχύος CAPTCHA σε λεπτά

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS= 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800  # 30 minutes (in seconds)
SESSION_SAVE_EVERY_REQUEST = True  # Refresh session expiration on every request


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'live.smtp.mailtrap.io'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'api'
EMAIL_HOST_PASSWORD = '388ed30f960c9bd511b4cbd740d05b7d'
DEFAULT_FROM_EMAIL = 'no-reply@cpnetuni.com'

TINYMCE_DEFAULT_CONFIG = {
    "height": 600,
    "width": 960,
    "language": "el",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code "
               "fullscreen insertdatetime media table help wordcount",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | "
               "alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist checklist | "
               "forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
               "fullscreen preview save | insertfile image media pageembed template link anchor codesample | "
               "a11ycheck ltr rtl | showcomments addcomment code",
    "fontsize_formats": "8pt 10pt 12pt 14pt 18pt 24pt 36pt 48pt",  # Εμφανίζεται η λίστα μεγέθους γραμματοσειράς
    "content_style": "body { font-family: Arial, sans-serif; font-size: 14px; }",
    "branding": False,  # Αφαιρεί το TinyMCE branding
    "toolbar_mode": "wrap",  # Βελτιώνει την εμφάνιση της toolbar
    "image_advtab": True,  # Ενεργοποιεί προχωρημένες επιλογές για εικόνες
    "contextmenu": "link image table",  # Εμφανίζει επιλογές όταν κάνεις δεξί κλικ
}

STRIPE_PUBLISHABLE_KEY = 'pk_live_51MlR2oGb8TMtV2YPsGpBrHOCyNWf3r68pRlib5nFxfbT4su4D0Q7csnmv8woLyDDLRpfqLwypmlNtr3EpREdLOEw00WJRRP8ZG'
STRIPE_SECRET_KEY = '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'
stripe.api_key = STRIPE_SECRET_KEY

django_heroku.settings(locals())



