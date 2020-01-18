class PastebinContent(object):
    def __init__(self,
                 author: str,
                 title: str,
                 content: str,
                 date: str):
        self.date = date
        self.content = content
        self.title = title
        self.author = author
