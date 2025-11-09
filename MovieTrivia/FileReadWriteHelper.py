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
        if (is_encoding):
            file.write(f"{message.encode("ascii", "ignore")}\n".replace("b\"b\'", "").replace("\'\"", "").strip() + "\n")
        else:
            file.write(f"{message.strip()}\n")    
            
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