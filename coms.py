from threading import Thread
import sys
import socket
import fcntl, os

class ServerManager:
    __slots__ = ('__listen', '__address', '__walkies', '__walkie1', '__walkie2')
    
    def __init__(self) -> None:
        self.__listen = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__address = ('0.0.0.0', 6420)
        self.__listen.bind(self.__address)
        self.__listen.setblocking(False)
        self.__listen.listen()
        self.__walkies = dict()
        self.__walkie1 = "10.42.0.132"
        self.__walkie1 = "10.42.0.132"
    
    def run(self):
        try:
            (sock, address) = self.__listen.accept()
            cm = ConnectionManager(sock, address)
            
            thread = Thread(target=cm.run, args=())
            self.__walkies[address] = cm.get_queues()
        except:
            pass
        
        
        if self.__walkie1 in self.__walkies and self.__walkie2 in self.__walkies:
            self.__walkies[self.__walkie1][1].append(self.__walkies[self.__walkie2][0].pop(0))
            self.__walkies[self.__walkie2][1].append(self.__walkies[self.__walkie1][0].pop(0))
    

class ConnectionManager:
    __slots__ = ('__client', '__address', '__port', '__sender', '__queue_r', '__queue_s')
    BUFFSIZE = 100
    
    def __init__(self, client: socket.socket, address: socket.AddressInfo) -> None:
        self.__client = client
        (self.__address, self.__port) = address
        self.__sender = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__sender.connect((self.__address, 6421))
        self.__client.setblocking(False)
        self.__queue_r = list()
        self.__queue_s = list()
        
    def get_queues(self):
        return (self.__queue_r, self.__queue_s)
        
    def run(self):
        while True:
            try:
                self.__queue_r.append(self.__client.recv(self.BUFFSIZE))
            except:
                pass
            try:
                self.__sender.send(self.__queue_s.pop(0))
            except:
                pass
        

ServerManager().run()
