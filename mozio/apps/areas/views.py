from ast import literal_eval as make_tuple

from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Polygon
from django.views.decorators.csrf import csrf_exempt

from .models import Area
from mozio.apps.providers.models import Provider

from mozio.response import good_response, error_response

def save_and_return(a):
    try:
        a.save()
    except ValidationError:
        return error_response('BadRequest')
    except Exception, e:
        print(e)
        return error_response('InternalServerError')

    return good_response(a.to_dict())

def parse_polygon(polygon):
    try:
        polygon = polygon.split('_')
        polygon = map(lambda s: s.strip().strip('()'), polygon)
        polygon = map(make_tuple, polygon)
        return Polygon(polygon)
    except:
        return None

def load_query_params(query):
    name = query.get('name')
    price = query.get('price')
    polygon = query.get('polygon')
    return (name, price, polygon)
 
# the view is implemented using CRUD, so all the requests
# go to the same path: example.com/areas/<provider_id>/<area_id>/?data=value
@csrf_exempt
def index(request, provider_id = '', area_id = '-1'):
    if not provider_id:
        return error_response('BadRequest')

    try:
        area_id = int(area_id)
    except:
        return error_response('BadRequest')

    if request.method == 'POST':
        return create(provider_id, area_id, request.GET)
    if request.method == 'GET':
        return read(provider_id, area_id, request.GET)
    if request.method == 'PUT':
        return update(provider_id, area_id, request.GET)
    if request.method == 'DELETE':
        return delete(provider_id, area_id, request.GET)
    
    return error_response('BadRequest')

def create(provider_id, area_id, query):
    if area_id != -1:
        return error_response('BadRequest')

    name, price, polygon = load_query_params(query)
    
    polygon = parse_polygon(polygon)
    
    # All the fields are required
    if not name or not price or not polygon:
        return error_response('BadRequest')

    try:
        p = Provider.objects.get(Id=provider_id)
    except Provider.DoesNotExist:
        return error_response('NotFound')

    a = Area(Provider=p, Name=name, Price=price, Polygon=polygon)

    return save_and_return(a)

def read(provider_id, area_id, query):
    if area_id == -1:
        return error_response('BadRequest')

    try:
        a = Area.objects.get(id=area_id)
    except Area.DoesNotExist:
        return error_response('NotFound')

    return good_response(a.to_dict())

def update(provider_id, area_id, query):
    if area_id == -1:
        return error_response('BadRequest')

    try:
        a = Area.objects.get(id=area_id)
    except Area.DoesNotExist:
        return error_response('NotFound')

    name, price, polygon = load_query_params(query)
    
    polygon = parse_polygon(polygon)
    
    if name:
        a.Name = name
    if price:
        a.Price = price
    if polygon:
        a.Polygon = polygon

    return save_and_return(a)

def delete(provider_id, area_id, query):
    if area_id == -1:
        return error_response('BadRequest')

    try:
        a = Area.objects.get(id=area_id)
    except Area.DoesNotExist:
        return error_response('NotFound')

    a.delete()
    return good_response()
