import socket

client = socket.create_connection(('127.0.0.1', 12000))
client.send("hello world".encode('utf-8'))
client.shutdown(socket.SHUT_WR)
