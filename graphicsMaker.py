from os import name
import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from PIL import ImageFont, ImageDraw, Image
from docFormatter import *
from format import *
from functions import *
import settings
import streamlit as st

def makeF12017(fullArray):
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

def makeF12008(fullArray):
        # Define user Inputs
        driverName = settings.driverName
        teamName = settings.teamName

        # Define Arrays
        npFullArray = np.array(fullArray)
        sampleRate = npFullArray[8][1]
        lapTime = npFullArray[9][1]
        npFullArray = npFullArray[18:,:]
        timeArr = np.transpose(npFullArray[:,0])
        deltaArr = np.transpose(npFullArray[:,16]).astype(np.float64)
        brakePosArr = np.transpose(npFullArray[:,19]).astype(np.float64)
        RPMArr = np.transpose(npFullArray[:,2*26+9]).astype(np.int64)
        gearArr = np.transpose(npFullArray[:,2*26+12])
        speedArr = np.transpose(npFullArray[:,2*26+13]).astype(np.float64)
        maxSpeed = max(speedArr)
        maxRPM = np.float64(npFullArray[2,81])
        throttlePosArr = np.transpose(npFullArray[:,4*26+7]).astype(np.float64)
        racePositionArr = np.transpose(npFullArray[:,90])
        noFrames = len(timeArr)

        # Define fonts
        fontpath = "assets/fonts/Corbel Bold.ttf"
        font200 = ImageFont.truetype(fontpath, 200)
        font150 = ImageFont.truetype(fontpath, 150)
        font100 = ImageFont.truetype(fontpath, 100)
        font75 = ImageFont.truetype(fontpath, 75)
        font40 = ImageFont.truetype(fontpath, 40)
        font25 = ImageFont.truetype(fontpath, 25)

        # Define initial frame
        background = cv2.imread("assets/bottomBar/backgroundBlue1080.png")
        backgroundColour = (0, 0, 255)
        height, width, layers = background.shape

        # Define images
        inputsBackground = Image.open("assets/F12008Set/inputBackground.png")
        inputShape = cv2.imread("assets/F12008Set/inputBackground.png")
        inputheight, inputwidth, inputlayers = inputShape.shape
        inputFrac = 1
        nameBoxBackground = Image.open("assets/F12008Set/nameBox/nameBoxBackground.png")
        nbShape = cv2.imread("assets/F12008Set/nameBox/nameBoxBackground.png")
        nbheight, nbwidth, nblayers = nbShape.shape
        nameBoxBackground = nameBoxBackground.resize((width, round(nbheight/nbwidth*width)))
        nbYoffset = round(height - nbheight/nbwidth*width)
        nbWFrac = width/nbwidth

        # Define video output
        FPS = sampleRate
        fourcc = VideoWriter_fourcc(*'MP42')
        video = VideoWriter('./output/'+ settings.currentFileName + '.avi', fourcc, float(FPS), (width, height))
        inputsX0 = width - inputwidth - 100
        inputsY0 = height - inputheight - 200
        rpmX0 = inputsX0 + round(inputFrac*182)
        rpmY0 = inputsY0 + round(inputFrac*184)
        rpmR = 130
        rpmRb = 10

        for i in range(0, int(FPS)):
                frame = background
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.rectangle((0, 0, width, height), fill=backgroundColour)
                #posX = math.trunc(width - 553 + QuadraticEaseOut(i, FPS, 353))
                #img_pil.paste(inputsBackground, (posX, 0), inputsBackground)
                posX = math.trunc(-width + QuadraticEaseOut(i, FPS, width))
                img_pil.paste(nameBoxBackground, (posX, nbYoffset), nameBoxBackground)
                draw.text((posX + round(637*nbWFrac), nbYoffset + round(210*nbWFrac)), driverName, font = font40, fill=(0, 0, 0, 0), anchor="ls")
                draw.text((posX + round(637*nbWFrac), nbYoffset +  round(325*nbWFrac)), teamName, font = font40, fill=(255, 255, 255, 0), anchor="ls")
                frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                video.write(frame)
                printProgressBar(i+1, len(timeArr)+float(FPS), prefix = 'Progress:', suffix = 'Complete')

        for i in range(0, noFrames):

                # Setup Frame
                frame = None
                frame = background
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.rectangle((0, 0, width, height), fill=backgroundColour)
                img_pil.paste(nameBoxBackground, (0, nbYoffset), nameBoxBackground)
                img_pil.paste(inputsBackground, (inputsX0, inputsY0), inputsBackground)
                draw.text((inputsX0+182, inputsY0+462), "200", font = font25, fill=(255, 255, 255, 0), anchor="lt")
                draw.text((inputsX0+264, inputsY0+424), str(round((round(maxSpeed/10)-20)/4)*2*10+200), font = font25, fill=(255, 255, 255, 0), anchor="lt")
                draw.text((inputsX0+300, inputsY0+364), str(round((round(maxSpeed/10)-20)/4)*3*10+200), font = font25, fill=(255, 255, 255, 0), anchor="lt")
                draw.text((inputsX0+305, inputsY0+309), str(round(maxSpeed/10)*10), font = font25, fill=(255, 255, 255, 0), anchor="lt")
                theta = calcAngle2008(RPMArr[i])
                theta2 = theta - 90/180
                draw.polygon([(rpmX0 - rpmR*math.cos(theta), rpmY0 - rpmR*math.sin(theta)), (rpmX0 - rpmRb*math.sin(theta2), rpmY0 - rpmRb*math.cos(theta2)), (rpmX0 + rpmRb*math.sin(theta2), rpmY0 + rpmRb*math.cos(theta2))], fill=(255, 255, 255, 0))

                # Speed display
                if(speedArr[i]<200):
                        it = round(speedArr[i]/20)
                else:
                        it = round((speedArr[i]-200)/(max(speedArr)-200)*9) + 10
                speedImage = Image.open("assets/F12008Set/speed_steps/speed_" + str(it).zfill(3) + ".png")
                img_pil.paste(speedImage, (inputsX0, inputsY0), speedImage)

                # Throttle and Brake Inputs
                if(RPMArr[i] > maxRPM * 0.92):
                        gearColour = (255, 0, 0, 0)
                else:
                        gearColour = (0,0,0,0)
                draw.rectangle((inputsX0+208, inputsY0+221, math.trunc(inputsX0+208+146*(throttlePosArr[i])/100), inputsY0+261), fill=(0, 188, 0))
                draw.rectangle((inputsX0+208, inputsY0+261, math.trunc(inputsX0+208+146*(brakePosArr[i])/100), inputsY0+301), fill=(188, 0, 0)) # Inverted colour RGBBGR
                draw.text((inputsX0 + 231, inputsY0 + inputFrac*(211+30)), "Throttle", font=font25, fill=(255, 255, 255, 0), anchor="lm")
                draw.text((inputsX0 + 231, inputsY0 + inputFrac*(251+30)), "Brake", font=font25, fill=(255, 255, 255, 0), anchor="lm")
                draw.text((inputsX0 + 299, inputsY0 + inputFrac*(184+20)), str(gearArr[i]), font=font40, fill=gearColour, anchor="ls")

                # Top bar
                img_pil.paste(nameBoxBackground, (0, nbYoffset), nameBoxBackground)
                draw.text((637*nbWFrac, nbYoffset + round(210*nbWFrac)), driverName, font = font40, fill=(0, 0, 0, 0), anchor="ls")

                # Time
                timeLarge  = formatTimeLarge(timeArr[i])
                timeMil = str(float(timeArr[i]) - math.trunc(float(timeArr[i])))
                #draw.text((960, 347), timeMil[1:][:3], font = font150, fill=(255,255,255,0), anchor="lb")
                #draw.text((960, 347), timeLarge, font = font200, fill=(255,255,255,0), anchor="rb")
                draw.text((round((637+822*0.8)*nbWFrac), nbYoffset + round((275+40)*nbWFrac)), timeMil[1:][:3], font = font40, fill=(255, 255, 255, 0), anchor="ls")
                draw.text((round((637+822*0.8)*nbWFrac), nbYoffset + round((275+40)*nbWFrac)), timeLarge, font = font40, fill=(255, 255, 255, 0), anchor="rs")

                # Adding Generated Frame to the array
                frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                video.write(frame)
                printProgressBar(int(FPS)+i+1, len(timeArr)+float(FPS), prefix = 'Progress:', suffix = 'Complete')
        
        # Setting up final frames for the laptime show
        frame = None
        frame = background
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        draw.rectangle((0, 0, width, height), fill=backgroundColour)
        img_pil.paste(nameBoxBackground, (0, nbYoffset), nameBoxBackground)

        # Top bar
        img_pil.paste(nameBoxBackground, (0, nbYoffset), nameBoxBackground)
        draw.text((637*nbWFrac, nbYoffset + round(210*nbWFrac)), driverName, font = font40, fill=(0, 0, 0, 0), anchor="ls")

        # Calculating Time Text
        timeLarge  = formatTimeLarge(lapTime)
        timeMil = str(float(lapTime) - math.trunc(float(lapTime)))
        draw.text((round((637+822*0.8)*nbWFrac), nbYoffset + round((275+40)*nbWFrac)), timeMil[1:][:3], font = font40, fill=(255, 255, 255, 0), anchor="ls")
        draw.text((round((637+822*0.8)*nbWFrac), nbYoffset + round((275+40)*nbWFrac)), timeLarge, font = font40, fill=(255, 255, 255, 0), anchor="rs")
        draw.text((round((637+822*0.1)*nbWFrac), nbYoffset + round((275+40)*nbWFrac)), str(deltaArr[-1]), font = font40, fill=(255, 255, 255, 0), anchor="ls")

        # Adding Generated Frame to the array
        frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        for i in range(0, int(FPS)*10):
                video.write(frame)

        cv2.destroyAllWindows()
        video.release()
        return "success"

