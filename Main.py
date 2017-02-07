from PasteBinScraper import *
from DTOs import *
import IOFunctions
import threading


def Main():
    options = ExecutionOption()
    options.DetermineMode("-d")
    # Testing the PasteBin Scarper Interface
    scrap = PasteBinScraper(options)
    scrap.Go(Statics.PASTE_BIN_URI)

    # Go for additional rounds
    while len(scrap.Items) <= 250:
        popped = scrap.Items.popitem()[1].Url
        # Call Go with ForceEnum = True to begin checking for more Pastes
        work = threading.Thread(scrap.Go(popped, True))
        work.start()
        # print("Grabbed " + str(len(scrap.Items)) + " new pastes!")

    # Save those to a file
    ioSet = IOSettings("PasteBin", "PasteBinCaps")
    IOFunctions.CreateCaptureFolder(ioSet)
    IOFunctions.CapPastes(scrap.Items, ioSet)

    print("\n\rFinished!")


Main()
