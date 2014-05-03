############################################################
# Some code taken from Gus Henry's hw10.py file            #
# car image from http://www.freestockphotos.biz/           #
# stick figure image from http://bbsimg.ngfiles.com/       #
# tree image from http://www.clipartbest.com/              #
# crappy bird logo image from https://lh5.ggpht.com        #
# birdhouse tree image from http://comps.canstockphoto.com #
# hawk image from http://13moon.com                        #
# cloud image from http://www.gamesparks.com/              #
# storm cloud image from http://www.clker.com              #
############################################################

import random, os, glob, copy
from Tkinter import *

class Animation(object):
    # Override these methods when creating your own animation
    def mousePressed(self, event): pass
    def mouseReleased(self, event): pass
    def mouseMoved(self, event): pass
    def keyPressed(self, event): pass 
    def keyReleased(self, event): pass
    def timerFired(self): pass
    def init(self): pass
    def redrawAll(self): pass
    
    # Call app.run(width,height) to get your app started
    def run(self, width=800, height=600):
        # create the root and the canvas
        root = Tk()
        root.title("Crappy Bird")
        root.resizable(width=FALSE, height=FALSE)
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.data = { }
        self.canvas.pack()
        # set up events
        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.redrawAll()
        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()
        def mouseReleasedWrapper(event):
            self.mouseReleased(event)
            redrawAllWrapper()
        def mouseMovedWrapper(event):
            self.mouseMoved(event)
            redrawAllWrapper()
        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()
        def keyReleasedWrapper(event):
            self.keyReleased(event)
            redrawAllWrapper()
        root.bind("<Button-1>", mousePressedWrapper)
        root.bind("<B1-ButtonRelease>", mouseReleasedWrapper)
        root.bind("<B1-Motion>", mouseMovedWrapper)
        root.bind("<KeyPress>", keyPressedWrapper)
        root.bind('<KeyRelease>',keyReleasedWrapper)
        # set up timerFired events
        self.timerFiredDelay = 10 # milliseconds
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            # pause, then call timerFired again
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)
        # init and get timerFired running
        self.init()
        timerFiredWrapper()
        # and launch the app
        root.mainloop() 


########################
# main animation class #
########################

