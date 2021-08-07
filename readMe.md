
# Create onscreen graphics from MOTEC data using Python
## Installation
Make sure you have `numpy` and `virtualenv` installed by running the following code in the terminal
```Batch
pip install virtualenv
virtualenv env --python=python3.6
source env/bin/activate
pip install numpy
pip install opencv-python
```
Unpack the python files and filestructure in the repositry to a folder on you desktop and change the `runGraphics.bat` file to match your installation.
## Data Preparation
The script uses MOTEC data to create graphics but, for some reason, you cannot just use raw exports. Make sure to do the following
1. Open the data you want converted in MOTEC i2 Pro and export them to a CSV and save it somewhere else on your system
    a. Export to CSV at any sample rate you want but do include both `time` and `distance` data
2. Open the exported CSV in excel and `Save as...`  a `.csv` file without making any changes to the `/data/` folder under a recognisable name
## Running the code
That's it, all the preparation has been done and you can run the `*.bat` file or open the `main.py` file in a Python interpreter and run it. This will automatically run the code for all csv files located in the data folder and export the video with the same name in the `/output/` folder.