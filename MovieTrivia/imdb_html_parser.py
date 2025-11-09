from html.parser import HTMLParser
from FileReadWriteHelper import *
from MovieTriviaGame import *

from urllib import request


class ImdbHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.__data = None
        self.__tag = None
        self.__tag_attrs = None

    def handle_starttag(self, tag, attrs):
        FileReadWriteHelper.write_data(f"Start Tag: {tag}", FileReadWriteHelper._directory_path, FileReadWriteHelper._scraped_data_file_name)
        self.__tag = tag
        self.__tag_attrs = dict(attrs)
        for attr in attrs:
            attrName, attrValue = attr
            FileReadWriteHelper.write_data(f"    Attr: {attrName} = {attrValue}", FileReadWriteHelper._directory_path, FileReadWriteHelper._scraped_data_file_name)
            
        if self.__tag == "a" and self.__tag_attrs and self.__tag_attrs.get('class') == "ipc-title-link":
            href = self.__tag_attrs.get('href')
            FileReadWriteHelper.write_data(f"    Link: {href}", FileReadWriteHelper._directory_path, FileReadWriteHelper._scraped_data_file_name)

    def handle_endtag(self, tag):
        FileReadWriteHelper.write_data(f"End Tag: {tag}", FileReadWriteHelper._directory_path, FileReadWriteHelper._scraped_data_file_name)

    def handle_data(self, data):
        if self.__tag == "script":
            return
        if self.__tag == "h3" and self.__tag_attrs and self.__tag_attrs['class'] == "ipc-title__text":
            FileReadWriteHelper.write_data(f"==================== Movie Title: {data}", FileReadWriteHelper._directory_path, FileReadWriteHelper._scraped_data_file_name)
        FileReadWriteHelper.write_data(f"    Data: {data}", FileReadWriteHelper._directory_path, FileReadWriteHelper._scraped_data_file_name)

    def unknown_decl(self, data):
        FileReadWriteHelper.write_data(f"Unknown: {data}", FileReadWriteHelper._directory_path, FileReadWriteHelper._scraped_data_file_name)
        
    def run_scraper(self, url: str):
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
    
parser = ImdbHTMLParser()

# parser.run_scraper("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
# MovieTriviaGame.parse_top_25_movies()

parser.run_scraper("https://www.imdb.com/title/tt0050083/?ref_=chttp_t_5")
MovieTriviaGame.parse_top_25_movies()

 
 
 
 
 
 
