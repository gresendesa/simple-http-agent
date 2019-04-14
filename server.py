from classes import http

server = http.Server(port=50007)

def handle(connection):
	print('Message from', connection.address)
	while connection.is_alive: #Reads connection util end of transmition
		data = connection.read(length=5)
		connection.send(data)
		print(data)

server.start(callback=handle)
