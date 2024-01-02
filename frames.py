import tkinter  # Import the tkinter library for creating the GUI
from PIL import ImageTk  # Import the ImageTk module from the PIL library for displaying images
from PIL import Image  # Import the Image module from the PIL library for image processing

class Frames:
    xAxis = 0  # Initialize a variable to store the X-axis position
    yAxis = 0  # Initialize a variable to store the Y-axis position
    MainWindow = 0  # Initialize a variable to store the main window
    MainObj = 0  # Initialize a variable to store the main object
    winFrame = object()  # Initialize a variable to store the window frame
    btnClose = object()  # Initialize a variable to store the Close button
    btnView = object()  # Initialize a variable to store the View button
    image = object()  # Initialize a variable to store an image
    method = object()  # Initialize a variable to store a method
    callingObj = object()  # Initialize a variable to store a calling object
    labelImg = 0  # Initialize a variable to store an image label

    def __init__(self, mainObj, MainWin, wWidth, wHeight, function, Object, xAxis=10, yAxis=10):
        # Constructor: Initializes the frame with provided parameters
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.MainWindow = MainWin
        self.MainObj = mainObj
        self.MainWindow.title("Brain Detection from MRI Images")
        if (self.callingObj != 0):
            self.callingObj = Object

        if (function != 0):
            self.method = function

        global winFrame  # Declare a global variable for the frame
        self.winFrame = tkinter.Frame(self.MainWindow, width=wWidth, height=wHeight)
        self.winFrame['borderwidth'] = 5
        self.winFrame['relief'] = 'ridge'
        self.winFrame.place(x=xAxis, y=yAxis)

        self.btnClose = tkinter.Button(self.winFrame, text="Close", width=8,
                                      command=lambda: self.quitProgram(self.MainWindow))
        self.btnClose.place(x=1020, y=600)
        self.btnView = tkinter.Button(self.winFrame, text="View", width=8, command=lambda: self.NextWindow(self.method))
        self.btnView.place(x=900, y=600)

    def setCallObject(self, obj):
        # Set the calling object
        self.callingObj = obj

    def setMethod(self, function):
        # Set the method
        self.method = function

    def quitProgram(self, window):
        # Quit the program by destroying the main window
        global MainWindow
        self.MainWindow.destroy()

    def getFrames(self):
        global winFrame  # Get the frame
        return self.winFrame

    def unhide(self):
        # Make the frame visible
        self.winFrame.place(x=self.xAxis, y=self.yAxis)

    def hide(self):
        # Hide the frame
        self.winFrame.place_forget()

    def NextWindow(self, methodToExecute):
        # Switch to the next window or frame
        listWF = list(self.MainObj.listOfWinFrame)

        if (self.method == 0 or self.callingObj == 0):
            print("Calling Method or the Object from which Method is called is 0")
            return

        if (self.method != 1):
            methodToExecute()

        if (self.callingObj == self.MainObj.DT):
            img = self.MainObj.DT.getImage()
        else:
            print("Error: No specified object for getImage() function")

        jpgImg = Image.fromarray(img)
        current = 0

        for i in range(len(listWF)):
            listWF[i].hide()
            if (listWF[i] == self):
                current = i

        if (current == len(listWF) - 1):
            listWF[current].unhide()
            listWF[current].readImage(jpgImg)
            listWF[current].displayImage()
            self.btnView['state'] = 'disable'
        else:
            listWF[current + 1].unhide()
            listWF[current + 1].readImage(jpgImg) 
            listWF[current + 1].displayImage()

        print("Step " + str(current) + " Extraction complete!")

    def removeComponent(self):
        # Remove components (buttons)
        self.btnClose.destroy()
        self.btnView.destroy()

    def readImage(self, img):
        # Read and store an image
        self.image = img

    def displayImage(self):
        imgTk = self.image.resize((250, 250), Image.LANCZOS)
        imgTk = ImageTk.PhotoImage(image=imgTk)
        self.image = imgTk
        self.labelImg = tkinter.Label(self.winFrame, image=self.image)
        self.labelImg.place(x=700, y=150)
