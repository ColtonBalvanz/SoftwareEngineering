#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, BOTH


class Application(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="grey")   
         
        self.parent = parent
        
        self.initUI()
        
    
    def initUI(self):
      
        self.parent.title("My Tool Client")
        self.pack(fill=BOTH, expand=1)
        

def main():
  
    root = Tk()
    root.geometry("800x600+0+0")
    app = Application(root)
    root.mainloop()  


if __name__ == '__main__':
    main()
