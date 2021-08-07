from videoMaker import *
import os
import glob

extension = 'csv'
os.chdir('data/')
fileNames = glob.glob('*.{}'.format(extension))
os.chdir('../')
for file in range(0, len(fileNames)):
        base = os.path.basename('data/' + fileNames[file])
        name = os.path.splitext(base)
        print("Working on: " + name[0])
        makeVideo(name[0], 'JoSaPol')

print("All done!")