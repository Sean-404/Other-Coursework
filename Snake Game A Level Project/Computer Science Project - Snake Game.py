#AQA A Level Computer Science project
import time
import pygame
from pygame.locals import *
import random
import math
import sqlite3
import os
import os.path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
#These import all of the necessary modules for the game
pygame.init()
#This initialises the pygame module
#Colours
white=(255,255,255)
black=(0,0,0)
red=(200,0,0)
lightRed=(255,0,0)
green=(0,150,0)
lightGreen=(0,255,0)
paleGreen=(152,251,152)
blue=(0,150,255)
lightBlue=(145,206,250)
yellow=(200,200,0)
lightYellow=(255,255,0)
#These colours are represented using RGB values

scoreColour=black

gameSaved=False
Student=False
Teacher=False
GCSEAnalysis=False
ALevelAnalyis=False

displayWidth=800
displayHeight=600
gameDisplay=pygame.display.set_mode((displayWidth,displayHeight))
#This sets the dimensions for the game display, which is 800x600
pygame.display.set_caption("Maths Revision Snake Game")
#This sets the caption on the window of the game

snakeimg=pygame.image.load("snake sprite.png")
#This loads the snake sprite to the snakeimg variable

cwd=os.getcwd()
#This gets the current working directory that this python file is stored in

GCSEQuestions=[]
ALevelQuestions=[]
#This creates 2 empty lists which will be filled with topics that the user decides

fileNameGCSE="GCSE_Data.txt"
fileNameALevel="ALevel_Data.txt"
LeaderboardFileName="Leaderboard.txt"

snakeColour=lightGreen

clock=pygame.time.Clock()
#This updates the clock which is an object that helps track time
FPS=60
#This sets the framerate of the game
blockSpeed=4
#This sets the speed of the snake
blockSize=20
#This sets the size of the snake

questionUsed=0
difficulty="KS4"

lines=0

direction="right"

smallFont=pygame.font.SysFont(None,25)
mediumFont=pygame.font.SysFont(None,45)
largeFont=pygame.font.SysFont(None,100)
#This sets the size of the fonts

questionMoved=False

def pause():
    global paused
    paused=True
    while paused==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    #This executes code if the user presses the c key
                    paused=False
                elif event.key==pygame.K_q:
                    #This executes code if the user presses the q key
                    pygame.quit()
                    #This shuts down the pygame module
                    quit()
                    #This shuts down python

            #This while loop continues to run until the paused variable is False
        gameDisplay.fill(white)
        #This fills the screen with the colour white, which was created before
        messageToScreen("Paused",green,-100,size="large")
        messageToScreen("Press C to resume or Q to quit",black,25)
        messageToScreen("The buttons can be used to resume or quit as well",black,75)
        #This calls up a function which is used to display text onto a screen
        button("Resume",150,500,100,50,green,lightGreen,action="resume")
        button("Quit",550,500,100,50,red,lightRed,action="quit")
        #These call up a function which displays text onto an interactive button
        #Each button is assigned an action which executes code if it is pressed
        if questionMoved==True:
            gameDisplay.blit(questionText,[275,5])
            #This checks if the question is moved so that it is displayed in the centre of the screen
        else:
            gameDisplay.blit(questionText,[400,5])
            #This displays the question text in the coordinates shown above
        pygame.display.update()
        #This command updates the pygame display, whenever text/images/buttons are displayed, the display always has to be updated
        clock.tick(30)
        #This sets the framerate at which the game will run, which is 30 frames per second

def score(score):
    text=smallFont.render("Score: "+str(score),True,scoreColour)
    gameDisplay.blit(text,[5,5])
    #This creates a function which is used to display the score onto the screen
    #The score is displayed onto the coordinates [5,5]

def lives(lives):
    text=smallFont.render("Lives: "+str(lives),True,scoreColour)
    gameDisplay.blit(text,[725,5])
    #This uses the same code as the score function, but for the lives variable

def randAppleGen():
    randAppleX=random.randrange(0,(displayWidth-blockSize),10)
    randAppleY=random.randrange(0,(displayHeight-blockSize),10)
    #This generates random coordinates for the answer to be displayed onto
    wrongRandAppleX=random.randrange(0,(displayWidth-blockSize),10)
    wrongRandAppleY=random.randrange(0,(displayHeight-blockSize),10)
    #This generates random coordinates for the wrong answer to be displayed onto
    return randAppleX,randAppleY
    return wrongRandAppleX,wrongRandAppleY
    #This returns the coordinates from the function

def introStudentOrTeacher():
    intro=True
    while intro==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        #This ensures that the code below is on the screen until the user quits or presses a button
        gameDisplay.fill(white)
        messageToScreen("Are you a student or a teacher?",green,-150,"medium")
        button("Student",200,400,100,50,green,lightGreen,action="student")
        button("Teacher",500,400,100,50,green,lightGreen,action="teacher")
        pygame.display.update()

def gameIntro():
    global gameSaved
    gameSaved=False
    intro=True
    while intro==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        messageToScreen("Maths Revision Snake Game",green,-150,"medium")
        messageToScreen("Made by Sean McKenna",black, -100,"small")
        messageToScreen("The objective of the game is to eat the correct answer. There will be 2 possible answers.",black,-50,"small")
        messageToScreen("The more you eat, the longer you get.",black,-20)
        messageToScreen("If you run into yourself or the edges, you lose!",black,10)
        messageToScreen("Controls: W=Up A=Left S=Down D=Right.",black,40)
        messageToScreen("Press P to pause the game.",black,70)
        messageToScreen("It is recommended to go to the options menu first to select the difficulty",black,100)
        if Teacher==True:
            messageToScreen("You can see student's data in the options menu",red,150)
            #This is only displayed if the user selects the teacher button at the start of the game
        clock.tick(30)
        button("Play",150,500,100,50,green,lightGreen,action="play")
        button("Options",350,500,100,50,yellow,lightYellow,action="options")
        button("Quit",550,500,100,50,red,lightRed,action="quit")
        pygame.display.update()
        
def options():
    gameOptions=True
    while gameOptions==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        messageToScreen("Options",green,-150,"medium")
        messageToScreenWithY("Difficulty",black,250,300,"small")
        button("KS4",50,400,100,50,green,lightGreen,action="KS4")
        button("GCSE",200,400,100,50,green,lightGreen,action="GCSE")
        button("A-Level",350,400,100,50,green,lightGreen,action="ALevel")
        button("Leaderboard",482.5,400,125,50,blue,lightBlue,action="Leaderboard")
        button("Go back",650,400,100,50,green,lightGreen,action="goBack")
        if Teacher==True:
            button("Teacher Analysis",175,500,150,50,red,lightRed,action="teacherAnalysis")
            #This button is only shown if the user selects the teacher button at the start of the game
        clock.tick(30)
        pygame.display.update()

def GCSEAnalysis():
    GCSEAnalysis=True
    global fig
    analysis=True
    while analysis==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        messageToScreen("GCSE Teacher Analysis",green,-150,"medium")
        try:
            file=open(fileNameGCSE,"r")
            #This opens the GCSE_Data.txt file or a text file searched by the teacher in read mode
            data=file.read()
            #This reads the data and stores it in the data variable
            y=[row.split(" ")[0] for row in data]
            #This splits the data in the data variable and stores it in y
            topics=("Pythagoras","Rounding","StandardForm","HCF","LCM","Percentages","Factorials")
            ind=np.arange(len(topics))
            #This returns evenly spaced values within a given interval
            #The length of topics here is 7 so ind will be ([0,1,2,3,4,5,6])
            width=0.7
            fig,ax=plt.subplots()
            #This returns a tuple containing a figure and axes object
            try:
                rects=ax.bar(ind,y,width,color="r")
            except TypeError:
                pass
            #This determines the height of each bar
            ax.set_ylabel("Number of questions wrong")
            #This sets the label on the y axis
            ax.set_xlabel("GCSE Topics")
            #This sets the label on the x axis
            ax.set_title("Number of questions wrong for GCSE Maths topics")
            #This sets the title of the graph
            ax.set_xticks(ind+width/1000)
            #This sets the x ticks
            ax.set_xticklabels((topics),rotation=45)
            #This sets the labels for the bars on the x axis, for this graph, it's the topics
            plt.tight_layout()
            canvas=agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer=canvas.get_renderer()
            rawData=renderer.tostring_rgb()
            size=canvas.get_width_height()
            surf=pygame.image.fromstring(rawData,size,"RGB")
            #This code is used to display the graph onto a pygame window
            gameDisplay.blit(surf,(0,0))
            button("Save graph",500,500,100,50,blue,lightBlue,action="Save graph GCSE")
            button("Go back",650,400,100,50,green,lightGreen,action="teacherAnalysis")
            button("Search user",100,500,120,50,blue,lightBlue,action="SearchGCSE")
        except FileNotFoundError:
            #This is an example of exception handling
            #If the program encounters a FileNotFoundError, it tells the user that it's not found
            #This prevents the program from crashing
            messageToScreen("text file not found",blue,0,"medium")
            button("Go back",650,400,100,50,green,lightGreen,action="teacherAnalysis")
        pygame.display.update()
        plt.close()

