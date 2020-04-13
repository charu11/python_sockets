import socket
import time
#create the socket
#AF_INET == ipv4
#SOCK_STREAM
HEADERSIZE = 10


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1134))
s.listen(5)

while True:
    # now our endpoint knows about the other endpoint
    client_socket, address = s.accept()
    print(f"connection from {address} has been established")

    msg = 'welcome to the server................'
    msg = f'{len(msg):<{HEADERSIZE}}' + msg

    client_socket.send(bytes(msg, "utf-8"))

    while True:
        time.sleep(3)
        msg = f'the time is {time.time()}'
        msg = f'{len(msg):<{HEADERSIZE}}' + msg

        print(msg)

        client_socket.send(bytes(msg, 'utf-8'))

