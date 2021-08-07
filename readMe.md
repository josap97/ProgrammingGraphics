
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
## Using the resulting video
It is not possible to generate a video with transparency layers, this is why the background is blue. Taking this away is relatively easy:
1. Open Premiere Pro and import the video
2. Place the rendered video on your timeline and resize it to where it looks good
3. Apply the `Ultra Key` effect to the clip resulting from this repos script
4. In the `Effect Controls` pane, click the colour picker icon and click on the blue background
5. You can now finetune the look by changing the other sliders, I found that leaving the Setting to `Default` looks best
## Customisation
It is possible to customise the way the graphics look by changing the images in `assets` to match what you want them to look like. The photoshop files are provided. However, do make sure that you export the files under the same name and with the same resolution! Equal aspect ratio simply is not enough as the images are pasted on the frame directly without any resizing. I may add this in the future but do not really see the point of spending that time for now.