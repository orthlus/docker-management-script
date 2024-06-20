#!/usr/bin/python
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

    for row in content:
        if re.match(r'^ {2}[a-z]', row):
            print(row.strip().split(':')[0])
        if 'container_name' in row:
            print(row.replace('container_name:', '').strip())


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
