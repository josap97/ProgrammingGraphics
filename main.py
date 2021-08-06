import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from PIL import ImageFont, ImageDraw, Image
from csvReader import *
from format import *

# Define Arrays
fullArray = readCSV('data/spa_&_rss_formula_hybrid_2017_&_josap97_&_stint_3_test.csv')
npFullArray = np.array(fullArray)
sampleRate = npFullArray[8][1]
tire = npFullArray[5][1]
npFullArray = npFullArray[18:, :]
timeArr = np.transpose(npFullArray[:,0])
distanceArr = np.transpose(npFullArray[:,1])
deltaArr = np.transpose(npFullArray[:,16])
brakePosArr = np.transpose(npFullArray[:,19])
lateralGArr = np.transpose(npFullArray[:,24]).astype(np.float64)
longiGArr = np.transpose(npFullArray[:,25]).astype(np.float64)
carPosArr = [np.transpose(npFullArray[:,26+6]), np.transpose(npFullArray[:,26+7])]
DRSActArr = np.transpose(npFullArray[:,25+26])
DRSAvailArr = np.transpose(npFullArray[:,2*26])
ERSCharge = np.transpose(npFullArray[:,2*26+16])
RPMArr = np.transpose(npFullArray[:,2*26+9])
gearArr = np.transpose(npFullArray[:,2*26+12])
speedArr = np.transpose(npFullArray[:,2*26+13])
lastSectorArr = np.transpose(npFullArray[:,2*26+25])
maxRPM = npFullArray[2,3*26+4]
throttlePosArr = np.transpose(npFullArray[:,4*26+7])
noFrames = len(timeArr)

# Define tempStores
lastSectorPrev = 0
deltaSectorPrev = 0
sectorImprovement = 0

# Define fonts
fontpath = "assets/fonts/Formula1-Regular.ttf"
fontTime = ImageFont.truetype(fontpath, 200)
fontTimeMil = ImageFont.truetype(fontpath, 150)

# Define initial frame
background = cv2.imread("assets/bottomBar/bottomBar.png")
height, width, layers = background.shape

# Define images
steeringWheel = cv2.imread("assets/icons/steeringWheel.png")

# Define video output
FPS = sampleRate
seconds = 10
fourcc = VideoWriter_fourcc(*'MP42')
video = VideoWriter('./output/graphics.avi', fourcc, float(FPS), (width, height))

for i in range(0, noFrames):

    if(lastSectorPrev == 0):
        lastSectorPrev = lastSectorArr[i]
        sectorImprovement = deltaArr[i]
    elif(lastSectorPrev != lastSectorArr[i]):
        sectorImprovement = deltaArr[i] - sectorImprovement
        lastSectorPrev = lastSectorArr[i]

    frame = None
    frame = background
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)

    # Calculating Time Text
    timeLarge  = formatTimeLarge(timeArr[i])
    timeMil = str(float(timeArr[i]) - math.trunc(float(timeArr[i])))
    draw.text((860, 347), timeMil[1:][:3], font = fontTimeMil, fill=(255,255,255,0), anchor="lb")
    draw.text((860, 347), timeLarge, font = fontTime, fill=(255,255,255,0), anchor="rb")

    # Bar Inputs
    cv2.rectangle(frame, (1421, math.trunc(140+280*(100 - float(ERSCharge[i]))/100)), (1444, 140 + 280), (244, 216, 26), -1)
    cv2.circle(frame, (1602 + math.trunc(140*(lateralGArr[i])/5), 281 - math.trunc(140*(longiGArr[i]/5))), 5, (0, 0, 255), -1)

    # Adding Generated Frame to the array
    frame = np.array(img_pil)
    video.write(frame)
    printProgressBar(i+1, len(timeArr), prefix = 'Progress:', suffix = 'Complete', length = 50)

cv2.destroyAllWindows()
video.release()