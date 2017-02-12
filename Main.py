from PasteBinScraper import *
from DTOs import *
import IOFunctions


def Main():
    GatherPasteBin()


def GatherPasteBin():
    ######################## PasteBin Area ########################
    # Set the Execution Options
    options = ExecutionOption()
    # These will be parameters when the program is live, setting here for testing.
    params = "-d -v"
    options.DetermineMode(params)
    options.DetermineVerbose(params)
    options.SetThrottleTime(.5)
    options.SetHaltTime(1)
    options.SetPasteGoal(2000)
    # Set the IO Settings
    ioSet = IOSettings("PasteBin", "PasteBinCaps")
    IOFunctions.CreateCaptureFolder(ioSet)
    ioSet.SetStorageThreshold(1)
    # Testing the PasteBin Scarper Interface
    scrap = PasteBinScraper(options, ioSet)
    scrap.Go(Statics.PASTE_BIN_URI)

    print("\n\rFinished!")


Main()
