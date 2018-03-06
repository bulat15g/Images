# coding=utf-8
from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image
from pynput import keyboard, mouse

import tools.Worker


class window_class():
    root=Tk()
    worker = tools.Worker

    globalPicName = None
    statusText__private = Text()

    textBufferIsStatus= "hello"
    statusVariable= "one"

    panelFrame = Frame(root, height=100, bg='gray')
    imageFrame = Frame(root, height=340)
    panelIMAGE=Label()

    rootsFilename=str

    def setStatusText(self):
        self.statusText__private.delete('1.0', END)
        self.statusText__private.insert(1.0, "status:" + self.statusVariable +
                                        "\n" + str(self.textBufferIsStatus))

    def __init__(self):
        self.initUI()

    def start__public(self):
        self.root.mainloop()

    def initUI(self):
        def onKeyPress(event):
            if(str(event)=="Key.shift"):self.setImageFrame()
            if(str(event)=="'q'" or str(event)=="Key.esc"):self.onExit()

        def onMousePress(event):
            print("hello"+event)

        def setRootParams():
            self.root.title("Simple menu")
            self.root.geometry("800x600+250+150")


            key_lis=keyboard.Listener(on_press=onKeyPress)
            key_lis.start()
            #todo FUCKIGN MOUSE
            mouse_lis=mouse.Listener(on_click=onMousePress)
            mouse_lis.start()

        def setMenuBar():
            menubar = Menu(self.root)
            self.root.config(menu=menubar)
            fileMenu = Menu(menubar)
            fileMenu.add_command(label="OpenImage", command=self.openImage)
            fileMenu.add_command(label="Exit", command=self.onExit)

            menubar.add_cascade(label="File", menu=fileMenu)
        def setPanelFrame():
            self.panelFrame.pack(side='top', fill='x')
        def setButtonsOnUpperFrame():
            loadBtn = Button(self.panelFrame, text='Load',command=self.openImage)
            saveBtn = Button(self.panelFrame, text='Save',command=self.getWindowShape)
            updateBtn = Button(self.panelFrame, text='Update',command=self.setImageFrame)

            loadBtn.bind("<Button-1>", )
            saveBtn.bind("<Button-1>", )
            updateBtn.bind("<Button-1>", )

            loadBtn.place(x=10, y=10, width=40, height=40)
            saveBtn.place(x=60, y=10, width=40, height=40)
            updateBtn.place(x=110, y=10, width=70, height=40)
        def setTextOnFrame():
            self.statusText__private = Text(self.panelFrame)
            self.setStatusText()
            self.statusText__private.place(x=270, y=5, width=500, height=80)

        setRootParams();setMenuBar();setPanelFrame()
        setButtonsOnUpperFrame();setTextOnFrame()

    def setImageFrame(self):
        if(self.globalPicName!=None):
            self.panelIMAGE.destroy()
            x = self.rootsFilename
            img = Image.open(x)
            geom=self.getWindowShape()
            img = img.resize((geom[0], geom[1]-80),Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.panelIMAGE = Label(self.root, image=img)
            self.panelIMAGE.image = img
            self.panelIMAGE.pack()


    def openImage(self):
        self.root.filename = filedialog.askopenfilename(title="Select file",
                                                        filetypes=(
                                                            ("all files", "*.*"), ("jpeg files", "*.jpg"),
                                                                   ("png files", "*.png"))
                                                        )
        self.globalPicName = self.root.filename
        if self.globalPicName!="":

            self.rootsFilename=self.root.filename
            # print("openImageMethodReport \nimage selected=" + self.globalPicName)

            self.textBufferIsStatus= "image:=" + str(self.globalPicName)
            self.setStatusText()

        else :self.textBufferIsStatus= "some shut happens"

    def getWindowShape(self):
        geom=re.split(r"[x,+]",self.root.geometry())
        return (int(geom[0]),int(geom[1]))

    def onExit(self):
        self.root.quit()



