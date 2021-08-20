import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from PIL import ImageFont, ImageDraw, Image
from docFormatter import *
from format import *
from functions import *
import settings
import streamlit as st

def makeF1(fullArray):
        progess = st.progress(0)
        # Define user Inputs
        driverName = settings.driverName

        # Define Arrays
        npFullArray = np.array(fullArray)
        sampleRate = npFullArray[8][1]
        lapTime = npFullArray[9][1]
        tire = getTyreName(npFullArray[5][1])
        npFullArray = npFullArray[18:,:]
        timeArr = np.transpose(npFullArray[:,0])
        deltaArr = np.transpose(npFullArray[:,16]).astype(np.float64)
        brakePosArr = np.transpose(npFullArray[:,19]).astype(np.float64)
        lateralGArr = np.transpose(npFullArray[:,24]).astype(np.float64)
        longiGArr = np.transpose(npFullArray[:,25]).astype(np.float64)
        carPositionXArr = np.transpose(npFullArray[:,32]).astype(np.float64)
        carPositionYArr = np.transpose(npFullArray[:,33]).astype(np.float64)
        DRSActArr = np.transpose(npFullArray[:,25+26])
        DRSAvailArr = np.transpose(npFullArray[:,2*26])
        RPMArr = np.transpose(npFullArray[:,2*26+9]).astype(np.int64)
        gearArr = np.transpose(npFullArray[:,2*26+12])
        speedArr = np.transpose(npFullArray[:,2*26+13]).astype(np.float64)
        lastSectorArr = np.transpose(npFullArray[:,2*26+25]).astype(np.float64)
        maxRPM = np.float64(npFullArray[2,81])
        throttlePosArr = np.transpose(npFullArray[:,4*26+7]).astype(np.float64)
        steeringAngleArr = np.transpose(npFullArray[:,3*26+25]).astype(np.float64)
        racePositionArr = np.transpose(npFullArray[:,90])
        noFrames = len(timeArr)

        # Calculate ERS
        ERSCharge = np.transpose(npFullArray[:,2*26+16]).astype(np.float64)
        ERSdeployedArr = np.transpose(npFullArray[:,69]).astype(np.float64)
        ERSMax = max(ERSdeployedArr)
        ERSdeployed = np.multiply(ERSdeployedArr, 1/ERSMax)

        # Define tempStores
        lastSectorPrev = lastSectorArr[0]
        sectorImprovementArr = []
        sectorImprovement = 0

        # Define fonts
        fontpath = "assets/fonts/Formula1-Regular.ttf"
        font200 = ImageFont.truetype(fontpath, 200)
        font150 = ImageFont.truetype(fontpath, 150)
        font100 = ImageFont.truetype(fontpath, 100)
        font75 = ImageFont.truetype(fontpath, 75)
        font50 = ImageFont.truetype(fontpath, 50)
        font25 = ImageFont.truetype(fontpath, 25)

        # Define initial frame
        background = cv2.imread("assets/bottomBar/backgroundBlue.png")
        backgroundColour = (0, 0, 255)
        height, width, layers = background.shape

        # Define images
        steeringWheel = Image.open("assets/icons/steeringWheel.png")
        DRSNo = Image.open("assets/icons/DRSNo.png")
        DRSAvail = Image.open("assets/icons/DRSAvail.png")
        DRSActive = Image.open("assets/icons/DRSActive.png")
        sectorGreenImage = Image.open("assets/bottomBar/sectorGreen.png")
        sectorYellowImage = Image.open("assets/bottomBar/sectorYellow.png")
        sectorPurpleImage = Image.open("assets/bottomBar/sectorPurple.png")
        topBar = Image.open("assets/bottomBar/topBar.png")
        bottomBar = Image.open("assets/bottomBar/bottomBar.png")
        barInputs = Image.open("assets/bottomBar/barInputs.png")
        tyreImage = Image.open(tire)
        tyreImage = tyreImage.resize((125, 125))
        teamColour = settings.teamColour

        # Define video output
        FPS = sampleRate
        fourcc = VideoWriter_fourcc(*'MP42')
        video = VideoWriter('./output/'+ settings.currentFileName + '.avi', fourcc, float(FPS), (width, height))

        if (settings.showTrackMap):
                trackMapMax = generateTrackMap(carPositionXArr, carPositionYArr, backgroundColour, height, width)
                trackMapImage = Image.open('assets/trackmaps/'+ settings.currentFileName +'.png')

        for i in range(0, int(FPS)):
                frame = background
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.rectangle((0, 0, width, height), fill=backgroundColour)
                posX = math.trunc(-width + QuadraticEaseOut(i, FPS, width))
                img_pil.paste(topBar, (posX, 0), topBar)
                draw.text((posX+413, 65), racePositionArr[0], font = font75, fill=(0, 0, 0, 0), anchor="mm")
                draw.text((posX+533, 65), driverName, font = font100, fill=(255, 255, 255, 0), anchor="lm")
                draw.text((posX+2250, 65), str(settings.driverNumber), font = font100, fill=teamColour, anchor="mm")
                draw.rectangle((posX + 480, 17, posX + 493, 112), fill=teamColour)
                frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                video.write(frame)
                progess.progess(stProgressBar(i+1, len(timeArr)+2*float(FPS)))

        for i in range(0, int(FPS)):
                frame = background
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.rectangle((0, 0, width, height), fill=backgroundColour)
                posY = math.trunc(-height + QuadraticEaseOut(i, FPS, height))
                img_pil.paste(bottomBar, (0, posY), bottomBar)
                img_pil.paste(topBar, (0, 0), topBar)
                draw.text((413, 65), racePositionArr[0], font = font75, fill=(0, 0, 0, 0), anchor="mm")
                draw.text((533, 65), driverName, font = font100, fill=(255, 255, 255, 0), anchor="lm")
                draw.text((math.trunc(2250-QuadraticEaseOut(i, FPS, 100)), 65), str(settings.driverNumber), font = font100, fill=teamColour, anchor="mm")
                draw.rectangle((480, 17, 493, 112), fill=teamColour)
                tyreImage.putalpha(math.trunc(QuadraticEaseOut(i, FPS, 255)))
                img_pil.paste(tyreImage, (2300, 10), tyreImage)
                if(settings.showTrackMap):
                        #trackMapImage.putalpha(math.trunc(QuadraticEaseOut(i, FPS, 255)))
                        img_pil.paste(trackMapImage, (0, 0), trackMapImage)
                frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                video.write(frame)
                progess.progess(stProgressBar(int(FPS)+i+1, len(timeArr)+2*float(FPS), prefix = 'Progress:', suffix = 'Complete'))

        for i in range(0, noFrames):

                # Setup Frame
                frame = None
                frame = background
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.rectangle((0, 0, width, height), fill=backgroundColour)
                img_pil.paste(bottomBar, (0, 0), bottomBar)
                img_pil.paste(topBar, (0, 0), topBar)
                img_pil.paste(barInputs, (0, 0), barInputs)
                draw.rectangle((480, 17, 493, 112), fill=teamColour)

                # Calculating Time Text
                timeLarge  = formatTimeLarge(timeArr[i])
                timeMil = str(float(timeArr[i]) - math.trunc(float(timeArr[i])))
                draw.text((960, 347), timeMil[1:][:3], font = font150, fill=(255,255,255,0), anchor="lb")
                draw.text((960, 347), timeLarge, font = font200, fill=(255,255,255,0), anchor="rb")

                # Bar Inputs
                draw.rectangle((1421, math.trunc(140+280*(100 - ERSCharge[i])/100), 1444, 140 + 280), fill=(16, 132, 149)) # Inverted colour RGBBGR
                draw.rectangle((1426, math.trunc(140+np.multiply(ERSdeployed[i], 280)), 1447, 140 + 280), fill=(26, 216, 244)) # Inverted colour RGBBGR
                draw.rectangle((1840, math.trunc(140+280*(100 - throttlePosArr[i])/100), 1863, 140 + 280), fill=(0, 188, 0))
                draw.rectangle((1806, math.trunc(140+280*(100 - brakePosArr[i])/100), 1829, 140 + 280), fill=(188, 0, 0)) # Inverted colour RGBBGR

                # GForce
                gForceX = 1602 + math.trunc(140*(lateralGArr[i])/5)
                gForceY = 281 - math.trunc(140*(longiGArr[i]/5))
                draw.ellipse((gForceX-5, gForceY-5, gForceX+5, gForceY+5), fill=(255, 0, 0))

                # Draw Car on TrackMap
                if(settings.showTrackMap):
                        img_pil.paste(trackMapImage, (0, 0), trackMapImage)
                        carCoords = carCoordOnTrackMap(carPositionXArr[i], carPositionYArr[i], height, width, trackMapMax)
                        radius = 7
                        draw.ellipse((round(carCoords[0]-radius), round(carCoords[1]-radius), round(carCoords[0]+radius), round(carCoords[1]+radius)), fill=teamColour)

                # Steering and Inputs
                steeringAngle = -1*steeringAngleArr[i]
                if(steeringAngle<0):
                        steeringAngle = 360 + steeringAngle
                img_pil.paste(steeringWheel.rotate(steeringAngle), (1910, 145), steeringWheel.rotate(steeringAngle))
                if(RPMArr[i] > maxRPM * 0.92):
                        gearColour = (255, 0, 0, 0)
                else:
                        gearColour = (255,255,255,0)
                draw.text((2010, 375), str(math.trunc(speedArr[i])), font = font50, fill=(255,255,255,0), anchor="ms")
                draw.text((2010, 400), "Speed", font = font25, fill=(255,255,255,0), anchor="ms")
                draw.text((2210, 200), "Gear", font = font50, fill=(255,255,255,0), anchor="ms")
                draw.text((2210, 345), gearArr[i], font = font150, fill=gearColour, anchor="ms")

                # DRS
                if(DRSActArr[i]=="1"):
                        img_pil.paste(DRSActive, (2300, 229), DRSActive)
                elif(DRSAvailArr[i]=="1"):
                        img_pil.paste(DRSAvail, (2300, 229), DRSAvail)
                else:
                        img_pil.paste(DRSNo, (2300, 229), DRSNo)


                # Top bar
                draw.text((413, 65), racePositionArr[i], font = font75, fill=(0, 0, 0, 0), anchor="mm")
                draw.text((533, 65), driverName, font = font100, fill=(255, 255, 255, 0), anchor="lm")
                draw.text((2150, 65), str(settings.driverNumber), font = font100, fill=teamColour, anchor="mm")
                img_pil.paste(tyreImage, (2300, 10), tyreImage)

                # Sector Analysis
                if(lastSectorPrev == 0):
                        lastSectorPrev = lastSectorArr[i]
                elif(lastSectorPrev != lastSectorArr[i]):
                        if(deltaArr[i] < sectorImprovement):
                                if(deltaArr[i]<0 and sectorImprovement>0):
                                        sectorImprovementArr.append("sectorPurple")
                                else:
                                        sectorImprovementArr.append("sectorGreen")
                                sectorImprovement = deltaArr[i]
                        else:
                                sectorImprovementArr.append("sectorYellow")
                                sectorImprovement = deltaArr[i]
                        lastSectorPrev = lastSectorArr[i]
        
                for sec in range(0, len(sectorImprovementArr)):
                        posX = 324 + 355*sec
                        posY = 378
                        if(sectorImprovementArr[sec] == "sectorGreen"):
                                img_pil.paste(sectorGreenImage, (posX, posY), sectorGreenImage)
                        elif(sectorImprovementArr[sec] == "sectorYellow"):
                                img_pil.paste(sectorYellowImage, (posX, posY), sectorYellowImage)
                        elif(sectorImprovementArr[sec] == "sectorPurple"):
                                img_pil.paste(sectorPurpleImage, (posX, posY), sectorPurpleImage)

                # Adding Generated Frame to the array
                frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                video.write(frame)
                progess.progess(stProgressBar(2*int(FPS)+i+1, len(timeArr)+2*float(FPS), prefix = 'Progress:', suffix = 'Complete'))
        
        # Setting up final frames for the laptime show
        # Setup Frame
        frame = None
        frame = background
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        draw.rectangle((0, 0, width, height), fill=backgroundColour)
        img_pil.paste(bottomBar, (0, 0), bottomBar)
        img_pil.paste(topBar, (0, 0), topBar)
        draw.rectangle((480, 17, 493, 112), fill=teamColour)

        # Calculating Time Text
        timeLarge  = formatTimeLarge(lapTime)
        timeMil = str(float(lapTime) - math.trunc(float(lapTime)))
        draw.text((960, 347), timeMil[1:][:3], font = font150, fill=(255,255,255,0), anchor="lb")
        draw.text((960, 347), timeLarge, font = font200, fill=(255,255,255,0), anchor="rb")
        draw.text((1425, 347), str(deltaArr[-1]), font = font150, fill=(0,255,0,0), anchor="lb")

        # Top bar
        draw.text((413, 65), racePositionArr[-1], font = font75, fill=(0, 0, 0, 0), anchor="mm")
        draw.text((533, 65), driverName, font = font100, fill=(255, 255, 255, 0), anchor="lm")
        draw.text((2150, 65), str(settings.driverNumber), font = font100, fill=teamColour, anchor="mm")
        img_pil.paste(tyreImage, (2300, 10), tyreImage)

        # Sector Analysis
        if(deltaArr[-1] < sectorImprovement):
                if(deltaArr[-1]<0 and sectorImprovement>0):
                        sectorImprovementArr.append("sectorPurple")
                else:
                        sectorImprovementArr.append("sectorGreen")
        else:
                sectorImprovementArr.append("sectorYellow")

        for sec in range(0, len(sectorImprovementArr)):
                posX = 324 + 355*sec
                posY = 378
                if(sectorImprovementArr[sec] == "sectorGreen"):
                        img_pil.paste(sectorGreenImage, (posX, posY), sectorGreenImage)
                elif(sectorImprovementArr[sec] == "sectorYellow"):
                        img_pil.paste(sectorYellowImage, (posX, posY), sectorYellowImage)
                elif(sectorImprovementArr[sec] == "sectorPurple"):
                        img_pil.paste(sectorPurpleImage, (posX, posY), sectorPurpleImage)

        # Adding Generated Frame to the array
        frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        for i in range(0, int(FPS)*10):
                video.write(frame)

        cv2.destroyAllWindows()
        video.release()
        return "success"

def makeGT(frameRate,timeArr,gearArr,throttleArr,brakeArr,deltaArr,steeringArr,speedArr,RPMArr,MaxRPM):
        # Define fonts
        fontpath = "assets/fonts/GT-Regular"
        font200 = ImageFont.truetype(fontpath, 200)
        font150 = ImageFont.truetype(fontpath, 150)
        font100 = ImageFont.truetype(fontpath, 100)
        font75 = ImageFont.truetype(fontpath, 75)
        font50 = ImageFont.truetype(fontpath, 50)
        font25 = ImageFont.truetype(fontpath, 25)

        # Define initial frame
        background = cv2.imread("assets/bottomBar/backgroundBlue.png")
        backgroundColour = (0, 0, 255)
        height, width, layers = background.shape

        # Define images
        steeringWheel = Image.open("assets/icons/steeringWheel.png")
        topBar = Image.open("assets/GTBar/mainBar.png")
        teamColour = settings.teamColour

        # Define video output
        FPS = frameRate
        fourcc = VideoWriter_fourcc(*'MP42')
        video = VideoWriter('./output/'+ settings.currentFileName + '.avi', fourcc, float(FPS), (width, height))

        if not(deltaArr==""):
                return "success"