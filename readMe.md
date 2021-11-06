# Create onscreen graphics from AC MOTEC data using Python
The following scripts have been made to work with MOTEC telemetry captured with acti for Assetto Corsa. Unfortunately, no equivalent could be made to work with the data captured from Assetto Corsa Competizione 
## Installation
Make sure you have `numpy` and `virtualenv` installed by running the following code in the terminal
```sh
pip install virtualenv
virtualenv env --python=python3.6
source env/bin/activate
pip install numpy
pip install opencv-python
```
Unpack the python files and filestructure in the repositry to a folder on you desktop and change the `runGraphics.bat` file to match your installation.

In order to be able to run the webclient, make sure to have `streamlit` installed by
```sh
pip install streamlit
```
## Data Preparation
The script uses MOTEC data to create graphics but, for some reason, you cannot just use raw exports. The script will convert each and every sample of data you give as input, this means that if you want graphics for a single lap you must only export that single lap. The script will not look for your fastest lap or detect complete laps, it will just convert the entire exported range of data. Make sure to do the following.
1. Open the data you want converted in MOTEC i2 Pro and export them to a CSV and save it somewhere else on your system
    a. Export to CSV at any sample rate you want but do include both `time` and `distance` data
2. Open the exported CSV in excel and `Save as...`  a `.csv` file without making any changes to the `/data/` folder with the following name `(name,number,team) info.csv` where:
    a. `name` is the driver name using normal latin characters
    b. `number` is the number of the driver in the file, limited to max 3 numbers
    c. `team` is the team name the driver drives for. You can add teams by adding to the `assets/config.ini` file. By default you can choose for the following:
        * ferrari
        * forceIndia
        * haas
        * mclaren
        * mercedes
        * redBull
        * renault
        * sauber
        * torroRosso
        * williams
        * alpine
        * alphaTauri
        * astonMartin
        * alfaRomeo
    d. `info` is a container for any information you want to add to the file name, the script does not look at this so if free to fill in as you please
## Running the code
That's it, all the preparation has been done and you can run the `*.bat` file or open the `main.py` file in a Python interpreter and run it. This will automatically run the code for all csv files located in the data folder and export the video with the same name in the `/output/` folder.
## Using the resulting video
It is not possible to generate a video with transparency layers, this is why the background is blue. Taking this away is relatively easy:
1. Open Premiere Pro and import the video
2. Place the rendered video on your timeline and resize it to where it looks good
3. Apply the `Ultra Key` effect to the clip resulting from this repos script
4. In the `Effect Controls` pane, click the colour picker icon and click on the blue background
5. You can now finetune the look by changing the other sliders, I found that leaving the Setting to `Default` looks best

If you use this for your own projects, please tag JoSaPolGaming on Twitter or Instagram. This is not a requirement but we would like to see what people create with it. We would like to ask you to link to this repo in your YouTube videos.
## Customisation
It is possible to customise the way the graphics look by changing the images in `assets` to match what you want them to look like. The photoshop files are provided. However, do make sure that you export the files under the same name and with the same resolution! Equal aspect ratio simply is not enough as the images are pasted on the frame directly without any resizing. I may add this in the future but do not really see the point of spending that time for now.
