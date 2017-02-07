
class Statics():

    PASTE_BIN_URI = "http://pastebin.com"

class ExecutionOption():

    EXECUTION_MODE = "Live"

    def __init__(self):
        self.EXECUTION_MODE = "Live"

    def isDebug(self):
        if self.EXECUTION_MODE == "Live":
            return False
        else:
            return True

    def DetermineMode(self, params):
        if "-d" in params:
            self.EXECUTION_MODE = "Debug"
        else:
            self.EXECUTION_MODE = "Live"