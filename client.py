import socket

HOST = (socket.gethostname(), 6000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(HOST)
print('Connected to', HOST)

request = b'GET / HTTP/1.1\r\nHost:localhost:6000\r\n\r\n'
sent = 0
while sent < len(request):
    sent = sent + client.send(request[sent:])

print('msg sent..')
