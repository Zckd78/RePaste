from scraper.CoarseComb import *
import scraper.IScraper
from data.Structs import *
import datetime
import sys
import time
import requests
import bs4
import threading
from utilities import IOFunctions

class PasteBinScraper():
    Retries = 5

    def __init__(self, exOptions: ExecutionOption, ioSet: IOSettings):
        self.Name = "PasteBin Scraper"
        self.CurrentUri = ""
        self.Items = {}
        self.History = []
        # Options DTOs for transferring settings between here and other classes
        self.ExecutionOptions = exOptions
        self.IOSettings = ioSet
        # Variables pertaining to slowing down the speed of requesting pages
        self.HaltAdjustIncOriginal = .025
        self.HaltAdjustInc = .11
        self.HaltTime = exOptions.HaltTime
        self.LargestPaste = PublicPaste()

    ## Root Function - Navigates to a page, and decides what to do from there.
    def Go(self, url: str):
        print("Started on: " + time.ctime())
        self.CurrentUri = url

        # Go so many rounds
        while len(self.Items) <= self.ExecutionOptions.PasteGoal:
            # We just keep hitting the main page, and looking at the recent pastes from there
            try:
                res = self.GetRequest(self.CurrentUri)
            except:
                e = sys.exc_info()[0]
                print(" Error in Go, Failed to reach Pastebin.com! Trying Again...")
                self.Retries -= 1
                self.Go(url)
            bsoupAll = self.GetSoup(res)
            self.EnumerateRecentPastes(bsoupAll)

            # Wait before the next round so we don't DoS poor PasteBin =-D
            time.sleep(self.ExecutionOptions.ThrottleTime)




    # Simply returns a Beautiful Soup object
    def GetSoup(self, res):
        # Create the Beautiful Soup Object
        return bs4.BeautifulSoup(res.text, "html.parser")

    ## When given the url, returns the request.get obj
    def GetRequest(self, url):
        # Go grab the page
        res = requests.get(url)

        # Error checking
        try:
            res.raise_for_status()
        except Exception as exc:
            print('Error in IScraper: %s' % (exc))
            return

        return res

    """
    ------------------------ BEGIN SITE SPECIFIC CODE ------------------------
    # Code here is specific to the Site we're Parsing and Capturing from
    # When creating a new Scraper, edit code here to change it's function
    --------------------------------------------------------------------------
    """

    def SerializePublicPaste(self, url: str, bsoupAll: bs4.BeautifulSoup):

        title = self.GetTitle(url)
        # Catching where sometimes the Poster doesn't have this element.
        posterSelect = bsoupAll.select(".paste_box_frame > .paste_box_info > .paste_box_line1 > h1")
        if len(posterSelect) > 0:
            poster = posterSelect[0].text
        else:
            poster = "{Couldn't Serialize}"
        date = bsoupAll.select(".paste_box_frame > .paste_box_info > .paste_box_line2 > img > img > span")[0].attrs[
            'title']
        expires = \
            bsoupAll.select(".paste_box_frame > .paste_box_info > .paste_box_line2 > img > img")[0].contents[
                3].text.split(
                '\t')
        # Catching where sometimes the expiration date doesn't parse this way.
        if len(expires) > 3:
            expires = expires[4].replace('\r', '').replace('\n', '').replace(' ', '')
        else:
            expires = "UnParsed"

        # Build out the Raw URI using the title.
        rawURI = "http://www.pastebin.com/raw/" + title
        res = self.GetRequest(rawURI)
        bSoupRaw = self.GetSoup(res)

        # Assign Raw data
        raw = (bSoupRaw.text)

        if self.ExecutionOptions.isVerbose():
            fifth = int((len(raw)) / 5)
            self.PrintDebugTitle("Serializing [%s]" % (url))
            self.PrintDebugTitle("Paste Raw Snippet")
            try:
                # Print a fifth of the snippet, to gauge size offhand
                print(str(raw[0:fifth]))
            except:
                print(" Cannot Print Raw Paste Text, Unicode Error!!")

        # Creating the comb object to define the filters that match the paste
        comb = CoarseComb()
        matching = comb.CombText(raw)
        publicPaste = PublicPaste(url, poster, title, date, expires, raw, matches=matching)
        publicPaste.PasteLength = len(raw)
        # Store the largest paste to save later
        if publicPaste.PasteLength > self.LargestPaste.PasteLength:
            self.LargestPaste = publicPaste
        # Store the paste we serialized
        self.Items[title] = publicPaste

        # Save it to file right away
        IOFunctions.CapturePasteBinItem(self.Items[title], self.IOSettings)
        return

    def EnumerateRecentPastes(self, bsoupAll):

        # Grabs the list items (<li>) on the side for public pastes happening in real time.
        sideMenu = bsoupAll.select("#menu_2 > .right_menu > li")
        # We want to start from the oldest (bottom most) paste, so that we're grabbing newer pastes.
        sideMenu.reverse()
        # Start Digging into those pastes and Serialize them
        for tag in sideMenu:
            title = tag.contents[0].attrs['href'].replace('/', '')
            uri = Statics.PASTE_BIN_URI + tag.contents[0].attrs['href']
            # Don't bother enumerating Posts we've seen before.
            if title not in self.History:
                try:
                    res = self.GetRequest(uri)
                except:
                    e = sys.exc_info()[0]
                    print(" Error in EnumerateRecentPastes : " + str(e))
                    continue
                thisSoup = self.GetSoup(res)

                work = threading.Thread(self.SerializePublicPaste(uri, thisSoup), name="SerializePaste")
                work.start()
                # Reset the half time
                self.HaltTime = self.ExecutionOptions.HaltTime
                self.HaltAdjustInc = self.HaltAdjustIncOriginal
                # Add item to history to prevent duplicates
                self.History.append(title)
                time.sleep(self.ExecutionOptions.ThrottleTime)
            else:
                # Slow it down a bit...
                haltTime = self.HaltTime + self.HaltAdjustInc
                time.sleep(haltTime)
                if self.HaltAdjustInc < 1.0:
                    self.HaltAdjustInc += self.HaltAdjustInc
                else:
                    self.HaltAdjustInc = self.HaltAdjustInc / 5

                title = "! Already Tried {" + uri + "} - Waiting " + str(haltTime) + " seconds !"
                self.PrintDebugTitle(title)

        """
        # Handle the threads we started.
        # Make sure they all finished before moving on.
        workersAlive = True
        while workersAlive:
            workers = threading.enumerate()
            for work in workers:
                #work.join()
                if work.isAlive():
                    workersAlive = True
                elif not work.isAlive() :
                    workersAlive = False
        """

        # Finally done with this round
        return



    def PrepareStatsReport(self):
        self.PrintDebugTitle("Statistic Report for " + self.Name)
        print("Number of Pastes Scraped: "+ len(self.History))
        print("")

    """

    This mess was going to display the duration of execution. Perhaps one day...

    def PrintTime(self, tVal):
        finalString = "Elapsed Time: "

        if tVal.days > 0 and tVal.seconds > 3600 and tVal.minutes > 0 and tVal.seconds > 0:
            finalString += str(tVal.days) + " days, " + str(tVal.seconds / 3600) + " hours, " + str(tVal.seconds / 60) + " minutes, and " + str(tVal.seconds) + " seconds."
        # if tVal.hours and tVal.hours > 0 and tVal.minutes and tVal.minutes > 0 and tVal.seconds and tVal.seconds > 0:
        #    finalString = str(tVal.hours) + " hours, " + str(tVal.minutes) + " minutes, and " + str(tVal.seconds) + " seconds."
        if tVal.seconds > 3600 and tVal.minutes > 0 and tVal.seconds > 0:
            finalString += str(tVal.seconds / 3600) + " hours, " + str(tVal.seconds / 60) + " minutes, and " + str(tVal.seconds) + " seconds."
        if tVal.days > 0 and tVal.seconds > 3600 and tVal.minutes > 0 and tVal.seconds > 0:
            finalString += str(tVal.days) + " days, " + str(tVal.seconds / 3600) + " hours, " + str(
                tVal.seconds / 60) + " minutes, and " + str(tVal.seconds) + " seconds."

        print(finalString)

    """

    def PrintDebugTitle(self, text: str):
        output = "[> " + text + " <]"
        print(output.center(80, '~'))

    def GetTitle(self, url):
        return url.replace("http://pastebin.com/", '')

    def SavePaste(self, item: PublicPaste):
        IOFunctions.CapturePasteBinItem(item, self.IOSettings)
