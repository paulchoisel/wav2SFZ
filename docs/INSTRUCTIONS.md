 
# SETUP

I assume that you have Python3 installed and access to a command line.

 - Install the tool with pip : 

`pip install wav2sfz`


# Instructions

## Preparing the audio file

 - Use audacity (or any other software) to clip the silences at both ends of your audio track. 
 - Export the file in Wave format. Don't use a framerate too high (44100 bits/s works fine)
[Quick Audacity tutorial](https://manual.audacityteam.org/man/tutorial_editing_an_existing_file.html)

## Using the tool

 - In a terminal, navigate to the folder containing your Wave file
 - Execute the tool 

```
wav2sfz <<AudioTrackName>> <<Tempo>>

Example :

wav2sfz MyTune.wav 128
```

 - If nothing is printed, the tool executed successfully, otherwise, an error occurred. Please report the errors you encounter !
 - You should find a new folder named after your file name and the suffix SFZ. This folder contains the SFZ soundbanks as well as the corresponding samples. It also contains a MusicXML template that we'll use to import the tune in Musescore.

## Importing the result in Musescore

 - Move the .musicxml file out of the newly created folder
 - Move the folder (now containing only .sfz and .wav files) in the folder where Musescore stores the user soundbanks. If you don't know where that location is : Open Musescore, navigate to Edit -> Preferences and look in the bottom left corner, what is written next to "SoundFonts"

The next steps depend on if you already have a score or not : 

### You don't have a score yet :

 - Open the MusicXML file with Musescore
 - Navigate to Edit -> Instruments
 - Make the existing instruments invisible
 - Add your instruments

### You already have a score
 - Open your score and the MusicXML file with Musescore
 - In your existing score, navigate to Edit -> Instruments
 - Add as many organs as there are instruments in the MusicXML file
 - Copy and paste the notes from the MusicXML file to the organs you created in your existing score
 - Close the MusicXML file

## Assign the soundbanks to the organs

 - In Musescore, in View, enable the Synthesizer panel
 - Select the Zerberus tab
 - Click on Add
 - In the new Window, select the SFZ soundbanks corresponding to your audio track and select Load
 - Close the synthesizer window
 - In View, enable the Mixer panel (or press F10)
 - In the Mixer, select the instruments we added (or the one that were predefined in the MusicXML file)
 - From left to right, assign the sounds corresponding to your audio track
 - Go to the beginning of the score, press play and you should here your audio track ! 