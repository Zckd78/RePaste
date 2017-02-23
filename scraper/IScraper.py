import bs4
from data.Structs import *

"""
Originally I had this file the standard class for extracting from PasteBin, but decided to overwrite it with classes
that inherit from this one. I could then use dependency injection to fire off any type of Scraper
"""


class IScraper():
    def __init__(self, options: ExecutionOption):
        self.Name = "PasteBinScraper"
        self.Items = {}
        self.ExecutionOptions = options

    def Go(self, url, forceEnum=False):
        return

    def SerializePublicPaste(self, url, bsoupAll: bs4.BeautifulSoup):
        return

    def DetermineDir(self, url):
        return

    def EnumerateRecentPastes(self, bsoupAll):
        return

    def GetSoup(self, res):
        return

    def GetRequest(self, url):
        return

    def PrintDebugTitle(self, text: str):
        print(text.center(80, '-'))
