from videoMaker import *
import os
import glob
import settings

extension = 'csv'
os.chdir('data/')
fileNames = glob.glob('*.{}'.format(extension))
os.chdir('../')
print("Qeuing " + str(len(fileNames)) + " graphics renders;")
settings.init()
for file in range(0, len(fileNames)):
        base = os.path.basename('data/' + fileNames[file])
        name = os.path.splitext(base)
        settings.currentFileName = name[0]
        settings.driverName = 'JoSaPol'
        print("Working on: #" + str(file+1) + ": " + name[0])
        makeVideo()

print("All done!")