from numpy import floor, trunc
import math

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def formatTimeLarge(timeString):
        if(float(timeString)<1):
                timeLarge = str("00")
        elif(float(timeString)>1 and float(timeString)<60):
                timeMin = ""
                timeSec = str(math.trunc(float(timeString))).zfill(2)
                timeLarge = timeSec
        elif(float(timeString)>=60):
                timeMin = math.trunc(float(timeString))
                timeSec = str(math.trunc(float(timeString) - timeMin)).zfill(2)
                timeLarge = timeMin + ":" + timeSec
        else:
                timeLarge = "problem: " + timeString
        return timeLarge

def ERSChargeHeight(charge):
        return 80 + 282*charge