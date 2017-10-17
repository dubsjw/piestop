#!/usr/bin/env python3

#Global Values
address = '127.0.0.1'	# The address of the spjs.
port = '8989'		# The port that spjs is using.

import websocket
import Threading

def on_message(ws, message):
	print(message)

def on_close(ws):
	print('Connection closed.')

def on_error(ws, error):
	print(error)

def on_open(ws):
	def run(*args):
		print('The connection has been opened...')
		ws.send('!')
	threading.Thread(target=

if __name__ == '__main__':
	#Create the websocketclass
	#Loop until button hit and send message.
	ws = websocket.WebSocketApp('ws://92.168.1.190:8989',
		on_error = on_error,
		on_close = on_close,
		on_message = on_message)

	ws.on_open = on_open
	
	ws.run_forever()
