from django.shortcuts import redirect
from .models import UserPreferences

def changecurrency(request):
    data = request.GET
    currency = data.get("currency")
    next_path = data.get("next")
    if request.user and request.user.is_authenticated:
        UserPreferences.objects.update_or_create(user=request.user, defaults={'currency': currency})
    else:
        UserPreferences.objects.update_or_create(sessionid=request.session.session_key, defaults={'currency': currency})
    return redirect(next_path)
