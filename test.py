import PySimpleGUI as sg
import subprocess
import socket
import sys
import threading
import signal

rendezvous_ip = "45.33.109.87"

def connect(window, host_name):
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
        event, values = window.read(100)
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            window.close()
            sys.exit()

        try:
            data = sock.recv(1024).decode()
        except socket.timeout:
            continue

        if data.strip() == 'ready':
            print('checked in with server, waiting')
            break

    while True:
        event, values = window.read(100)
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            window.close()
            sys.exit()

        try:
            data = sock.recv(1024).decode()
            break
        except socket.timeout:
            continue

    ip, sport, dport, player_num = data.split(' ')
    sport = int(sport)
    dport = int(dport)

    print('\ngot peer')
    print('  ip:          {}'.format(ip))
    print('  source port: {}'.format(sport))
    print('  dest port:   {}\n'.format(dport))
    print('  player num:   {}\n'.format(player_num))

    # punch hole
    # equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
    print('punching hole')

    sock.close()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))
    sock.sendto(b'0', (ip, dport))
    sock.close()

    print('ready to exchange messages\n')

    if player_num == "1":
        subprocess.run(['hello_tetra.exe', '--local-port', '{}'.format(sport), '--players', 'localhost', '{}:{}'.format(ip, dport)])
    else:
        subprocess.run(['hello_tetra.exe', '--local-port', '{}'.format(dport), '--players', '{}:{}'.format(ip, sport), 'localhost'])

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Enter passphrase to host or join game')],
            # [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.InputText()],
            [sg.Button('Connect') ]]

# Create the Window
window = sg.Window('esports caster v0.01', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    # print('You entered', values[0])
    connect(window, values[0])

window.close()
