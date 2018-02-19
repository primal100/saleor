from django.conf import settings
from django.forms import forms, fields, widgets
from templated_email import send_templated_mail

class ContactForm(forms.Form):
    name = fields.CharField()
    email = fields.EmailField()
    subject = fields.CharField()
    message = fields.CharField(widget=widgets.Textarea)

    def send_email(self):
        context = {'name': self.cleaned_data['name'],
                   'subject': self.cleaned_data['subject'],
                   'message': self.cleaned_data['message']}
        send_templated_mail(
            template_name='source/core/contactus',
            from_email=self.cleaned_data['email'],
            recipient_list=[settings.CONTACT_EMAIL],
            context=context)
