import socket
import select
import errno


HEADER_LENGTH = 10

IP = '127.0.0.1'
PORT = 1234

# set up the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# avoid the address already in use
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind and listen
server_socket.bind((IP, PORT))
server_socket.listen()

# create a list of sockets for select to keep track of
socket_list = {server_socket}
clients = {}

print(f'Listening for connections on {IP}: {PORT}')


# for receive messages
def receive_messages(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        # if client closes the connection and there will be no header
        if not len(message_header):
            return False

        # convert the header into a length
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data':client_socket.recv(message_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_messages(client_socket)
            if user is False:
                continue

            # append the new client_socket to socket_list
            socket_list.append(client_socket)

            clients[client_socket] = user
            print('Accepted new connections from {}: {}, username:{}'.format(*client_address, user['data'].decode('utf-8')))

        else:
            message = receive_messages(notified_socket)

            if message is False:
                print('closed the connection from :{}'.format(clients[notified_socket]['data'].decode('utf-8')))
                socket_list.remove(notified_socket)

                del clients[notified_socket]

                continue

            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]

        









