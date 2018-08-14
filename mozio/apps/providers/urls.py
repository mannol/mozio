from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^providers/(?P<provider_id>.+)/$', views.index, name='index'),
    url(r'^providers/(?P<provider_id>.+)/?([?#]+.+)?$', views.index, name='index'),
    url(r'^providers(/.*)?$', views.index, name='index'),
]