def ALevelAnalysis():
    ALevelAnalysis=True
    global fig
    analysis=True
    while analysis==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        messageToScreen("A Level Teacher Analysis",green,-150,"medium")
        try:
            file=open(fileNameALevel,"r")
            data=file.read()
            y=[row.split(" ")[0] for row in data]
            topics=("Discriminant","Differentiation","Remainder Theorem","Logarithms","Degrees to radians","Radians to degrees")
            ind=np.arange(len(topics))
            width=0.7
            fig,ax=plt.subplots()
            try:
                rects=ax.bar(ind,y,width,color="r")
            except TypeError:
                pass
            ax.set_ylabel("Number of questions wrong")
            ax.set_xlabel("A Level Topics")
            ax.set_title("Number of questions wrong for A Level Maths topics")
            ax.set_xticks(ind+width/1000)
            ax.set_xticklabels((topics),rotation=45)
            plt.tight_layout()
            canvas=agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer=canvas.get_renderer()
            rawData=renderer.tostring_rgb()
            size=canvas.get_width_height()
            surf=pygame.image.fromstring(rawData,size,"RGB")
            gameDisplay.blit(surf,(0,0))
            button("Save graph",500,500,100,50,blue,lightBlue,action="Save graph A Level")
            button("Search user",100,500,120,50,blue,lightBlue,action="SearchALevel")
        except FileNotFoundError:
            messageToScreen("text file not found",blue,0,"medium")
        button("Go back",650,400,100,50,green,lightGreen,action="teacherAnalysis")
        pygame.display.update()
        plt.close()

def teacherAnalysis():
    analysis=True
    while analysis==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        messageToScreen("Teacher Analysis",green,-150,"medium")
        messageToScreen("Here you can select the analysis for GCSE and A Level students",green,-100,"small")
        button("GCSE",200,450,100,50,blue,lightBlue,action="GCSEAnalysis")
        button("A Level",400,450,100,50,blue,lightBlue,action="ALevelAnalysis")
        button("Go back",650,450,100,50,green,lightGreen,action="options")
        pygame.display.update()

def GCSEOptionsScreen():
    GCSEOptions=True
    while GCSEOptions==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        messageToScreen("GCSE Topics",green,-150,"medium")
        #GCSEQuestions=["Pythagoras","Rounding","StandardForm","HCF","LCM","Percentages"]
        button("Pythagoras",75,300,125,50,blue,lightBlue,action="Pythagoras")
        button("Remove",75,375,125,50,red,lightRed,action="Remove Pythagoras")
        button("Rounding",225,300,125,50,blue,lightBlue,action="Rounding")
        button("Remove",225,375,125,50,red,lightRed,action="Remove Rounding")
        button("Standard Form",375,300,175,50,blue,lightBlue,action="StandardForm")
        button("Remove",375,375,125,50,red,lightRed,action="Remove Standard Form")
        button("HCF",75,450,125,50,blue,lightBlue,action="HCF")
        button("Remove",75,525,125,50,red,lightRed,action="Remove HCF")
        button("LCM",225,450,125,50,blue,lightBlue,action="LCM")
        button("Remove",225,525,125,50,red,lightRed,action="Remove LCM")
        button("Percentages",375,450,125,50,blue,lightBlue,action="Percentages")
        button("Remove",375,525,125,50,red,lightRed,action="Remove Percentages")
        button("Factorials",512.5,450,125,50,blue,lightBlue,action="Factorials")
        button("Remove",512.5,525,125,50,red,lightRed,action="Remove Factorials")
        button("Go back",650,450,100,50,green,lightGreen,action="options")
        #These buttons enable the user to add and remove specific topics for the game
        messageToScreenWithY(str(GCSEQuestions),black,400,225,"small")
        pygame.display.update()

def ALevelOptionsScreen():
    ALevelOptions=True
    while ALevelOptions==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        messageToScreen("A Level Topics",green,-150,"medium")
        button("Discriminant",75,300,125,50,blue,lightBlue,action="Discriminant")
        button("Remove",75,375,125,50,red,lightRed,action="Remove Discriminant")
        button("Differentiation",225,300,125,50,blue,lightBlue,action="Differentiation")
        button("Remove",225,375,125,50,red,lightRed,action="Remove Differentiation")
        button("Remainder Theorem",375,300,175,50,blue,lightBlue,action="RemainderTheorem")
        button("Remove",375,375,125,50,red,lightRed,action="Remove Remainder Theorem")
        button("Logarithms",75,450,125,50,blue,lightBlue,action="Logarithms")
        button("Remove",75,525,125,50,red,lightRed,action="Remove Logarithms")
        button("Radians",225,450,125,50,blue,lightBlue,action="Radians")
        button("Remove",225,525,125,50,red,lightRed,action="Remove Radians")
        button("Degrees",375,450,125,50,blue,lightBlue,action="Degrees")
        button("Remove",375,525,125,50,red,lightRed,action="Remove Degrees")
        button("Go back",650,450,100,50,green,lightGreen,action="options")
        #This is similar to the GCSE options screen, but for A Level topics
        messageToScreenWithY(str(ALevelQuestions),black,400,225,"small")
        pygame.display.update()

