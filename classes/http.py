from classes.low_level import TCPAgent, Socket, Stream
import sys

class HTTPConnection:
	def __init__(self, socket_connection):
		self.socket_connection = socket_connection

	def capture_initial_message(self):
		while not self.socket_connection.stream.has_double_CRLF():
			self.socket_connection.read()

		return HTTPMessage(self.socket_connection.stream.extract(length=self.socket_connection.stream.size()))

	def capture_body(self, length):
		count = length
		while count > 0:
			count -= self.socket_connection.read()

		return self.socket_connection.stream.extract(length=length)

	def pick_message(self):
		message = self.capture_initial_message()
		content_length = int(message.headers[HTTPMessage.CONTENT_LENGTH_LABEL]) if HTTPMessage.CONTENT_LENGTH_LABEL  in message.headers else None
		message.append_to_body(self.capture_body(length=(content_length - message.body_length())) if content_length else b'')
		return message

	def messages(self):
		close = False
		while not close:
			message = self.pick_message()
			close = message.has_connection_close()
			yield message

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

class HTTPMessage:

	CONTENT_LENGTH_LABEL = b'Content-Length'
	CONNECTION_LABEL = b'Connection'

	def __init__(self, message):
		try:
			separated = message.split(Stream.Double_CRLF, 2)
			self.meta, self.body = tuple(separated) if len(separated)==2 else tuple(separated[0], b'')
		except:
			raise Exception('Inconsistent HTTP message')

		lines = self.meta.split(Stream.CRLF)
		self.request_line = lines.pop(0).split(Stream.SP)
		self.headers = dict([tuple(line.split(b':'+Stream.SP)) for line in lines])

	def append_to_body(self, content):
		self.body += content

	def body_length(self):
		return len(self.body)

	def has_connection_close(self):
		connection_status = self.headers[HTTPMessage.CONNECTION_LABEL] if HTTPMessage.CONNECTION_LABEL in self.headers else None
		return connection_status == b'close'

	class Builder:

		def __init__(self, request_line: tuple, headers: list, body):
			body_length = len(body)
			if body_length > len(b''): 
				headers.append((HTTPMessage.CONTENT_LENGTH_LABEL, str.encode(str(body_length))))
			self.content = ((Stream.SP).join(list(request_line))) + Stream.CRLF + (Stream.CRLF).join([(b':'+Stream.SP).join(i) for i in headers]) + Stream.Double_CRLF + body

		def get(self):
			return self.content
