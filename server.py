import yaml
import socket
from argparse import ArgumentParser

# import ctypes, sys

# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False

# if is_admin():
#     # Code of your program here
#     pass
# else:
#     # Re-run the program with admin rights
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

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

host, port = config.get('host'), config.get('port')

try:
    print('creating socet...')
    server_socket = socket.socket()
    print(f'binding socket on {host}:{port}')
    server_socket.bind((host, port))
    print(f'listening for /{5}/ clients')
    server_socket.listen(5)

    print(f'Server started on {host}:{port}. Ctrl+C for exit.')

    while True:
        print('waiting for client connections... ')
        client, address = server_socket.accept()
        print(f'Client was detected {address[0]}:{address[1]}')

        client_request = client.recv(config.get('buffersize')).decode()
        print(f'Client send message {client_request}')

        client.send((f'ECHO {client_request}').encode())
        client.close()
except KeyboardInterrupt:
    print('Server shutdown.')
except OSError:
    print(f'Cant start server. No administrative privelegue or {host}:{port} is busy')