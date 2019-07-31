from protocol import make_response
from decorators import debug_log

@debug_log
def get_echo(request):
    print('get_echo controller call')
    data = request.get('data')
    return make_response(request, 200, data)

