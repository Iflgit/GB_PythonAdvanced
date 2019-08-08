import yaml
import socket
import json
import threading
import zlib
from argparse import ArgumentParser
from datetime import datetime


def read(sock, buffersize):
    while True:
        try:
            response = sock.recv(buffersize)
        except Exception as err:
            print(f'Internal client error {err}. Stop reading.')
            return

        try:
            bytes_response = zlib.decompress(response)
        except Exception as err:
            print(f'Error in recieved data with {err}. Now stop receiving data.')
            return
        else:
            print(bytes_response.decode())

def make_request(action, data):
    request = {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data
    }
    return request

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False, help='Sets config file'
)
parser.add_argument(
    '-p', '--port', type=int, required=False, help='Sets server port number'
)
parser.add_argument(
    '-a', '--address', type=str, required=False, help = 'Sets server ip address'
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

if args.port:
    config.update({'port':args.port})

if args.address:
    config.update({'host':args.host})

host, port = config.get('host'), config.get('port')

try:
    print(f'creating socket...')
    client_socket = socket.socket()
    # client_socket.settimeout(5)
    print(f'connecting to {host}:{port}')
    client_socket.connect((host, port))
    print('Client was started')

    read_thread = threading.Thread(
        target=read, args=(client_socket, config.get('buffersize'))
    )
    read_thread.start()

    while True:
        action = input('Enter action: ')
        data = input('Enter message: ')

        request = make_request(action, data)

        str_request = json.dumps(request)

        bytes_requests = zlib.compress(str_request.encode())

        client_socket.send(bytes_requests)
        print(f'Client sending data: /{str_request}/')
except ConnectionRefusedError:
    print('Connection error, check server please.')
except KeyboardInterrupt:
    print('client shutdown.')
