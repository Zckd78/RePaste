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
        self.THROTTLE_TIME = 1
        self.HALT_TIME = 2

    def isDebug(self):
        if self.EXECUTION_MODE == "Live":
            return False
        else:
            return True

    def SetThrottleTime(self, secs):
        self.THROTTLE_TIME = secs

    def DetermineMode(self, params):
        if "-d" in params:
            self.EXECUTION_MODE = "Debug"
        else:
            self.EXECUTION_MODE = "Live"
