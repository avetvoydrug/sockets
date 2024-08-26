import socket
import select
# pickle can serialize
HEADER_LENGTH = 10
HOST = (socket.gethostname(), 6000)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(HOST)
server.listen()
print('listening now ///')
socket_list = [server]
clients_list = {}

def receive_msg(client: socket.socket):
    try:
        msg_header = client.recv(HEADER_LENGTH)
        if not len(msg_header):
            return False
        msg_len = int(msg_header.decode('UTF-8').strip())

        return {
            'header': msg_header,
            'data': client.recv(msg_len).decode('UTF-8'),
        }
    except:
        return False

while True:
    rs, _, xs = select.select (socket_list, [], socket_list)
    for sock in rs:
        if sock == server:
            client, addr = server.accept()

            user = receive_msg(client)
            if user is False:
                continue
            socket_list.append(client)
            clients_list[client] = user

            print(f'New conn from {addr} with data {user["data"]}')
        else:
            msg = receive_msg(client)
            if msg is False:
                print(f'Conn from {addr} has been interrupted')
                socket_list.remove(sock)
                del clients_list[sock]
                continue
                
            user = clients_list(sock)

            for client in clients_list:
                if client is not sock:
                    client.send(f'New msg from {user["data"]} is {msg["data"]}')
    
    for sock in xs:
        socket_list.remove(sock)
        del clients_list[sock]
