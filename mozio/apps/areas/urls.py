from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^areas/(?P<provider_id>.+)/(?P<area_id>.+)$', views.index, name='index'),
    url(r'^areas/(?P<provider_id>.+)/(?P<area_id>.+)?([?#]+.+)?$', views.index, name='index'),
    url(r'^areas/(?P<provider_id>.+)(/.*)?$', views.index, name='index'),
]

