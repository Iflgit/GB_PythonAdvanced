import yaml
import socket
import json
import logging
import threading
import select
from argparse import ArgumentParser
from protocol import validate_request, make_response
from actions import resolve
from handlers import handle_default_request

def read(sock, connections, requests, buffersize):
    try:
        bytes_request = sock.recv(buffersize)
    except Exception:
        connections.remove(sock)
    else:
        client_requests.append(bytes_request)

def write(sock, connections, response):
    try:
        sock.send(response)
    except Exception:
        connections.remove(sock)

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, 
    required=False, help='Sets config file'
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

connections = []
client_requests = []

try:
    logging.info('creating socet...')
    server_socket = socket.socket()

    logging.info(f'binding socket on {host}:{port}')
    server_socket.bind((host, port))
    # server_socket.setblocking(False)
    server_socket.settimeout(0)

    logging.info(f'listening for up to {5} clients')
    server_socket.listen(5)

    logging.info(f'Server started on {host}:{port}. Ctrl+C for exit.')

    while True:
        try:
            # logging.info('waiting for client connections... ')
            client_socket, client_address = server_socket.accept()
            logging.info(f'Client was detected {client_address[0]}:{client_address[1]}')
            connections.append(client_socket)
        except:
            pass
        try:
            rlist, wlist, xlist, = select.select(connections, connections, connections, 0)
        except:
            continue

        for read_client in rlist:
            read_thread = threading.Thread(
                target=read, 
                args=(read_client, connections, client_requests, config.get('buffersize'))
                )
            read_thread.start()

        if client_requests:
            bytes_request = client_requests.pop()
            bytes_response = handle_default_request(bytes_request)
            for write_client in wlist:
                write_thread = threading.Thread(
                    target=write, args=(write_client, connections, bytes_response)
                )
                write_thread.start()

except KeyboardInterrupt:
    logging.info('Server shutdown.')
except OSError:
    logging.critical(f'Cant start server. No administrative privelegue or {host}:{port} is busy')
except Exception as err:
    logging.critical(f'Unhandled Internal server error: {err}')
