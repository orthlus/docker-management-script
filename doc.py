#!/usr/bin/python3
import subprocess
import sys
import re

docker_compose_default_filename = 'docker-compose-app.yml'
allowed_commands = ['up', 'down', 'pull', 'start', 'stop', 'restart', 'logs']
helpers = ['ls']


def usage():
    print('usage:\n\targs:')
    print('\t1.docker service name (required for some commands)')
    print('\t\talso allowed "all" for control all services in file')
    print('\t2.docker command (required)')
    print('\t\tallowed - ' + ','.join(allowed_commands))
    print('\t3.docker compose file (optional)')
    print('\t\tdefault file - ' + docker_compose_default_filename)
    print('\n\talso there are helpers - ' + ','.join(helpers))
    exit(0)


def run(_command: str): subprocess.run(_command.split(' '), shell=True)


def get_approve(_command, _service):
    s_in = input(f'do you want run "{_command} {_service}"? ')
    if s_in != 'y' and s_in != 'd':
        exit(0)


def ls_docker_file():
    if len(args) == 2:
        docker_file = args[2]
    elif len(args) == 1:
        docker_file = docker_compose_default_filename

    with open(docker_file, encoding='utf8') as file:
        content = file.readlines()

    yml_not_services_keys = ['x-logging:', 'volumes:']
    in_services = False
    data = {}
    last_service = ''
    for row in content:
        if row.startswith('#'):
            continue
        cleaned_row = row.replace('\n', '')

        if cleaned_row == 'services:':
            in_services = True
        if cleaned_row in yml_not_services_keys:
            in_services = False

        if in_services:
            if re.match(r'^ {2}[a-z]', cleaned_row):
                service_name = cleaned_row.strip().split(':')[0]
                data[service_name] = ''
                last_service = service_name
            if 'container_name' in cleaned_row:
                container_name = cleaned_row.replace('container_name:', '').strip()
                data[last_service] = container_name

    for service, container in data.items():
        if container == '':
            print(service)
        else:
            print(f'{service} ({container})')


def call_helpers():
    match args[0]:
        case 'ls':
            ls_docker_file()


def call_default():
    if len(args) == 3:
        docker_file = args[2]
    elif len(args) == 2:
        docker_file = docker_compose_default_filename
    else:
        usage()

    service = args[0]
    command = args[1]
    if command not in allowed_commands:
        usage()

    if command == 'logs':
        command = 'logs --follow'
    if command == 'up':
        command = 'up -d'

    if service == 'all':
        command_to_run = f'docker compose -f {docker_file} {command}'
    else:
        command_to_run = f'docker compose -f {docker_file} {command} {service}'

    get_approve(command, service)
    run(command_to_run)


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) < 1:
        usage()
    if args[0] in helpers:
        call_helpers()
    else:
        call_default()
