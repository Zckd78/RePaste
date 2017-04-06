import data.Structs

def PrintTitle(text: str):
    output = "[> " + text + " <]"
    SafePrint(output.center(80, '-'))

def PrintOutLine(text: str):
    output = "[+]--> " + text
    SafePrint(output)

def PrintVerboseTitle(text: str):
    output = "[> " + text + " <]"
    SafePrint(output.center(80, '-'))

def PrintVerbose(options:data.Structs.ExecutionOption, text: str):
    if options.VerboseMode:
        PrintVerboseTitle(text)

def PrintDebugOutline(text: str):
    output = "[!]--> " + text
    SafePrint(output)

def PrintDebug(options:data.Structs.ExecutionOption, text: str):
    if options.DebugMode:
        PrintDebugOutline(text)

# Had to write this because sometime we get non-utf-8 chars, so we print that encoded.
def SafePrint(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        print("[!]--> {Unicode Error happened, printing UTF-8 Instead..}")
        print(StripNonUnicode(text))

def UniCode(text: str):
    return str(text.encode("utf-8"))

def StripNonUnicode(text):
    return text.encode('ascii', 'ignore')