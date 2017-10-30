#!/usr/bin/env python3

import websocket
import threading
import time
import json

#Global Values
address = '127.0.0.1'	# The address of the spjs.
port = '8989'		# The port that spjs is using.
comport = 'COM1'	# Com port placeholder, the script will detect the one in use.

def on_message(ws, message):
	print(time.clock())
	print(message)
	if message.startswith('{\n\t"SerialPorts:":'):
		print('True')

def on_close(ws):
	print('Websocket connection has closed.')

def on_error(ws, error):
	print(error)

def on_open(ws):
	print('Websocket connection opened!')
	ws.send('list')
	print('sent list')

if __name__ == '__main__':
	#Connect websocket in another thread.
	endpoint = 'ws://{0}:{1}/ws'.format(address, port)
	ws = websocket.WebSocketApp(endpoint,
		on_error = on_error,
		on_close = on_close,
		on_message = on_message)

	# Bind the on_open function.
	ws.on_open = on_open

	# Run in another thread.
	wsthread = threading.Thread(target=ws.run_forever)
	wsthread.start()


	# Loop until button pressed.
	while not ws.sock.connected:
		print('Attempting to connect...')
		time.sleep(250)
		
		
	print('Sending Feed-Hold...')
	# ws.send('sendjson {"P":"COM3","Data":[{"D":"!"}]}')
	ws.send('send {0} !'.format(comport))
	print('Sent!')

	wsthread.join()

