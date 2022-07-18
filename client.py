import subprocess
import socket
import sys
import threading
import signal

if len(sys.argv) < 3:
    print('not enough arguments. Expected IP of rendezvous server and player number.')
    quit()

rendezvous_ip = sys.argv[1]
host_name = sys.argv[2]

print('starting connection protocol using rendezvous IP {}, host name {}'.format(
    rendezvous_ip, host_name
))

rendezvous = (rendezvous_ip, 55555)

# connect to rendezvous
print('connecting to rendezvous server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
# sock.sendto(b'0', rendezvous)
sock.settimeout(1)
sock.sendto(host_name.encode(), rendezvous)

while True:
    if keyboard.is_pressed("q"):
        sys.exit()

    try:
        data = sock.recv(1024).decode()
    except socket.timeout:
        continue

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

while True:
    try:
        data = sock.recv(1024).decode()
        break
    except socket.timeout:
        continue
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))

# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', sport))
sock.sendto(b'0', (ip, dport))
sock.close()

print('ready to exchange messages\n')

# listen for
# equiv: nc -u -l 50001
# def listen():
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.bind(('0.0.0.0', sport))

    # while True:
        # data = sock.recv(1024)
        # print('\rpeer: {}\n> '.format(data.decode()), end='')

# listener = threading.Thread(target=listen, daemon=True);
# listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('0.0.0.0', dport))

# while True:
    # msg = input('> ')
    # sock.sendto(msg.encode(), (ip, sport))

# if player_number == 1:
    # subprocess.run(['hello_tetra.exe', '--local-port', '{}'.format(sport), '--players', 'localhost', '{}:{}'.format(ip, dport)])
# else:
    # subprocess.run(['hello_tetra.exe', '--local-port', '{}'.format(dport), '--players', '{}:{}'.format(ip, sport), 'localhost'])
