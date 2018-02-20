from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView
from .forms import ContactForm
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

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_email()
        result = super().form_valid(form)
        messages.success(self.request,
                         "Thanks for your e-mail We will respond as soon as possible")
        return result

    def get_initial(self):
        initial = super(ContactView, self).get_initial()

        if self.request.user and self.request.user.is_authenticated:
            initial['email'] = self.request.user.email

        return initial
