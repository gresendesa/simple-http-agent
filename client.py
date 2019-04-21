from classes import http

http_connection = http.HTTPAgent(host='localhost', port=50007).connect()

print('Server connected', http_connection.socket_connection.address)

message = http.HTTPMessage.Builder(request_line=(b'HTTP/1.1', b'200', b'OK'), headers=[(b'Connection', b'close'), (b'Content-Length', b'6821'), (b'Content-Type', b'text/html')], body=b'teste').get_bytes()

http_connection.send_message(message)

http_connection.close()

