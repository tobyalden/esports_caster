import PySimpleGUI as sg
import subprocess
import socket
import sys
import threading
import signal
import textwrap
import string
import random
import pyperclip

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
        print('starting as player 1')
        subprocess.run(['esport_heaven_online.exe', '--local-port', '{}'.format(sport), '--players', 'localhost', '{}:{}'.format(ip, dport)])
    else:
        print('starting as player 2')
        subprocess.run(['esport_heaven_online.exe', '--local-port', '{}'.format(dport), '--players', '{}:{}'.format(ip, sport), 'localhost'])

# sg.theme('Default')   # Add a touch of color
# All the stuff inside your window.
text = "\n".join(textwrap.wrap('Enter a code and press Join to join a player already hosting, or press Host to recieve a code and begin hosting', 40))
layout = [
            [sg.Text('Code:'), sg.InputText(key='_TEXTBOX_', disabled=False)],
            [sg.Button('Join', key='_JOIN_'), sg.Button('Host', key='_HOST_')],
            [sg.Text(text, key='_TEXT_')],
        ]

# Create the Window
window = sg.Window('SpellCaster v0.01', layout, size=(300, 200))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    if event == '_HOST_':
        code = ''.join(random.choices(string.ascii_letters, k=8))
        window['_TEXTBOX_'].Update(code)
        window['_TEXTBOX_'].Update(disabled = True)
        window['_JOIN_'].Update(disabled = True)
        window['_HOST_'].Update(disabled = True)
        window['_TEXT_'].Update("Hosting... Code copied to clipboard.")
        pyperclip.copy(code)
        print('Hosting with code', code)
        connect(window, code)
    if event == '_JOIN_':
        if len(values['_TEXTBOX_']) != 8:
            window['_TEXT_'].Update("Invalid code!\nPlease double check what the host sent you.")
        else:
            code = values['_TEXTBOX_']
            window['_TEXT_'].Update("Joining with code " + code)
            window['_JOIN_'].Update(disabled = True)
            window['_HOST_'].Update(disabled = True)
            print('Joining using code', code)
            connect(window, code)

window.close()
