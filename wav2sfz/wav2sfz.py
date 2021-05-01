import argparse
import math
from pymusicxml import Score, Part, Measure, BeamedGroup, Note, Rest, MetronomeMark
import os
from typing import TextIO, Tuple
import wave

from .constants import MIDI_MAX_NOTES, SEMI_TONES_NUMBER, SECONDS_PER_MINUTE, Pitches
from .utils import isFile, isWriteableDirectory


def exportBar(
        waveObject: wave.Wave_read,
        outputPath: str, barNumber: int,
        barDuration: float
) -> None:
    outputFile = wave.open(outputPath, 'wb')
    outputFile.setnchannels(waveObject.getnchannels())
    outputFile.setsampwidth(waveObject.getsampwidth())
    outputFile.setframerate(waveObject.getframerate())
    waveObject.setpos(int(barNumber * barDuration * waveObject.getframerate()))
    outputFile.writeframes(waveObject.readframes(
        int(barDuration * waveObject.getframerate())))
    outputFile.close()


def initSFZFile(sfzDir: str, songName: str, numberOfParts: int) -> list[TextIO]:

    sfzFiles = [
        open(os.path.join(sfzDir, f'{songName}_{partNumber}.sfz'), "w")
        for partNumber in range(numberOfParts)
    ]

    for sfzFile in sfzFiles:
        sfzFile.write('<control>\ndefault_path=.\n<global>\n<group>\n')
    return sfzFiles


def addKeyToSFZFile(sfzFiles: list[TextIO], sampleName: str, keyNumber: int) -> None:
    sfzFiles[int(keyNumber / MIDI_MAX_NOTES)].write(
        f"<region> sample={sampleName} key={keyNumber % MIDI_MAX_NOTES}\n")


def initMusicXMLData(songName: str, numberOfParts: int) -> Tuple[Score, list[Part]]:
    score = Score(title=songName)
    parts = [Part(f"{songName}_{partNumber}") for partNumber in range(numberOfParts)]
    for part in parts:
        score.append(part)
    return score, parts


def getNoteFromBarNumber(barNumber: int) -> str:
    pitch = list(Pitches)[barNumber % SEMI_TONES_NUMBER]
    return f"{pitch.value}{int(barNumber/SEMI_TONES_NUMBER) - 1}"


def addNoteToMusicXMLData(parts: list[Part], barNumber: int, tempo: int, beatsPerBar: int) -> None:
    for partNumber, part in enumerate(parts):
        if int(barNumber / MIDI_MAX_NOTES) == partNumber:
            part.append(
                Measure([
                    BeamedGroup([
                        Note(
                            getNoteFromBarNumber(barNumber % MIDI_MAX_NOTES), beatsPerBar,
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


def convertWav2sfz(waveFilePath, tempo, beatsPerBar, soundfontFolder, musicXMLFilePath):

    # Open the source wave file
    waveObject = wave.open(waveFilePath, "rb")

    # Contants
    tempo = tempo
    beatsPerBar = beatsPerBar
    barDuration = (SECONDS_PER_MINUTE * beatsPerBar) / tempo
    songName = os.path.basename(waveFilePath).replace('.wav', "")
    sfzDir = os.path.join(soundfontFolder, f"{songName}_SFZ")
    numberOfBars = math.ceil(
        (waveObject.getnframes() / waveObject.getframerate()) / barDuration)
    # MIDI can only work with 128 notes, so if the source wave file has more than
    # 128 bars, we have to use several parts/instruments
    numberOfParts = math.ceil(numberOfBars / MIDI_MAX_NOTES)

    # Create the SFZ folder
    os.mkdir(sfzDir)

    # Create the .sfz file (holding the mapping between the samples and the keys)
    sfzFiles = initSFZFile(sfzDir, songName, numberOfParts)

    # Create the PyMusicXML objects to store the score data
    score, parts = initMusicXMLData(songName, numberOfParts)

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
        addNoteToMusicXMLData(parts, barNumber, tempo, beatsPerBar)

    for sfzFile in sfzFiles:
        sfzFile.close()
    score.export_to_file(musicXMLFilePath)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("waveFilePath", type=isFile)
    parser.add_argument("tempo", type=int)
    parser.add_argument("--beatsPerBar", type=int, default=4)
    parser.add_argument("--soundfontFolder", type=isWriteableDirectory, default=None)
    parser.add_argument("--musicXMLFilePath", type=isWriteableDirectory, default=None)
    args = parser.parse_args()

    soundfontFolder = args.soundfontFolder
    if soundfontFolder is None:
        soundfontFolder = os.path.join(os.path.dirname(args.waveFilePath))

    musicXMLFilePath = args.musicXMLFilePath
    if musicXMLFilePath is None:
        musicXMLFilePath = os.path.join(
            os.path.dirname(args.waveFilePath),
            f"{os.path.basename(args.waveFilePath)}.musicxml"
        )

    convertWav2sfz(
        args.waveFilePath,
        args.tempo,
        args.beatsPerBar,
        soundfontFolder,
        musicXMLFilePath
    )


if __name__ == '__main__':
    main()
