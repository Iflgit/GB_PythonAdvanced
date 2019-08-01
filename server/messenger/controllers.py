from protocol import make_response
from decorators import debug_log

@debug_log
def send_message(request):
    return make_response(request, 200)

