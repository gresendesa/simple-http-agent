from classes import tcp
from classes import http

def handle(connection):
	while connection.is_alive:
		data = connection.read()
		print(data)

tcp.Client(host='localhost', port=50007).send(msg=http.Client.Request().build(), callback=handle)


