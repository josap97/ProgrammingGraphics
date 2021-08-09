from videoMaker import *
import numpy as np
import os, glob, settings, docFormatter

extension = 'csv'
os.chdir('data/')
fileNames = glob.glob('*.{}'.format(extension))
os.chdir('../')
print("Qeuing " + str(len(fileNames)) + " graphics renders;")
settings.init()
settings.teamArray = readConfig()
for file in range(0, len(fileNames)):
        base = os.path.basename('data/' + fileNames[file])
        name = os.path.splitext(base)
        settings.currentFileName = name[0]

        fileSplit = (name[0][1:]).split(')')
        infoArray = fileSplit[0].split(',')
        if(infoArray[2] in settings.teamArray):
                indices = np.where(settings.teamArray == infoArray[2])

                # Define your user Settings
                settings.driverName = infoArray[0]
                settings.driverNumber = infoArray[1]
                settings.teamName = settings.teamArray[int(indices[0]),0]
                settings.teamColour = (int(settings.teamArray[int(indices[0]),1]), int(settings.teamArray[int(indices[0]),2]), int(settings.teamArray[int(indices[0]),3]))
                print("Working on: #" + str(file+1) + ": " + name[0])
                makeVideo()
        else:
                print('Please check your name or config file formatting for the current file')
        

print("All done!")