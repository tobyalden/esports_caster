import socket
import sys

print('starting server')

known_port = 50002

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 55555))
sock.settimeout(1)

while True:
    clients = {}

    while True:
        try:
            data, address = sock.recvfrom(128)
        except socket.timeout:
            continue

        print('connection from: {}'.format(address))
        host_name = data.decode()
        print('host name is: {}'.format(host_name))
        # clients.append(address)
        if clients.get(host_name) == None:
            clients[host_name] = []
        clients[host_name].append(address)

        sock.sendto(b'ready', address)

        if len(clients[host_name]) == 2:
            print('got 2 clients, sending details to each')
            break

    for host_name in clients:
        if len(clients[host_name]) == 2:
            c1 = clients[host_name].pop()
            c1_addr, c1_port = c1
            c2 = clients[host_name].pop()
            c2_addr, c2_port = c2

            sock.sendto('{} {} {} {}'.format(c1_addr, c1_port, known_port, 1).encode(), c2)
            sock.sendto('{} {} {} {}'.format(c2_addr, c2_port, known_port, 2).encode(), c1)
