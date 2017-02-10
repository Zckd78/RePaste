import io
import os
import sys
from DTOs import *
from PasteObj import *


def CapturePasteBinItem(paste: PublicPaste, settings: IOSettings):
    Save(paste.Title, paste.Raw, settings)


def CreateCaptureFolder(settings: IOSettings):
    folder = os.getcwd() + "\\" + settings.StorageFolder
    if not os.path.exists(folder):
        os.mkdir(folder)
    elif os.path.exists(folder) and os.path.isdir(folder):
        return  # Do Nothing, folder exists
    return


def Save(title: str, fileStream: str, settings: IOSettings):
    destFolder = MergePaths(os.getcwd(),settings.StorageFolder)
    if os.path.exists(destFolder) and os.path.isdir(destFolder):
        destFile = MergePaths(destFolder ,(title + ".txt"))
        if not os.path.exists(destFile):
            try:
                with io.open(destFile, 'w', encoding='utf8') as file:
                    file.write(fileStream)
            except:
                e = sys.exc_info()[0]
                print(" Error in IOFunctions : " + str(e))
    return True

def MergePaths(path1, path2):
    return path1 + "\\" + path2
