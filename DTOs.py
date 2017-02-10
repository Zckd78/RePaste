## DTO stands for Data Transfer Objects.
## I use these as custom object for transporting data around in functions and files.

class Statics():
    PASTE_BIN_URI = "http://pastebin.com"


class IOSettings():
    def __init__(self, title, folder):
        self.Title = title
        self.StorageFolder = folder



class ExecutionOption():

    def __init__(self):
        self.EXECUTION_MODE = "Live"
        self.VERBOSE_MODE = True
        self.THROTTLE_TIME = .2
        self.HALT_TIME = .5

    def isVerbose(self):
        if self.VERBOSE_MODE == True:
            return True
        else:
            return False

    def SetThrottleTime(self, secs):
        self.THROTTLE_TIME = secs

    def SetHaltTime(self, secs):
        self.HALT_TIME = secs

    def DetermineVerbose(self, params):
        if "-v" in params:
            self.VERBOSE_MODE = True
        else:
            self.VERBOSE_MODE = False

    def DetermineMode(self, params):
        if "-d" in params:
            self.EXECUTION_MODE = "Debug"
        else:
            self.EXECUTION_MODE = "Live"
