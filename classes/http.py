import classes.tcp as tcp

class Server(tcp.Server):
	pass

class Client(tcp.Client):
	pass


class Client:
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

