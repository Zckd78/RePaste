from scraper.PasteBinScraper import *
from data.Structs import *
from utilities import IOFunctions
import sys

def Main():
    args = sys.argv[1:]
    GatherPasteBin(args)


def GatherPasteBin(params):
    ######################## PasteBin Area ########################
    # Set the Execution Options
    options = ExecutionOption()
    # These will be parameters when the program is live, setting here for testing.
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
    try:
        scrap.Go(Statics.PASTE_BIN_URI)
    except KeyboardInterrupt:
        print("CTRL-C Pressed, Exiting...")


    # Print out results here
    scrap.PrepareStatsReport()
    print("\n\rFinished!")

# Light the coals in this crazy train.
Main()
