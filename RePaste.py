from scraper.PasteBinScraper import *
from data.Structs import *
from utilities import IOFunctions

def Main():
    GatherPasteBin()


def GatherPasteBin():
    ######################## PasteBin Area ########################
    # Set the Execution Options
    options = ExecutionOption()
    # These will be parameters when the program is live, setting here for testing.
    params = ""
    options.DetermineMode(params)
    options.DetermineVerbose(params)
    options.SetThrottleTime(.5)
    options.SetHaltTime(1)
    options.SetPasteGoal(1000)
    # Set the IO Settings
    ioSet = IOSettings("PasteBin", "PasteBinCaps")
    IOFunctions.CreateCaptureFolder(ioSet)
    ioSet.SetStorageThreshold(0)
    # Testing the PasteBin Scarper Interface
    scrap = PasteBinScraper(options, ioSet)
    scrap.Go(Statics.PASTE_BIN_URI)

    # Eventually print out results here
    # Have to add those trackers to a new DTO
    print("\n\rFinished!")

# Light the coals in this crazy train.
Main()
