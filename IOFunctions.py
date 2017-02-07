import io
import os
import sys
from DTOs import *
from PasteObj import *


def CreateCaptureFolder(settings: IOSettings):
    folder = os.getcwd() + "\\" + settings.StorageFolder
    if not os.path.exists(folder):
        os.mkdir(folder)
    elif os.path.exists(folder) and os.path.isdir(folder):
        return  # Do Nothing, folder exists
    return


def Save(title, fileStream, settings: IOSettings):
    destFolder = settings.StorageFolder
    if os.path.exists(destFolder) and os.path.isdir(destFolder):
        thisFile = open(destFolder + "\\" + title + ".txt", 'w')
        try:
            thisFile.write(fileStream)
        except:
            e = sys.exc_info()[0]
            print(" Error in IOFunctions : " + str(e))
        thisFile.close()

    return True


def CapPastes(pastes: [PublicPaste], settings: IOSettings):
    for paste in pastes.items():
        Save(paste[0], paste[1].Raw, settings)