def button(text,x,y,width,height,inactiveColour,activeColour,action=None):
    global questionUsed
    global difficulty
    global paused
    global Student
    global Teacher
    global ALevelQuestions
    global GCSEQuestions
    global fileNameGCSE
    global fileNameALevel
    cur=pygame.mouse.get_pos()
    #This returns the position of the mouse
    click=pygame.mouse.get_pressed()
    #This returns 1 if the mouse button is pressed
    if x+width>cur[0]>x and y+height>cur[1]>y:
        pygame.draw.rect(gameDisplay,activeColour,(x,y,width,height))
        #This displays the active colour if the mouse is hovering over a button
        if click[0]==1 and action!=None:
            #This checks if the user has pressed the mouse and that there is no current action
            if action=="quit":
                #Each button is assigned an action
                #If an action is met, code is executed. In this case, if the user clicks the quit button, the code below will execute
                pygame.quit()
                quit()

            if action=="options":
                options()

            if action=="play":
                gameLoop()

            if action=="KS4":
                questionUsed=1
                #This variable is set to 1 so that the program knows that the difficulty is KS4
                #This will be used later on in the program for the database and the game loop
                difficulty="KS4"

            if action=="GCSE":
                questionUsed=2
                difficulty="GCSE"
                GCSEOptionsScreen()
                #This calls up the GCSEOptions function

            if action=="ALevel":
                questionUsed=3
                difficulty="A Level"
                ALevelOptionsScreen()

            if action=="goBack":
                gameIntro()
                #This sends the user back to the title screen

            if action=="Leaderboard":
                LeaderboardScreen()
                #This sends the user to the leaderboard

            if action=="resume":
                paused=False
                #If paused is set to False, the game will resume

            if action=="student":
                Student=True
                #This means that the user can't access the teacher analysis tool
                gameIntro()

            if action=="teacher":
                Teacher=True
                #This means that the user can access the teacher analysis tool
                gameIntro()

            if action=="teacherAnalysis":
                teacherAnalysis()

            if action=="Discriminant":
                if "Discriminant" not in ALevelQuestions:
                    #This checks that the topic is not already in the list
                    ALevelQuestions.append("Discriminant")
                    #This appends the topic "Discriminant" to the list

            if action=="Differentiation":
                if "Differentiation" not in ALevelQuestions:
                    ALevelQuestions.append("Differentiation")

            if action=="RemainderTheorem":
                if "RemainderTheorem" not in ALevelQuestions:
                    ALevelQuestions.append("RemainderTheorem")

            if action=="Logarithms":
                if "Logarithms" not in ALevelQuestions:
                    ALevelQuestions.append("Logarithms")

            if action=="Radians":
                if "Radians" not in ALevelQuestions:
                    ALevelQuestions.append("Radians")

            if action=="Degrees":
                if "Degrees" not in ALevelQuestions:
                    ALevelQuestions.append("Degrees")

            if action=="Remove Discriminant":
                if "Discriminant" in ALevelQuestions:
                    #This checks that the topic is in the list
                    #If it is not in the list, an error will occur as you cannot remove an item that isn't present
                    ALevelQuestions.remove("Discriminant")

            if action=="Remove Differentiation":
                if "Differentiation" in ALevelQuestions:
                    ALevelQuestions.remove("Differentiation")

            if action=="Remove Remainder Theorem":
                if "RemainderTheorem" in ALevelQuestions:
                    ALevelQuestions.remove("RemainderTheorem")

            if action=="Remove Logarithms":
                if "Logarithms" in ALevelQuestions:
                    ALevelQuestions.remove("Logarithms")

            if action=="Remove Radians":
                if "Radians" in ALevelQuestions:
                    ALevelQuestions.remove("Radians")

            if action=="Remove Degrees":
                if "Degrees" in ALevelQuestions:
                    ALevelQuestions.remove("Degrees")

            if action=="Pythagoras":
                if "Pythagoras" not in GCSEQuestions:
                    GCSEQuestions.append("Pythagoras")

            if action=="Rounding":
                if "Rounding" not in GCSEQuestions:
                    GCSEQuestions.append("Rounding")

            if action=="StandardForm":
                if "StandardForm" not in GCSEQuestions:
                    GCSEQuestions.append("StandardForm")

            if action=="HCF":
                if "HCF" not in GCSEQuestions:
                    GCSEQuestions.append("HCF")

            if action=="LCM":
                if "LCM" not in GCSEQuestions:
                    GCSEQuestions.append("LCM")

            if action=="Percentages":
                if "Percentages" not in GCSEQuestions:
                    GCSEQuestions.append("Percentages")

            if action=="Factorials":
                if "Factorials" not in GCSEQuestions:
                    GCSEQuestions.append("Factorials")

            if action=="Remove Pythagoras":
                if "Pythagoras" in GCSEQuestions:
                    GCSEQuestions.remove("Pythagoras")

            if action=="Remove Rounding":
                if "Rounding" in GCSEQuestions:
                    GCSEQuestions.remove("Rounding")

            if action=="Remove Standard Form":
                if "StandardForm" in GCSEQuestions:
                    GCSEQuestions.remove("StandardForm")

            if action=="Remove HCF":
                if "HCF" in GCSEQuestions:
                    GCSEQuestions.remove("HCF")

            if action=="Remove LCM":
                if "LCM" in GCSEQuestions:
                    GCSEQuestions.remove("LCM")

            if action=="Remove Percentages":
                if "Percentages" in GCSEQuestions:
                    GCSEQuestions.remove("Percentages")

            if action=="Remove Factorials":
                if "Factorials" in GCSEQuestions:
                    GCSEQuestions.remove("Factorials")

            if action=="GCSEAnalysis":
                GCSEAnalysis()

            if action=="ALevelAnalysis":
                ALevelAnalysis()

            if action=="Save graph A Level":
                if "_Data.txt" in fileNameALevel:
                    #This checks if "_Data.txt" is in the file name
                    imageName=fileNameALevel.replace("_Data.txt","")
                    #This replaces the string with an empty space
                fig.savefig(imageName+"_Graph.png")
                #This saves the ALevelGraph as a png file for the teacher

            if action=="Save graph GCSE":
                if "_Data.txt" in fileNameGCSE:
                    imageName=fileNameGCSE.replace("_Data.txt","")
                fig.savefig(imageName+"_Graph.png")

            if action=="SearchGCSE":
                fileNameGCSE=getFileName(gameDisplay)
                if fileNameGCSE=="GCSE_Data.txt":
                    pass
                else:
                    fileNameGCSE=findFile(fileNameGCSE,(cwd+"\Student Data"))
                GCSEAnalysis()

            if action=="SearchALevel":
                fileNameALevel=getFileName(gameDisplay)
                if fileNameALevel=="ALevel_Data.txt":
                    pass
                else:
                    fileNameALevel=findFile(fileNameALevel,(cwd+"\Student Data"))
                ALevelAnalysis()
                
    else:
        pygame.draw.rect(gameDisplay,inactiveColour,(x,y,width,height))
        #This displays the button if the mouse is not hovering over it

    textToButton(text,black,x,y,width,height)
    #This calls up the function that displays text to the buttons

def snake(blockSize,snakeList):
    global snakeColour
    if direction=="right":
        head=pygame.transform.rotate((snakeimg),270)
        #This rotates the snake sprite by 270 degrees
    if direction=="left":
        head=pygame.transform.rotate((snakeimg),90)
        #This rotates the snake sprite by 90 degrees
    if direction=="up":
        head=snakeimg
    if direction=="down":
        head=pygame.transform.rotate((snakeimg),180)
        #This rotates the snake sprite by 180 degrees
        
    gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))
    #This displays the snake head and body
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay,snakeColour,[XnY[0],XnY[1],blockSize,blockSize])
        #This draws the snake

def textObjects(text,colour,size):
    if size=="small":
        textSurface=smallFont.render(text,True,colour)
    elif size=="medium":
        textSurface=mediumFont.render(text,True,colour)
    elif size=="large":
        textSurface=largeFont.render(text,True,colour)
    return textSurface,textSurface.get_rect()
    #This function creates the text objects

def textToButton(msg,colour,buttonX,buttonY,buttonWidth,buttonHeight,size="small"):
    textSurf,textRect=textObjects(msg,colour,size)
    textRect.center=((buttonX+(buttonWidth/2)),buttonY+(buttonHeight/2))
    gameDisplay.blit(textSurf,textRect)
    #This function creates the text that will be displayed onto the buttons
    
def messageToScreen(msg,colour,y_displace=0,size="small"):
    textSurf,textRect=textObjects(msg,colour,size)
    textRect.center=(displayWidth/2),(displayHeight/2)+y_displace
    gameDisplay.blit(textSurf,textRect)
    #This displays the text that is used on the GUIs

def messageToScreenWithY(msg,colour,x,y,size="small"):
    textSurf,textRect=textObjects(msg,colour,size)
    textRect.center=(x,y)
    gameDisplay.blit(textSurf,textRect)
    #This is the same as the messageToScreen function but the y coordinates can be changed here

