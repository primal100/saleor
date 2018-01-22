from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import views as django_views, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlsafe_base64_decode
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from saleor.cart.utils import find_and_assign_anonymous_cart

from .forms import LoginForm, PasswordSetUpForm, SignupForm
from .utils import send_activation_mail

UserModel = get_user_model()


@find_and_assign_anonymous_cart()
def login(request):
    kwargs = {
        'template_name': 'account/login.html', 'authentication_form': LoginForm}
    return django_views.LoginView.as_view(**kwargs)(request, **kwargs)


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, _('You have been successfully logged out.'))
    return redirect(settings.LOGIN_REDIRECT_URL)


def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save(request)
        if settings.EMAIL_VERIFICATION_REQUIRED:
            messages.success(request, _('User has been created. Check your e-mail to verify your e-mail address.'))
            redirect_url = reverse_lazy("account_login")
        else:
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = auth.authenticate(
                request=request, email=email, password=password)
            if user:
                auth.login(request, user)
            messages.success(request, _('User has been created'))
            redirect_url = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
        return redirect(redirect_url)
    ctx = {'form': form}
    return TemplateResponse(request, 'account/signup.html', ctx)


def password_reset(request):
    kwargs = {
        'template_name': 'account/password_reset.html',
        'success_url': reverse_lazy('account_reset_password_done'),
        'email_template_name': 'account/email/password_reset_message.txt',
        'subject_template_name': 'account/email/password_reset_subject.txt'}
    return django_views.PasswordResetView.as_view(**kwargs)(request, **kwargs)


class PasswordResetConfirm(django_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_from_key.html'
    success_url = reverse_lazy('account_reset_password_complete')
    set_password_form = PasswordSetUpForm
    token = None
    uidb64 = None


def password_reset_confirm(request, uidb64=None, token=None):
    kwargs = {
        'template_name': 'account/password_reset_from_key.html',
        'success_url': reverse_lazy('account_reset_password_complete'),
        'set_password_form': 'PasswordSetUpForm',
        'token': token,
        'uidb64': uidb64}
    return PasswordResetConfirm.as_view(**kwargs)(
        request, **kwargs)


class EmailVerificationView(View):
    success_url = reverse_lazy('account_login')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if self.token_generator.check_token(self.user, token):
                self.user.email_verified = True
                self.user.save()
                messages.success(self.request, _("E-mail verification successful. You may now login."))
            else:
                send_activation_mail(self.request, self.user)
                messages.error(self.request, _("E-mail verification failed. Activation e-mail resent."))
        else:
            messages.error(self.request, _("E-mail verification failed. User not found."))
        return HttpResponseRedirect(reverse_lazy('account_login'))

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring on Python 3
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        return user


email_confirmation = EmailVerificationView.as_view()
