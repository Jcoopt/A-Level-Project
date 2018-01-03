import tkinter as tk
import os
import socket
import sys
import threading
import pickle
#from datetime import datetime
class SudokuApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #tk.minsize(220,220)
        self.minsize(220,220)
        #NetworkInterfaceObject=NetworkInterfaceClass()
        self.startLabel=tk.Label(master=self, text="Click the button when ready")
        self.startLabel.grid(row=0)
        # label.grid(row=0,column=0)
        self.StartButton = tk.Button(self, command=self.ChangeToSudokuFrame, text="Ready")
        self.StartButton.grid(row=20, column=0)
        self.NetworkInterfaceObject = NetworkInterfaceClass()
        self.NetworkInterfaceObject.start()

    def ChangeToSudokuFrame(self):
        self.startLabel.grid_forget()
        self.StartButton.grid_forget()
        self.SudokuGridObject = SudokuGridInterface(self,self.NetworkInterfaceObject.sudokuNums,self.NetworkInterfaceObject.s)



class StartInterface(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.root=controller
        self.root.configure(background='black')
        tk.Label(master=self,text="Click the button when ready").grid(row=0)
       # label.grid(row=0,column=0)
        StartButton=tk.Button(self.root, command=controller.ChangeToSudokuFrame, text="Ready")
        StartButton.grid(row=20,column=0)


class SudokuGridInterface(tk.Frame):
    def __init__(self,controller,sudokuNumsFromNetwork,conn):
        self.sudokuNums=sudokuNumsFromNetwork
        self.conn=conn
        #self.master = master
        #master.title("Sudoku Grid")
        self.root=controller
        self.root.configure(background='black')
        self.sudoku =self.sudokuNums #[""]*81
        #self.sudokuNums=["  "]*81
        self.btn_list=[]
        self.sel_list = []
        self.CreateSudokuGridButtons()
        self.CreateSudokuSelectionButtons()
        print(self.sudokuNums[0])

    def CreateSudokuGridButtons(self,):
        for k in range(9):
            for i in range(9):
                padding = 6
                SudokuIndex = (9 * k) + i
                IdxInt = (10 * k) + i
                if self.sudokuNums[SudokuIndex] != "  ":
                    b = tk.Button(self.root, text=self.sudokuNums[SudokuIndex])
                    ##sudoku[idx] = inputSelection
                else:
                    b = tk.Button(self.root, text=self.sudokuNums[SudokuIndex], command=lambda idx=IdxInt: self.onCellClick(idx))
                xPad = yPad = x1 = x2 = y1 = y2 = 0
                if k == 3 or k == 6 or k == 0:
                    x1 = padding
                if i == 3 or i == 6 or i == 0:
                    y1 = padding

                if i == 8:
                    y2 = padding
                xPad = (x1, x2)
                yPad = (y1, y2)
                b.grid(row=i, column=k, padx=xPad, pady=yPad, ipadx=5, ipady=3)
                self.btn_list.append(b)

    def CreateSudokuSelectionButtons(self):##MAKE RECURSIVE
        for p in range(9):
            sel = tk.Button(self.root, text=str(p + 1), command=lambda selid=p: self.selClick(selid), bg="red")
            sel.grid(row=10, column=p)
            self.sel_list.append(sel)
    def onCellClick(self,idx):
        """Run on click of a cell, changes the clicked cell to the chosen number"""
        if idx // 10 >= 1:
            idx = idx - (idx // 10)
        self.sudoku[idx] = inputSelection
        self.btn_list[idx]["text"] = str(inputSelection)
        self.SudokuToSend=pickle.dumps(self.sudoku)
        self.conn.send(self.SudokuToSend)

        #SEND LIST TO SERVER HERE
        print(self.sudoku)

    def selClick(self,selid):
        """Run on click of an input number, changes the clicked number's colour to blue(signifying that
        it is selected) converts all others to red(signifying not selected). Sets all others to red to
        prevent errors when selecting the same number twice"""
        global inputSelection
        inputSelection = selid + 1
        if self.sel_list[selid]['bg'] == "red":
            self.sel_list[selid]['bg'] = "blue"
            storelis = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            storelis.pop(int(selid))

            for StoreListIndex, StoreListItem in enumerate(storelis):
                self.sel_list[storelis[StoreListIndex]]['bg'] = "red"
class NetworkInterfaceClass(threading.Thread):
    def __init__(self):
        super().__init__()
        global messageBuffer
        messageBuffer=[]
        self.s = socket.socket()
        host = socket.gethostname()
        port = 8080
        hostname = host
        self.s.connect(("127.0.0.1", port))
        SudokuDataRecieved=self.s.recv(4096)
        print(SudokuDataRecieved)
        self.sudokuNums=pickle.loads(SudokuDataRecieved)
        print(self.sudokuNums)

    def run(self):
        self.ready=False

        while True:
            while self.ready:
                self.s.send(str.encode("Ready"))
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






"""root = tk.Tk()
root.minsize(220, 200)
root.configure(background='black')
networkInterfaceObject=NetworkInterfaceClass()
startGui=StartInterface(root,networkInterfaceObject
SudokuGUI = SudokuGridInterface(root)"""
app=SudokuApplication()
app.mainloop()

#root.mainloop()