from videoMaker import *
import numpy as np
import os, glob, settings, configparser, docFormatter, graphicsMaker

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
settings.enableEnduranceBlur = config.getboolean('General', 'enableEnduranceBlur')
for file in range(0, len(fileNames)):
        base = os.path.basename('data/' + fileNames[file])
        name = os.path.splitext(base)
        settings.currentFileName = name[0]

        fileSplit = (name[0][1:]).split(')')
        infoArray = fileSplit[0].split(',')
        

        # Define your user Settings
        settings.sessionSim = (infoArray[0]).lower()
        settings.driverName = infoArray[1]
        settings.driverNumber = infoArray[2]
        settings.sessionYear = infoArray[4]
        settings.sessionSeries = infoArray[5]
        print("Working on: #" + str(file+1) + ": " + name[0])
        if(((settings.sessionSeries).lower() == "F1".lower()) and (settings.sessionYear == "2017")):
                if(config.has_option('TEAM'+infoArray[3], 'name')):
                        settings.teamName = config.get('TEAM'+infoArray[3], 'name')
                        colourFull = (config.get('TEAM'+infoArray[3], 'colour')).split(',')
                        settings.teamColour = (int(colourFull[0]), int(colourFull[1]), int(colourFull[2]))
                        fullArray = readCSV('data/' + settings.currentFileName + '.csv')
                        graphicsMaker.makeF12017(fullArray)
                else:
                        print('Please check your name or config file formatting for the current file')
        elif(((settings.sessionSeries).lower() == "F1".lower()) and (settings.sessionYear == "2008")):
                if(config.has_option('TEAM'+infoArray[3], 'name')):
                        settings.teamName = config.get('TEAM'+infoArray[3], 'name')
                        colourFull = (config.get('TEAM'+infoArray[3], 'colour')).split(',')
                        settings.teamColour = (int(colourFull[0]), int(colourFull[1]), int(colourFull[2]))
                        fullArray = readCSV('data/' + settings.currentFileName + '.csv')
                        graphicsMaker.makeF12008(fullArray)
                else:
                        print('Please check your name or config file formatting for the current file')
        elif(((settings.sessionSeries).lower() == "GT".lower())):
                settings.teamName = infoArray[3]
                fullArray = readCSV('data/' + settings.currentFileName + '.csv')
                if(settings.sessionSim == "ac"):
                        result = docFormatter.readACArr(fullArray)
                elif(settings.sessionSim == "acc"):
                        result = docFormatter.readACCArr(fullArray)
                #print(result)
                graphicsMaker.makeGT(result["FPS"],result["time"],result["gear"],result["throttle"],result["brake"],result["delta"],result["steering"],result["speed"],result["RPM"],result["maxRPM"])
        elif((settings.sessionSeries).lower() == "Endu".lower()):
                settings.teamName = infoArray[3]
                fullArray = readCSV('data/' + settings.currentFileName + '.csv')
                if(settings.sessionSim == "ac"):
                        result = docFormatter.readACArr(fullArray)
                elif(settings.sessionSim == "rf2"):
                        result = docFormatter.readrF2Arr(fullArray)
                #print(result)
                graphicsMaker.makeEndurance(result["FPS"],result["time"],result["gear"],result["throttle"],result["brake"],result["delta"],result["steering"],result["speed"],result["RPM"],result["maxRPM"],result["airTemp"],result["trackTemp"])
        
        

print("All done!")