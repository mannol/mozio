from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^query/(?P<lat>.+)/(?P<lon>.+)(/.*)?$', views.index, name='index'),
]
