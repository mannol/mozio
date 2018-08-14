from django.contrib.gis.geos import Point

from mozio.apps.areas.models import Area
from mozio.response import good_response, error_response

# the view is implemented using CRUD, so all the requests
# go to the same path: example.com/providers/<provider_id>/?data=value
def index(request, lat = '', lon = ''):
    if request.method != 'GET':
        return error_response('BadRequest')

    try:
        lat = float(lat)
        lon = float(lon)
    except:
        return error_response('BadRequest')

    # this query is fast because it uses ST_Within on a gis index
    # NOTE: limits are not used for simplicity
    objects = Area.objects.filter(Polygon__contains=Point(x=lon, y=lat))

    return good_response(map(lambda x: x.to_dict(), objects))
