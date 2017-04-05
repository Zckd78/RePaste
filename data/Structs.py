
class PublicPaste():
    def __init__(self,
                 url="",
                 poster="",
                 title="",
                 date="",
                 expires="",
                 raw="",
                 tag=None,
                 matches=None,
                 length=0
                 ):
        self.Poster = poster
        self.Title = title
        self.Date = date
        self.Expires = expires
        self.Raw = raw
        self.Tag = tag
        self.Url = url
        self.MatchingCriteria = matches
        self.PasteLength = length

class Statics():
    PASTE_BIN_URI = "http://pastebin.com"

class Statistics():
    def __init__(self):
        self.SavedPastes = 0
        self.RequestsMade = 0
        self.ErrorsEncountered = 0
        self.LargestPaste = ""

class IOSettings():
    def __init__(self, title, folder, threshold=0):
        self.Title = title
        self.StorageFolder = folder
        # Number of matching criteria in order to save.
        self.StorageThreshold = threshold

    def SetStorageThreshold(self, val):
        if val >= 0:
            self.StorageThreshold = val


class ExecutionOption():
    def __init__(self):
        self.ExecutionMode = "Live"
        self.DebugMode = False
        self.VerboseMode = False
        self.LoggingMode = True
        self.PasteGoal = 1000
        self.ThrottleTime = .2
        self.HaltTime = .5
        self.Retries = 5

    def isVerbose(self):
        if self.VerboseMode == True:
            return True
        else:
            return False

    def SetThrottleTime(self, secs):
        self.ThrottleTime = secs

    def SetHaltTime(self, secs):
        self.HaltTime = secs

    def SetPasteGoal(self, goal):
        self.PasteGoal = goal

    def DetermineVerbose(self, params):
        if "-v" in params:
            self.VerboseMode = True
            print("---{ Activating Verbose Output }---")
        else:
            self.VerboseMode = False

    def DetermineMode(self, params):
        if "-d" in params:
            self.DebugMode = True
            print("---{ Activating Debug Output }---")
        else:
            self.DebugMode = False

        if "-d" in params:
            self.DebugMode = True
            print("---{ Logging Output  }---")
        else:
            self.DebugMode = False
