#!/usr/bin/env python3

#Global Values
address = '127.0.0.1'	# The address of the spjs.
port = '8989'		# The port that spjs is using.

import websocket
import threading
import time

def on_message(ws, message):
	print(message)

def on_close(ws):
	print('Connection closed.')

def on_error(ws, error):
	print(error)

def on_open(ws):
	print('Connection opened!')

if __name__ == '__main__':
	#Create the websocketclass
	#Loop until button hit and send message.
	ws = websocket.WebSocketApp('ws://localhost:8989/ws',
		on_error = on_error,
		on_close = on_close,
		on_message = on_message)

	ws.on_open = on_open

	# Run the ws listener thread.
	wsthread = threading.Thread(target=ws.run_forever)
	wsthread.start()

	while ws.sock.connected:
		ws.send('list')
		time.sleep(1)
