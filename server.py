from classes import http, file

def handler(http_connection):

	print('Client connected', http_connection.socket_connection.address)

	for m in http_connection.messages():

		urn = m.request_line[1].decode("utf-8").strip('/')

		fname = 'index.html' if urn == '' else urn

		if file.exists(name=fname):
			response = http.HTTPMessage.Builder(request_line=(b'HTTP/1.1', b'200', b'OK'), headers=[(b'Connection', b'close'), (b'Content-Type', bytes(file.mime(fname), 'utf-8'))], body=file.get_content(fname)).get()
		else:
			response = http.HTTPMessage.Builder(request_line=(b'HTTP/1.1', b'404', b'Not Found'), headers=[(b'Connection', b'close'), (b'Content-Type', b'text/html')], body=b'').get()

		if m.request_line[0] == b'GET':

			print(b'[GET request received] Object requested: ', m.request_line[1])

		elif m.request_line[0] == b'POST':

			print('[POST request received] Data received (', m.headers[b'Content-Length'], 'bytes):', m.body)

		http_connection.send_message(response)

	http_connection.close()

print('Simple HTTP server')

http.HTTPAgent(host='', port=50007).listen(handler=handler)