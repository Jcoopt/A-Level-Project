import os
import socket
import sys
import threading


class interfaceClass(threading.Thread):
    def __init__(self):
        super().__init__()
        global messageBuffer
        messageBuffer=[]
        self.s = socket.socket()
        host = socket.gethostname()
        port = 8080
        network = "172.19.152.197"
        if input("Use IP?") == "Y":
            hostname = network
        else:
            hostname = host
        self.s.connect(("127.0.0.1", port))


    def run(self):
        while True:
            name = input("Name: ")
            self.s.send(str.encode(name))
            print((self.s.recv(1024).decode('UTF-8')))
            recieveDataThread=recieveDataClass(self.s)
            recieveDataThread.start()
            while True:
                message = ""
                while message == "":
                    message = str(input("message: "))
                self.s.send(str.encode(message))
            self.s.close

class sendDataClass(threading.Thread):

    def __init__(self, s):
        super().__init__()
        print("sendDataClass started")
        self.s=s

    def run(self):
        self.sendData()

    def sendData(self):
        global messageBuffer
        LogLength = len(messageBuffer)
        while True:
            if len(messageBuffer) > LogLength:
                last = messageBuffer[-1]
                self.s.send(str.encode(last))
                LogLength = len(messageBuffer)


class recieveDataClass(threading.Thread):
    #global messageBuffer
    def __init__(self, s):
        super().__init__()
        print("recieveDataClass start")
        self.s=s
    def clear(self):
        os.system('cls')
        sys.stdout.flush()

    def write(self,message):
        sys.stdout.write(str(message))
        sys.stdout.flush()

    def run(self):
        self.recieveData()

    def recieveData(self):
        global messageBuffer
        while True:
            incom = self.s.recv(1024).decode('UTF-8')
            messageBuffer.append(incom)
            self.clear()
            for length in range(len(messageBuffer)):
                self.write(messageBuffer[length])
                self.write("\n")
            self.write("\nMessage:")

interfaceThread=interfaceClass()
interfaceThread.start()