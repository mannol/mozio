from django.http import JsonResponse

def good_response(data = None):
    return JsonResponse({'success': True, 'data': data})

def error_response(name):
    return JsonResponse({'success': False, 'error': name})
