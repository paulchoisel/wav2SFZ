# Using the tool (console)

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

## Next

You already have a score and you want to import the audio track : [04-Importing the result](04-Importing_the_result.md)  
You don't have a score yet and want to use the template : [05-Using the template score.md](05-Using_the_template_score.md)