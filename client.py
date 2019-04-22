from classes import application_layer, file

http_connection = application_layer.HTTPAgent(host='localhost', port=50007).connect()

print('Simple HTTP Browser')

print('Server connected', http_connection.socket_connection.address)

message = application_layer.HTTPMessage.Builder(request_line=(b'GET', b'/', b'HTTP/1.1'), headers=[(b'Content-Type', b'text/html')], body=b'').get()

http_connection.send_message(message)

r = http_connection.pick_message()

if r.headers[b'Content-Type'] == b'text/html':

	references = file.get_src(r.body)

	print('References found: ', references)

	for i in references:

		src_request = application_layer.HTTPMessage.Builder(request_line=(b'GET', i, b'HTTP/1.1'), headers=[(b'Content-Type', b'text/html')], body=b'').get()

		http_connection.send_message(src_request)

		server_response = http_connection.pick_message()

		print(b"[Response for " + i + b": " + server_response.request_line[1] + b"]")

	post_request = application_layer.HTTPMessage.Builder(request_line=(b'POST', b'/', b'HTTP/1.1'), headers=[(b'Content-Type', b'text/html'), (b'Connection', b'close')], body=b"{'json_message':'Hello Server. Receive my post message'}").get()

	http_connection.send_message(post_request)

	server_response = http_connection.pick_message()

	print(b"[Response for POST: " + server_response.request_line[1] + b"]")

http_connection.close()

