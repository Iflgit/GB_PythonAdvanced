import yaml
from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False, help='config.yaml file with path'
)

args = parser.parse_args()

print(args)

config = {
    'host': 'localhost',
    'port':8000
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        config.update(file_config)

print(f'Config: {config}')

try:
    print('\nCtrl+C for exit')
    data = input('Input data: ')

    print('send data')

    print('recive data')
except KeyboardInterrupt:
    print('\nExiting...')