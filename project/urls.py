from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app1/', include('project.app1.urls', namespace='app1')),
    url(r'^google/', include('project.google_api.urls', namespace='google')),
    url(r'^facebook/', include('project.facebook.urls', namespace='facebook')),
    url(r'^user/', include('project.users.urls', namespace='user')),
    url(r'^async/', include('project.async_works.urls', namespace='async')),
]
