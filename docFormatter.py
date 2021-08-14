import csv, os, settings, argparse, subprocess
import numpy as np

def readCSV(path):
        with open(path, newline='') as csvfile:
                data = list(csv.reader(csvfile))
        return data

def readConfig():
        teams = []
        configFile = open('assets/config.txt', 'r')
        for x in configFile:
                x = x.rstrip()
                if not("#" in x):
                        lineSplit = x.split(',')
                        currTeam = [lineSplit[0], lineSplit[1], lineSplit[2], lineSplit[3]]
                        teams.append(currTeam)
        return np.array(teams)

def generatePDF():
        content = r'''
                \documentclass{article}
                \begin{document}
                ... P \& B 
                \textbf{\huge %(school)s \\}
                \vspace{1cm}
                \textbf{\Large %(title)s \\}
                ...
                \end{document}
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--course')
        parser.add_argument('-t', '--title')
        parser.add_argument('-n', '--name',) 
        parser.add_argument('-s', '--school', default='My U')

        args = parser.parse_args()

        with open('data/cache/' + settings.currentFileName + '.tex', 'w') as f:
                f.write(content)
        
        cmd = ['pdflatex', '-interaction', 'nonstopmode', 'data/cache/' + settings.currentFileName + '.tex']
        proc = subprocess.Popen(cmd)
        proc.communicate()

        retcode = proc.returncode
        if not retcode == 0:
                os.unlink('output/' + settings.currentFileName + '.pdf')
                raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))
        os.unlink('data/cache/' + settings.currentFileName + '.tex')
        os.unlink('data/cache/' + settings.currentFileName + '.log')

def readAC(dataArr):
        result = dict()
        # Define Arrays
        npFullArray = np.array(dataArr)
        result['FPS'] = npFullArray[8][1]
        lapTime = npFullArray[9][1]
        npFullArray = npFullArray[18:,:]
        result['time'] = np.transpose(npFullArray[:,0])
        result['delta'] = np.transpose(npFullArray[:,16]).astype(np.float64)
        result['brake'] = np.transpose(npFullArray[:,19]).astype(np.float64)
        result['RPM'] = np.transpose(npFullArray[:,2*26+9]).astype(np.int64)
        result['gear'] = np.transpose(npFullArray[:,2*26+12])
        result['speed'] = np.transpose(npFullArray[:,2*26+13]).astype(np.float64)
        lastSectorArr = np.transpose(npFullArray[:,2*26+25]).astype(np.float64)
        result['throttle'] = np.transpose(npFullArray[:,4*26+7]).astype(np.float64)
        result['steering'] = np.transpose(npFullArray[:,3*26+25]).astype(np.float64)
        result['maxRPM'] = max(np.transpose(npFullArray[:,2*26+9]).astype(np.int64))
        return result

def readACC(dataArr):
        result = dict()
        # Define Arrays
        npFullArray = np.array(dataArr)
        result['FPS'] = npFullArray[8][1]
        lapTime = npFullArray[9][1]
        npFullArray = npFullArray[18:,:]
        result['time'] = np.transpose(npFullArray[:,0])
        result['delta'] = ""
        result['brake'] = np.transpose(npFullArray[:,7]).astype(np.float64)
        result['RPM'] = np.transpose(npFullArray[:,11]).astype(np.float64)
        result['gear'] = np.transpose(npFullArray[:,8])
        result['speed'] = np.transpose(npFullArray[:,5]).astype(np.float64)
        lastSectorArr = ""
        result['throttle'] = np.transpose(npFullArray[:,6]).astype(np.float64)
        result['steering'] = np.transpose(npFullArray[:,4]).astype(np.float64)
        result['maxRPM'] = max(np.transpose(npFullArray[:,11]).astype(np.int64))
        return result