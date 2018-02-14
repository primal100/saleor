from django.shortcuts import redirect
from .models import UserPreferences

def changecurrency(request):
    data = request.GET
    currency = data.get("currency")
    next_path = data.get("next")
    if request.user and request.user.is_authenticated:
        UserPreferences.objects.update_or_create(user=request.user, defaults={'currency': currency})
    else:
        UserPreferences.objects.update_or_create(session=request.session, defaults={'currency': currency})
    return redirect(next_path)
