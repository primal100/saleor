from saleor.settings import *

ROOT_URLCONF = 'shop.urls'

WSGI_APPLICATION = 'shop.wsgi.application'

TIME_ZONE = 'Africa/Kampala'
USE_I18N = False

CONTACT_EMAIL = 'nilepottery@gmail.com'

INSTALLED_APPS = [
    # External apps that need to go before django's
    'storages',

    # Django modules
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.postgres',
    'django.forms',

    # Local apps
    'saleor.account',
    'saleor.discount',
    'saleor.product',
    'saleor.cart',
    'saleor.checkout',
    'saleor.core',
    'saleor.graphql',
    'saleor.order.OrderAppConfig',
    'saleor.dashboard',
    'saleor.shipping',
    'saleor.search',
    'saleor.site',
    'saleor.data_feeds',

    # External apps
    'versatileimagefield',
    'django_babel',
    'bootstrap4',
    'django_fsm',
    'django_prices',
    'django_prices_openexchangerates',
    'graphene_django',
    'mptt',
    'payments',
    'webpack_loader',
    'social_django',
    'django_countries',
    'django_filters',
    'django_celery_results',
    'impersonate',
    'phonenumber_field',

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
        'client_id': 'ASNU9Lt0AYxvzhuVL8P4ycsav3KtdXWsoZ8Kuz0if2IBvZ6TaGNzIQUvhF8qRjjj3Cv9PPlZRXzeRzcH',
        'secret': os.environ.get("PAYPAL_SECRET"),
        'endpoint': os.environ.get('PAYPAL_URL'),
        'capture': False}),
    'stripe': ('payments.stripe.StripeProvider', {
        'secret_key': os.environ.get("STRIPE_SECRET"),
        'public_key': 'pk_test_nxCSX2soBvRTS1Q5MYejQ8vN'})
    }
CHECKOUT_PAYMENT_CHOICES = [
    ('paypal', 'Paypal'), ('stripe', 'Credit Card')]
