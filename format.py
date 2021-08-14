from numpy import floor, trunc
import math
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import settings

def formatTimeLarge(timeString):
        if(float(timeString)<1):
                timeLarge = str("00")
        elif(float(timeString)>1 and float(timeString)<60):
                timeMin = ""
                timeSec = str(math.trunc(float(timeString))).zfill(2)
                timeLarge = timeSec
        elif(float(timeString)>=60):
                timeMin = math.trunc(float(timeString)/60)
                timeSec = str(math.trunc(float(timeString) - timeMin*60)).zfill(2)
                timeLarge = str(timeMin) + ":" + timeSec
        else:
                timeLarge = "problem: " + timeString
        return timeLarge

def ERSChargeHeight(charge):
        return 80 + 282*charge

def getTyreName(tyreString):
        split = str(tyreString).split(":")
        tyreName = split[1].lower()
        if("c" in tyreName):
                if("4" in tyreName):
                        image = "medium 2019.png"
                elif("5" in tyreName):
                        image = "hard.png"
                else:
                        image = "soft 2019.png"
        else:
                
                if("soft" in tyreName):
                        if("ultra" in tyreName):
                                image =  "ultra.png"
                        elif("super" in tyreName):
                                image = "super.png"
                        elif("hyper" in tyreName):
                                image = "hyper.png"
                        else:
                                image = "soft.png"
                elif("medium" in tyreName):
                        image = "medium.png"
                elif("hard" in tyreName):
                        image = "hard.png"
                else:
                        image = "soft 2019.png"
        return "assets/tyres/" + image

trackMapSize = 400
def generateTrackMap(carPosX, carPosY, backgroundColour, frameH, frameW):
        backgroundColour = (0, 0, 0)
        image = Image.new('RGBA', (frameW, frameH))
        draw = ImageDraw.Draw(image)
        maxValue = max(max(carPosX),max(carPosY))
        carPosX = frameW - trackMapSize*6/12 - np.multiply(carPosX,trackMapSize/(2*maxValue))
        carPosY = frameH/2 + np.multiply(carPosY,trackMapSize/(2*maxValue))
        radius = 5.0
        for p in range(0, len(carPosX)):
                draw.ellipse((round(carPosX[p]-radius), round(carPosY[p]-radius), round(carPosX[p]+radius), round(carPosY[p]+radius)), fill=backgroundColour)
        image.save('assets/trackmaps/'+ settings.currentFileName +'.png', "PNG")
        return maxValue

def carCoordOnTrackMap(carPosX, carPosY, frameH, frameW, maxValue):
        carCoordX = frameW - (trackMapSize*6/12) - carPosX*trackMapSize/(2*maxValue)
        carCoordY = frameH/2 + carPosY*trackMapSize/(2*maxValue)
        return carCoordX, carCoordY