from datetime import datetime

def validate_request(request):
    print('validate_request call')
    if 'action' in request and 'time' in request:
        return True
    return False

def make_response(request, code, data=None):
    print('make_response call')
    return{
        'action': request.get('action'),
        'time': datetime.now().timestamp(),
        'code': code,
        'data': data
    }

