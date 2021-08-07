import csv
import os

def readCSV(path):
        with open(path, newline='') as csvfile:
                data = list(csv.reader(csvfile))
        return data