class playGame(Animation):

    def initPlaySpecs(self):
        self.targetSpecList = []
        self.obstacleSpecList = []
        self.powerupSpecList = []
        self.crapInstanceList = []
        self.targetInstanceList = []
        self.obstacleInstanceList = []
        self.powerupInstanceList = []
        # only the list of levles, etc
        # regular init should include all the 
        # stuff for each level, which changes

    def makeEditorOptionsList(self):
        targets = ["car", "human", "birdhouseTree"]
        obstacles = ["hawk", "tree", "cloud", "stormCloud"]
        powerups = ["worm"]
        self.editorOptionsList = [ ('car', '800'),
                                   ('human', '1100'),
                                   ('hawk', '1700', '200'),
                                   ('tree', '500', 'None'),
                                   ('cloud', '700', '100'),
                                   ('stormCloud', '900', '300') ]
        for index in xrange(len(self.editorOptionsList)):
            if self.editorOptionsList[index][0] in targets:
                self.editorOptionsList[index] = \
                OptionsTarget(self.editorOptionsList[index], index)
            elif self.editorOptionsList[index][0] in obstacles:
                self.editorOptionsList[index] = \
                OptionsObstacle(self.editorOptionsList[index], index)
            elif self.editorOptionsList[index][0] in [powerups]:
                self.editorOptionsList[index] = \
                OptionsPowerup(self.editorOptionsList[index], index)

    def loadFromFile(self, levelFile):
        targets = ["car", "human", "birdhouseTree"]
        obstacles = ["hawk", "tree", "cloud", "stormCloud"]
        powerups = ["worm"]
        for line in levelFile:
            currentLine = line.split()
            if "#" in line:
                pass
            elif currentLine[currentLine.index("type:")+1] == "background":
                self.backgroundColor = \
                currentLine[currentLine.index("type:")+1]
            elif currentLine[currentLine.index("type:")+1][:-1] in targets:
                targetType = currentLine[currentLine.index("type:")+1][:-1]
                targetLocation = currentLine[currentLine.index("location:")+1]
                self.targetSpecList.append((targetType, targetLocation))
            elif currentLine[currentLine.index("type:")+1][:-1] in obstacles:
                obstacleType = currentLine[currentLine.index("type:")+1][:-1]
                obstacleLocation = \
                currentLine[currentLine.index("location:")+1][:-1]
                obstacleHeight = currentLine[currentLine.index("height:")+1]
                self.obstacleSpecList.append((obstacleType, 
                    obstacleLocation, obstacleHeight))
            elif currentLine[currentLine.index("type:")+1][:-1] in powerups:
                powerupType = currentLine[currentLine.index("type:")+1][:-1]
                powerupLocation = \
                currentLine[currentLine.index("location:")+1][:-1]
                powerupHeight = currentLine[currentLine.index("height:")+1]
                self.powerupSpecList.append((powerupType, 
                    powerupLocation, powerupHeight))

    def saveLevel(self):
        play.levelList = glob.glob(os.getcwd()+"/levels/level*.txt")
        levelFile = open(self.levelList[self.currentLevel-1], "w")
        levelFile.write("type: background, color: grey\n")
        for target in self.targetInstanceList:
            location = (target.xValuePlacement-play.editingLevelScreen.left) \
            * 3000.0 / (1.0*play.editingLevelScreen.width)
            levelFile.write("type: " + target.type + ", location: " \
                + str(location) + "\n")
        for obstacle in self.obstacleInstanceList:
            location = (obstacle.xValuePlacement-play.editingLevelScreen.left) \
            * 3000.0 / play.editingLevelScreen.width
            height = (obstacle.yValuePlacement-play.editingLevelScreen.top) \
            * play.height / (1.0*play.editingLevelScreen.height)
            levelFile.write("type: " + obstacle.type + ", location: " + \
                str(location) + ", height: " + str(height) + "\n")
        for powerup in self.powerupInstanceList:
            location = (target.xValuePlacement-play.editingLevelScreen.left) \
            * 3000.0 / play.editingLevelScreen.width
            height = (powerup.yValuePlacement-play.editingLevelScreen.top) \
            * play.height / (1.0*play.editingLevelScreen.height)
            levelFile.write("type: " + powerup.type + ", location: " + \
                str(location) + ", height: " + str(height) + "\n")


    def init(self):
        self.currentState = "splashScreen"
        self.fires = 0
        self.displayInstructions = True
        self.displaySplashScreen = True
        self.padding = 2
        self.background = Background(self.width, self.height)
        self.backButton = BackButton()
        self.logo = Logo()
        self.crapHit = False
        self.score = Score()
        self.movementIncrease = 2
        self.addTiming = 200
        self.initImages()
        self.initSmallImages()
        self.makeEditorOptionsList()
        self.endLevelScreen = EndLevelScreen()
        self.splashScreen = SplashScreen()
        self.editorScreen = MainEditorScreen()
        self.editingLevelScreen = EditingLevelScreen()
        self.mouseHeld = False

    def initImages(self):
        self.crapImage = PhotoImage(file="images/crap.gif")
        self.canvas.data["crapImage"] = self.crapImage
        self.humanImage = PhotoImage(file="images/human.gif")
        self.canvas.data["humanImage"] = self.humanImage
        self.carImage = PhotoImage(file="images/car.gif")
        self.canvas.data["carImage"] = self.carImage
        self.treeImage = PhotoImage(file="images/tree.gif")
        self.canvas.data["treeImage"] = self.treeImage
        self.logoImage = PhotoImage(file="images/logo.gif")
        self.canvas.data["logoImage"] = self.logoImage
        self.birdhouseTreeImage = PhotoImage(file="images/birdhouse-tree.gif")
        self.canvas.data["birdhouseTreeImage"] = self.birdhouseTreeImage
        self.hawkImage = PhotoImage(file="images/hawk.gif")
        self.canvas.data["hawkImage"] = self.hawkImage
        self.cloudImage = PhotoImage(file="images/cloud.gif")
        self.canvas.data["cloudImage"] = self.cloudImage
        self.stormCloudImage = PhotoImage(file="images/stormCloud.gif")
        self.canvas.data["stormCloudImage"] = self.stormCloudImage

    def initSmallImages(self):
        self.hawkImageSmall = PhotoImage(file="images/hawkSmall.gif")
        self.canvas.data["hawkImageSmall"] = self.hawkImageSmall
        self.cloudImageSmall = PhotoImage(file="images/cloudSmall.gif")
        self.canvas.data["cloudImageSmall"] = self.cloudImageSmall
        self.carImageSmall = PhotoImage(file="images/carSmall.gif")
        self.canvas.data["carImageSmall"] = self.carImageSmall
        self.humanImageSmall = PhotoImage(file="images/humanSmall.gif")
        self.canvas.data["humanImageSmall"] = self.humanImageSmall
        self.treeImageSmall = PhotoImage(file="images/treeSmall.gif")
        self.canvas.data["treeImageSmall"] = self.treeImageSmall
        self.birdhouseTreeImageSmall = \
        PhotoImage(file="images/birdhouse-treeSmall.gif")
        self.canvas.data["birdhouseTreeImageSmall"] = \
        self.birdhouseTreeImageSmall
        self.stormCloudImageSmall = \
        PhotoImage(file="images/stormCloudSmall.gif")
        self.canvas.data["stormCloudImageSmall"] = self.stormCloudImageSmall


    def timerFired(self):
        if self.currentState == "playingLevel":
            for target in self.targetInstanceList:
                target.xValuePlacement -= self.movementIncrease
                target.left -= self.movementIncrease
                target.right -= self.movementIncrease
            for obstacle in self.obstacleInstanceList:
                obstacle.xValuePlacement -= self.movementIncrease
                obstacle.left -= self.movementIncrease
                obstacle.right -= self.movementIncrease
            for crapIndex in xrange(len(self.crapInstanceList)):
                if self.crapInstanceList[crapIndex] != None:
                    self.crapInstanceList[crapIndex].checkForCollisions()
                    if self.crapInstanceList[crapIndex].bottom < \
                    play.height and self.crapInstanceList[crapIndex].onObject \
                    == False:
                        self.crapInstanceList[crapIndex].speed *= 1.05
                        self.crapInstanceList[crapIndex].top += \
                        self.crapInstanceList[crapIndex].speed
                        self.crapInstanceList[crapIndex].bottom += \
                        self.crapInstanceList[crapIndex].speed
                        self.crapInstanceList[crapIndex].left -= \
                        self.movementIncrease
                        self.crapInstanceList[crapIndex].right -= \
                        self.movementIncrease
                    elif self.crapInstanceList[crapIndex].bottom < \
                    play.height and \
                    self.crapInstanceList[crapIndex].onObject == True:
                        self.crapInstanceList[crapIndex].top -= \
                        self.crapInstanceList[crapIndex].speed
                        self.crapInstanceList[crapIndex].bottom -= \
                        self.crapInstanceList[crapIndex].speed
                        self.crapInstanceList[crapIndex].speed = 0
                        self.crapInstanceList[crapIndex].left -= \
                        self.movementIncrease
                        self.crapInstanceList[crapIndex].right -= \
                        self.movementIncrease
                    else:
                        self.crapInstanceList[crapIndex].bottom = play.height
                        self.crapInstanceList[crapIndex].left -= \
                        self.movementIncrease
                        self.crapInstanceList[crapIndex].right -= \
                        self.movementIncrease
                        self.crapInstanceList[crapIndex].top = \
                        play.height - self.crapInstanceList[crapIndex].height
                        self.crapInstanceList[crapIndex].onGround = True
                    if self.crapInstanceList[crapIndex].onGround == True:
                        self.crapInstanceList[crapIndex].timeOnGround += 1
                    if self.crapInstanceList[crapIndex].timeOnGround == 100:
                         self.crapInstanceList[crapIndex] = None
            self.fires += 1
            if self.fires % 500 == 0:
                self.addTiming -= 20
            self.deleteOffScreenObjects()
            self.player.checkForCollisions()
        self.redrawAll()

    def makeObjectInstances(self):
        for eachTargetSpec in self.targetSpecList:
            self.targetInstanceList += [Target(eachTargetSpec)]
        for eachObstacleSpec in self.obstacleSpecList:
            self.obstacleInstanceList += [Obstacle(eachObstacleSpec)]

    def makeObjectInstancesForEditing(self):
        for eachTargetSpec in self.targetSpecList:
            self.targetInstanceList += [EditorTarget(eachTargetSpec)]
        for eachObstacleSpec in self.obstacleSpecList:
            self.obstacleInstanceList += [EditorObstacle(eachObstacleSpec)]

    def deleteOffScreenObjects(self):
        if len(self.targetInstanceList) > 0:
            if self.targetInstanceList[0].right < 0:
                self.targetInstanceList = self.targetInstanceList[1:]
        if len(self.obstacleInstanceList) > 0:
            if self.obstacleInstanceList[0].right < 0:
                self.obstacleInstanceList = self.obstacleInstanceList[1:]
    
    def mousePressed(self, event):
        if self.currentState == "splashScreen":
            if self.splashScreen.levelButton.left < event.x < \
            self.splashScreen.levelButton.right and \
            self.splashScreen.levelButton.top < event.y < \
            self.splashScreen.levelButton.bottom:
                self.levelScreen = LevelScreen()
                self.currentState = "levelScreen"
            elif self.splashScreen.editorButton.left < event.x < \
            self.splashScreen.editorButton.right and \
            self.splashScreen.editorButton.top < event.y < \
            self.splashScreen.editorButton.bottom:
                self.currentState = "editorScreen"
        elif self.currentState == "levelScreen":
            if play.backButton.left < event.x < play.backButton.right and \
            play.backButton.top < event.y < play.backButton.bottom:
                self.currentState = "splashScreen"
            for levelIndex in xrange(len(self.levelList)):
                if self.levelList[levelIndex].left < event.x < \
                self.levelList[levelIndex].right and \
                self.levelList[levelIndex].top < event.y < \
                self.levelList[levelIndex].bottom:
                    self.currentState = "startingLevel"
                    self.initPlaySpecs()
                    self.loadFromFile(self.levelList[levelIndex].levelFile)
                    self.makeObjectInstances()
        elif self.currentState == "editorScreen":
            if play.backButton.left < event.x < play.backButton.right and \
            play.backButton.top < event.y < play.backButton.bottom:
                self.currentState = "splashScreen"
            for levelIndex in xrange(len(self.levelList)):
                if self.levelList[levelIndex].left < event.x < \
                self.levelList[levelIndex].right and \
                self.levelList[levelIndex].top < event.y < \
                self.levelList[levelIndex].bottom:
                    self.currentState = "editingLevel"
                    self.currentLevel = levelIndex+1
                    self.initPlaySpecs()
                    self.loadFromFile(self.levelList[levelIndex].levelFile)
                    self.makeObjectInstancesForEditing()
        elif self.currentState == "editingLevel":
            if play.backButton.left < event.x < play.backButton.right and \
            play.backButton.top < event.y < play.backButton.bottom:
                self.currentState = "editorScreen"
            elif self.mouseHeld == False:
                for target in self.targetInstanceList:  
                    if target.left < event.x < target.right and target.top < \
                    event.y < target.bottom:
                        self.currentMover = target
                        self.mouseHeld = True
                for obstacle in self.obstacleInstanceList:
                    if obstacle.left < event.x < obstacle.right and \
                    obstacle.top < event.y < obstacle.bottom:
                        self.currentMover = obstacle
                        self.mouseHeld = True
                for item in self.editorOptionsList:
                    if item.left < event.x < item.right and item.top < \
                    event.y < item.bottom:
                        if type(item) == OptionsTarget:
                            self.currentMover = EditorTarget((item.type, 
                                item.xValuePlacement))
                            self.targetInstanceList += [self.currentMover]
                            self.mouseHeld = True
                        elif type(item) == OptionsObstacle:
                            self.currentMover = EditorObstacle((item.type, 
                                item.xValuePlacement, item.yValuePlacement))
                            self.obstacleInstanceList += [self.currentMover]
                            self.mouseHeld = True
                        elif type(item) == OptionsPowerup:
                            self.currentMover = EditorPowerup((item.type, 
                                item.xValuePlacement))
                            self.powerupInstanceList += [self.currentMover]
                            self.mouseHeld = True
                if self.editingLevelScreen.saveButton.left < event.x < \
                self.editingLevelScreen.saveButton.right and \
                self.editingLevelScreen.saveButton.top < event.y < \
                self.editingLevelScreen.saveButton.bottom:
                    self.saveLevel()
                    self.currentState = "editorScreen"
        elif self.currentState == "levelLost":
            if play.backButton.left < event.x < play.backButton.right and \
            play.backButton.top < event.y < play.backButton.bottom:
                self.currentState = "levelScreen"
        elif self.currentState == "levelFinished":
            if play.endLevelScreen.backToLevelsButton.left < event.x < \
            play.endLevelScreen.backToLevelsButton.right and \
            play.endLevelScreen.backToLevelsButton.top < event.y < \
            play.endLevelScreen.backToLevelsButton.bottom:
                self.currentState = "levelScreen"

    def mouseReleased(self, event):
        if self.currentState == "editingLevel" and self.mouseHeld == True:
            if self.editingLevelScreen.deleteSpace.left < event.x < \
            self.editingLevelScreen.deleteSpace.right and \
            self.editingLevelScreen.deleteSpace.top < event.y < \
            self.editingLevelScreen.deleteSpace.bottom and \
            self.currentMover.type != "birdhouseTree":
                if type(self.currentMover) == EditorTarget:
                    self.targetInstanceList.remove(self.currentMover)
                elif type(self.currentMover) == EditorObstacle:
                    self.obstacleInstanceList.remove(self.currentMover)
                elif type(self.currentMover) == EditorPowerup:
                    self.powerupInstanceList.remove(self.currentMover)
                self.currentMover = None
                self.mouseHeld = False
                return
            if type(self.currentMover) == EditorTarget or \
            self.currentMover.type == "tree":
                self.currentMover.yValuePlacement = \
                self.editingLevelScreen.bottom
                self.currentMover.bottom = self.currentMover.yValuePlacement
                self.currentMover.top = self.currentMover.bottom - \
                2*self.currentMover.height
            if self.currentMover.type == "birdhouseTree":
                self.currentMover.xValuePlacement = \
                play.editingLevelScreen.right
                self.currentMover.left = self.currentMover.xValuePlacement - \
                self.currentMover.width
                self.currentMover.right = self.currentMover.xValuePlacement + \
                self.currentMover.width
            self.currentMover = None
            self.mouseHeld = False

    def mouseMoved(self, event):
        if self.currentState == "editingLevel" and self.mouseHeld == True:
            self.currentMover.xValuePlacement = event.x
            self.currentMover.yValuePlacement = event.y
            self.currentMover.left = event.x - self.currentMover.width
            self.currentMover.right = event.x + self.currentMover.width
            self.currentMover.top = event.y - 2*self.currentMover.height
            self.currentMover.bottom = event.y
            play.redrawAll()

    def keyPressed(self, event):
        if self.currentState == "startingLevel":
            if event.keysym == "space":
                self.currentState = "playingLevel"
                self.player = Bird(self.width, self.height)
        elif self.currentState == "playingLevel":
            if event.keysym == "Left":
                self.player.movingLeft = True
            elif event.keysym == "Right":
                self.player.movingRight = True
            elif event.keysym == "Up":
                self.player.movingUp = True
            elif event.keysym == "Down":
                self.player.movingDown = True
            elif event.keysym == "space":
                self.fireCrap()
            elif event.keysym == "h":
                self.displayInstructions = not self.displayInstructions

    def keyReleased(self, event):
        if self.currentState == "playingLevel":
            if event.keysym == "Left":
                self.player.movingLeft = False
            elif event.keysym == "Right":
                self.player.movingRight = False
            elif event.keysym == "Up":
                self.player.movingUp = False
            elif event.keysym == "Down":
                self.player.movingDown = False
    
    def fireCrap(self):
        self.crapInstanceList += [Crap()]

    def redrawAll(self):
        self.background.draw()
        if self.currentState == "splashScreen":
            self.splashScreen.draw()
        elif self.currentState == "levelScreen":
            self.levelScreen.draw()
        elif self.currentState == "playingLevel":
            for targetIndex in xrange(len(self.targetInstanceList)):
                self.targetInstanceList[targetIndex].draw()
            for obstacleIndex in xrange(len(self.obstacleInstanceList)):
                self.obstacleInstanceList[obstacleIndex].draw()
            for crap in xrange(len(self.crapInstanceList)):
                if self.crapInstanceList[crap] != None:
                    self.crapInstanceList[crap].draw()
            self.player.draw()
            self.player.moveLeft()
            self.player.moveRight()
            self.player.moveUp()
            self.player.moveDown()
            self.score.draw()
        elif self.currentState == "levelFinished":
            for targetIndex in xrange(len(self.targetInstanceList)):
                self.targetInstanceList[targetIndex].draw()
            for obstacleIndex in xrange(len(self.obstacleInstanceList)):
                self.obstacleInstanceList[obstacleIndex].draw()
            for crap in xrange(len(self.crapInstanceList)):
                if self.crapInstanceList[crap] != None:
                    self.crapInstanceList[crap].draw()
            self.player.draw()
            self.score.draw()
            self.endLevelScreen.draw()
        elif self.currentState == "startingLevel":
            self.score.scoreValue = 0
            self.canvas.create_text(self.width/2, self.height/6, 
                text="Instructions", font=("Helvetica", 30, "bold"), 
                fill="black")
            self.canvas.create_text(self.width/2, self.height/4+40, 
                text="Defecate on cars and humans to gain points.", 
                font=("Helvetica", 15, "bold"), fill="black")
            self.canvas.create_text(self.width/2, self.height/4+60, 
                text="Avoid trees, hawks, and clouds to stay alive.", 
                font=("Helvetica", 15, "bold"), fill="black")
            self.canvas.create_text(self.width/2, self.height/4+80, 
                text="", 
                font=("Helvetica", 15, "bold"), fill="black")
            self.canvas.create_text(self.width/2, self.height/4+150, 
                text="Press the spacebar to begin, and also to defecate.", 
                font=("Helvetica", 15, "bold"), fill="black")
        elif self.currentState == "levelLost":
            self.canvas.create_rectangle(self.width/3, 5*self.height/11, 
                2*self.width/3, 6*self.height/11, fill="red")
            self.canvas.create_text(self.width/2, self.height/2, 
                text="You lose.", 
                font=("Helvetica", 30, "bold"), fill="black")
            self.backButton.draw()
        elif self.currentState == "editorScreen":
            self.editorScreen.draw()
        elif self.currentState == "editingLevel":
            self.editingLevelScreen.draw(self.currentLevel)
            for targetIndex in xrange(len(self.targetInstanceList)):
                self.targetInstanceList[targetIndex].draw()
            for obstacleIndex in xrange(len(self.obstacleInstanceList)):
                self.obstacleInstanceList[obstacleIndex].draw()

