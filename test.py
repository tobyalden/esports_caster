import PySimpleGUI as sg

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
    print('You entered', values[0])

window.close()
