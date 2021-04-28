import argparse
import math
from pymusicxml import Score, Part, Measure, BeamedGroup, Note, Rest, MetronomeMark
import os
import wave

from utils import isFile


def exportBar(waveObject, outputPath, barNumber, barDuration):
    outputFile = wave.open(outputPath, 'wb')
    outputFile.setnchannels(waveObject.getnchannels())
    outputFile.setsampwidth(waveObject.getsampwidth())
    outputFile.setframerate(waveObject.getframerate())
    waveObject.setpos(int(barNumber * barDuration * waveObject.getframerate()))
    outputFile.writeframes(waveObject.readframes(
        int(barDuration * waveObject.getframerate())))
    outputFile.close()


def initSFZFile(sfzDir, songName, numberOfParts):

    sfzFiles = [
        open(os.path.join(sfzDir, f'{songName}_{partNumber}.sfz'), "w")
        for partNumber in range(numberOfParts)
    ]

    for sfzFile in sfzFiles:
        sfzFile.write('<control>\ndefault_path=.\n<global>\n<group>\n')
    return sfzFiles


def addKeyToSFZFile(sfzFiles, sampleName, keyNumber):
    sfzFiles[int(keyNumber / 128)].write(f"<region> sample={sampleName} key={keyNumber % 128}\n")


def initMusicXMLData(songName, numberOfParts):
    score = Score(title=songName)
    parts = [Part(f"{songName}_{partNumber}") for partNumber in range(numberOfParts)]
    for part in parts:
        score.append(part)
    return score, parts


pitches = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]


def getNoteFromBarNumber(barNumber):
    pitch = pitches[barNumber % 12]
    return f"{pitch}{int(barNumber/12) - 1}"


def addNoteToMusicXMLData(parts, barNumber, tempo):
    for partNumber, part in enumerate(parts):
        if int(barNumber / 128) == partNumber:
            part.append(
                Measure([
                    BeamedGroup([
                        Note(
                            getNoteFromBarNumber(barNumber % 128), beatsPerBar,
                            directions=MetronomeMark(1, tempo) if barNumber == 0 else [])
                    ]),
                ],
                    time_signature=(beatsPerBar, 4) if barNumber == 0 else None))
        else:
            part.append(
                Measure([
                    BeamedGroup([
                        Rest(beatsPerBar)]
                    )
                ],
                    time_signature=(beatsPerBar, 4) if barNumber == 0 else None))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("waveFilePath", type=isFile)
    parser.add_argument("tempo", type=int)
    parser.add_argument("--beatsPerBar", type=int, default=4)
    args = parser.parse_args()

    # Open the source wave file
    waveFilePath = args.waveFilePath
    waveObject = wave.open(waveFilePath, "rb")

    # Contants
    tempo = args.tempo
    beatsPerBar = args.beatsPerBar
    barDuration = (60 * beatsPerBar) / tempo
    songName = waveFilePath.replace('.wav', "")
    sfzDir = f"{songName}SFZ"
    numberOfBars = math.ceil(
        (waveObject.getnframes() / waveObject.getframerate()) / barDuration)
    # MIDI can only work with 128 notes, so if the source wave file has more than
    # 128 bars, we have to use several parts/instruments
    numberOfParts = math.ceil(numberOfBars / 128)

    # Create the SFZ folder
    os.mkdir(sfzDir)

    # Create the .sfz file (holding the mapping between the samples and the keys)
    sfzFiles = initSFZFile(sfzDir, songName, numberOfParts)

    # Create the PyMusicXML objects to store the score data
    score, parts = initMusicXMLData(songName, numberOfParts)
    musicXMLFilePath = os.path.join(sfzDir, f'{songName}.musicxml')

    # For each bar, export a sample, add a line in the sfz file and add the corresponding note
    # in the MusicXML data
    for barNumber in range(numberOfBars):

        # Constants
        barNumberString = str(barNumber + 1)
        sampleName = f"{songName}_Bar{barNumberString}.wav"
        samplePath = os.path.join(sfzDir, sampleName)

        # Extract the sample from the source wave file
        exportBar(waveObject, samplePath, barNumber, barDuration)

        # Add a line in the sfz file
        addKeyToSFZFile(sfzFiles, sampleName, barNumber)

        # Add the corresponding notes in the score
        addNoteToMusicXMLData(parts, barNumber, tempo)

    for sfzFile in sfzFiles:
        sfzFile.close()
    score.export_to_file(musicXMLFilePath)
