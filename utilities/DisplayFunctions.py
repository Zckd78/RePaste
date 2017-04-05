import data.Structs

def PrintTitle(text: str):
    output = "[> " + text + " <]"
    print(output.center(80, '-'))

def PrintOutLine(text: str):
    output = "[+]--> " + text
    print(output)

def PrintVerboseTitle(self, text: str):
    output = "[> " + text + " <]"
    print(output.center(80, '-'))


def PrintVerbose(options:data.Structs.ExecutionOption, text: str):
    if options.VerboseMode:
        PrintVerboseTitle(text)


def PrintDebugTitle(self, text: str):
    output = "[) " + text + " (]"
    print(output.center(80, '-'))


def PrintDebug(options:data.Structs.ExecutionOption, text: str):
    if options.DebugMode:
        PrintDebugTitle(text)