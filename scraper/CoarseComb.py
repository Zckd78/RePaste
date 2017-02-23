import re


class CoarseComb():
    FilterList = [
        'User_Pass',
        'IP_Addr',
        'URL',
        'Bash_Script',
        'PHP_Code',
        'PHP_Eval',
        'Python_Code',
        'Cpp_Code'
    ]

    def __init__(self):
        self.MatchingCriteria = []

    def CombText(self, text: str):
        self.InspectedText = text

        # Matches User/Pass
        if "username" in self.InspectedText or "password" in self.InspectedText:
            self.MatchingCriteria.append(self.FilterList[0])
        # Attempting to match user:pass type pastes
        pattern = re.compile("\w[:]\w")
        result = pattern.search(self.InspectedText)
        if result:
            self.MatchingCriteria.append(self.FilterList[1])

        # Search for IPs without Port numbers
        pattern = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        result = pattern.search(self.InspectedText)
        if result:
            self.MatchingCriteria.append(self.FilterList[1])

        # Search for IPs with Port numbers
        pattern = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,5}")
        result = pattern.search(self.InspectedText)
        if result:
            self.MatchingCriteria.append(self.FilterList[1])

        # Matches URL
        pattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        result = pattern.search(self.InspectedText)
        if result:
            self.MatchingCriteria.append(self.FilterList[2])

        # Matches Bash Scripting
        if "#!/bin/bash" in self.InspectedText:
            self.MatchingCriteria.append(self.FilterList[3])

        # Matches PHP Code Marker
        if "<?php" in self.InspectedText:
            self.MatchingCriteria.append(self.FilterList[4])

        # Matches PHP eval( Markers
        if "eval(base64_decode(" in self.InspectedText or "eval(" in self.InspectedText:
            self.MatchingCriteria.append(self.FilterList[5])

        # Matches Python code
        if "import " in self.InspectedText or "#!/usr/bin/python" in self.InspectedText:
            self.MatchingCriteria.append(self.FilterList[6])

        # Matches C++ #include code
        if "#include" in self.InspectedText:
            self.MatchingCriteria.append(self.FilterList[7])

        return self.MatchingCriteria
