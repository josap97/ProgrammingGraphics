import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from PIL import ImageFont, ImageDraw, Image
import streamlit as st
import math

# Define fonts
fontpath = "RobotoMono-Regular.ttf"
font200 = ImageFont.truetype(fontpath, 200)
font150 = ImageFont.truetype(fontpath, 150)
font100 = ImageFont.truetype(fontpath, 100)
font75 = ImageFont.truetype(fontpath, 75)
font50 = ImageFont.truetype(fontpath, 50)
font25 = ImageFont.truetype(fontpath, 25)

file1 = open('timetext.txt', 'r')
Lines = file1.readlines()
 
frameRate = 60
background = cv2.imread("background.png")
backgroundColour = (0, 0, 255)
height, width, layers = background.shape

# Define video output
fourcc = VideoWriter_fourcc(*'MP42')
video = VideoWriter('timer.avi', fourcc, float(frameRate), (width, height))

count = 0
# Strips the newline character
for line in Lines:
        frame = background
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        draw.text((width, math.trunc(height/2)), line, font = font200, fill=(255, 255, 255, 0), anchor="rm")
        frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        video.write(frame)
        count += 1
        print("Line{}: {}".format(count, line.strip()))