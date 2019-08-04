import yaml
import socket
import json
import logging
from argparse import ArgumentParser
from protocol import validate_request, make_response
from actions import resolve

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False, help='Sets config file'
)

args = parser.parse_args()

config = {
    'host': 'localhost',
    'port': 8001,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        config.update(file_config)

'''just keep it there for history

logger = logging.getLogger('main')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('main.log')
stream_handler = logging.StreamHandler()

file_handler.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.DEBUG)

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)
'''

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

host, port = config.get('host'), config.get('port')

try:
    logging.info('creating socet...')
    server_socket = socket.socket()
    logging.info(f'binding socket on {host}:{port}')
    server_socket.bind((host, port))
    logging.info(f'listening for up to {5} clients')
    server_socket.listen(5)

    logging.info(f'Server started on {host}:{port}. Ctrl+C for exit.')

    while True:
        logging.info('waiting for client connections... ')
        client_socket, client_address = server_socket.accept()
        logging.info(f'Client was detected {client_address[0]}:{client_address[1]}')

        client_request = client_socket.recv(config.get('buffersize')).decode()
        logging.info(f'Client send data {client_request}')

        request = json.loads(client_request)

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

        str_responce = json.dumps(response)
        client_socket.send(str_responce.encode())
        client_socket.close()
except KeyboardInterrupt:
    logging.info('Server shutdown.')
except OSError:
    logging.critical(f'Cant start server. No administrative privelegue or {host}:{port} is busy')
except Exception as err:
    logging.critical(f'Unhandled Internal server error: {err}')
