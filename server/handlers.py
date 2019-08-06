import json
import logging
from protocol import validate_request, make_response
from actions import resolve
from middlewares import compression_middleware, encription_middleware
from decorators import trace_log



@trace_log
@compression_middleware
@encription_middleware
def handle_default_request(bytes_request):
    request = json.loads(bytes_request.decode())

    if validate_request(request):
        action_name = request.get('action')
        controller = resolve(action_name)
        if controller:
            try:
                logging.info(f'Client send valid request {request}')
                response = controller(request)
            except Exception as err:
                logging.critical(f'Internal server error: {err}')
                response = make_response(request, 500, data='Internal erver error')
        else:
            logging.error(f'Controller with action name {action_name} does not exists')
            response = make_response(request, 404, 'Action not found')
    else:
        logging.info(f'Client send invalid request {request}')
        response = make_response(request, 400, 'Wrong request')

    str_response = json.dumps(response)
    return str_response.encode()
