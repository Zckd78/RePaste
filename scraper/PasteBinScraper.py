from scraper.CoarseComb import *
from data.Structs import *
import datetime
import sys
import time
import requests
import bs4
import threading
import codecs
from utilities import IOFunctions, DisplayFunctions

class PasteBinScraper():
    Retries = 5

    def __init__(self, exOptions: ExecutionOption, ioSet: IOSettings):
        self.Name = "PasteBin.com"
        self.CurrentUri = ""
        self.Items = {}
        self.History = []
        self.OutputLog = ""
        self.Interrupt = False
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
        # Display and Save starting time
        startTime = "Started on: " + time.ctime() + "\n"
        self.OutputLog += startTime
        print(startTime)
        self.CurrentUri = url

        # Go so many rounds
        while len(self.Items) <= self.ExecutionOptions.PasteGoal:
            # We just keep hitting the main page, and looking at the recent pastes from there
            if self.Retries > 0:
                try:
                    res = self.GetRequest(self.CurrentUri)
                except Exception as excpt:
                    print(" Error in Go, Failed to reach %s Trying Again..." % self.Name)
                    self.Retries -= 1
                    self.Go(url)
                if res is not None:
                    bsoupAll = self.GetSoup(res)
                    self.EnumerateRecentPastes(bsoupAll)
                    # Catch when we've interrupted the program with Ctrl+C
                    if self.Interrupt:
                        return
            else:
                print(" Halting Go(), unable to reach %s -> SHUTTING DOWN!" % self.Name)
                break

            # Wait before the next round so we don't DoS poor PasteBin =-D
            time.sleep(self.ExecutionOptions.ThrottleTime)
        self.PrepareStatsReport()
        return


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
            print('Error in PasteBin Scraper: %s' % (exc))
            res = None
            return res

        return res

    """
    ------------------------ BEGIN SITE SPECIFIC CODE ------------------------
    # Code here is specific to the Site we're Parsing and Capturing
    # When creating a new Scraper, edit code here to change it's function
    --------------------------------------------------------------------------
    """

    def SerializePublicPaste(self, url: str, bsoupAll: bs4.BeautifulSoup):

        pasteID = self.GetPasteID(url)
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
        rawURI = "http://www.pastebin.com/raw/" + pasteID
        res = self.GetRequest(rawURI)

        # Sometimes we fail to get the page at this point. Just return, and we can do the next one.
        if res is None:
            return

        bSoupRaw = self.GetSoup(res)

        # Assign Raw data
        raw = bSoupRaw.text
        fifth = int((len(raw)) / 5)

        # Print a fifth of the snippet, to gauge size offhand
        DisplayFunctions.PrintVerbose(self.ExecutionOptions, "Paste Raw Snippet")
        DisplayFunctions.PrintVerbose(self.ExecutionOptions,str(raw[0:fifth]))

        # Creating the comb object to define the filters that match the paste
        comb = CoarseComb()
        matching = comb.CombText(raw)
        publicPaste = PublicPaste(url, poster, pasteID, date, expires, raw, matches=matching)
        publicPaste.PasteLength = len(raw)
        # Store the largest paste to save later
        if publicPaste.PasteLength > self.LargestPaste.PasteLength:
            self.LargestPaste = publicPaste
        # Store the paste we serialized
        self.Items[pasteID] = publicPaste

        # Display the paste
        self.OutputResults(publicPaste)

        # Save it to file right away
        IOFunctions.CapturePasteBinItem(self.Items[pasteID], self.IOSettings)
        return

    def EnumerateRecentPastes(self, bsoupAll):
        try:
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
                    except Exception:
                        e = sys.exc_info()[0]
                        print(" Error in EnumerateRecentPastes : " + str(e))
                        continue
                    except KeyboardInterrupt:
                        self.Interrupt = True
                        return

                    if res is not None:
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
                        continue
                else:
                    # Slow it down a bit...
                    haltTime = self.HaltTime + self.HaltAdjustInc
                    time.sleep(haltTime)
                    if self.HaltAdjustInc < 1.0:
                        self.HaltAdjustInc += self.HaltAdjustInc
                    else:
                        self.HaltAdjustInc = self.HaltAdjustInc / 5
                    #
                    title = "Already Tried [ " + uri + " ] - Waiting " + str(haltTime) + " seconds"
                    DisplayFunctions.PrintDebug(self.ExecutionOptions, title)

            # Finally done with this round
        except KeyboardInterrupt:
            self.Interrupt = True
            return

        return

    def PrepareStatsReport(self):
        if self.Name and len(self.History) >= 1:
            print("\n\n")
            title = "[> Statistic Report for " + self.Name + "<]"
            DisplayFunctions.PrintTitle(title.center(80,'-'))
            print("Number of Pastes Scraped: "+ str(len(self.History)))
            print("Largest Paste Scraped: [ " + self.LargestPaste.PasteID + " ] { Size: " + str(len(self.LargestPaste.Raw)) + " }")

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

    def OutputResults(self, paste:PublicPaste):

        # Give some feedback
        outline = "Serialized [ " + paste.Url + " ]"

        # Display Title, if it's not the default
        outline += "{ Title: " + paste.Title

        # Display Length of the paste
        outline += ", Size: " + str(len(paste.Raw))

        # Display Matching criteria
        if len(paste.MatchingCriteria) >= 1:
            outline += ", Matches: "
            count = 0
            for match in paste.MatchingCriteria:
                if match == paste.MatchingCriteria[0] and count == 0:
                    outline += match
                    count += 1
                else:
                    outline += ", " + match

        outline += " } \n"
        DisplayFunctions.PrintOutLine(outline)
        self.OutputLog += outline

    def GetPasteID(self, url):
        return url.replace("http://pastebin.com/", '')

    def SavePaste(self, item: PublicPaste):
        IOFunctions.CapturePasteBinItem(item, self.IOSettings)

