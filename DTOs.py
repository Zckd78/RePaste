## DTO stands for Data Transfer Objects.
## I use these as custom object for transporting data around in functions and files.

class Statics():
    PASTE_BIN_URI = "http://pastebin.com"


class IOSettings():
    def __init__(self, title, folder):
        self.Title = title
        self.StorageFolder = folder
        # Number of matching criteria in order to save.
        self.StorageThreshold = 0

    def SetStorageThreshold(self, val):
        if val >= 0:
            self.StorageThreshold = val


class ExecutionOption():
    def __init__(self):
        self.ExecutionMode = "Live"
        self.VerboseMode = True
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
        else:
            self.VerboseMode = False

    def DetermineMode(self, params):
        if "-d" in params:
            self.ExecutionMode = "Debug"
        else:
            self.ExecutionMode = "Live"
