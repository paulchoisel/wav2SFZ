import os
import pygubu
# Needed for pyinstaller
import pygubu.builder.ttkstdwidgets
import sys
import tkinter as tk
import wave

from enum import Enum
from importlib import resources
from tkinter import filedialog, messagebox, ttk

from .wav2sfz import convertWav2sfz
from .utils import isFile, isWriteableDirectory


class MessageBoxMessage:

    def __init__(self, title, message):
        self.title = title
        self.message = message


class MessageBoxMessages(Enum):

    WAVE_FILE_NOT_VALID_FILE = MessageBoxMessage(
        "Wave file is not a valid file.",
        "The path to the .wav file does not lead to a valid/readable file.\n"
        "Please make sure you entered a valid path, "
        "and check you have the permissions to read the file."
    )
    WAVE_FILE_NOT_VALID_WAVE_FILE = MessageBoxMessage(
        "Wave file is not a valid Wave file",
        "The path to the .wav file does not lead to a valid Wave file.\n"
        "The tool is only compatible with .wav files.\n"
        "Please use an appropriate software (Audacity for example) "
        "to convert your audio file in the Wave format."
    )
    TEMPO_NOT_INT = MessageBoxMessage(
        "The tempo is not valid.",
        "The tempo value is not valid.\n"
        "Please enter a valid number."
    )
    SOUNDFONT_FOLDER_NOT_WRITEABLE = MessageBoxMessage(
        "The Musescore soundfont folder is not writeable.",
        "The path to the Musescore soundfont folder is not writeable.\n"
        "Please make sure you entered a valid path and you have the permissions to write in it."
    )
    MUSICXML_PATH_NOT_WRITEABLE = MessageBoxMessage(
        "The output MusicXML file is not writeable.",
        "The path to the output MusicXML file is not writeable.\n"
        "Please make sure you entered a valid path and you have the permissions to write in it."
    )
    CONVERSION_SUCCESSFUL = MessageBoxMessage(
        "Conversion successful !",
        "Conversion successful !\n"
        "Please follow the rest of the instructions here :\n"
        "INSERT LINK"
    )


def getDataPath(pyinstallerPath, setuptoolsPath):
    """
    Return the right path to the UI, according to if the
    tool is bundledwith pyinstaller or setuptools
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, pyinstallerPath)
    return os.path.join(resources.files('wav2sfz'), setuptoolsPath)


class wav2sfzApp(pygubu.TkApplication):

    def __init__(self, root):
        super(wav2sfzApp, self).__init__(root)

        # Create the UI
        self.builder = pygubu.Builder()
        # self.builder.add_from_file(uiPath())
        self.builder.add_from_file(getDataPath("ui/ui.ui", 'UI/ui.ui'))

        # Apply the style (https://github.com/TkinterEP/ttkthemes/tree/master/ttkthemes/themes)
        root.tk.call('source', getDataPath("yaru/yaru.tcl", 'UI/yaru/yaru.tcl'))
        guiStyle = ttk.Style()
        guiStyle.theme_use('yaru')

        # Set the window title
        self.set_title("Wav2sfz")

        # Store a reference to the root frame
        self.mainWindow = self.builder.get_object('mainFrame')

        # Input fields
        self.waveFileEntry = self.builder.get_object('waveFileEntry')
        self.tempoEntry = self.builder.get_object('tempoSpinbox')
        self.soundfontFolderEntry = self.builder.get_object('soundfontFolderEntry')
        self.musicXMLPathEntry = self.builder.get_object('musicXMLPathEntry')

        self.builder.connect_callbacks(self)

    @staticmethod
    def setEntryText(entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)

    @staticmethod
    def displayMessageBox(messageBoxMessage, messageBoxFunction=messagebox.showerror):
        messageBoxFunction(
            title=messageBoxMessage.title,
            message=messageBoxMessage.message
        )

    def validateInput(self):
        try:
            isFile(self.waveFileEntry.get())
            wave.open(self.waveFileEntry.get(), "rb").close()
        except ValueError:
            return self.displayMessageBox(MessageBoxMessages.WAVE_FILE_NOT_VALID_FILE.value)
        except wave.Error:
            return self.displayMessageBox(MessageBoxMessages.WAVE_FILE_NOT_VALID_WAVE_FILE.value)

        try:
            int(self.tempoEntry.get())
        except ValueError:
            return self.displayMessageBox(MessageBoxMessages.TEMPO_NOT_INT.value)

        try:
            isWriteableDirectory(self.soundfontFolderEntry.get())
        except ValueError:
            return self.displayMessageBox(MessageBoxMessages.SOUNDFONT_FOLDER_NOT_WRITEABLE.value)

        try:
            isWriteableDirectory(os.path.dirname(self.musicXMLPathEntry.get()))
        except ValueError:
            return self.displayMessageBox(MessageBoxMessages.MUSICXML_PATH_NOT_WRITEABLE.value)

        return True

    def convertWavFile(self):
        if not self.validateInput():
            return

        try:
            convertWav2sfz(
                self.waveFileEntry.get(),
                int(self.tempoEntry.get()),
                4,
                self.soundfontFolderEntry.get(),
                self.musicXMLPathEntry.get()
            )
            self.displayMessageBox(
                MessageBoxMessages.CONVERSION_SUCCESSFUL.value, messagebox.showinfo)
        except Exception as e:
            messagebox.showerror(title="An error occurred...", message=str(e))

    def browseWaveFile(self):
        waveFilePath = filedialog.askopenfilename(filetypes=[('Wave file', '*.wav')])
        self.setEntryText(self.waveFileEntry, waveFilePath)

        if not self.musicXMLPathEntry.get():
            self.setEntryText(self.musicXMLPathEntry, waveFilePath.replace(".wav", ".musicxml"))

    def browseSoundfontFolder(self):
        self.setEntryText(self.soundfontFolderEntry, filedialog.askdirectory())

    def browseMusicXMLFile(self):
        self.setEntryText(self.musicXMLPathEntry, filedialog.asksaveasfilename(
            initialfile="result.musicxml"))

    def run(self):
        self.mainWindow.mainloop()


def main():
    root = tk.Tk()
    app = wav2sfzApp(root)
    app.run()


if __name__ == '__main__':
    main()
