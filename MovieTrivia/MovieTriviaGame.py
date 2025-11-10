from FileReadWriteHelper import *


class MovieTriviaGame:
    
    
    @staticmethod
    def parse_movie(directory: str = FileReadWriteHelper._directory_path, filename: str = FileReadWriteHelper._scraped_data_file_name):
        data = FileReadWriteHelper.read_data(directory, filename)
        director = None
        trivia_link = None
        is_looking_at_cast = False
        cast: list[str] = []
        
        for line in data:
            # Directed by  
            if (director is None and "Directed by " in line):
                director = line[line.index("Directed by ")+len("Directed by "):]
                director = director[:director.index(".")]
                FileReadWriteHelper.write_data("Director: " + director, is_encoding=False)
            
            # Link to trivia 
            if (trivia_link is None and "Attr: href = /title/tt" in line and "/trivia/" in line): 
                trivia_link = line
                FileReadWriteHelper.write_data(trivia_link.replace("Attr: href = ", "https://www.imdb.com"))
                
            
            # Add cast members 
            if ("?ref_=tt_cst_t_" in line):
                is_looking_at_cast = True
                
            if (is_looking_at_cast and len(cast) < 10 and "Data: " in line):
                cast_member: str = line.replace("Data: ", "")
                cast.append(cast_member)
                FileReadWriteHelper.write_data(cast_member)
                is_looking_at_cast = False
                
    
    @staticmethod
    def parse_trivia(directory: str = FileReadWriteHelper._directory_path, filename: str = FileReadWriteHelper._scraped_data_file_name):
        # Attr: class = ipc-html-content-inner-div
        data = FileReadWriteHelper.read_data(directory, filename)
        trivia_questions: list[str] = []
        actor_names: list[str] = []
        hold_trivia_question: str = ""
        movie_counter = 0
        
        is_trivia_question = False
        is_a_tag = False
        
        # Add trivia questions
        for line in data:
            if "Attr: class = ipc-html-content-inner-div" in line:
                is_trivia_question = True
            
            if not is_trivia_question:
                continue            
            
            if "End Tag: div" in line:
                is_trivia_question = False
                parsed_data = hold_trivia_question.replace("\"", "").replace("\\", "").replace("\'", "").replace(" b ", "").replace("_           ", "").replace("      ", " ")[1:-2].strip()
                trivia_questions.append(parsed_data)
                hold_trivia_question = ""
                movie_counter += 1
            
            # Flag for getting trivia names
            if "Start Tag: a" in line:
                is_a_tag = True
            elif "End Tag: a" in line:
                is_a_tag = False
            
            # Add trivia names and questions 
            if(is_a_tag and "Data: " in line):
                parsed_line = line.replace("Data: ", "")
                actor_names.append(f"{movie_counter}:{parsed_line}")
                hold_trivia_question += ''.join('_ ' if val.lower() in "abcdefghijklmnopqrstuvwxyz" else "  " for val in parsed_line)
            elif ("Data: " in line):
                hold_trivia_question += line.replace("Data: ", "")


        trivia_answers = []
        for actor in actor_names:
            trivia_answers.append(
            {
                "trivia_question_index": int(actor[:actor.index(":")]),
                "actor": actor[4:].strip().replace("\'", "")
            })

        for index, question in enumerate(trivia_questions):
            FileReadWriteHelper.write_data("Question: " + question, is_encoding=False)
            [FileReadWriteHelper.write_data("   - " + answer["actor"], is_encoding=False) for answer in trivia_answers if int(answer["trivia_question_index"]) == index]
            
    
            
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