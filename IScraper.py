import bs4
import requests
from PasteObj import *
import re
from DTOs import *
import os
import threading

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

    def BuildSoup(self, res):
        return

    ## When given the url, returns the request.get obj
    def GetRequest(self, url):
        return
