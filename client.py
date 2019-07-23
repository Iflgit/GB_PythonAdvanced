import yaml
import socket
from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False, help='Sets config file path'
)

parser.add_argument(
    '-p', '--port', type=int, required=False, help='Sets port number'
)

parser.add_argument(
    '-a', '--address', type=str, required=False, help = 'Sets ip address for bind'
)

args = parser.parse_args()

#if args.help:
#    parser.print_help()
#    exit(0)

config = {
    'host': 'localhost',
    'port': 8000,
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
    print(f'connecting to {host}:{port}')
    sock = socket.socket()
    sock.connect((host, port))
    print('Client was started')

    message = input('Enter data: ')

    sock.send(message.encode())
    print(f'Client send data {message}')

    response = sock.recv(config.get('buffersize')).decode()
    print(f'Server send data {response}')
except ConnectionRefusedError:
    print('Connection error, please check server')
except KeyboardInterrupt:
    print('client shutdown.')