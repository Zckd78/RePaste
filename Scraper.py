import bs4
import requests
from PasteObj import *
import re
from DTOs import *
import os
import threading


class Scraper():
    def __init__(self, options: ExecutionOption):
        self.Name = "PasteBinScraper"
        self.Items = {}
        self.ExecutionOptions = options

    def Go(self, url, forceEnum=False):

        res = self.GetRequest(url)
        bsoupAll = self.BuildSoup(res)

        # Zero means we're in the PasteBin Index
        if self.DetermineDir(url) == 0 or forceEnum:
            self.EnumerateRecentPastes(bsoupAll)
        else:
            self.SerializePublicPaste(url, bsoupAll)


    def SerializePublicPaste(self, url, bsoupAll: bs4.BeautifulSoup):

        title = url.split('/')[3]
        # We only want new pastes
        if title not in self.Items:

            # Serialize the items on page into objects
            poster = bsoupAll.select(".paste_box_frame > .paste_box_info > .paste_box_line1 > h1")[0].text
            date = bsoupAll.select(".paste_box_frame > .paste_box_info > .paste_box_line2 > img > img > span")[0].attrs[
                'title']
            expires = \
                bsoupAll.select(".paste_box_frame > .paste_box_info > .paste_box_line2 > img > img")[0].contents[
                    3].text.split(
                    '\t')[4].replace('\r', '').replace('\n', '').replace(' ', '')
            raw = bsoupAll.select(".paste_code")[0].text

            if self.ExecutionOptions.isDebug():
                fifth = int((len(raw)) / 5)
                title = "Serializing [%s]" % (url)
                title = title.center(100, '-')
                print(title)
                print("Paste Raw Snippet".center(100, '-'))
                print(raw[0:fifth])

            self.Items[title] = PublicPaste(url, poster, title, date, expires, raw)
        else:
            if self.ExecutionOptions.isDebug():
                print("\r\nAlready Serialized [%s]\r\n" % (url))
            return

    # Quick check to see if we're still on the Index of Pastebin, or a Public Paste
    def DetermineDir(self, url):
        dirEnum = {'Home': 0, 'Paste': 1}
        if url == Statics.PASTE_BIN_URI:
            return dirEnum['Home']
        else:
            return dirEnum['Paste']

    def EnumerateRecentPastes(self, bsoupAll):

        # Grabs the list items (<li>) on the side for public pastes happening in real time.
        sideMenu = bsoupAll.select("#menu_2 > .right_menu > li")
        # We want to start from the oldest (bottom most) paste, so that we're grabbing newer and newer pastes.
        sideMenu.reverse()
        # Start Digging into those pastes and Serialize them
        for tag in sideMenu:
            uri = Statics.PASTE_BIN_URI + tag.contents[0].attrs['href']
            work = threading.Thread(self.Go(uri))
            work.start()

    def BuildSoup(self, res):
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
            print('Error in Scraper: %s' % (exc))
            return

        return res
