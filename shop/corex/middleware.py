import logging

import google_measurement_protocol as ga
from django.conf import settings
from django.utils.translation import get_language

from saleor.core.analytics import _report, get_client_id
from saleor.core.utils import get_client_ip, get_currency_for_country

logger = logging.getLogger(__name__)

def report_view(client_id, ip, path, language, headers):
    host_name = headers.get('HTTP_HOST', None)
    referrer = headers.get('HTTP_REFERER', None)
    pv = ga.PageView(path, host_name=host_name, referrer=referrer)
    extra_info = [{'ul': language, 'uip': ip}]
    extra_headers = {}
    user_agent = headers.get('HTTP_USER_AGENT', None)
    if user_agent:
        extra_headers['user-agent'] = user_agent
    _report(client_id, pv, extra_info=extra_info, extra_headers=extra_headers)

def google_analytics(get_response):
    """Report a page view to Google Analytics."""
    def middleware(request):
        client_id = get_client_id(request)
        path = request.path
        language = get_language()
        headers = request.META
        try:
            ip = get_client_ip(request)
            report_view(
                client_id, ip, path=path, language=language, headers=headers)
        except Exception:
            logger.exception('Unable to update analytics')
        return get_response(request)
    return middleware


def currency(get_response):
    """Take a country and assign a matching currency to `request.currency`."""
    def middleware(request):
        if hasattr(request, 'user') and request.user.is_authenticated and request.user.currency:
            request.currency = request.user.currency
        elif hasattr(request, 'session') and request.session.get('currency', None):
            request.currency = request.session['currency']
        if hasattr(request, 'country') and request.country is not None:
            request.currency = get_currency_for_country(request.country)
        else:
            request.currency = settings.DEFAULT_CURRENCY
        return get_response(request)

    return middleware
