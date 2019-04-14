import classes.tcp as tcp

class Server(tcp.Server):
	def start(self):
		super(Server, self).start(callback=self.tcp_handler)

	def tcp_handler(self, connection):
		print('Message from', connection.address)
		while connection.is_alive: #Reads connection util end of transmition
			data = connection.read(length=5)
			connection.send(data)
			print(data)

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

	class Request:

		def parse(self):
			pass

		def build(self):
			return b"""GET /somedir/page.html HTTP/1.1\r
Host: www.someschool.edu\r
Connection: close\r
User-agent: Mozilla/5.0\r
Accepted-language: fr\r\n\r\n"""

