import socket
import sys

class Stream(object):

	SP = b' '
	CR = b'\r'
	LF = b'\n'
	CRLF = CR+LF
	Double_CRLF = CRLF+CRLF

	def __init__(self, initial=b''):
		self.content = initial

	def attach(self, text):
		self.content += text

	def has_double_CRLF(self):
		return Stream.Double_CRLF in self.content

	def size(self):
		return sys.getsizeof(self.content)

	def extract(self):
		data = self.content
		self.content = b''
		return data

	def __str__(self):
		return self.content

class Socket(object):

	def __init__(self, host, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Instancio o socket aqui
		self.host = host
		self.port = port

	class Connection(object):

		def __init__(self, socket, address: tuple):
			self.socket = socket
			self.address = address
			self.stream = Stream()

		def send(self, msg):
			self.socket.sendall(msg)

		def read(self, length=4096):
			data = self.socket.recv(length)
			self.stream.attach(data)
			return sys.getsizeof(data)

		def close(self):
			self.socket.close()

class TCPAgent(Socket):

	def listen(self, connection_handler):
		self.socket.bind((self.host, self.port))
		self.socket.listen(1)
		while True:
			print('Waiting for a new connection...')
			connection_handler(Socket.Connection(*self.socket.accept()))

	def connect(self):
		target = (self.host, self.port)
		self.socket.connect(target)
		print('Connected to the server...')
		return Socket.Connection(socket=self.socket, address=target)
		