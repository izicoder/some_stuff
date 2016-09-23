from os import system
from sys import argv


def conn_to(host, port):
    system('telnet {} {}'.format(host, port))


def scan(host):
    for p in range(1, 1025):
        print('=' * 10, 'port #{}'.format(p))
        conn_to(host, p)

if __name__ == '__main__':
    if len(argv) == 1:
        scan('localhost')
    else:
        scan(argv[1])
