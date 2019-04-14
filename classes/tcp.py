import socket

class Socket(object):

	def __init__(self, host, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Instancio o socket aqui
		self.host = host
		self.port = port

	def close(self):
		pass

class Client(Socket):

	def __init__(self, host, port):
		super(Client, self).__init__(host=host, port=port)

	def send(self, msg, callback):
		self.socket.connect((self.host, self.port))
		self.socket.sendall(msg)
		callback(self.socket)

class Server(Socket):

	def __init__(self, port, host=''):
		super(Server, self).__init__(host=host, port=port)

	def start(self, callback):
		self.socket.bind((self.host, self.port))
		self.socket.listen(1)
		while True:
			request = Server.Request(*self.socket.accept())
			callback(request)

	class Request(object):
		def __init__(self, connection, address):
			self.connection = connection
			self.address = address
			self.connection.settimeout(1)

		def reply(self, msg):
			self.connection.sendall(msg)