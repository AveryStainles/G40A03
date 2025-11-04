from html.parser import HTMLParser

from urllib import request

class ImdbHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.__data = None
        self.__tag = None
        self.__tag_attrs = None

    def handle_starttag(self, tag, attrs):
        print(f"Start Tag: {tag}")
        self.__tag = tag
        self.__tag_attrs = dict(attrs)
        for attr in attrs:
            attrName, attrValue = attr
            print(f"    Attr: {attrName} = {attrValue}")

        if self.__tag == "a" and self.__tag_attrs and self.__tag_attrs.get('class') == "ipc-title-link":
            href = self.__tag_attrs.get('href')
            print(f"    Link: {href}")

    def handle_endtag(self, tag):
        print(f"End Tag: {tag}")

    def handle_data(self, data):
        if self.__tag == "script":
            return
        if self.__tag == "h3" and self.__tag_attrs and self.__tag_attrs['class'] == "ipc-title__text":
            print(f"==================== Movie Title: {data}")
        print(f"    Data: {data}")

    def unknown_decl(self, data):
        print("Unknown", data)


parser = ImdbHTMLParser()

url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept": "text/html",
}
req = request.Request(url, headers=headers)
with request.urlopen(req) as resp:
    lines = list(line.decode("utf-8").strip() for line in resp.readlines())

for each_line in lines:
    parser.feed(each_line)

