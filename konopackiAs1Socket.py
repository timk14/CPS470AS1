# resources: https://docs.python.org/3/howto/sockets.html

import socket, select

TIMEOUT = 10  # unit is seconds
BUF_SIZE = 1024  # unit is bytes


class TCPsocket:
    # list our instance variables
    # Constructor: create an object
    def __init__(self):
        self.sock = None  # each object's instance variables
        self.host = ""  # remote host name
        print("create an object of TCPsocket")

    def createSocket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # self.sock is an instance variable
            print("created a tcp socket!")
        except socket.error as e:
            print("Failed to create a TCP socket {}".format(e))
            self.sock = None

    # www.google.com -> host name
    # given a host name, how to get its ip address
    # Return the ip of input hostname. Both ip and hostname in string
    def getIP(self, hostname):
        self.host = hostname
        try:
            ip = socket.gethostbyname(hostname)  # ip is a local variable to getIP(hostname), ip is of string type
        except socket.gaierror:
            print("Failed to gethostbyname")
            return None
        return ip

    # connect to a remote server: IP address, port
    def connect(self, ip, port):
        if self.sock is None or ip is None:
            return
        try:
            self.sock.connect((ip, port))  # server address is defined by (ip, port)
            print("Successfully connect to host:", ip)
        except socket.error as e:
            print("Failed to connect: {}".format(e))
            self.sock.close()
            self.sock = None

    # return the number of bytes sent
    def send(self, request):
        bytesSent = 0  # bytesSent is a local variable
        if self.sock is None:
            return 0
        try:
            bytesSent = self.sock.sendall(request.encode())  # encode(): convert string to bytes
        except socket.error as e:
            print("socket error in send: {}".format(e))
            self.sock.close()
            self.sock = None
        return bytesSent

    # Receive the reply from the server. Return the reply as string
    def receive(self):
        if self.sock is None:
            return ""
        reply = bytearray()  # b'', local variable, bytearray is multable
        bytesRecd = 0  # local integer

        self.sock.setblocking(0)  # flag 0 to set non-blocking mode of the socket
        ready = select.select([self.sock], [], [], TIMEOUT)  # https://docs.python.org/3/library/select.html
        if ready[0] == []:  # timeout
            print("Time out on", self.host)
            return ""
        # else reader has data to read
        try:
            while True:  # use a loop to receive data until we receive all data
                data = self.sock.recv(BUF_SIZE)  # returned chunk of data with max length BUF_SIZE. data is in bytes
                if data == b'':  # if empty bytes
                    break
                else:
                    reply += data  # append to reply
                    bytesRecd += len(data)
        except socket.error as e:
            print("socket error in receive: {}".format(e))
            self.sock.close()
            self.sock = None
        return str(reply)

    # Close socket
    def close(self):
        if not (self.sock is None):
            self.sock.close()
