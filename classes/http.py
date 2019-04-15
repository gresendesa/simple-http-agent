import classes.tcp as tcp
import re


class Message:

	def __init__(self, content = b''):
		self.stream = content
		self.raw_headers = b''
		self.raw_content = b''

	def fill(self, input):
		self.stream += input
		return self

	def has_headers(self):
		if b'\r\n\r\n' in self.stream:
			separated = self.stream.split(b'\r\n\r\n')
			self.raw_headers = separated[0]
			self.raw_content = separated[1]
			return True
		return False

	def get_meta(self):
		list_raw_headers = self.raw_headers.split(b'\r\n')
		meta = [tuple(line.split(b' ')) for line in list_raw_headers]
		return {
			'request-line': meta.pop(0),
			'headers': dict(meta),
		}

	class Request:

		def build(self):
			return b"""GET /somedir/page.html HTTP/1.1\r
Host: www.someschool.edu\r
Connection: close\r
User-agent: Mozilla/5.0\r
Content-Length: 20\r
Accepted-language: fr\r\n\r\n"""
		

class Server(tcp.Server):
	def start(self):
		super(Server, self).start(callback=self.tcp_handler)

	def tcp_handler(self, connection):
		print('Message from', connection.address)
		msg = Message()
		while connection.is_alive: # Get headers
			data = connection.read()
			connection.send(data)
			if msg.fill(data).has_headers():
				break
		connection.close()
		print(msg.get_meta())

class Client(tcp.Client):
	def send(self, msg):
		super(Client, self).send(msg, callback=self.tcp_handler)

	def tcp_handler(self, connection):
		while connection.is_alive:
			data = connection.read()
			print(data)

	class Response:

		def parse(self):
			pass

		def build(self):
			pass


class Parser():
	def __init__(self, msg):
		separated_msg = msg.split('\r\n\r\n')
		headers = separated_msg[0]
		content = separated_msg[1]
