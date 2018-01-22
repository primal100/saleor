from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.template import loader


def send_activation_mail(request, user):

    token_generator = default_token_generator

    email_template_name = 'account/email/confirm_email_message.txt'
    subject_template_name = 'account/email/confirm_email_subject.txt'

    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain

    email = user.email

    context = {
        'protocol': 'https' if request.is_secure() else 'http',
        'email': email,
        'domain': domain,
        'site_name': site_name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': token_generator.make_token(user),
    }

    subject = loader.render_to_string(subject_template_name)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, None, [email])

    email_message.send()
