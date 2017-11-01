#!/usr/bin/env python3

import websocket
import threading
import time
import json

# Global Values
address = '192.168.1.185'  # The address of the spjs.
port = '8989'  # The port that spjs is using.


class PieStop:
    def __init__(self):
        self.previousMsg = ''
        self.comport = 'COM1'

    def on_message(self, ws, message):
        print(message)
        if self.previousMsg == 'list':
            print('Parsing for default message port...')

            foundCom = False
            try:
                jsondata = json.loads(message)

                for serialport in jsondata['SerialPorts']:
                    if serialport['IsPrimary'] is True:
                        print('Setting default serial port as ' + serialport['Name'] + '.')
                        self.comport = serialport['Name']

                if not foundCom:
                    print("Couldn't find new comport, using default (" + self.comport + ").")

            except json.JSONDecodeError:
                print('Error decoding json, using default port ' + self.comport + '!')

        # Set the previous message up.
        self.previousMsg = message

    def on_close(self, ws):
        print('Web socket connection has closed.')


    def on_error(self, ws, error):
        print(error)


    def on_open(self, ws):
        print('Web socket connection opened!')
        ws.send('list')
        print('sent list')


    def start_button_loop(self, ws):
        # Loop for button press.
        while True:
            print('Sending Feed-Hold...')
            # ws.send('sendjson {"P":"COM3","Data":[{"D":"!"}]}')
            ws.send('send {0} !'.format(self.comport))
            print('Sent!')
            time.sleep(5)


if __name__ == '__main__':
    ps = PieStop()

    # Connect web socket in another thread.
    endpoint = 'ws://{0}:{1}/ws'.format(address, port)

    ws = websocket.WebSocketApp(endpoint,
                                on_error=ps.on_error,
                                on_close=ps.on_close,
                                on_message=ps.on_message)

    # Bind the on_open function.
    ws.on_open = ps.on_open

    # Run in another thread.
    wsthread = threading.Thread(target=ws.run_forever)
    wsthread.start()

    # Loop until button pressed.
    while not ws.sock.connected:
        print('Attempting to connect...')
        time.sleep(0.05)

    time.sleep(10)
    ps.start_button_loop(ws)


