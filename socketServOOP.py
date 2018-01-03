import socket
import threading
import sys
global messageBuffer
messageBuffer=[]

class RoomClass(threading.Thread):
    def __init__(self, index):
        super().__init__()
        print("roomClass Started")
        self.recieveThreadList=[]
        self.sendThreadList=[]

    def run(self):
        print("run")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 8080
        self.s.bind(('', self.port))
        self.s.listen(5)
        print(self.host)
        print("yo")
        while True:
            print("here")
            conn, addr = self.s.accept()
            welcome = str('Connected with ' + addr[0] + ':' + str(addr[1]))
            print(welcome)
            name = (conn.recv(1024)).decode('UTF-8')
            print(name)
            print("starting instantiation")
            self.recieveThreadList.append(recieveDataClass(conn, name))
            self.sendThreadList.append(sendDataClass(conn, name))
            print("starting classes")
            self.recieveThreadList[-1].start()
            self.sendThreadList[-1].start()
            print(self.recieveThreadList[-1].is_alive())
            print("both started")


class sendDataClass(threading.Thread):
    global messageBuffer
    def __init__(self, conn, name,):
        super().__init__()
        self.conn=conn
        self.name=name
    def run(self):
        self.sendData(self.conn,self.name)

    def sendData(self, conn, name):
        print("sendDataClass started")
        global messageBuffer
        LogLength = len(messageBuffer)
        while True:
            if len(messageBuffer) > LogLength:
                last = messageBuffer[-1]
                conn.send(str.encode(last))
                LogLength = len(messageBuffer)


class recieveDataClass(threading.Thread):
    global messageBuffer
    def __init__(self,conn, name):
        super().__init__()
        print("recieveDataClass start")
        self.conn = conn
        self.name = name

    def run(self):
        self.recieveData(self.conn,self.name)

    def recieveData(self, conn,name):
        global messageBuffer
        print(name, " has joined ")
        conn.send(str.encode("hello"))
        while True:
            incom = (conn.recv(1024))
            incom = incom.decode('UTF-8')
            message = str(name + " : " + incom)
            messageBuffer.append(message)
            print(message)
            if not incom:
                break
            if incom == "^^EXIT":
                conn.close()
        conn.close()
        sys.exit()

roomObject = RoomClass(1)
print("main")
roomObject.start()
