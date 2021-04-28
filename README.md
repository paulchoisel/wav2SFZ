# wav2sfz - Play any audio file over a Musescore part

When transcribing/arranging a tune, going back and forth in the media player to listen to specific parts of the music while typing the note in Musescore can be tedious.  
This tool allows to import and synchronize an audio track in Musescore to help you transcribe/arrange it.

### Notice

This tool is nothing more than a quick hack, to use while waiting for a better solution directly integrated in Musescore.  
As such, it is not easy to use (requires Python), even if I'll try to be as clear as possible in the instructions.

## Limitations

 - The audio track needs to be in time, the tool does not accommodate for time variations.
 - The time signature should be constant. (I'll maybe add a feature to introduce time changes)

## Requirements

 - Python 3.9 + PIP
 - Musescore 3.6
 - Audacity or any tool to crop and convert your audio file 
