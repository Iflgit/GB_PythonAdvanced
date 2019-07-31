from protocol import make_response
from decorators import debug_log

@debug_log
def send_message(request):
    print('send_message controller call')
    return make_response(request, 200)

