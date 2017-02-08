from IScraper import *
import DTOs


class PasteBinScraper(IScraper):
    def __init__(self, options: ExecutionOption):
        self.Name = "PasteBinIScraper"
        self.Items = {}
        self.ExecutionOptions = options

    ## Root Function - Navigates to a page, and decides what to do from there.
    def Go(self, url, forceEnum=False):
        # Zero means we're on the Index page
        if self.DetermineDir(url) == 0 or forceEnum:
            res = self.GetRequest(url)
            bsoupAll = self.BuildSoup(res)
            self.EnumerateRecentPastes(bsoupAll)
        else:
            title = url.split('/')[3]
            # We only want new pastes
            if title not in self.Items:
                res = self.GetRequest(url)
                bsoupAll = self.BuildSoup(res)
                self.SerializePublicPaste(url, bsoupAll)
            else:
                if self.ExecutionOptions.isDebug():
                    title = "! Already Tried {" + url + "} - Waiting " + str(self.ExecutionOptions.HALT_TIME) + " seconds !"
                    self.PrintDebugTitle(title)
                    time.sleep(self.ExecutionOptions.HALT_TIME)

    def SerializePublicPaste(self, url, bsoupAll: bs4.BeautifulSoup):

        title = url.split('/')[3]
        # Serialize the items on page into objects
        poster = bsoupAll.select(".paste_box_frame > .paste_box_info > .paste_box_line1 > h1")[0].text
        date = bsoupAll.select(".paste_box_frame > .paste_box_info > .paste_box_line2 > img > img > span")[0].attrs[
            'title']
        expires = \
            bsoupAll.select(".paste_box_frame > .paste_box_info > .paste_box_line2 > img > img")[0].contents[
                3].text.split(
                '\t')
        # Catching where sometimes the expiration date doesn't parse this way.
        if len(expires) > 3:
            expires = expires[4].replace('\r', '').replace('\n', '').replace(' ', '')
        else:
            expires = "UnParsed"
        raw = (bsoupAll.select(".paste_code")[0].text)

        if self.ExecutionOptions.isDebug():
            fifth = int((len(raw)) / 5)
            self.PrintDebugTitle("Serializing [%s]" % (url))
            self.PrintDebugTitle("Paste Raw Snippet")
            try:
                print(str(raw[0:fifth]))
            except:
                e = sys.exc_info()[0]
                print(" Error in PasteBinScraper : " + str(e))

        self.Items[title] = PublicPaste(url, poster, title, date, expires, raw)

        return

    # Quick check to see if we're still on the Index of Pastebin, or a Public Paste
    def DetermineDir(self, url):
        dirEnum = {'Home': 0, 'Paste': 1}
        if url == Statics.PASTE_BIN_URI:
            return dirEnum['Home']
        else:
            return dirEnum['Paste']

    def EnumerateRecentPastes(self, bsoupAll):

        # Grabs the list items (<li>) on the side for public pastes happening in real time.
        sideMenu = bsoupAll.select("#menu_2 > .right_menu > li")
        # We want to start from the oldest (bottom most) paste, so that we're grabbing newer and newer pastes.
        sideMenu.reverse()
        # Start Digging into those pastes and Serialize them
        for tag in sideMenu:
            uri = Statics.PASTE_BIN_URI + tag.contents[0].attrs['href']
            work = threading.Thread(self.Go(uri))
            work.start()
            time.sleep(self.ExecutionOptions.THROTTLE_TIME)

    def BuildSoup(self, res):
        # Create the Beautiful Soup Object
        return bs4.BeautifulSoup(res.text, "html.parser")

    ## When given the url, returns the request.get obj
    def GetRequest(self, url):
        # Go grab the page
        res = requests.get(url)

        # Error checking
        try:
            res.raise_for_status()
        except Exception as exc:
            print('Error in IScraper: %s' % (exc))
            return

        return res

    def PrintDebugTitle(self, text: str):
        output = "[> " + text + " <]"
        print(output.center(80, '~'))
