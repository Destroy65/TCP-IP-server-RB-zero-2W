import socket
from threading import Thread

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('0.0.0.0', 6420))
server.listen()
(walkie1_r, addr1) = server.accept()

print(addr1)

(walkie2_r, addr2) = server.accept()

print(addr2)

walkie1_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
walkie1_s.connect((addr2[0], 6421))

walkie2_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
walkie2_s.connect((addr1[0], 6421))

def send(sock1, sock2):
    while True:
        sock1.send(sock2.recv(100))

t = Thread(target=send, args=(walkie2_s, walkie1_r))
t.run()
send(walkie1_s, walkie2_r)