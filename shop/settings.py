from saleor.settings import *
CELERY_TASK_ALWAYS_EAGER = True

ROOT_URLCONF = 'shop.urls'

WSGI_APPLICATION = 'shop.wsgi.application'

TIME_ZONE = 'Africa/Kampala'
USE_I18N = False

CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL')

INSTALLED_APPS += [
    #Custom apps
    'shop.corex',
    'shop.orderx',
    'shop.productx'
]

STATICFILES_DIRS = [
    #('assets', os.path.join(PROJECT_ROOT, 'shop', 'static', 'assets')),
    ('images', os.path.join(PROJECT_ROOT, 'shop', 'static', 'images')),
] + STATICFILES_DIRS

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_ROOT, 'shop', 'templates'),
             os.path.join(PROJECT_ROOT, 'templates')],
    'OPTIONS': {
        'debug': DEBUG,
        'context_processors': context_processors,
        'loaders': loaders,
        'string_if_invalid': '<< MISSING VARIABLE "%s" >>' if DEBUG else ''}}]

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://saleor:saleor@localhost:5432/saleorshop',
        conn_max_age=600)}

context_processors += [
    'shop.corex.context_processors.currencies'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django_babel.middleware.LocaleMiddleware',
    'saleor.core.middleware.discounts',
    'shop.corex.middleware.google_analytics',
    'saleor.core.middleware.country',
    'shop.corex.middleware.currency',
    'saleor.core.middleware.site',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'impersonate.middleware.ImpersonateMiddleware']

PAYMENT_VARIANTS = {
    'paypal': ('payments.paypal.PaypalProvider', {
        'client_id': os.environ.get("PAYPAL_CLIENT_ID"),
        'secret': os.environ.get('PAYPAL_SECRET'),
        'endpoint': os.environ.get('PAYPAL_URL'),
        'capture': True}),
    'stripe': ('payments.stripe.StripeProvider', {
        'secret_key': os.environ.get('STRIPE_SECRET'),
        'public_key': os.environ.get('STRIPE_PUBLIC')})
    }
CHECKOUT_PAYMENT_CHOICES = [
    ('paypal', 'Paypal'), ('stripe', 'Credit Card')]
