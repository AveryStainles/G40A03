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
        

# parser.run_scraper("https://www.imdb.com/title/tt0111161/?ref_=chttp_t_1")
# MovieTriviaGame.parse_movie()

# parser.run_scraper("https://www.imdb.com/title/tt0111161/trivia/?ref_=tt_ov_ql_3")
# MovieTriviaGame.parse_trivia()
 
 
 
 
 