def makeGT(frameRate,timeArr,gearArr,throttleArr,brakeArr,deltaArr,steeringArr,speedArr,RPMArr,MaxRPM):
        # Define user Inputs
        driverName = settings.driverName
        frameRate = float(frameRate)

        # Define fonts
        fontpath = "assets/fonts/GT-Regular.otf"
        font200 = ImageFont.truetype(fontpath, 200)
        font150 = ImageFont.truetype(fontpath, 150)
        font100 = ImageFont.truetype(fontpath, 100)
        font75 = ImageFont.truetype(fontpath, 75)
        font50 = ImageFont.truetype(fontpath, 50)
        font25 = ImageFont.truetype(fontpath, 25)

        # Define initial frame
        background = cv2.imread("assets/GTBar/baseLayerBlue.png")
        backgroundColour = (0, 0, 255)
        height, width, layers = background.shape

        # Define images
        topBar = Image.open("assets/GTBar/GTBarMain.png")
        barInputs = Image.open("assets/GTBar/GTBarInputs.png")
        gradientImg = Image.open("assets/GTBar/GTBarGradient.png")
        gradientCV2 = cv2.imread("assets/GTBar/GTBarGradient.png")
        gradientX0 = 2586
        gradientWidth = 580
        gradientCV2h, gradientCV2w, gradientCV2l = gradientCV2.shape

        brandPath = "assets/brands/" + getBrandImg(settings.teamName)
        brandcv2 = cv2.imread(brandPath)
        brandImg = Image.open(brandPath)
        brandh, brandw, brandl = brandcv2.shape
        if(brandw < brandh):
                brandImage = brandImg.resize((173, round(brandh/brandw*173)))
        else:
                brandImage = brandImg.resize((round(brandh/brandw*127), 127))

        # Define video output
        fourcc = VideoWriter_fourcc(*'MP42')
        video = VideoWriter('./output/'+ settings.currentFileName + '.avi', fourcc, float(frameRate), (width, height))

        for i in range(0,int(frameRate)):
                frame = background
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.rectangle((0, 0, width, height), fill=backgroundColour)
                posX = math.trunc(-width + QuadraticEaseOut(i, frameRate, width))
                img_pil.paste(topBar, (posX, 0), topBar)
                img_pil.paste(brandImage, (posX + 1396, 564 - round(brandh/brandw*173/2)), brandImage)
                draw.text((posX+1594, 580), driverName, font = font100, fill=(255, 255, 255, 0), anchor="lm")
                draw.text((posX+2521+112, 580), str(settings.driverNumber), font = font100, fill=(0, 0, 0, 0), anchor="mm")
                frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                video.write(frame)
                printProgressBar(i+1, len(timeArr)+3*float(frameRate), prefix = 'Progress:', suffix = 'Complete')
        
        for i in range(0,int(0.5*frameRate)):
                # Add growing input bar section
                frame = background
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.rectangle((0, 0, width, height), fill=backgroundColour)
                inputBar = barInputs.crop((0, 0, width, 266 + round(QuadraticEaseOut(i, int(0.5*frameRate), 235))))
                img_pil.paste(inputBar, (-97 + round(QuadraticEaseOut(i, int(0.5*frameRate), 97)), 235 - round(QuadraticEaseOut(i, int(0.5*frameRate), 235))), inputBar)
                img_pil.paste(topBar, (0, 0), topBar)
                img_pil.paste(brandImage, (1396, 564 - round(brandh/brandw*173/2)), brandImage)
                draw.text((1594, 580), driverName, font = font100, fill=(255, 255, 255, 0), anchor="lm")
                draw.text((2521+112, 580), str(settings.driverNumber), font = font100, fill=(0, 0, 0, 0), anchor="mm")

                frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                video.write(frame)
                printProgressBar(int(frameRate)+i+1, len(timeArr)+3*float(frameRate), prefix = 'Progress:', suffix = 'Complete')
        
        for i in range(0,int(0.5*frameRate)):
                # Add growing input bar section
                frame = background
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.rectangle((0, 0, width, height), fill=backgroundColour)

                # Draw Gradient
                gradientImgCurr = gradientImg.crop((0, 0, gradientX0 + round(QuadraticEaseOut(i, int(frameRate), round(gradientWidth*(RPMArr[0] - min(RPMArr))/(max(RPMArr) - min(RPMArr))))), height))
                img_pil.paste(gradientImgCurr, (0, 0), gradientImgCurr)
                img_pil.paste(barInputs, (0, 0), barInputs)
                img_pil.paste(topBar, (0, 0), topBar)
                img_pil.paste(brandImage, (1396, 564 - round(brandh/brandw*173/2)), brandImage)

                draw.text((1594, 580), driverName, font = font100, fill=(255, 255, 255, 0), anchor="lm")
                draw.text((2521+112, 580), str(settings.driverNumber), font = font100, fill=(0, 0, 0, 0), anchor="mm")
                draw.text((2341+250, 270+100), str(round(QuadraticEaseOut(i, int(0.5*frameRate), speedArr[0]))), font=font150, fill=(0, 0, 0, 0), anchor="mm")
                draw.text((2341+250, 270+200), "SPEED", font=font50, fill=(0, 0, 0, 0), anchor="mb")
                draw.text((2746+200, 270+100), str(round(QuadraticEaseOut(i, int(0.5*frameRate), gearArr[0]))), font=font150, fill=(255, 255, 255, 0), anchor="mm")

                draw.polygon([(2743, 500), (2759, 460), (2759 + round(QuadraticEaseOut(i, int(0.5*frameRate), 324)*brakeArr[0]/100), 460), (2743 + round(QuadraticEaseOut(i, int(0.5*frameRate), 324)*brakeArr[0]/100), 500)], fill=(188, 0, 0))
                draw.polygon([(2759, 460), (2775, 420), (2775 + round(QuadraticEaseOut(i, int(0.5*frameRate), 324)*throttleArr[0]/100), 420), (2759 + round(QuadraticEaseOut(i, int(0.5*frameRate), 324)*throttleArr[0]/100), 460)], fill=(0, 188, 0))

                frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                video.write(frame)
                printProgressBar(int(1.5*frameRate)+i+1, len(timeArr)+3*float(frameRate), prefix = 'Progress:', suffix = 'Complete')
        
        for i in range(0, len(timeArr)):

                # Setup Frame
                frame = None
                frame = background
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.rectangle((0, 0, width, height), fill=backgroundColour)

                # Draw Gradient
                gradientImgCurr = gradientImg.crop((0, 0, gradientX0 + round(gradientWidth*(RPMArr[i] - min(RPMArr))/(max(RPMArr) - min(RPMArr))), height))
                img_pil.paste(gradientImgCurr, (0, 0), gradientImgCurr)

                img_pil.paste(topBar, (0, 0), topBar)
                img_pil.paste(barInputs, (0, 0), barInputs)
                img_pil.paste(brandImage, (1396, 564 - round(brandh/brandw*173/2)), brandImage)

                # Calculating Time Text
                timeLarge  = formatTimeLarge(timeArr[i])
                timeMil = str(float(timeArr[i]) - math.trunc(float(timeArr[i])))
                draw.text((2742+329*0.6, 610), timeMil[1:][:3], font = font50, fill=(255,255,255,0), anchor="lb")
                draw.text((2742+329*0.6, 610), timeLarge, font = font100, fill=(255,255,255,0), anchor="rb")

                # Bar Inputs
                draw.polygon([(2743, 500), (2759, 460), (2759 + round(324*brakeArr[i]/100), 460), (2743 + round(324*brakeArr[i]/100), 500)], fill=(188, 0, 0))
                draw.polygon([(2759, 460), (2775, 420), (2775 + round(324*throttleArr[i]/100), 420), (2759 + round(324*throttleArr[i]/100), 460)], fill=(0, 188, 0))

                # Inputs
                if(RPMArr[i] > MaxRPM * 0.92):
                        gearColour = (255, 0, 0, 0)
                else:
                        gearColour = (255,255,255,0)
                draw.text((1594, 580), driverName, font = font100, fill=(255, 255, 255, 0), anchor="lm")
                draw.text((2521+112, 580), str(settings.driverNumber), font = font100, fill=(0, 0, 0, 0), anchor="mm")
                draw.text((2341+250, 270+100), str(round(speedArr[i])), font=font150, fill=(0, 0, 0, 0), anchor="mm")
                draw.text((2341+250, 270+200), "SPEED", font=font50, fill=(0, 0, 0, 0), anchor="mb")
                draw.text((2746+200, 270+100), str(gearArr[i]), font=font150, fill=gearColour, anchor="mm")

                # Adding Generated Frame to the array
                frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                video.write(frame)
                printProgressBar(2*int(frameRate)+i+1, len(timeArr)+3*float(frameRate), prefix = 'Progress:', suffix = 'Complete')
        
        for i in range(0,int(0.5*frameRate)):
                # Add growing input bar section
                frame = background
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.rectangle((0, 0, width, height), fill=backgroundColour)

                # Draw Gradient
                gradientImgCurr = gradientImg.crop((0, 0, gradientX0 + round(QuadraticEaseOutInv(i, int(frameRate), round(gradientWidth*(RPMArr[-1] - min(RPMArr))/(max(RPMArr) - min(RPMArr))))), height))
                img_pil.paste(gradientImgCurr, (0, 0), gradientImgCurr)
                img_pil.paste(barInputs, (0, 0), barInputs)
                img_pil.paste(topBar, (0, 0), topBar)
                img_pil.paste(brandImage, (1396, 564 - round(brandh/brandw*173/2)), brandImage)

                draw.text((1594, 580), driverName, font = font100, fill=(255, 255, 255, 0), anchor="lm")
                draw.text((2521+112, 580), str(settings.driverNumber), font = font100, fill=(0, 0, 0, 0), anchor="mm")
                draw.text((2341+250, 270+100), str(round(QuadraticEaseOutInv(i, int(0.5*frameRate), speedArr[-1]))), font=font150, fill=(0, 0, 0, 0), anchor="mm")
                draw.text((2341+250, 270+200), "SPEED", font=font50, fill=(0, 0, 0, 0), anchor="mb")
                draw.text((2746+200, 270+100), str(round(QuadraticEaseOutInv(i, int(0.5*frameRate), gearArr[-1]))), font=font150, fill=(255, 255, 255, 0), anchor="mm")
                timeLarge  = formatTimeLarge(timeArr[-1])
                timeMil = str(float(timeArr[-1]) - math.trunc(float(timeArr[-1])))
                draw.text((2742+329*0.6, 610), timeMil[1:][:3], font = font50, fill=(255,255,255,0), anchor="lb")
                draw.text((2742+329*0.6, 610), timeLarge, font = font100, fill=(255,255,255,0), anchor="rb")

                draw.polygon([(2743, 500), (2759, 460), (2759 + round(QuadraticEaseOutInv(i, int(0.5*frameRate), 324)*brakeArr[-1]/100), 460), (2743 + round(QuadraticEaseOutInv(i, int(0.5*frameRate), 324)*brakeArr[-1]/100), 500)], fill=(188, 0, 0))
                draw.polygon([(2759, 460), (2775, 420), (2775 + round(QuadraticEaseOutInv(i, int(0.5*frameRate), 324)*throttleArr[-1]/100), 420), (2759 + round(QuadraticEaseOutInv(i, int(0.5*frameRate), 324)*throttleArr[-1]/100), 460)], fill=(0, 188, 0))

                frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                video.write(frame)
                printProgressBar(int(2*frameRate)+len(timeArr)+i+1, len(timeArr)+3*float(frameRate), prefix = 'Progress:', suffix = 'Complete')
        
        for i in range(0,int(0.5*frameRate)):
                # Add growing input bar section
                frame = background
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.rectangle((0, 0, width, height), fill=backgroundColour)
                inputBar = barInputs.crop((0, 0, width, 266 + round(QuadraticEaseOutInv(i, int(0.5*frameRate), 235))))
                img_pil.paste(inputBar, (-97 + round(QuadraticEaseOutInv(i, int(0.5*frameRate), 97)), 235 - round(QuadraticEaseOutInv(i, int(0.5*frameRate), 235))), inputBar)
                img_pil.paste(topBar, (0, 0), topBar)
                img_pil.paste(brandImage, (1396, 564 - round(brandh/brandw*173/2)), brandImage)
                draw.text((1594, 580), driverName, font = font100, fill=(255, 255, 255, 0), anchor="lm")
                draw.text((2521+112, 580), str(settings.driverNumber), font = font100, fill=(0, 0, 0, 0), anchor="mm")
                timeLarge  = formatTimeLarge(timeArr[-1])
                timeMil = str(float(timeArr[-1]) - math.trunc(float(timeArr[-1])))
                draw.text((2742+329*0.6, 610), timeMil[1:][:3], font = font50, fill=(255,255,255,0), anchor="lb")
                draw.text((2742+329*0.6, 610), timeLarge, font = font100, fill=(255,255,255,0), anchor="rb")

                frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                video.write(frame)
                printProgressBar(int(2.5*frameRate)+len(timeArr)+i+1, len(timeArr)+3*float(frameRate), prefix = 'Progress:', suffix = 'Complete')

        frame = background
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        draw.rectangle((0, 0, width, height), fill=backgroundColour)
        img_pil.paste(topBar, (0, 0), topBar)
        img_pil.paste(brandImage, (1396, 564 - round(brandh/brandw*173/2)), brandImage)
        draw.text((1594, 580), driverName, font = font100, fill=(255, 255, 255, 0), anchor="lm")
        draw.text((2521+112, 580), str(settings.driverNumber), font = font100, fill=(0, 0, 0, 0), anchor="mm")
        timeLarge  = formatTimeLarge(timeArr[-1])
        timeMil = str(float(timeArr[-1]) - math.trunc(float(timeArr[-1])))
        draw.text((2742+329*0.6, 610), timeMil[1:][:3], font = font50, fill=(255,255,255,0), anchor="lb")
        draw.text((2742+329*0.6, 610), timeLarge, font = font100, fill=(255,255,255,0), anchor="rb")

        frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        for i in range(0, int(frameRate*10)):
                video.write(frame)

        return "success"