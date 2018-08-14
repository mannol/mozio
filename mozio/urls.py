from django.conf.urls import url, include

urlpatterns = [
    url('api/', include('mozio.apps.providers.urls', namespace='providers')),
    url('api/', include('mozio.apps.areas.urls', namespace='areas')),
    url('api/', include('mozio.apps.query.urls', namespace='query')),
]
 