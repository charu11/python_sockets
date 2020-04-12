import socket

#create the socket
#AF_INET == ipv4
#SOCK_STREAM

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    # now our endpoint knows about the other endpoint
    clientsocket, address = s.accept()
    print(f"connection from {address} has been established")



