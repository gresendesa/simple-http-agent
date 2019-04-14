from classes import tcp

def handle(socket):
	data = socket.recv(1024)
	print('Received', repr(data))

tcp.Client(host='localhost', port=50007).send(msg=b'Hello World', callback=handle)