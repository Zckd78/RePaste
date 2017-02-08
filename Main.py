from PasteBinScraper import *
from DTOs import *
import IOFunctions
import threading
import time


def Main():
    options = ExecutionOption()
    options.DetermineMode("-d")
    options.SetThrottleTime(.2)
    GatherPasteBin(options)

def GatherPasteBin(options:ExecutionOption):

    ######################## PasteBin Area ########################
    # Set the IO Settings
    ioSet = IOSettings("PasteBin", "PasteBinCaps")
    IOFunctions.CreateCaptureFolder(ioSet)
    # Testing the PasteBin Scarper Interface
    scrap = PasteBinScraper(options)
    scrap.Go(Statics.PASTE_BIN_URI)

    # Go for additional rounds
    while len(scrap.Items) <= 1000:
        time.sleep(options.THROTTLE_TIME)
        popped = scrap.Items.popitem()[1].Url
        # Call Go with ForceEnum = True to begin checking for more Pastes
        worker1 = threading.Thread(scrap.Go(popped, True))
        worker1.start()
        while worker1.is_alive():
            time.sleep(.01)
        worker2 = threading.Thread(IOFunctions.CapPastes(scrap.Items, ioSet))
        worker2.start()
        # print("Grabbed " + str(len(scrap.Items)) + " new pastes!")

    print("\n\rFinished!")

Main()
