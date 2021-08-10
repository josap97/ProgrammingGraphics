import streamlit as st
import pandas as pd
import time


st.write("Testing")
mainText = st.empty()
mainText.text("This is the progress")

if st.button('start Counting'):
        for i in range(0, 10):
                mainText.text("Update " + str(i))
                time.sleep(1)

file = st.file_uploader('Pick a file')
if file:
        st.write(file)