import socket
import threading
import sys
import random
import pickle
import subprocess

from datetime import datetime

global messageBuffer
messageBuffer=[]

class HubClass(threading.Thread):
    def __init__(self, index):
        super().__init__()
        print("roomClass Started")
        self.ConnectionThreadList=[]
        GenerateSudokuNums = GenBoard()
        self.sudokuNums = GenerateSudokuNums.board

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
            print(self.sudokuNums)
            '''for item in self.sudokuNums:
                if type(item)==int:
                    conn.send(str.encode(str(self.sudokuNums[0])))
            '''
            self.DataToSend=pickle.dumps(self.sudokuNums)
            conn.send(self.DataToSend)
            self.ConnectionThreadList.append(RoomClass(conn))
            print(welcome)

class GenBoard():
    def __init__(self):
        self.board=self.GenSud()

    def GenSud(self):
        """Generates a sudoku grid using qqwing, and converts it to a list"""
        QqwingOut = subprocess.getoutput('C:/qqwing.exe --generate 1 --csv')
        QqwingSplit = QqwingOut.split(',')
        QqwingStrip = list(QqwingSplit[1])
        FrontStrip = QqwingStrip.pop(0)
        for SudokuListIndex, SudokuListItem in enumerate(QqwingStrip):
            if SudokuListItem == ".":
                QqwingStrip[SudokuListIndex] = "  "
        return QqwingStrip
class makeBoard():

    def __init__(self):
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.board = None
        while self.board is None:
            self.board = self.attemptBoard()
        self.board=self.StripFlags(self.board)
        self.board=self.NormaliseBoard(self.board)
    def StripFlags(self,board):
        strippedBoard=[]
        for row in board:
            for item in row:
                strippedBoard.append(item[0])
        return strippedBoard
    def NormaliseBoard(self,board):
        for x in range(1,9):
            board.insert((x*10)-1,str(x))
        return board
    def attemptBoard(self):
        board = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                checking = self.numbers[:]
                random.shuffle(checking)
                x = -1
                loopStart = 0
                while board[i][j] is None:
                    x += 1
                    if x == 9:
                        #No number is valid in this cell, start over
                        return None
                    checkMe = [checking[x],True]
                    if checkMe in board[i]:
                        #If it's already in this row
                        continue
                    checkis = False
                    for checkRow in board:
                        if checkRow[j] == checkMe:
                            #If it's already in this column
                            checkis = True
                    if checkis: continue
                    #Check if the number is elsewhere in this 3x3 grid based on where this is in the 3x3 grid
                    if i % 3 == 1:
                        if   j % 3 == 0 and checkMe in (board[i-1][j+1],board[i-1][j+2]): continue
                        elif j % 3 == 1 and checkMe in (board[i-1][j-1],board[i-1][j+1]): continue
                        elif j % 3 == 2 and checkMe in (board[i-1][j-1],board[i-1][j-2]): continue
                    elif i % 3 == 2:
                        if   j % 3 == 0 and checkMe in (board[i-1][j+1],board[i-1][j+2],board[i-2][j+1],board[i-2][j+2]): continue
                        elif j % 3 == 1 and checkMe in (board[i-1][j-1],board[i-1][j+1],board[i-2][j-1],board[i-2][j+1]): continue
                        elif j % 3 == 2 and checkMe in (board[i-1][j-1],board[i-1][j-2],board[i-2][j-1],board[i-2][j-2]): continue
                    #If we've reached here, the number is valid.
                    board[i][j] = checkMe
        return board


    def printBoard(self,board):
        spacer = "++---+---+---++---+---+---++---+---+---++"
        print (spacer.replace('-','='))
        for i,line in enumerate(board):
            print ("|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||".format(
                        line[0][0] if line[0][1] else ' ',
                        line[1][0] if line[1][1] else ' ',
                        line[2][0] if line[2][1] else ' ',
                        line[3][0] if line[3][1] else ' ',
                        line[4][0] if line[4][1] else ' ',
                        line[5][0] if line[5][1] else ' ',
                        line[6][0] if line[6][1] else ' ',
                        line[7][0] if line[7][1] else ' ',
                        line[8][0] if line[8][1] else ' ',))
            if (i+1) % 3 == 0: print(spacer.replace('-','='))
            else: print(spacer)


class RoomClass(threading.Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn



    def run(self):
        print("ROOMCLASS STARTED")
        ready = self.conn.recv(1024).decode('UTF-8')
        print("ready")
        if ready:
            # self.s.send(str.encode(HubClass.startTime))

            print("starting instantiation")
            self.recieveThreadList.append(recieveDataClass(self.conn))
            self.sendThreadList.append(sendDataClass(self.conn))
            print("starting classes")
            self.recieveThreadList[-1].start()
            self.sendThreadList[-1].start()
            print(self.recieveThreadList[-1].is_alive())
            print("both started")


class sendDataClass(threading.Thread):
    global messageBuffer
    def __init__(self, conn):
        super().__init__()
        self.conn=conn



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
            incomData = (conn.recv(1024))
            #incom = incom.decode('UTF-8')
            message = str(name + " : " + incom)
            messageBuffer.append(message)
            print(message)
            if not incom:
                break
            if incom == "^^EXIT":
                conn.close()
        conn.close()
        sys.exit()

HubObject = HubClass(1)
print("main")

HubObject.start()