####################
# Background class #
####################


class Background(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.backgroundColor = "light blue"

    def draw(self):
        play.canvas.create_rectangle(play.padding, play.padding, 
            self.width+play.padding, self.height+play.padding, 
            fill=self.backgroundColor)

class BackButton(object):

    def __init__(self):
        self.left = 0
        self.right = play.width/5
        self.top = 0
        self.bottom = play.height/10
        self.xCenter = (self.left+self.right)/2
        self.yCenter = (self.top+self.bottom)/2

    def draw(self):
        play.canvas.create_rectangle(self.top, self.left, 
            self.right, self.bottom, fill="black")
        play.canvas.create_text(self.xCenter, self.yCenter, 
                text="Back", 
                font=("Helvetica", 20, "bold"), fill="white")

############################
# Level Screen and buttons #
############################

class LevelScreen(object):

    def draw(self):
        play.levelList = glob.glob(os.getcwd()+"/levels/level*.txt")
        for eachLevelIndex in xrange(len(play.levelList)):
            levelFile = open(play.levelList[eachLevelIndex], "r+")
            play.levelList[eachLevelIndex] = LevelButton(levelFile, 
                eachLevelIndex)
        play.logo.draw()
        play.backButton.draw()
        for eachLevelIndex in xrange(len(play.levelList)):
            play.levelList[eachLevelIndex].draw()

class LevelButton(object):

    def __init__(self, levelFile, listIndex):
        self.levelFile = levelFile
        self.text = "Level", listIndex+1
        self.left = ((listIndex%4)*3 + 1) * play.width / 13
        self.right = self.left + 2*play.width/13 
        # 2/13ths of the window width right of the left side of the button
        self.top = ((listIndex/4)*3 + 4) * play.height / 13
        self.bottom = self.top + 2*play.height/13
        self.xCenter = (self.left+self.right)/2
        self.yCenter = (self.top+self.bottom)/2

    def draw(self):
        play.canvas.create_rectangle(self.left, self.top, 
            self.right, self.bottom, fill="grey")
        play.canvas.create_text(self.xCenter, self.yCenter, 
            text=self.text, font=("Helvetica", 20, "bold"), 
            fill="black")

#############################
# Splash screen and buttons #
#############################

class SplashScreen(object):

    def draw(self):
        play.logo.draw()
        self.levelButton = SplashButton()
        self.editorButton = SplashButton()
        self.levelButton.draw("left")
        self.editorButton.draw("right")

class SplashButton(object):

    def draw(self, side):
        if side == "left":
            self.left = play.width/8.0
            self.right = 3*play.width/8.0
            self.buttonText = "Play a Level"
        else:
            self.left = 5*play.width/8.0
            self.right = 7*play.width/8.0
            self.buttonText = "Level Editor"
        self.top = play.height/2.0
        self.bottom = 3*play.height/4.0
        self.xCenter = (self.left+self.right)/2.0
        self.yCenter = (self.top+self.bottom)/2.0
        play.canvas.create_rectangle(self.left, self.top, 
            self.right, self.bottom, fill="grey")
        play.canvas.create_text(self.xCenter, self.yCenter, 
            text=self.buttonText, font=("Helvetica", 15, "bold"), fill="black")

class MainEditorScreen(object):

    def draw(self):
        play.levelList = glob.glob(os.getcwd()+"/levels/level*.txt")
        for eachLevelIndex in xrange(len(play.levelList)):
            levelFile = open(play.levelList[eachLevelIndex], "r+")
            play.levelList[eachLevelIndex] = LevelButton(levelFile, 
                eachLevelIndex)
        play.logo.draw()
        play.backButton.draw()
        for eachLevelIndex in xrange(len(play.levelList)):
            play.levelList[eachLevelIndex].draw()

class EditingLevelScreen(object):

    def __init__(self):
        self.left = play.width/20
        self.right = 19*play.width/20
        self.top = 2*play.height/5
        self.bottom = 17*play.height/20
        self.textCenterX = play.width/2
        self.textCenterY = play.height/20
        self.width = self.right-self.left
        self.height = self.bottom-self.top
        self.deleteSpace = DeleteSpace

    def draw(self, currentLevel):
        self.levelText = "Editing Level %d" % currentLevel
        play.canvas.create_rectangle(self.left, self.top, 
            self.right, self.bottom, fill="red")
        play.canvas.create_text(self.textCenterX, self.textCenterY, 
            text=self.levelText, font=("Helvetica", 30, "bold"), fill="black")
        play.backButton.draw()
        for item in play.editorOptionsList:
            item.draw()
        self.deleteSpace = DeleteSpace()
        self.saveButton = SaveButton()
        self.saveButton.draw()
        self.deleteSpace.draw()


class DeleteSpace(object):

    def __init__(self):
        self.width = play.width/3
        self.height = play.height/10
        self.left = play.width/3
        self.right = 2*play.width/3
        self.top = 35*play.height/40
        self.bottom = 39*play.height/40
        self.textCenterX = play.width/2
        self.textCenterY = 37*play.height/40

    def draw(self):
        play.canvas.create_rectangle(self.left, self.top, self.right, 
            self.bottom, fill="red")
        play.canvas.create_text(self.textCenterX, self.textCenterY, 
            text="Drag here to delete", font=("Helvetica", 20, "bold"), 
            fill="black")

class SaveButton(object):

    def __init__(self):
        self.width = play.width/6
        self.height = play.height/10
        self.left = 19*play.width/24
        self.right = 23*play.width/24
        self.top = 35*play.height/40
        self.bottom = 39*play.height/40
        self.textCenterX = 21*play.width/24
        self.textCenterY = 37*play.height/40

    def draw(self):
        play.canvas.create_rectangle(self.left, self.top, self.right, 
            self.bottom, fill="green")
        play.canvas.create_text(self.textCenterX, self.textCenterY, 
            text="Save", font=("Helvetica", 20, "bold"), fill="black")

class EndLevelScreen(object):

    def __init__(self):
        self.width = play.width/3
        self.height = play.height/11
        self.top = play.height/20
        self.bottom = 5*play.height/30
        self.left = play.width/3
        self.right = 2*play.width/3

    def draw(self):
        play.canvas.create_rectangle(self.left, self.top, self.right, 
            self.bottom, fill="green")
        play.canvas.create_text(play.width/2, play.height/10, 
            text="You win!", font=("Helvetica", 32, "bold"), 
            fill="black")
        self.backToLevelsButton = BackToLevelsButton()
        self.backToLevelsButton.draw()


class BackToLevelsButton(object):

    def __init__(self):
        self.left = play.width/3
        self.right = 2*play.width/3
        self.top = 2*play.height/8
        self.bottom = 4*play.height/8

    def draw(self):
        play.canvas.create_rectangle(self.left, self.top, self.right, 
            self.bottom, fill="green")
        play.canvas.create_text(play.width/2, 3*play.height/8-15, 
            text="Back to", font=("Helvetica", 25, "bold"), 
            fill="black")
        play.canvas.create_text(play.width/2, 3*play.height/8+15, 
            text="Levels", font=("Helvetica", 25, "bold"), 
            fill="black")



########
# Logo #
########


class Logo(object):

    def __init__(self):
        width = play.width
        height = play.height
        self.left = width/4
        self.right = 3*width/4
        self.top = height/10
        self.bottom = height/5
        self.xCenter = (self.left+self.right)/2
        self.yCenter = (self.top+self.bottom)/2

    def draw(self):
        image = play.canvas.data["logoImage"]
        imageSize = ( (image.width(), image.height()) )
        play.canvas.create_image((self.left+self.right)/2, 
            (self.top+self.bottom)/2, anchor=CENTER, image=image)

#######################
# Actual Game objects #
#######################

class Bird(object):

    def __init__(self, width, height):
        self.birdRadius = 15
        self.birdCenterX = width/6
        self.birdCenterY = height/6
        self.birdTop = self.birdCenterY - self.birdRadius
        self.birdBottom = self.birdCenterY + self.birdRadius
        self.birdLeft = self.birdCenterX - self.birdRadius
        self.birdRight = self.birdCenterX + self.birdRadius
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.leftSpeed = 0.1
        self.rightSpeed = 0.1
        self.upSpeed = 0.1
        self.downSpeed = 0.1
        birdImage = PhotoImage(file="images/flappy-bird.gif")
        play.canvas.data["birdImage"] = birdImage

    def draw(self):
        image = play.canvas.data["birdImage"]
        imageSize = ( (image.width(), image.height()) )
        play.canvas.create_image((
            self.birdLeft+play.padding+self.birdRight+play.padding)/2, 
        (self.birdTop+self.birdBottom)/2, anchor=CENTER, image=image)

    def moveLeft(self):
        if self.movingLeft == True and self.birdLeft > play.padding and \
        play.currentState == "playingLevel":
            if self.leftSpeed <= 1.8: self.leftSpeed *= 1.025
            self.birdLeft -= self.leftSpeed
            self.birdRight -= self.leftSpeed
        elif self.movingLeft == False and self.leftSpeed > 0.1 and \
        self.birdLeft > play.padding and play.currentState == "playingLevel":
            self.leftSpeed /= 1.025
            self.birdLeft -= self.leftSpeed
            self.birdRight -= self.leftSpeed

    def moveRight(self):
        if self.movingRight == True and self.birdRight < \
        play.width-play.padding and play.currentState == "playingLevel":
            if self.rightSpeed <= 1.8: self.rightSpeed *= 1.025
            self.birdLeft += self.rightSpeed
            self.birdRight += self.rightSpeed
        elif self.movingRight == False and self.rightSpeed > 0.1 and \
        self.birdRight < play.width-play.padding and \
        play.currentState == "playingLevel":
            self.rightSpeed /= 1.025
            self.birdLeft += self.rightSpeed
            self.birdRight += self.rightSpeed

    def moveUp(self):
        if self.movingUp == True and self.birdTop > 0 and \
        play.currentState == "playingLevel":
            if self.upSpeed <= 1.8: self.upSpeed *= 1.025
            self.birdTop -= self.upSpeed
            self.birdBottom -= self.upSpeed
        elif self.movingUp == False and self.upSpeed > 0.1 and \
        self.birdTop > 0 and play.currentState == "playingLevel":
            self.upSpeed /= 1.025
            self.birdTop -= self.upSpeed
            self.birdBottom -= self.upSpeed

    def moveDown(self):
        if self.movingDown == True and self.birdBottom < (3*play.height/4) \
        and play.currentState == "playingLevel":
            if self.downSpeed <= 1.8: self.downSpeed *= 1.025
            self.birdTop += self.downSpeed
            self.birdBottom += self.downSpeed
        if self.movingDown == False and self.downSpeed > 0.1 and \
        self.birdBottom < play.height and play.currentState == "playingLevel":
            self.downSpeed /= 1.025
            self.birdTop += self.downSpeed
            self.birdBottom += self.downSpeed

    def checkForCollisions(self):
        if len(play.obstacleInstanceList) > 0:
            for obstacle in play.obstacleInstanceList:
                if (obstacle.left < self.birdLeft < obstacle.right or \
                    obstacle.left < self.birdRight < obstacle.right) and \
                (obstacle.top < self.birdTop < obstacle.bottom or \
                    obstacle.top < self.birdBottom < obstacle.bottom):
                    play.currentState = "levelLost"
        for target in play.targetInstanceList:
            if target.type == "birdhouseTree" and (target.left < \
                self.birdLeft < target.right or target.left < \
                self.birdRight < target.right):
                play.currentState = "levelFinished"

class Target(object):
    
    def __init__(self, spec):
        self.type = spec[0]
        self.image = play.canvas.data[self.type+"Image"]
        self.imageSize = ( (self.image.width(), self.image.height()) )
        self.width = self.imageSize[0]/2
        self.height = self.imageSize[1]/2
        self.xValuePlacement = int(float(spec[1]))
        self.yValuePlacement = play.height
        self.left = self.xValuePlacement - self.width
        self.right = self.xValuePlacement + self.width
        self.top = self.yValuePlacement - 2*self.height
        self.bottom = self.yValuePlacement
        if self.type == "human":
            self.left += self.width/3
            self.right -= self.width/4
            self.top += self.height/4
            self.bottom -= self.height/4
        if self.type == "car":
            self.top += self.height/3
            self.left += self.width/4
            self.right -= self.width/4
        self.isHit = False
        self.timeHit = 0
        
    def draw(self):
        if self.right > -20 and self.left < play.width+20:
            play.canvas.create_image(self.xValuePlacement, 
                self.yValuePlacement-self.height, anchor=CENTER, 
                image=self.image)

class EditorTarget(Target):

    def __init__(self, spec):
        super(EditorTarget, self).__init__(spec)
        self.image = play.canvas.data[self.type+"ImageSmall"]
        self.imageSize = ( (self.image.width(), self.image.height()) )
        self.width = self.imageSize[0]/2
        self.height = self.imageSize[1]/2
        self.xValuePlacement = play.editingLevelScreen.left + \
        self.xValuePlacement * (play.editingLevelScreen.width/3000.0)
        self.yValuePlacement = play.editingLevelScreen.top + \
        self.yValuePlacement * (1.0*play.editingLevelScreen.height/play.height)
        self.left = self.xValuePlacement - self.width
        self.right = self.xValuePlacement + self.width
        self.top = self.yValuePlacement - 2*self.height
        self.bottom = self.yValuePlacement

class OptionsTarget(EditorTarget):

    def __init__(self, spec, index):
        super(EditorTarget, self).__init__(spec)
        self.image = play.canvas.data[self.type+"ImageSmall"]
        self.imageSize = ( (self.image.width(), self.image.height()) )
        self.width = self.imageSize[0]/2
        self.height = self.imageSize[1]/2
        self.xValuePlacement = (index+1) * play.width/7
        self.yValuePlacement = 17*play.height/48
        self.left = self.xValuePlacement - self.width
        self.right = self.xValuePlacement + self.width
        self.top = self.yValuePlacement - 2*self.height
        self.bottom = self.yValuePlacement

class Obstacle(object):
    
    def __init__(self, spec):
        self.type = spec[0]
        self.image = play.canvas.data[self.type+"Image"]
        self.imageSize = ( (self.image.width(), self.image.height()) )
        self.xValuePlacement = int(float(spec[1]))
        if spec[2] == "None":
            self.yValuePlacement = play.height
        else:
            self.yValuePlacement = int(float(spec[2]))
        self.width = self.imageSize[0]/2
        self.height = self.imageSize[1]/2
        self.left = self.xValuePlacement - self.width
        self.right = self.xValuePlacement + self.width
        self.top = self.yValuePlacement - 2*self.height
        self.bottom = self.yValuePlacement
        if self.type == "hawk":
            self.top += self.height/2
            self.bottom -= self.height/6
            self.left += self.width/6
            self.right -= self.width/6
        elif self.type == "tree":
            self.top += self.height/4
            self.left += self.width/3
            self.right -= self.width/3
        elif self.type == "stormCloud":
            self.bottom -= 7*self.height/12
        elif self.type == "cloud":
            self.top += self.width/4
        self.isHit = False
        self.timeHit = 0
        
    def draw(self):
        if self.right > -20 and self.left < play.width+20:
            play.canvas.create_image(self.xValuePlacement, 
                self.yValuePlacement-self.height, anchor=CENTER, 
                image=self.image)

class EditorObstacle(Obstacle):

    def __init__(self, spec):
        super(EditorObstacle, self).__init__(spec)
        self.image = play.canvas.data[self.type+"ImageSmall"]
        self.imageSize = ( (self.image.width(), self.image.height()) )
        self.width = self.imageSize[0]/2
        self.height = self.imageSize[1]/2
        self.xValuePlacement = play.editingLevelScreen.left + \
        self.xValuePlacement * (play.editingLevelScreen.width/3000.0)
        self.yValuePlacement = play.editingLevelScreen.top + \
        self.yValuePlacement * (1.0*play.editingLevelScreen.height/play.height)
        self.left = self.xValuePlacement - self.width
        self.right = self.xValuePlacement + self.width
        self.top = self.yValuePlacement - 2*self.height
        self.bottom = self.yValuePlacement

class OptionsObstacle(EditorObstacle):

    def __init__(self, spec, index):
        super(EditorObstacle, self).__init__(spec)
        self.image = play.canvas.data[self.type+"ImageSmall"]
        self.imageSize = ( (self.image.width(), self.image.height()) )
        self.width = self.imageSize[0]/2
        self.height = self.imageSize[1]/2
        self.xValuePlacement = (index+1) * play.width/7
        self.yValuePlacement = 17*play.height/48
        self.left = self.xValuePlacement - self.width
        self.right = self.xValuePlacement + self.width
        self.top = self.yValuePlacement - 2*self.height
        self.bottom = self.yValuePlacement

class Crap(object):
    
    def __init__(self):
        self.height = self.width = 10
        self.top = play.player.birdTop
        self.left = play.player.birdLeft + play.player.birdRadius - \
        self.width/3
        self.bottom = self.top + self.height
        self.right = self.left + self.width
        self.speed = 1.2
        self.onGround = False
        self.timeOnGround = 0
        self.onObject = False

    def draw(self):
        if self.right > 0 and self.left < play.width:
            image = play.canvas.data["crapImage"]
            imageSize = ( (image.width(), image.height()) )
            play.canvas.create_image((self.left+self.right)/2, 
                (self.top+self.bottom)/2, anchor=CENTER, image=image)

    def checkForCollisions(self):
        if len(play.targetInstanceList) > 0:
            for target in play.targetInstanceList:
                if (target.left < self.left < target.right or \
                    target.left < self.right < target.right) and \
                (target.top < self.top < target.bottom or target.top < \
                    self.bottom < target.bottom):
                    self.onObject = True
                    if target.isHit == False:
                        target.isHit = True
                        play.score.scoreValue += 5
        if len(play.obstacleInstanceList) > 0:
            for obstacle in play.obstacleInstanceList:
                if (obstacle.left < self.left < obstacle.right or \
                    obstacle.left < self.right < obstacle.right) and \
                (obstacle.top < self.top < obstacle.bottom or obstacle.top \
                    < self.bottom < obstacle.bottom):
                    obstacle.isHit = True
                    self.onObject = True

class Score(object):

    def __init__(self):
        self.scoreValue = 0
        self.left = 0
        self.right = play.width/5
        self.top = 0
        self.bottom = play.height/10
        self.xCenter = play.width/12
        self.yCenter = play.height/20

    def draw(self):
        self.scoreText = "Score: %d" % self.scoreValue
        play.canvas.create_rectangle(self.left, self.top, self.right, 
            self.bottom, fill="white")
        play.canvas.create_text(self.xCenter, self.yCenter, 
            text=self.scoreText, font=("Helvetica", 15, "bold"), fill="black")

###########################################
# Run Game
###########################################

play = playGame()
play.run(600, 400)

