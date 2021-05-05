# wav2sfz - Play any audio file over a Musescore part

When transcribing/arranging a tune, going back and forth in the media player to listen to specific parts of the music while typing the note in Musescore can be tedious.  
This tool allows to import and synchronize an audio track in Musescore to help you transcribe/arrange it.

### Notice

This tool is nothing more than a quick hack, to use while waiting for a better solution directly integrated in Musescore.  
As such, it is not easy to use (requires Python), even if I'll try to be as clear as possible in the instructions.

## How does it work ?

This tools basically implements what is describe in this thread : https://musescore.org/en/node/273958  
Musescore does not provide a way to synchronize an audio track to your score, but what we can do is : 
 - Create a soundbank
 - Assign our audio track to a note
 - Choose this soundbank for an instrument in Musescore (an organ for example)
 - Make this instrument play the note we assign our audio track to

This works pretty well, however, you have to start the playback of your score at beginning or you will not hear your track.  
A workaround to this problem is to split the track into sections and assign a section to several notes of the soundbank.  
This works too, but it can become tedious, and the sections of the track may not align with the bars of the score.

This is where wav2sfz helps. The tool split the audio track into samples of one bar and create the corresponding SFZ file.  
The tool then creates a template score (as a MusicXML file) with a note on each bar. If you assign the soundbank to the instrument and play it, you will hear your track.

## How do I use it ?

[Instruction](docs/INSTRUCTIONS.md)

## Limitations

 - The audio track needs to be in time, the tool does not accommodate for time variations.
 - The time signature should be constant. (I'll maybe add a feature to introduce time changes)
