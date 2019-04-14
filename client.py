from classes import tcp

def handle(connection):
	if connection.is_alive:
		data = connection.read()
		connection.send(b'zeta')
		data = connection.read()
		connection.send(b'zeta2')
		print(data)

tcp.Client(host='localhost', port=50007).send(msg=b'Hello World', callback=handle)