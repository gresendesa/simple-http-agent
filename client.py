from classes import http

http.Client(host='localhost', port=50007).send(msg=http.Message.Request().build())