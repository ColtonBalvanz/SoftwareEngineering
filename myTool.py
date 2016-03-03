#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, Button, BOTH, Label
import time


class Application(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="grey")   
         
        self.parent = parent
        
        self.initUI()
        
    
    def initUI(self):
      
        self.parent.title("My Tool Client")
        self.pack(fill=BOTH, expand=1)
        quitButton = Button(self, text="Exit",
            command=self.quit, padx=50, pady=30)
        quitButton.place(x=674, y=0)
        myToolLabel = Label(self, text="Welcome to MyTool!", font=("Helvetica",16), padx=50)
        employeeName = Label(self, text="Julio", font=("Helvetica",10), padx=50)
        myToolLabel.place(x=0, y=0)
        employeeName.place(x=0, y=30)
        dateAndTime = Label(self, text=time.asctime())
        dateAndTime.place(x=0, y=50)
        

def main():
  
    root = Tk()
    root.geometry("800x600+0+0")
    app = Application(root)
    root.mainloop()  


if __name__ == '__main__':
    main()
