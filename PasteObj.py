class PublicPaste():
    def __init__(self, url, poster=None, title=None, date=None, expires=None, raw=None, tag=None):
        self.Poster = poster
        self.Title = title
        self.Date = date
        self.Expires = expires
        self.Raw = raw
        self.Tag = tag
        self.Url = url
