import io
import os
import sys
from data.Structs import *


def SaveLog(outputLog):
    folder = os.getcwd() + "\\" + "OutputLog"
    if not os.path.exists(folder):
        os.mkdir(folder)

    destFile = MergePaths(folder, ("OutputLog.txt"))
    try:
        with io.open(destFile, 'w', encoding='utf8') as file:
            print("Saving output log to: " + destFile)
            file.write(outputLog)
    except IOError as ioerr:
        print(" Error in IOFunctions : " + str(ioerr))


def CapturePasteBinItem(paste: PublicPaste, settings: IOSettings):
    if settings.StorageThreshold <= len(paste.MatchingCriteria):
        # Only save worthy pastes
        if len(paste.MatchingCriteria) > 0:
            Save(paste, settings)


def CreateCaptureFolder(settings: IOSettings):
    folder = os.getcwd() + "\\" + settings.StorageFolder
    if not os.path.exists(folder):
        os.mkdir(folder)
    elif os.path.exists(folder) and os.path.isdir(folder):
        return  # Do Nothing, folder exists
    return


def Save(paste: PublicPaste, settings: IOSettings):
    # Only place the paste
    if settings.StorageThreshold > 0:
        # Create a destination folder based on the first Matching Criteria
        firstCriteria = paste.MatchingCriteria[0]
        storageFolder = os.getcwd() + "\\" + settings.StorageFolder
        destFolder = MergePaths(storageFolder, firstCriteria)
    else:
        destFolder = MergePaths(os.getcwd(), settings.StorageFolder)

    if not os.path.exists(destFolder):
        os.mkdir(destFolder)

    # Append the title of the paste, given it's not the default "Untitled"
    destFile = ""
    if paste.Title == "Untitled":
        destFile = MergePaths(destFolder, (paste.PasteID + ".txt"))
    else:
        destFile = MergePaths(destFolder, (paste.PasteID + "_" + paste.Title + ".txt"))
    if not os.path.exists(destFile):
        try:
            with io.open(destFile, 'w', encoding='utf8') as file:
                file.write(paste.Raw)
        except:
            e = sys.exc_info()[0]
            print(" Error in IOFunctions : " + str(e))

    return True


def MergePaths(path1, path2):
    return path1 + "\\" + path2
