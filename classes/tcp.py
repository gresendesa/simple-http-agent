import socket

class Socket(object):

	def __init__(self, host, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Instancio o socket aqui
		self.host = host
		self.port = port

	class Connection(object):

		def __init__(self, socket, address=()):
			self.socket = socket
			self.address = address
			self.is_alive = True

		def send(self, msg):
			if msg: self.socket.sendall(msg)

		def read(self):
			try:
				return self.socket.recv(1024)
			except ConnectionResetError:
				self.is_alive = False
				print('ISSUE: Connection closed by client')

		def close(self):
			self.socket.close()

class Client(Socket):

	def __init__(self, host, port):
		super(Client, self).__init__(host=host, port=port)

	def send(self, msg, callback):
		self.socket.connect((self.host, self.port))
		self.socket.sendall(msg)
		callback(Socket.Connection(socket=self.socket))

class Server(Socket):

	def __init__(self, port, host=''):
		super(Server, self).__init__(host=host, port=port)

	def start(self, callback):
		self.socket.bind((self.host, self.port))
		self.socket.listen(1)
		while True:
			connection = Socket.Connection(*self.socket.accept())
			callback(connection)