from numpy import floor, trunc
import math

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
                if("ultra" in tyreName):
                        image =  "ultra.png"
                elif("super" in tyreName):
                        image = "super.png"
                elif("soft" in tyreName):
                        image = "soft.png"
                elif("medium" in tyreName):
                        image = "medium.png"
                elif("hard" in tyreName):
                        image = "hard.png"
                elif("hyper" in tyreName):
                        image = "hyper.png"
                else:
                        image = "soft 2019.png"
        return "assets/tyres/" + image