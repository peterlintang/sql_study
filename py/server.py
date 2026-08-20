import socket

server = socket.create_server(('',12000))
while True:
    (conn,addr) = server.accept()
    #print(conn,addr)
    a = conn.recv(1024)
    print(a)
    conn.close()

server.close()
