from videoMaker import *
import numpy as np
import os, glob, settings, configparser

extension = 'csv'
os.chdir('data/')
fileNames = glob.glob('*.{}'.format(extension))
os.chdir('../')
print("Qeuing " + str(len(fileNames)) + " graphics renders;")

# Read the cofig file
config = configparser.ConfigParser()
thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'assets/config.ini')
config.read(initfile)
settings.init()
settings.showTrackMap = config.getboolean('General', 'showTrackMap')
settings.showTeamName = config.getboolean('General', 'showTeamName')
for file in range(0, len(fileNames)):
        base = os.path.basename('data/' + fileNames[file])
        name = os.path.splitext(base)
        settings.currentFileName = name[0]

        fileSplit = (name[0][1:]).split(')')
        infoArray = fileSplit[0].split(',')
        if(config.has_option('TEAM'+infoArray[2], 'name')):

                # Define your user Settings
                settings.driverName = infoArray[0]
                settings.driverNumber = infoArray[1]
                settings.sessionYear = infoArray[3]
                settings.teamName = config.get('TEAM'+infoArray[2], 'name')
                colourFull = (config.get('TEAM'+infoArray[2], 'colour')).split(',')
                settings.teamColour = (int(colourFull[0]), int(colourFull[1]), int(colourFull[2]))
                print("Working on: #" + str(file+1) + ": " + name[0])
                makeVideo()
        else:
                print('Please check your name or config file formatting for the current file')
        

print("All done!")