from FileReadWriteHelper import *


class MovieTriviaGame:
    
    
    @staticmethod
    def parse_movie(directory: str = FileReadWriteHelper._directory_path, filename: str = FileReadWriteHelper._scraped_data_file_name):
        data = FileReadWriteHelper.read_data(directory, filename)
        for line in data:
            if ("Data: " in line): 
                FileReadWriteHelper.write_data(line)
    
    @staticmethod
    def parse_trivia(directory: str = FileReadWriteHelper._directory_path, filename: str = FileReadWriteHelper._scraped_data_file_name):
        pass
    
            
    @staticmethod
    def parse_top_25_movies(directory: str = FileReadWriteHelper._directory_path, filename: str = FileReadWriteHelper._scraped_data_file_name):
        data = FileReadWriteHelper.read_data(directory, filename)
        last_link: str | None = None
        target_line_counter = 6
        movie_counter = 0

        for line in data:
            if "Attr: href = /title/tt" in line and "_=chttp_t_" in line:
                last_link = line.replace("Attr: href = ", "https://www.imdb.com")
                FileReadWriteHelper.write_data(last_link)
                target_line_counter = 6
                
            elif (target_line_counter > 0  
                and last_link is not None 
                and "Data: " in line 
                and "Data: (" not in line 
                and "Data: )" not in line 
                and "Data: Rate" not in line 
                and "Data: Mark as watched" not in line):

                FileReadWriteHelper.write_data(line)
                target_line_counter -= 1
                if (target_line_counter == 0):
                    movie_counter += 1
                    test = "Data: #" + str(movie_counter)
                    FileReadWriteHelper.write_data(test, is_encoding=False)