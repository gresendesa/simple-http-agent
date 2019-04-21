from classes.low_level import TCPAgent
from classes.low_level import Socket, Stream

class HTTPConnection(object):
	def __init__(self, socket_connection):
			self.socket_connection = socket_connection

	def capture_header(self):
		while not self.socket_connection.stream.has_double_CRLF():
			self.socket_connection.read()

		return HTTPMessage(self.socket_connection.stream.extract())

	def pick_message(self):
		pass

	def send_message(self, message):
		self.socket_connection.socket.sendall(message)

	def close(self):
		self.socket_connection.close()

class HTTPAgent(TCPAgent):
	
	def listen(self, handler):

		handle = lambda connection: handler(HTTPConnection(socket_connection=connection))
		super().listen(connection_handler=handle)

	def connect(self):

		return HTTPConnection(socket_connection=super().connect())

class HTTPMessage(object):

	def __init__(self, message):
		try:
			separated = message.split(Stream.Double_CRLF, 2)
			self.meta, self.body = tuple(separated) if len(separated)==2 else tuple(separated[0], b'')
		except:
			raise Exception('Inconsistent HTTP message')

		lines = self.meta.split(Stream.CRLF)
		self.request_line = lines.pop(0).split(Stream.SP)
		self.headers = dict([tuple(line.split(Stream.SP)) for line in lines])

	def append_to_body(self, content):
		self.body += content

	class Builder:

		def __init__(self, request_line: tuple, headers: list, body):
			self.content = ((Stream.SP).join(list(request_line))) + Stream.CRLF + (Stream.CRLF).join([(b':'+Stream.SP).join(i) for i in headers]) + Stream.Double_CRLF + body

		def get_bytes(self):
			return self.content
