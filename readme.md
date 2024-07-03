# Script for management docker compose on linux

## Install:
- copy doc.py on linux host
- `chmod +x doc.py`

For easiest call 'doc.py' can be just 'doc'

Also on host must be:
- installed docker
- docker compose file (.yml/.yaml)

### Docker file name
Default docker file name - docker-compose-app.yml. Other name must be passed to script

### Example
For example, `$ cat docker-compose-app.yml`
```
services:
  pg:
    container_name: postgres
    image: postgres:16
  wg:
    container_name: wireguard
    image: lscr.io/linuxserver/wireguard:latest
```
To pull and up one docker service from file, for example, postgres, commands will be:
- `doc pg pull`
- `doc pg up`

This script can be secure management docker, for example here impossible accidentally down all docker services, for this must be passed 'all' explicitly 

Also, `ls` command printed all services and container names from docker compose file

```
$ doc.py ls
pg
postgres
wg
wireguard
```

Usage (duplicated in script):
```
args:
1.docker service name (required for some commands)
        also allowed "all" for control all services in file
2.docker command (required)
        allowed - up,down,pull,start,stop,restart,logs
3.docker compose file (optional)
        default file - docker-compose-app.yml

also there are helpers - ls
```
