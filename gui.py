import tkinter  # Importing the tkinter library for GUI
from PIL import Image  # Importing the Image module from PIL
from tkinter import filedialog  # Importing filedialog from tkinter
import cv2 as cv  # Importing OpenCV as cv
from frames import *  # Importing necessary classes/functions from frames module
from displayTumor import *  # Importing DisplayTumor class from displayTumor module
# Importing necessary functions/classes from predictTumor module
from predictTumor import *

# Creating a class named Gui


class Gui:
    # Initializing class variables
    MainWindow = 0
    listOfWinFrame = list()
    FirstFrame = object()
    val = 0
    fileName = 0
    DT = object()
    mriImage = None  # Defining 'mriImage' as a global variable

    wHeight = 700  # Setting window height
    wWidth = 1180  # Setting window width

    # Constructor method
    def __init__(self):
        global MainWindow  # Declaring MainWindow as a global variable
        MainWindow = tkinter.Tk()  # Creating main window using tkinter
        MainWindow.geometry('1200x720')  # Setting window dimensions
        # Making window non-resizable
        MainWindow.resizable(width=False, height=False)

        self.DT = DisplayTumor()  # Creating an instance of DisplayTumor class

        self.fileName = tkinter.StringVar()  # Initializing fileName as a StringVar

        # Creating the FirstFrame using Frames class
        self.FirstFrame = Frames(
            self, MainWindow, self.wWidth, self.wHeight, 0, 0)
        # Disabling btnView initially
        self.FirstFrame.btnView['state'] = 'disable'

        # Appending FirstFrame to listOfWinFrame
        self.listOfWinFrame.append(self.FirstFrame)

        # Creating and configuring the WindowLabel
        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Kindly Upload Image to Detect Brain Tumor",
                                    height=1, width=40)
        WindowLabel.place(x=320, y=30)  # Setting the position of WindowLabel
        WindowLabel.configure(background="White", font=(
            "Comic Sans MS", 16, "bold"))

        self.val = tkinter.IntVar()  # Initializing val as IntVar

        # Creating the 'Detect Tumor' Radiobutton
        RB1 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="Detect Tumor", variable=self.val,
                                  value=1, command=self.check)
        # Setting the position of 'Detect Tumor' Radiobutton
        RB1.place(x=250, y=200)

        # Creating the 'View Tumor Region' Radiobutton
        RB2 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="View Tumor Region",
                                  variable=self.val, value=2, command=self.check)
        # Setting the position of 'View Tumor Region' Radiobutton
        RB2.place(x=250, y=250)

        # Creating the 'Browse' button
        browseBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Browse", width=8, command=self.browseWindow,
                                   fg="#715151")
        # Setting the position of 'Browse' button
        browseBtn.place(x=800, y=550)

        MainWindow.mainloop()  # Starting the main loop for GUI

    # Function to get list of window frames
    def getListOfWinFrame(self):
        return self.listOfWinFrame

    # Function to browse and open image window
    def browseWindow(self):
        global mriImage
        FILEOPENOPTIONS = dict(defaultextension='*.*',
                               filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileName = filedialog.askopenfilename(
            **FILEOPENOPTIONS)  # Asking user to select an image file
        image = Image.open(self.fileName)  # Opening the selected image
        imageName = str(self.fileName)  # Converting the filename to a string
        # Assigning the image to 'mriImage'
        Gui.mriImage = cv.imread(imageName, 1)
        self.listOfWinFrame[0].readImage(image)  # Reading the image
        self.listOfWinFrame[0].displayImage()  # Displaying the image
        self.DT.readImage(image)  # Reading the image in DisplayTumor class

    # Function to check and process image for tumor detection
    def check(self):
        global mriImage
        # print(Gui.mriImage)  # Printing 'mriImage'
        if Gui.mriImage is None:  # Checking if 'mriImage' is None
            tkinter.messagebox.showerror(
                "Error", "Please upload an image before detecting the tumor.")  # Showing error message
            return
        if (self.val.get() == 1):  # Checking if 'val' is 1
            self.listOfWinFrame = 0  # Resetting listOfWinFrame
            self.listOfWinFrame = list()  # Creating an empty list
            # Appending FirstFrame to listOfWinFrame
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(
                self.DT)  # Setting the DisplayTumor object

            # Predicting tumor using 'mriImage'
            res = predictTumor(Gui.mriImage)

            if res > 0.5:  # Checking prediction value
                resLabel = tkinter.Label(self.FirstFrame.getFrames(
                ), text="Tumor Detected", height=1, width=20)
                resLabel.configure(background="White", font=(
                    "Comic Sans MS", 16, "bold"), fg="red")
            else:
                resLabel = tkinter.Label(
                    self.FirstFrame.getFrames(), text="No Tumor", height=1, width=20)
                resLabel.configure(background="White", font=(
                    "Comic Sans MS", 16, "bold"), fg="green")

            resLabel.place(x=700, y=450)  # Placing the result label on GUI

        elif (self.val.get() == 2):  # Checking if 'val' is 2
            self.listOfWinFrame = 0  # Resetting listOfWinFrame
            self.listOfWinFrame = list()  # Creating an empty list
            # Appending FirstFrame to listOfWinFrame
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(
                self.DT)  # Setting the DisplayTumor object
            # Setting removeNoise method of DisplayTumor
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)

            secFrame = Frames(self, MainWindow, self.wWidth,
                              self.wHeight, self.DT.displayTumor, self.DT)
            # Creating secondary frame using Frames class

            # Appending secondary frame to listOfWinFrame
            self.listOfWinFrame.append(secFrame)

            for i in range(len(self.listOfWinFrame)):  # Looping through listOfWinFrame
                if (i != 0):  # Checking if index is not 0
                    # Hiding frames except the first one
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()  # Unhiding the first frame

            if (len(self.listOfWinFrame) > 1):  # Checking length of listOfWinFrame
                # Setting button state to active
                self.listOfWinFrame[0].btnView['state'] = 'active'

        else:
            print("Not Working")  # Printing message if condition is not met


# Creating an instance of Gui class
mainObj = Gui()