def displayBox(screen, message):
    messageToScreen("Input your name for the score",black,-120,"medium")
    messageToScreen("You will be taken back to the main menu after you press Enter",black,-70)
    pygame.draw.rect(screen, (0,0,0),((screen.get_width() / 2) - 100,(screen.get_height() / 2) - 10,200,20), 0)
    pygame.draw.rect(screen, (0,0,0),((screen.get_width() / 2) - 102,(screen.get_height() / 2) - 12,204,24), 1)
    #This creates the text box that the user will input their name into for the leaderboard
    if len(message) != 0:
        screen.blit(smallFont.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        #This displays the user's input onto the message box
    pygame.display.update()

def displayBoxSearch(screen,message):
    gameDisplay.fill(white)
    messageToScreen("Input file name",black,-120,"medium")
    pygame.draw.rect(screen, (0,0,0),((screen.get_width() / 2) - 100,(screen.get_height() / 2) - 10,250,20), 0)
    pygame.draw.rect(screen, (0,0,0),((screen.get_width() / 2) - 102,(screen.get_height() / 2) - 12,254,24), 1)
    if len(message) != 0:
        screen.blit(smallFont.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.update()

def getKey():
    while True:
        event=pygame.event.poll()
        #This gets a single event from the queue
        if event.type==pygame.KEYDOWN:
            return event.key
        else:
            pass

def getUserName(gameDisplay, question):
    pygame.font.init()
    currentString=[]
    #This creates a list called currentString, which will become a stack
    keyInput=pygame.key.get_pressed()
    #This gets the key pressed
    displayBox(gameDisplay, question + ": " + "".join(currentString))
    #This calls up the displayBox function which creates the text box
    while True:
        inkey=getKey()
        #This calls up the getKey function
        if inkey==pygame.K_BACKSPACE:
            if len(currentString)!=0:
                #This checks that the length of the stack is more than 0
                #This is because you cannot pop from an empty list
                currentString.pop()
                #This removes the most recent character from the stack, as it's a Last In First Out Structure (LIFO)
            gameDisplay.fill(white,(175,255,450,30))
            #This removes the "Maximum limit reached" text
        elif inkey==pygame.K_RETURN:
            break
            #This breaks the while loop if the user presses Enter
        elif inkey==pygame.K_MINUS:
            if len(currentString)<13:
                currentString.append("_")
            else:
                messageToScreen("Maximum limit reached",black,-25,"small")
        elif inkey<=127:
            if len(currentString)<13:
                if pygame.key.get_mods()&KMOD_SHIFT or pygame.key.get_mods()&KMOD_CAPS:
                    #This checks that the user is holding shift or is using caps lock
                    currentString.append(chr(inkey).upper())
                    #The uppercase character is appended to the stack
                else:
                    currentString.append(chr(inkey))
                    #This lowercase character is appended to the stack
            else:
                messageToScreen("Maximum limit reached",black,-25,"small")
                #This alerts the user that the stack is full
        displayBox(gameDisplay,question+": "+"".join(currentString))
        #The text box is displayed with the currentString variable
    return "".join(currentString)

def findFile(fileName,path):
    for root,dirs,files in os.walk(path):
        if fileName in files:
                return os.path.join(root,fileName)
        else:
            if questionUsed==2:
                return "GCSE_Data.txt"
            else:
                return "ALevel_Data.txt"

def getFileName(gameDisplay):
    currentString=[]
    keyInput=pygame.key.get_pressed()
    displayBoxSearch(gameDisplay,"File Name: " + "".join(currentString))
    while True:
        inkey=getKey()
        if inkey==pygame.K_BACKSPACE:
            if len(currentString)!=0:
                currentString.pop()
            gameDisplay.fill(white,(175,255,450,30))
        elif inkey==pygame.K_RETURN:
            break
        elif inkey==pygame.K_MINUS:
            currentString.append("_")
        elif inkey<=127:
            if pygame.key.get_mods()&KMOD_SHIFT or pygame.key.get_mods()&KMOD_CAPS:
                currentString.append(chr(inkey).upper())
            else:
                currentString.append(chr(inkey))
        displayBoxSearch(gameDisplay,"File Name: "+"".join(currentString))
    return "".join(currentString)
  
def saveFile():
    global name
    saveScreen=True
    while saveScreen==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    saveScreen=False
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        name=getUserName(gameDisplay, "Name")
        #This calls up the function used to get the user name
        pygame.display.update()
        playerIDFunction()
        #This calls up the function to randomly generate a player ID
        database()
        #This calls up the function to create a database and/or insert the user data into the database
        gameIntro()
        #This sends the user back to the title screen

def questionOnScreenKS4():
    global Num1
    global Num2
    global Answer
    global questionText
    global answerText
    global wrongAnswerText
    Num1=random.randint(2,12)
    Num2=random.randint(2,12)
    #This generates two random numbers between 2 and 12
    Answer=Num1*Num2
    wrongAnswer=random.randint(4,144)
    #This generates a random wrong answer between 4 and 144
    numberGeneration=False
    while numberGeneration==False:
        if Answer==wrongAnswer:
            #This compares the Answer and wrongAnswer
            #If they're the same, another wrong answer is generated
            wrongAnswer=random.randint(4,144)
        else:
            numberGeneration=True

    questionText=smallFont.render(str(Num1)+" X "+str(Num2),True,scoreColour)
    #This creates the questionText
    answerText=smallFont.render(str(Answer),True,scoreColour)
    #This creates the answerText which will be displayed onto the screen
    wrongAnswerText=smallFont.render(str(wrongAnswer),True,scoreColour)
    #This creates the wrongAnswerText which will be displayed onto the screen

def questionOnScreenGCSE():
    global Num1
    global Num2
    global Answer
    global wrongAnswer
    global questionText
    global answerText
    global wrongAnswerText
    global questionMoved
    global question
    #GCSEQuestions=["Pythagoras","Rounding","StandardForm","HCF","LCM","Percentages","Factorials"]
    if GCSEQuestions==[]:
        gameDisplay.fill(white)
        messageToScreen("Topic list is empty. Returning to options...",blue,-100,"medium")
        pygame.display.update()
        time.sleep(3)
        GCSEOptionsScreen()
        #This tells the user that the list is empty and they will be taken to the GCSEOptionsScreen
        #This is so that the game doesn't choose from an empty list which will crash the game
    question=random.choice(GCSEQuestions)
    if question=="Pythagoras":
        Num1=random.randint(0,10)
        Num2=random.randint(0,10)
        Num1Square=Num1**2
        Num2Square=Num2**2
        #This squares the two numbers. The double * is used to perform exponential calculations
        Answer=Num1Square+Num2Square
        wrongAnswer=random.randint(0,200)
        numberGeneration=False
        while numberGeneration==False:
            if Answer==wrongAnswer:
                wrongAnswer=random.randint(0,200)
            else:
                numberGeneration=True
                
        questionText=smallFont.render("a^2 = "+str(Num1)+"^2 +"+str(Num2)+"^2",True,scoreColour)
        answerText=smallFont.render("a^2="+str(Answer),True,scoreColour)
        wrongAnswerText=smallFont.render("a^2="+str(wrongAnswer),True,scoreColour)

    if question=="Rounding":
        Num1=random.randint(0,100000)
        sigFig=random.randint(1,5)
        #This generates a random value for the number of significant figures that Num1 will be rounded to
        Answer=round(Num1,-int(math.floor(math.log10(abs(Num1)))-(sigFig-1)))
        #This rounds the Num1 value to the number of significant figures generated in sigFig
        wrongAnswerSigFig=random.randint(1,5)
        randomSigFig=False
        while randomSigFig==False:
            if sigFig==wrongAnswerSigFig:
                wrongAnswerSigFig=random.randint(1,5)
                randomSigFig=False
            else:
                randomSigFig=True
            #This while loop generates a value for the number of significant figures
            #For the wrong answer, that is not the same as the correct answer
        wrongAnswer=round(Num1,-int(math.floor(math.log10(abs(Num1)))-(wrongAnswerSigFig-1)))
        randWrongAnswer=False
        while randWrongAnswer==False:
            if Answer==wrongAnswer:
                wrongAnswer=round(Num1,-int(math.floor(math.log10(abs(Num1)))-(wrongAnswerSigFig-1)))
            else:
                randWrongAnswer=True

        questionMoved=False
        questionText=smallFont.render(str(Num1)+" to "+str(sigFig)+" sig figs ",True,scoreColour)
        answerText=smallFont.render(str(Answer),True,scoreColour)
        wrongAnswerText=smallFont.render(str(wrongAnswer),True,scoreColour)

    if question=="StandardForm":
        Num1=random.randint(1,10)
        Index=random.randint(-2,3)
        Answer=Num1**Index
        Answer=round(Answer,2)
        #This rounds the value in Answer to 2 decimal places
        wrongAnswerIndex=random.randint(-2,3)
        wrongAnswer=Num1**wrongAnswerIndex
        wrongAnswer=round(wrongAnswer,2)
        wrongIndex=False
        while wrongIndex==False:
            if Answer==wrongAnswer:
                wrongAnswerIndex=random.randint(-2,3)
                wrongAnswer=Num1**wrongAnswerIndex
                wrongAnswer=round(wrongAnswer,2)
            else:
                wrongIndex=True
        questionMoved=False
        questionText=smallFont.render(str(Num1)+"^"+str(Index),True,scoreColour)
        answerText=smallFont.render(str(Answer),True,scoreColour)
        wrongAnswerText=smallFont.render(str(wrongAnswer),True,scoreColour)

    if question=="HCF":
        Num1=random.randint(1,100)
        Num2=random.randint(1,100)
        if Num1>Num2:
            smaller=Num2
        else:
            smaller=Num1
        for i in range(1,smaller+1):
            if((Num1%i==0) and (Num2%i==0)):
            #This checks that the remainder when Num1 divided by i is the same as the remainder when Num2 is divided by i
               HCF=i

        #This algorithm is used to find the Highest Common Factor of two randomly generated values

        wrongAnswer=random.randint(1,100)
        randWrongAnswer=False
        while randWrongAnswer==False:
            if HCF==wrongAnswer:
                wrongAnswer=random.randint(1,100)
            else:
                randWrongAnswer=True
        questionMoved=False
        questionText=smallFont.render("Find HCF of "+str(Num1)+" and "+str(Num2),True,scoreColour)
        answerText=smallFont.render(str(HCF),True,scoreColour)
        wrongAnswerText=smallFont.render(str(wrongAnswer),True,scoreColour)

    if question=="LCM":
        Num1=random.randint(1,100)
        Num2=random.randint(1,100)
        if Num1>Num2:
            larger=Num1
        else:
            larger=Num2

        while True:
            if((larger%Num1==0) and (larger%Num2==0)):
                LCM=larger
                break
            #This algorithm is similar to the HCF algorithm, but checks the larger number rather than the smaller number
            larger+=1

        wrongAnswer=random.randint(1,100)
        randWrongAnswer=False
        while randWrongAnswer==False:
            if LCM==wrongAnswer:
                wrongAnswer=random.randint(1,100)
            else:
                randWrongAnswer=True

        questionMoved=False
        questionText=smallFont.render("Find LCM of "+str(Num1)+" and "+str(Num2),True,scoreColour)
        answerText=smallFont.render(str(LCM),True,scoreColour)
        wrongAnswerText=smallFont.render(str(wrongAnswer),True,scoreColour)

    if question=="Percentages":
        Num1=random.randint(10,200)
        percentage=random.randint(1,100)
        Answer=((percentage/100)*Num1)
        #This converts the percentage into a decimal and multiplies it by Num1
        Answer=round(Answer)
        wrongAnswer=random.randint(10,200)
        randWrongAnswer=False
        while randWrongAnswer==False:
            if Answer==wrongAnswer:
                wrongAnswer=random.randint(10,200)
            else:
                randWrongAnswer=True
        questionMoved=False
        questionText=smallFont.render(str(percentage)+"% of "+str(Num1),True,scoreColour)
        answerText=smallFont.render(str(Answer),True,scoreColour)
        wrongAnswerText=smallFont.render(str(wrongAnswer),True,scoreColour)

    if question=="Factorials":
        Num1=random.randint(2,5)
        Answer=factorial(Num1)
        #This is an example of a recursive algorithm
        #It calls up the factorial function which calls itself up until Num1 is 1
        wrongNum=False
        while wrongNum==False:
            wrongAnswer=random.randint(1,50)
            if wrongAnswer%2==0:
                wrongNum=True
            else:
                wrongAnswer=random.randint(1,50)
        questionMoved=False
        questionText=smallFont.render(str(Num1)+"!",True,scoreColour)
        answerText=smallFont.render(str(Answer),True,scoreColour)
        wrongAnswerText=smallFont.render(str(wrongAnswer),True,scoreColour)

def factorial(Num1):
    if Num1==0:
        return 1
    else:
        return Num1*factorial(Num1-1)
    #This recursive algorithm returns the randomly generated number multiplied by itself - 1 until it reaches 1

def questionOnScreenALevel():
    global Num1
    global Num2
    global Num3
    global Answer
    global wrongAnswer
    global questionText
    global answerText
    global wrongAnswerText
    global questionMoved
    global question
    #topics=("Discriminant","Differentiation","Remainder Theorem","Logarithms","Radians","Degrees")
    if ALevelQuestions==[]:
        gameDisplay.fill(white)
        messageToScreen("Topic list is empty. Returning to options...",blue,-100,"medium")
        pygame.display.update()
        time.sleep(3)
        ALevelOptionsScreen()
    question=random.choice(ALevelQuestions)
    if question=="Discriminant":
        Num1=random.randint(1,2)
        Num2=random.randint(1,5)
        Num3=random.randint(1,10)
        #Discriminant=b^2-4ac
        Answer=(Num2**2)-(4*Num1*Num3)
        #This performs the equation b^2-4ac which is used to calculate the discriminant of an equation
        wrongAnswer=random.randint(1,21)
        randWrongAnswer=False
        while randWrongAnswer==False:
            if Answer==wrongAnswer:
                wrongAnswer=random.randint(1,21)
            else:
                randWrongAnswer=True

        questionText=smallFont.render("Find discriminant of "+str(Num1)+"x^2 +"+str(Num2)+"x +"+str(Num3),True,scoreColour)
        questionMoved=True
        answerText=smallFont.render(str(Answer),True,scoreColour)
        wrongAnswerText=smallFont.render(str(wrongAnswer),True,scoreColour)

    if question=="Differentiation":
        Num1=random.randint(1,5)
        Num2=random.randint(1,5)
        #Differentiate
        newNum1=Num1*Num2
        newNum2=Num2-1
        #The differential of a function is the coefficient multiplied by the power, then 1 is taken away from the power
        #Example: the differential of 2x^3 is 6x^2
        wrongNum1=random.randint(1,5)
        wrongNum2=random.randint(1,5)
        wrongNewNum1=wrongNum1*wrongNum2
        wrongNewNum2=wrongNum2-1
        randWrongAnswer=False
        while randWrongAnswer==False:
            if newNum1==wrongNewNum1 and newNum2==wrongNewNum2:
                wrongNum1=random.randint(1,5)
                wrongNum2=random.randint(1,5)
                wrongNewNum1=wrongNum1*wrongNum2
                wrongNewNum2=wrongNum2-1
            else:
                randWrongAnswer=True
        questionMoved=False
        questionText=smallFont.render("Differentiate "+str(Num1)+"x^"+str(Num2),True,scoreColour)
        answerText=smallFont.render(str(newNum1)+"x^"+str(newNum2),True,scoreColour)
        wrongAnswerText=smallFont.render(str(wrongNewNum1)+"x^"+str(wrongNewNum2),True,scoreColour)

    if question=="RemainderTheorem":
        calc=""
        randNum=False
        while randNum==False:
            Num1=random.randint(-3,3)
            if Num1==0:
                Num1=random.randint(-3,3)
            else:
                if Num1==-3 or Num1==-2 or Num1==-1:
                    calc=="-"
                    #This ensures that the correct sign is displayed to the user
                else:
                    calc="+"
                randNum=True
        newNum1=-Num1
        Num2=random.randint(1,3)
        Num3=random.randint(1,3)
        Num4=random.randint(1,3)
        newNum2=Num2*(newNum1**2)
        newNum3=Num3*newNum1
        questionString=str(Num2)+"x^2 + "+str(Num3)+"x + "+str(Num4)
        value=Num1
        answer=newNum2+newNum3+Num4
        wrongAnswer=random.randint(-5,40)
        randWrongAnswer=False
        while randWrongAnswer==False:
            if answer==wrongAnswer:
                wrongAnswer=random.randint(-5,30)
            else:
                randWrongAnswer=True

        questionText=smallFont.render("Find remainder when "+questionString+" is divided by x"+calc+str(Num1),True,scoreColour)
        questionMoved=True
        answerText=smallFont.render(str(answer),True,scoreColour)
        wrongAnswerText=smallFont.render(str(wrongAnswer),True,scoreColour)

    if question=="Logarithms":
        choice=random.randint(1,3)
        if choice==1:
            Num1=random.randint(2,5)
            Num2=random.randint(2,5)
            answer=Num1**Num2
            #This will ask a question such as log base 2 of x = 5. Find x
            #In this case x will be 32
            wrongAnswer=random.randint(1,144)
            randWrongAnswer=False
            while randWrongAnswer==False:
                if answer==wrongAnswer:
                    wrongAnswer=random.randint(1,144)
                else:
                    randWrongAnswer=True
            questionMoved=False
            questionText=smallFont.render(("log "+str(Num1)+" x = "+str(Num2)+". Find x"),True,scoreColour)
            answerText=smallFont.render(str(answer),True,scoreColour)
            wrongAnswerText=smallFont.render(str(wrongAnswer),True,scoreColour)
            
        elif choice==2:
            Num1=random.randint(1,12)
            Num2=random.randint(1,12)
            answer=Num1*Num2
            #Using the laws of logarithms, log(a) + log(b) = log(ab)
            wrongAnswer=random.randint(1,144)
            randWrongAnswer=False
            while randWrongAnswer==False:
                if answer==wrongAnswer:
                    wrongAnswer=random.randint(1,144)
                else:
                    randWrongAnswer=True
            questionMoved=False
            questionText=smallFont.render(("log("+str(Num1)+") + log("+str(Num2)+")"),True,scoreColour)
            answerText=smallFont.render(("log("+str(answer)+")"),True,scoreColour)
            wrongAnswerText=smallFont.render(("log("+str(wrongAnswer)+")"),True,scoreColour)

        elif choice==3:
            Num1=random.randint(10,144)
            Num2=random.randint(1,144)
            answer=round(Num1/Num2,2)
            #Using the laws of logarithms, log(a) - log(b) = log(a/b)
            wrongAnswer=round(random.uniform(1,144),2)
            randWrongAnswer=False
            while randWrongAnswer==False:
                if answer==wrongAnswer:
                    wrongAnswer=round(random.uniform(1,80),2)
                else:
                    randWrongAnswer=True
            questionMoved=False
            questionText=smallFont.render(("log("+str(Num1)+") - log("+str(Num2)+")"),True,scoreColour)
            answerText=smallFont.render(("log("+str(answer)+")"),True,scoreColour)
            wrongAnswerText=smallFont.render(("log("+str(wrongAnswer)+")"),True,scoreColour)

    if question=="Radians":
        Num1=random.randint(0,360)
        answer=math.radians(Num1)
        #This converts Num1 from degrees into radians
        answer=answer/math.pi
        #Using math.pi is a more accurate value for pi than using 3.14
        #The answer has to be divided by pi as it will be expressed in terms of pi radians
        answer=round(answer,2)
        wrongAnswer=random.uniform(0,2)
        wrongAnswer=round(wrongAnswer,2)
        randWrongAnswer=False
        while randWrongAnswer==False:
            if answer==wrongAnswer:
                wrongAnswer=random.uniform(0,2)
                wrongAnswer=round(wrongAnswer,2)
            else:
                randWrongAnswer=True
        questionMoved=True
        questionText=smallFont.render("Convert "+str(Num1)+" degrees to radians",True,scoreColour)
        answerText=smallFont.render(str(answer)+"pi",True,scoreColour)
        wrongAnswerText=smallFont.render(str(wrongAnswer)+"pi",True,scoreColour)

    if question=="Degrees":
        Num1=random.uniform(0,2*math.pi)
        #This randomly generates a value between 0 and 2pi (or 0 and 6.2831...)
        answer=math.degrees(Num1)
        #This converts Num1 from radians to degrees
        answer=round(answer,1)
        wrongAnswer=random.uniform(0,360)
        wrongAnswer=round(wrongAnswer,1)
        randWrongAnswer=True
        while randWrongAnswer==False:
            if answer==wrongAnswer:
                wrongAnswer=random.randint(0,360)
                wrongAnswer=round(wrongAnswer,1)
            else:
                randWrongAnswer=True
        questionMoved=True
        question1=Num1/math.pi
        question1=round(question1,2)
        questionText=smallFont.render("Convert "+str(question1)+" pi radians to degrees",True,scoreColour)
        answerText=smallFont.render(str(answer),True,scoreColour)
        wrongAnswerText=smallFont.render(str(wrongAnswer),True,scoreColour)
        
def playerIDFunction():
    global playerID
    playerID=random.randint(10000,99999)
    #This randomly generates a 5 digit ID number for the player

def database():
    global Leaderboard
    connection=sqlite3.connect("MathsGameData.db")
    #This creates a database file
    c=connection.cursor()
    #This establishes a connection to the database
    c.execute('''CREATE TABLE IF NOT EXISTS users(playerID INTEGER PRIMARY KEY, name TEXT, score INTEGER, difficulty TEXT)''')
    #This executes SQL code which creates a table called users, where the playerID will serve as the primary key
    if gameSaved==True:
        #This checks that the player has saved the game
        #If they have, then their playerID, name, score and difficulty will be inserted into the table created before
        c.execute('''INSERT INTO users(playerID, name, score, difficulty) VALUES(?,?,?,?)''',(playerID,name,gameScore,difficulty))
    c.execute('''SELECT playerID,name,score,difficulty FROM users ORDER BY score DESC''')
    #This selects the data from the table users and orders it by the score
    #This is so that the leaderboard shows the player with the highest score at the top
    allRows=c.fetchall()
    #This fetches all of the rows of a query result, returning a list
    for row in allRows:
        File=open("Leaderboard.txt","w")
        #This creates a text file which in write mode
        for row in allRows:
            File.write('{0} User Name: {1} | Score = {2} | Difficulty: {3}'.format(row[0],row[1],row[2],row[3]))
            File.write("\n")
            #This writes all the data of players from the database to the text file
        File.close()
        #This closes the text file as the program has stopped writing to it

    c.execute('''CREATE TABLE IF NOT EXISTS GCSEQuestions(playerID INTEGER REFERENCES users, Pythagoras INTEGER, Rounding INTEGER, StandardForm INTEGER, HCF INTEGER, LCM INTEGER, Percentages INTEGER, Factorials INTEGER)''') 
    c.execute('''CREATE TABLE IF NOT EXISTS ALevelQuestions(playerID INTEGER REFERENCES users, Discriminant INTEGER, Differentiation INTEGER, RemainderTheorem INTEGER, Logarithms INTEGER, Radians INTEGER, Degrees INTEGER)''')
    #This creates two new tables which will be used for the teacher analysis tool
    #This establishes a relation to table users as playerID is the foreign key in these two tables

    if gameSaved==True:
        if questionUsed==2:
        #This checks if the user has selected GCSE questions or A Level questions
            c.execute('''INSERT INTO GCSEQuestions(playerID, Pythagoras, Rounding, StandardForm, HCF, LCM, Percentages, Factorials) VALUES (?,?,?,?,?,?,?,?)''',(playerID,pythagorasWrong,roundingWrong,standardFormWrong,HCFWrong,LCMWrong,percentagesWrong,factorialsWrong))
        if questionUsed==3:
            c.execute('''INSERT INTO ALevelQuestions(playerID, Discriminant, Differentiation, RemainderTheorem, Logarithms, Radians, Degrees) VALUES (?,?,?,?,?,?,?)''',(playerID,discriminantWrong,differentiationWrong,remainderTheoremWrong,logarithmsWrong,radiansWrong,degreesWrong))

    if questionUsed==2:
        c.execute('''SELECT (Pythagoras), (Rounding), (StandardForm), (HCF), (LCM), (Percentages), (Factorials) FROM GCSEQuestions, users WHERE GCSEQuestions.playerID==users.playerID''')
        if not os.path.exists(cwd+"\Student Data"):
            #This checks if there is an existing directory called Student Data
            os.makedirs(cwd+"\Student Data")
            #This creates a new directory called Student Data
        allRows=c.fetchall()
        for row in allRows:
            file1=os.path.join(cwd+"\Student Data",name+".txt")
            fileStudentGCSE=open(file1,"w")
            fileStudentGCSE.write("Student name: "+name+"\n\n")
            fileStudentGCSE.write("Pythagoras questions wrong: {0}\nRounding questions wrong: {1}\nStandard form questions wrong: {2}\nHCF questions wrong: {3}\nLCM questions wrong: {4}\nPercentages questions wrong: {5}\nFactorials questions wrong: {6}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            worstTopicValue=max(row)
            worstTopicIndex=row.index(worstTopicValue)
            fileStudentGCSE.write("\n\n")
            if worstTopicIndex==0:
                worstTopic="Pythagoras"
            elif worstTopicIndex==1:
                worstTopic="Rounding"
            elif worstTopicIndex==2:
                worstTopic="Standard Form"
            elif worstTopicIndex==3:
                worstTopic="Highest Common Factor"
            elif worstTopicIndex==4:
                worstTopic="Lowest Common Multiple"
            elif worstTopicIndex==5:
                worstTopic="Percentages"
            elif worstTopicIndex==6:
                worstTopic="Factorials"
            fileStudentGCSE.write("The topic that needs to be improved the most is: ")
            fileStudentGCSE.write(worstTopic)
            fileStudentGCSE.close()

        for row in allRows:
            file1=os.path.join(cwd+"\Student Data",name+"_Data.txt")
            file=open(file1,"w")
            file.write("{0}{1}{2}{3}{4}{5}{6}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            file.close()
        
            
        c.execute('''SELECT SUM(Pythagoras), SUM(Rounding), SUM(StandardForm), SUM(HCF), SUM(LCM), SUM(Percentages), SUM(Factorials) FROM GCSEQuestions, users WHERE GCSEQuestions.playerID==users.playerID''')
        #This gets the total amount of questions answered wrong for each topic from GCSEQuestions
        #This also checks that the playerID in GCSEQuestions is the same as the one in users
        allRows=c.fetchall()
        for row in allRows:
            File=open("GCSE_Analysis.txt","w")
            for row in allRows:
                File.write("Pythagoras questions wrong: {0}\nRounding questions wrong: {1}\nStandard form questions wrong: {2}\nHCF questions wrong: {3}\nLCM questions wrong: {4}\nPercentages questions wrong: {5}\nFactorials questions wrong: {6}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                worstTopicValue=max(row)
                #This chooses the maximum value in the row out of all of the topics
                worstTopicIndex=row.index(worstTopicValue)
                #This selects the index that the maximum value is located
                File.write("\n\n")
                if worstTopicIndex==0:
                    worstTopic="Pythagoras"
                elif worstTopicIndex==1:
                    worstTopic="Rounding"
                elif worstTopicIndex==2:
                    worstTopic="Standard Form"
                elif worstTopicIndex==3:
                    worstTopic="Highest Common Factor"
                elif worstTopicIndex==4:
                    worstTopic="Lowest Common Multiple"
                elif worstTopicIndex==5:
                    worstTopic="Percentages"
                elif worstTopicIndex==6:
                    worstTopic="Factorials"
                    #This finds the topic based on the index of the maximum value and sets that as the topic that had the worst performance from players
                File.write("The topic that needs to be improved the most is: ")
                File.write(worstTopic)
            File.close()
        c.execute('''SELECT SUM(Pythagoras), SUM(Rounding), SUM(StandardForm), SUM(HCF), SUM(LCM), SUM(Percentages), SUM(Factorials) FROM GCSEQuestions''')
        allRows=c.fetchall()
        for row in allRows:
            file=open("GCSE_Data.txt","w")
            for row in allRows:
                file.write("{0}{1}{2}{3}{4}{5}{6}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                #This data text file will be used for the values on the y axis of the graph
            file.close()

    #From here the code is the same as the code above but with A Level topics instead    
    if questionUsed==3:
        c.execute('''SELECT (Discriminant), (Differentiation), (RemainderTheorem), (Logarithms), (Radians), (Degrees) FROM ALevelQuestions''')
        allRows=c.fetchall()
        if not os.path.exists(cwd+"\Student Data"):
            os.makedirs(cwd+"\Student Data")
        for row in allRows:
            file1=os.path.join(cwd+"\Student Data",name+".txt")
            fileStudentALevel=open(file1,"w")
            fileStudentALevel.write("Student name: "+name+"\n\n")
            fileStudentALevel.write("Discriminant questions wrong: {0}\nDifferentiation questions wrong: {1}\nRemainder theorem questions wrong: {2}\nLogarithms questions wrong: {3}\nDegrees to radians questions wrong: {4}\nRadians to degrees questions wrong: {5}".format(row[0],row[1],row[2],row[3],row[4],row[5]))
            worstTopicValue=max(row)
            worstTopicIndex=row.index(worstTopicValue)
            fileStudentALevel.write("\n\n")
            if worstTopicIndex==0:
                worstTopic="Discriminant"
            elif worstTopicIndex==1:
                worstTopic="Differentiation"
            elif worstTopicIndex==2:
                worstTopic="Remainder theorem"
            elif worstTopicIndex==3:
                worstTopic="Logarithms"
            elif worstTopicIndex==4:
                worstTopic="Degrees to radians"
            elif worstTopicIndex==5:
                worstTopic="Radians to degrees"
            fileStudentALevel.write("The topic that needs to be improved the most is: ")
            fileStudentALevel.write(worstTopic)
        fileStudentALevel.close()

        for row in allRows:
            file1=os.path.join(cwd+"\Student Data",name+"_Data.txt")
            file=open(file1,"w")
            file.write("{0}{1}{2}{3}{4}{5}".format(row[0],row[1],row[2],row[3],row[4],row[5]))
        file.close()
       
        c.execute('''SELECT SUM(Discriminant), SUM(Differentiation), SUM(RemainderTheorem), SUM(Logarithms), SUM(Radians), SUM(Degrees) FROM ALevelQuestions,users WHERE ALevelQuestions.playerID==users.playerID''')
        allRows=c.fetchall()
        for row in allRows:
            File=open("ALevel_Analysis.txt","w")
            for row in allRows:
                File.write("Discriminant questions wrong: {0}\nDifferentiation questions wrong: {1}\nRemainder theorem questions wrong: {2}\nLogarithms questions wrong: {3}\nDegrees to radians questions wrong: {4}\nRadians to degrees questions wrong: {5}".format(row[0],row[1],row[2],row[3],row[4],row[5]))
                worstTopicValue=max(row)
                worstTopicIndex=row.index(worstTopicValue)
                File.write("\n\n")
                if worstTopicIndex==0:
                    worstTopic="Discriminant"
                elif worstTopicIndex==1:
                    worstTopic="Differentiation"
                elif worstTopicIndex==2:
                    worstTopic="Remainder theorem"
                elif worstTopicIndex==3:
                    worstTopic="Logarithms"
                elif worstTopicIndex==4:
                    worstTopic="Degrees to radians"
                elif worstTopicIndex==5:
                    worstTopic="Radians to degrees"
                File.write("The topic that needs to be improved the most is: ")
                File.write(worstTopic)
        File.close()
        c.execute('''SELECT SUM(Discriminant), SUM(Differentiation), SUM(RemainderTheorem), SUM(Logarithms), SUM(Radians), SUM(Degrees) FROM ALevelQuestions,users WHERE ALevelQuestions.playerID==users.playerID''')
        allRows=c.fetchall()
        for row in allRows:
            file=open("ALevel_Data.txt","w")
            for row in allRows:
                file.write("{0}{1}{2}{3}{4}{5}".format(row[0],row[1],row[2],row[3],row[4],row[5]))
        file.close()
    connection.commit()
    #This saves the changes to the database

def LeaderboardScreen():
    gameDisplay.fill(white)
    LeaderboardGUI=True
    while LeaderboardGUI==True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        messageToScreen("Leaderboard",red,-200,"medium")
        try:
            LeaderboardFile=open("Leaderboard.txt","r")
            #This opens the Leaderboard.txt file in read mode
            lines=LeaderboardFile.readlines()
            #This reads each of the lines and stores them in the variable lines
            LeaderboardFile.close()
            #This closes the text file as it is not needed anymore
            text=mediumFont.render("Hello world",True,scoreColour)
            textRect=text.get_rect()
            #This gets the dimensions of the rendered text image which returns width and height attributed
            textRect.centerx=250
            textRect.centery=150
            #This sets the coordinates of the text image
            for i in lines:
                text=smallFont.render(i[:-1],True,scoreColour)
                #This renders each line in the lines variable
                textRect.centery+=25
                #This increases the y coordinate by 25 each time the loop is iterated
                gameDisplay.blit(text,textRect)
        except FileNotFoundError:
            #This catches a FileNotFoundError in case the leaderboard file does not exist
            #This is so that it notifies the user that it's not there instead of crashing
            messageToScreen("Leaderboard file not found",blue,0,"medium")
        button("Go back",650,500,100,50,green,lightGreen,action="options")
        pygame.display.update()

def gameLoop():
    global gameScore
    global direction
    global pauseCount
    global answerText
    global questionMoved
    global gameSaved
    gameScore=0
    gameLives=3
    global pythagorasWrong
    global roundingWrong
    global standardFormWrong
    global HCFWrong
    global LCMWrong
    global percentagesWrong
    global factorialsWrong
    global discriminantWrong
    global differentiationWrong
    global remainderTheoremWrong
    global logarithmsWrong
    global radiansWrong
    global degreesWrong
    pythagorasWrong=0
    roundingWrong=0
    standardFormWrong=0
    HCFWrong=0
    LCMWrong=0
    percentagesWrong=0
    factorialsWrong=0
    discriminantWrong=0
    differentiationWrong=0
    remainderTheoremWrong=0
    logarithmsWrong=0
    radiansWrong=0
    degreesWrong=0
    gameExit=False
    gameOver=False
    lead_x=displayWidth/2
    lead_y=displayHeight/2
    lead_x_change=5
    lead_y_change=0

    snakeList=[]
    snakeLength=1
    
    global blockSpeed
    global blockSize
    blockSpeed=blockSpeed
    blockSize=blockSize
    
    randAppleX,randAppleY=randAppleGen()
    wrongRandAppleX,wrongRandAppleY=randAppleGen()
    #This generates the coordinates of the answer and the wrong answer
    if randAppleX==wrongRandAppleX+-10:
        randAppleX,randAppleY=randAppleGen()
        wrongRandAppleX,wrongRandAppleY=randAppleGen()
    if randAppleY==wrongRandAppleY+-10:
        randAppleX,randAppleY=randAppleGen()
        wrongRandAppleX,wrongRandAppleY=randAppleGen()
        #This checks if the coordinates of the right and wrong answer are too close
        #If they're too close, the coordinates will be generated again
        
    if questionMoved==True:
        if randAppleY==5+-30 or randAppleX==275+-30 or randAppleX==725+-30 or randAppleX==displayWidth+-30 or randAppleY==displayHeight+-30 or randAppleX==5+-30 or randAppleY==5+-30:
            randAppleX,randAppleY=randAppleGen()
        elif wrongRandAppleY==5+-30 or wrongRandAppleX==275+-30 or wrongRandAppleX==725+-30 or wrongRandAppleX==displayWidth+-30 or wrongRandAppleY==displayHeight+-30 or wrongRandAppleX==5+-30 or wrongRandAppleY==5+-30:
            wrongRandAppleX,wrongRandAppleY=randAppleGen()
    else:
        if randAppleY==5+-30 or randAppleX==400+-30 or randAppleX==725+-30 or randAppleX==displayWidth+-30 or randAppleY==displayHeight+-30 or randAppleX==5+-30 or randAppleY==5+-30:
            randAppleX,randAppleY=randAppleGen()
        elif wrongRandAppleY==5+-30 or wrongRandAppleX==400+-30 or wrongRandAppleX==725+-30 or wrongRandAppleX==displayWidth+-30 or wrongRandAppleY==displayHeight+-30 or randAppleX==5+-30 or randAppleY==5+-30:
            wrongRandAppleX,wrongRandAppleY=randAppleGen()

    #This generates a question based on the topic that they chose
    if questionUsed==1:
        questionOnScreenKS4()
    elif questionUsed==2:
        questionOnScreenGCSE()
    elif questionUsed==3:
        questionOnScreenALevel()
    else:
        questionOnScreenKS4()
    
    while gameExit==False:
        while gameOver==True:
            #This is the code that runs when the user runs out of lives or runs into the edges of the screen
            blockSpeed=4
            gameDisplay.fill(white)
            messageToScreen("Game Over",red,y_displace=-50,size="large")
            scoreText=smallFont.render("Score: "+str(gameScore),True,scoreColour)
            gameDisplay.blit(scoreText,[380,300])
            messageToScreen("Press C to play again, M to go to the Menu, S to save the score, or Q to quit",black,50)
            button("Play",150,500,100,50,green,lightGreen,action="play")
            button("Menu",355,500,100,50,green,lightGreen,action="goBack")
            button("Quit",550,500,100,50,red,lightRed,action="quit")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        #This will quit the game
                        gameExit=True
                        gameOver=False
                    if event.key==pygame.K_c:
                        #This will play the game again
                        gameLoop()
                    if event.key==pygame.K_m:
                        #This will take the user back to the title screen
                        gameIntro()
                    if event.key==pygame.K_s:
                        gameSaved=True
                        #If the user presses "s", they will be able to save their score and their name to the database
                        saveFile()
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit=True
                gameOver=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_a:
                    #This is what happens when the user presses "a"
                    direction="left"
                    lead_x_change=-blockSpeed
                    lead_y_change=0
                elif event.key==pygame.K_d:
                    #This is what happens when the user presses "d"
                    direction="right"
                    lead_x_change=blockSpeed
                    lead_y_change=0
                elif event.key==pygame.K_w:
                    #This is what happens when the user presses "w"
                    direction="up"
                    lead_y_change=-blockSpeed
                    lead_x_change=0
                elif event.key==pygame.K_s:
                    #This is what happens when the user presses "s"
                    direction="down"
                    lead_y_change=blockSpeed
                    lead_x_change=0

                elif event.key==pygame.K_p:
                    #When the user presses "p", the game will be paused
                    pause()
                    
        if lead_x>=displayWidth or lead_x<=0 or lead_y>=displayHeight or lead_y<=0:
            #This checks if the snake's position is equal to the edges of the screen
            gameOver=True
                
        lead_x+=lead_x_change
        lead_y+=lead_y_change

        gameDisplay.fill(lightBlue)
        AppleThickness=25
        gameDisplay.blit(answerText,(randAppleX,randAppleY))
        #This displays the answer text to the randomly generated coordinates
        if questionMoved==True:
            #This is displayed to the left slightly in case the question text is long
            #This is so that the text is more aligned to the centre of the screen
            gameDisplay.blit(questionText,[275,5])
        else:
            gameDisplay.blit(questionText,[400,5])
        gameDisplay.blit(wrongAnswerText,(wrongRandAppleX,wrongRandAppleY))
        #This displays the wrong answer text to the randomly generated coordinates
        
        snakeHead=[]
        #This creates a list for the snake head which will be the snakeimg file
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        #This appends the coordinates of the head of the snake to the list
        snakeList.append(snakeHead)
        snake(blockSize,snakeList)
        #This calls up the snake function which is used to render the snake onto the screen

        if len(snakeList)>snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment==snakeHead:
                #This checks if the snake runs into itself which will result in a game over
                gameOver=True
        
        score(snakeLength-1)
        lives(gameLives)
        #This is used to display the score and lives to the screen
        
        if lead_x>randAppleX and lead_x<randAppleX+AppleThickness or lead_x+blockSize>randAppleX and lead_x+blockSize<randAppleX+AppleThickness:
            if lead_y>randAppleY and lead_y<randAppleY+AppleThickness or lead_y+blockSize>randAppleY and lead_y+blockSize<randAppleY+AppleThickness:
                #This checks if the snake collides with the correct answer
                randAppleX,randAppleY=randAppleGen()
                wrongRandAppleX,wrongRandAppleY=randAppleGen()
                #This generates new coordinates for the answers
                if questionUsed==1:
                    questionOnScreenKS4()
                elif questionUsed==2:
                    questionOnScreenGCSE()
                elif questionUsed==3:
                    questionOnScreenALevel()
                else:
                    questionOnScreenKS4()
                #This calls up the functions to generate another question
                gameScore=gameScore+1
                #This appends 1 to the score
                blockSpeed+=0.1
                #This increases the block speed by 0.1
                #This is to increase the difficulty of the game over time
                snakeLength=snakeLength+1
                #This increments the length of the snake by 1

        if lead_x>wrongRandAppleX and lead_x<wrongRandAppleX+AppleThickness or lead_x+blockSize>wrongRandAppleX and lead_x+blockSize<wrongRandAppleX+AppleThickness:
            if lead_y>wrongRandAppleY and lead_y<wrongRandAppleY+AppleThickness or lead_y+blockSize>wrongRandAppleY and lead_y+blockSize<wrongRandAppleY+AppleThickness:
                #This checks if the snake collides with the incorrect answer
                randAppleX,randAppleY=randAppleGen()
                wrongRandAppleX,wrongRandAppleY=randAppleGen()
                #This generates new coordinates for the next correct and incorrect answer
                if questionUsed==1:
                    questionOnScreenKS4()
                elif questionUsed==2:
                    questionOnScreenGCSE()
                    if question=="Pythagoras":
                        pythagorasWrong+=1
                        #This adds 1 to the topic that the user got wrong
                        #This will be used for the teacher analysis tool
                    if question=="Rounding":
                        roundingWrong+=1
                    if question=="StandardForm":
                        standardFormWrong+=1
                    if question=="HCF":
                        HCFWrong+=1
                    if question=="LCM":
                        LCMWrong+=1
                    if question=="Percentages":
                        percentagesWrong+=1
                    if question=="Factorials":
                        factorialsWrong+=1
                elif questionUsed==3:
                    questionOnScreenALevel()
                    if question=="Discriminant":
                        discriminantWrong+=1
                    if question=="Differentiation":
                        differentiationWrong+=1
                    if question=="RemainderTheorem":
                        remainderTheoremWrong+=1
                    if question=="Logarithms":
                        logarithmsWrong+=1
                    if question=="Radians":
                        radiansWrong+=1
                    if question=="Degrees":
                        degreesWrong+=1
                else:
                    questionOnScreenKS4()
                gameLives-=1
                #This decreases the number of lives by 1

        if gameLives==0:
            gameOver=True
            #When the user runs out of lives, the game will end

        pygame.display.update()
        #This updates the display
        
        clock.tick(FPS)
        #This issues a framerate equal to the value in variable FPS, which is 60 frames per second

    pygame.quit()
    #This shuts down the pygame module
    quit()
    #This closes python

introStudentOrTeacher()
#This calls up the function which asks the user if they're a student or teacher
#This is the first function called up in the program
