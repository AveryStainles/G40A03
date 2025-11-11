from pathlib import Path

class FileReadWriteHelper:
    _file_name: str = "parsed_data.txt"
    _scraped_data_file_name: str = "temp.txt"
    _directory_path: str = "./MovieTrivia/Data"
    _file_path: Path = Path(f"{_directory_path}/{_file_name}")
        
        
    @staticmethod
    def write_data(message: str, directory_path: str = _directory_path, file_name: str = _file_name, is_encoding: bool = True) -> None:
        file_path: Path = Path(f"{directory_path}/{file_name}")
        file = open(file_path, "a")
        file.write(f"{message.encode("ascii", "ignore") if (is_encoding) else message.strip()}\n".replace("b\"b\'", "").replace("\'\"", "").replace(" ,", ",").strip() + "\n")
            
    @staticmethod
    def read_data(directory_path: str = _directory_path, file_name: str = _file_name) -> list[str] | None:
        file_path: Path = Path(f"{directory_path}/{file_name}")
        
        if (not file_path.is_file()):
            return
        
        content: list[str] = []        
        file = open(file_path, "r")
        for task_as_string in file.readlines():
            content.append(task_as_string.strip())
        file.close()
        
        return content
    
    
    
    
    
    
    
    # DATA EXAMPLE
# =================================================

# content_link: https://www.imdb.com/title/tt0468569/?ref_=chttp_t_3
# title:            Data: 3. The Dark Knight
# year:             2008
# runtime:          2h 32m
# content_rating: PG-13
# score:            9.1
# views:            3.1M
# rating:           #3

# Director: Frank Darabont
# trivia_link: https://www.imdb.com/title/tt0111161/trivia/?ref_=tt_ov_ql_3
# cast: 
#   - Tim Robbins
#   - Morgan Freeman
#   - Bob Gunton
#   - William Sadler
#   - Clancy Brown
#   - Gil Bellows
#   - Mark Rolston
#   - James Whitmore
#   - Jeffrey DeMunn
#   - Larry Brandenburg

# Question: Andy and Reds opening chat in the prison yard, in which Red is throwing a baseball, took nine hours to shoot because director _ _ _ _ _   _ _ _ _ _ _ _ _ insisted on many takes of the scene before he was satisfied. _ _ _ _ _ _   _ _ _ _ _ _ _ threw the baseball for the entire nine hours without a word of complaint. He showed up for work the next day with his left arm in a sling.
# - Frank Darabont
# - Morgan Freeman
