from classes import http

server = http.Server(port=50007)

def handle(request):
	print('Message from', request.address)
	try:
		while True: #Reads connection util end of transmition
			data = request.connection.recv(1024)
			print(data)
	except OSError:
		request.reply(b'ACK')

server.start(callback=handle)
