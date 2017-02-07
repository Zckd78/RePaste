
class PublicPaste():

    def __init__(self,  url, poster, title, date, expires, raw, tag=None):
        self.Poster = poster
        self.Title = title
        self.Date = date
        self.Expires = expires
        self.Raw = raw
        self.Tag = tag
        self.Url = url

