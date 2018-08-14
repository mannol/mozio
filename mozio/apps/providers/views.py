from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

from .models import Provider
from mozio.response import good_response, error_response

def load_query_params(query):
    name = query.get('name')
    email = query.get('email')
    phone = query.get('phone')
    language = query.get('lang')
    currency = query.get('currency')
    return (name, email, phone, language, currency)

def save_and_return(p):
    try:
        p.save()
    except ValidationError:
        return error_response('BadRequest')
    except:
        return error_response('InternalServerError')

    return good_response(p.to_dict())

# the view is implemented using CRUD, so all the requests
# go to the same path: example.com/providers/<provider_id>/?data=value
# Also: NOTE: i disabled security for simplicity, obviously,
# I wouldn't do it in production env.
@csrf_exempt
def index(request, provider_id = ''):
    if request.method == 'POST':
        return create(provider_id, request.GET)
    if request.method == 'GET':
        return read(provider_id, request.GET)
    if request.method == 'PUT':
        return update(provider_id, request.GET)
    if request.method == 'DELETE':
        return delete(provider_id, request.GET)
    
    return error_response('BadRequest')

def create(provider_id, query):
    # if the user provided a provider_id it means the request is invalid
    if provider_id:
        return error_response('BadRequest')

    name, email, phone, language, currency = load_query_params(query)
    
    # All the fields are required
    if not name or not email or not phone or not language or not currency:
        return error_response('BadRequest')

    p = Provider(Name=name, Email=email, PhoneNumber=phone, Language=language, Currency=currency)

    return save_and_return(p)

def read(provider_id, query):
    if not provider_id:
        return error_response('BadRequest')

    try:
        p = Provider.objects.get(Id=provider_id)
    except Provider.DoesNotExist:
        return error_response('NotFound')

    return good_response(p.to_dict())

def update(provider_id, query):
    if not provider_id:
        return error_response('BadRequest')

    try:
        p = Provider.objects.get(Id=provider_id)
    except Provider.DoesNotExist:
        return error_response('NotFound')

    name, email, phone, language, currency = load_query_params(query)
    
    if name:
        p.Name = name
    if email:
        p.Email = email
    if phone:
        p.PhoneNumber = phone
    if language:
        p.Language = language
    if currency:
        p.Currency = currency

    return save_and_return(p)

def delete(provider_id, query):
    if not provider_id:
        return error_response('BadRequest')

    try:
        p = Provider.objects.get(Id=provider_id)
    except Provider.DoesNotExist:
        return error_response('NotFound')

    p.delete()
    return good_response()
