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