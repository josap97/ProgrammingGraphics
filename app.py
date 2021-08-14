from re import I
import streamlit as st
import pandas as pd
import numpy as np
import time, glob, os, settings, configparser, graphicsMaker, docFormatter

extension = 'png'
brandArr = []
os.chdir('assets/brands/')
fileNames = glob.glob('*.{}'.format(extension))
os.chdir('../../')
for i in range(0, len(fileNames)):
        brandArr.append(fileNames[i][:4])

st.set_page_config(page_title='Programming Graphics', page_icon = 'assets/brands/mercedes.png', initial_sidebar_state = 'auto')
st.title('Programming Graphics')
st.text('This app will allow you to input your exported MOTEC data and export it as video graphics.')

file = st.file_uploader('Choose the exported MOTEC data', accept_multiple_files=True, type='csv')
formContainer = st.empty()
if file:
        formContainer = st.form('Form1')#, clear_on_submit=True)
        formContainer.write("Before qeuing " + str(len(file)) + " graphics renders, please choose the type of graphics you want to create and for what game")
        for f in range(0, len(file)):
                #st.write(file[f].getvalue())
                formContainer.selectbox('Select for ' + str(file[f].name), ['Assetto Corsa Formula 1', 'Assetto Corsa GT3', 'Assetto Corsa Competizione GTs'], key='graphicType'+str(f))
                formContainer.checkbox('Add trackmap to the export', key='trackMap'+str(f))
                if("GT" in st.session_state['graphicType'+str(f)]):
                        formContainer.selectbox('Car brand', brandArr, key='graphicBrand' + str(f))
                np.array(file[f].getvalue())
        startEncode = formContainer.form_submit_button('Start converting files')

        if startEncode:
                formContainer.empty()
                progress = st.progress(0)
                currInfo = st.empty()
                # Read the cofig file
                config = configparser.ConfigParser()
                thisfolder = os.path.dirname(os.path.abspath(__file__))
                initfile = os.path.join(thisfolder, 'assets/config.ini')
                config.read(initfile)
                settings.init()
                settings.showTrackMap = config.getboolean('General', 'showTrackMap')
                settings.showTeamName = config.getboolean('General', 'showTeamName')
                for i in range(0, len(file)):
                        encodeType = st.session_state['graphicType'+str(i)]
                        settings.currentFileName = (file[i].name)[:-4]
                        name = settings.currentFileName

                        fileSplit = (name[1:]).split(')')
                        infoArray = fileSplit[0].split(',')
                        print(name)
                        # Define your user Settings
                        settings.driverName = infoArray[0]
                        settings.driverNumber = infoArray[1]
                        if(("F1" in st.session_state['graphicType'+str(i)]) and (config.has_option('TEAM'+infoArray[2], 'name'))):
                                settings.teamName = config.get('TEAM'+infoArray[2], 'name')
                                colourFull = (config.get('TEAM'+infoArray[2], 'colour')).split(',')
                                settings.teamColour = (int(colourFull[0]), int(colourFull[1]), int(colourFull[2]))
                                currInfo.text("Working on: #" + str(i+1) + ": " + name)
                                #graphicsMaker.makeF1(file[i].getvalue())
                        elif("GT" in st.session_state['graphicType'+str(i)]):
                                settings.teamName = config.get('TEAM'+infoArray[2], 'name')
                                if("Competizione" in st.session_state['graphicType'+str(i)]):
                                        result = docFormatter.readACC(file[i].getvalue())
                                else:
                                        result = docFormatter.readAC(file[i].getvalue())
                                graphicsMaker(result.FPS,result.time,result.gear,result.throttle,result.brake,result.delta,result.steering,result.speed,result.RPM,result.maxRPM)
                                        
                        else:
                                st.error('Please check your name or config file formatting for the current file')