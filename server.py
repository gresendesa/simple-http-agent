from classes import http

def handler(http_connection):
	print('Client connected', http_connection.socket_connection.address)
	print(http_connection.capture_header().headers)
	http_connection.close()

http.HTTPAgent(host='', port=50007).listen(handler=handler)