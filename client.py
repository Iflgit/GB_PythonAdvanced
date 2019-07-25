import yaml
import socket
from argparse import ArgumentParser


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

#if args.help:
#    parser.print_help()
#    exit(0)

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
    client_socket.settimeout(5)
    print(f'connecting to {host}:{port}')
    client_socket.connect((host, port))
    print('Client was started')

    message = input('Enter data: ')

    client_socket.send(message.encode())
    print(f'Client sending data: /{message}/')

    response = client_socket.recv(config.get('buffersize')).decode()
    print(f'Server send data {response}')
except ConnectionRefusedError:
    print('Connection error, please check server')
except KeyboardInterrupt:
    print('client shutdown.')