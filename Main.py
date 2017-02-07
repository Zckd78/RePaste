from Scraper import *
from DTOs import *
import threading


def Main():

    options = ExecutionOption()
    options.DetermineMode("-d")
    scrap = Scraper(options)
    scrap.Go(Statics.PASTE_BIN_URI)

    while len(scrap.Items) <= 10:
        popped = scrap.Items.popitem()[1].Url
        # Call Go with ForceEnum = True to begin checking for more Pastes
        work = threading.Thread(scrap.Go(popped,True))
        print("Grabbed " + str(len(scrap.Items)) + " new pastes!")

    print("\n\rFinished!")

Main()