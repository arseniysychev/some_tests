from django import forms


class MailSendForm(forms.Form):
    email = forms.EmailField()
