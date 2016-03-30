from datetime import date, datetime

from django.conf import settings
from django.shortcuts import HttpResponse, render
from django.db.models import F, Func, Count
from django.views.generic import View, TemplateView, FormView

from utils.email_sender import HTMLEmail
from .forms import MailSendForm
from .models import User


def get_age(born):
    today = date.today()
    return today.year - born.year + (
        (today.month, today.day) < (born.month, born.day)
    )


def test_age_get(request):
    q = request.GET.getlist('q', default=[])
    q = [tuple(int(age) for age in str(i).split('-')) for i in q]
    a = User.objects.annotate(age=F('born'))
    return HttpResponse(a)


class SendMailView(FormView):
    template_name = 'users/send_email.html'
    form_class = MailSendForm

    # success_url = '/thanks/'

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        html_email = HTMLEmail(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            images_dir=settings.MEDIA_ROOT,
            template_html='{base}/{path}'.format(
                base=settings.BASE_DIR,
                path='project/users/templates/users/email.html'
            ),
            auth=dict(
                user=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
            ),
        )
        html_email.send(
            subject='subject',
            sender=settings.EMAIL_HOST_USER,
            sender_name='sender_name',
            recipient=form.cleaned_data['email'],
            recipient_name='recipient_name',
            context={'param_1': 'aaaa'},
            images=('background.jpeg',),
        )
        return super(SendMailView, self).form_valid(form)
