from django.conf.urls import url

from .views import test_age_get, SendMailView

urlpatterns = [
    url(r'^$', test_age_get),
    url(r'^send$', SendMailView.as_view(), name='email_send'),
]
