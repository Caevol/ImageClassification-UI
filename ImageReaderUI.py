# Author: Logan Pedersen
# Basic UI for image classification
# Click any images that contain bees
# when there are no more bees, press the NO MORE BEES button
# moves the files to appropriate folders


from Tkinter import *
import tkFileDialog
from PIL import ImageTk, Image
import os


GRID_X = 14
GRID_Y = 7
IMAGE_SIZE_X = 125
IMAGE_SIZE_Y = 125

global imageList
global indexNum
global buttonList
global panel
global beeFile
global noBeeFile

def walkThroughImages(file_path) :
    global imageList
    imageList = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith(".png"):
                imageList.append(os.path.join(root, file))

def noBeeInImageAction(button):
    image = button.imageName
    if not image == '':
        fileName = os.path.basename(image)
        os.rename(image, os.path.join(noBeeFile, fileName))
    button.configure(image=None)
    button.image = None 
    button.imageName = ''

def beeInImageAction(x, y):
    button = buttonList[y][x]

    image = button.imageName
    if not image == '':
        fileName = os.path.basename(image)
        os.rename(image, os.path.join(beeFile, fileName))
    button.configure(image = None)
    button.image = None
    button.imageName = ''

def resetImages():
    global buttonList
    for i in buttonList:
        for j in i:
            noBeeInImageAction(j)
    setAllImages()

def setAllImages():
    global indexNum
    for y in xrange(GRID_Y):
		for x in xrange(GRID_X):
			setImage(x, y)
			indexNum += 1

def setImage(x, y) :
    global imageList
    global buttonList
    global indexNum

    if indexNum < len(imageList) :
        activeImage = imageList[indexNum]
        pilImg = Image.open(activeImage)
        pilImg = pilImg.resize((IMAGE_SIZE_X, IMAGE_SIZE_Y), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(pilImg)
        buttonList[y][x].configure(image=img)
        buttonList[y][x].image = img
        buttonList[y][x].imageName = activeImage



def main():
    master = Tk()

    global indexNum
    global activeImages
    global panel
    global buttonList
    global beeFile
    global noBeeFile

    buttonList = []
    indexNum = 0
    activeImage = []

    file_path = tkFileDialog.askdirectory(title = "Select images file")
    beeFile = tkFileDialog.askdirectory(title="SELECT FILE FOR IMAGES WITH BEES")
    noBeeFile = tkFileDialog.askdirectory(title="SELECT FILE FOR IMAGES WITHOUT ANY BEES")
    walkThroughImages(file_path)

# Create buttons and place them in buttonList
    for y in xrange(GRID_Y):
        smallList = []
        for x in xrange(GRID_X):
            b = Button(master)
            b.imageName = ''
            b.grid(row = y+1, column = x+1)
            smallList.append(b)

        buttonList.append(smallList)

# assign each button functionality
    for y in xrange(len(buttonList)):
        for x in xrange(len(buttonList)):
            button = buttonList[y][x]
            button.configure(command = lambda x=x, y=y: beeInImageAction(x, y))
            button.command = lambda x=x, y=y: beeInImageAction(x, y)


    bee = Button(master, text="NO MORE BEES", command=resetImages)
    bee.grid(row=GRID_Y+1, column=int(GRID_X / 2) + 1)

    setAllImages()

    mainloop()


if __name__ == "__main__":
    main()