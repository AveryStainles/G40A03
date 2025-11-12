from FileReadWriteHelper import *
from imdb_html_parser import *
from Models.Movie import Movie


class MovieTriviaGame:
    _movie_title = None
    _url_parser = ImdbHTMLParser()
    
    @staticmethod
    def run_scraper(url: str):
        FileReadWriteHelper.clear_data()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept": "text/html",}

        req = request.Request(url, headers=headers)
        with request.urlopen(req) as resp:
            lines = list(line.decode("utf-8").strip() for line in resp.readlines())
            for each_line in lines:
                MovieTriviaGame._url_parser.feed(each_line)

    
    #  Parses a single movie title
    @staticmethod
    def parse_movie(movie: Movie, directory: str = FileReadWriteHelper._directory_path, filename: str = FileReadWriteHelper._scraped_data_file_name):
        MovieTriviaGame.run_scraper(movie.content_link)
        data = FileReadWriteHelper.read_data(directory, filename)
        is_looking_at_cast = False
        
        for line in data:
            # Directed by  
            if (movie.director is "" and "Directed by " in line):
                director = line[line.index("Directed by ")+len("Directed by "):]
                director = director[:director.index(".")]
                movie.director = director[:-1].strip()
            
            # Link to trivia 
            if (movie.trivia_link is "" and "Attr: href = /title/tt" in line and "/trivia/" in line): 
                movie.trivia_link = line.replace("Attr: href = ", "https://www.imdb.com")[2:-1].strip()
            
            # Add cast members 
            if ("?ref_=tt_cst_t_" in line):
                is_looking_at_cast = True
                
            if (is_looking_at_cast and len(movie.cast_members) < 10 and "Data: " in line):
                movie.cast_members.append(line.replace("Data: ", "")[2:-1].strip())
                is_looking_at_cast = False
    
        return movie
        
    
    @staticmethod
    def parse_trivia(movie:Movie, directory: str = FileReadWriteHelper._directory_path, filename: str = FileReadWriteHelper._scraped_data_file_name):
        MovieTriviaGame.run_scraper(movie.trivia_link)
        data = FileReadWriteHelper.read_data(directory, filename)
        trivia_questions: list[str] = []
        actor_names: list[str] = []
        hold_trivia_question: str = ""
        movie_counter = 0
        
        is_trivia_question = False
        is_a_tag = False
        
        # Add trivia questions
        for line in data:
            # We found a trivia question
            if "Attr: class = ipc-html-content-inner-div" in line:
                is_trivia_question = True
            
            if not is_trivia_question:
                continue            
            
            # Complete trivia question
            if "End Tag: div" in line:
                is_trivia_question = False
                parsed_data = hold_trivia_question.replace("\"", "").replace("\\", "").replace("\'", "").replace(" b ", "").replace("_           ", "").replace("      ", " ").replace("    .", ".").replace("     :", ":")[1:].strip()
                trivia_questions.append(parsed_data)
                hold_trivia_question = ""
                movie_counter += 1
            
            # Flag for getting trivia names
            if "Start Tag: a" in line:
                is_a_tag = True
            elif "End Tag: a" in line:
                is_a_tag = False
            
            # Add trivia answers and questions 
            if(is_a_tag and "Data: " in line):
                parsed_line = line.replace("Data: ", "")
                actor_names.append(f"{movie_counter}:{parsed_line}")
                hold_trivia_question += ''.join('_ ' if val.lower() in "abcdefghijklmnopqrstuvwxyz" else "  " for val in parsed_line)
            elif ("Data: " in line):
                hold_trivia_question += line.replace("Data: ", "")


        trivia_answers = {}
        for actor in actor_names:
            index = int(actor[:actor.index(":")])
            data = actor[4:].strip().replace("\'", "")
            if (index in trivia_answers.keys()):
                trivia_answers[index].append(data)
            else:
                trivia_answers[index] = [data]

        for index in trivia_answers.keys():
            actors = trivia_answers[index]
            movie.trivia_questions.append((trivia_questions[index], list(actors)))

            
    @staticmethod
    def parse_top_25_movies(directory: str = FileReadWriteHelper._directory_path, filename: str = FileReadWriteHelper._scraped_data_file_name, url: str = "https://www.imdb.com/chart/top/?ref_=nv_mv_250") -> list[Movie]:
        # Setup .txt files with parsed data
        _movies = []
        MovieTriviaGame.run_scraper(url)

        parsed_data = []
        data = FileReadWriteHelper.read_data(directory, filename)
        last_link: str | None = None
        target_line_counter = 6
        movie_counter = 0

        for line in data:
            # Enough data was collected for a Movie object to be created
            if (len(parsed_data) == 7):
                model = Movie()
                model.set_movie_id(len(_movies))
                model.set_title(parsed_data[0]) 
                model.set_year(parsed_data[1])
                model.set_runtime(parsed_data[2])
                model.set_content_rating(parsed_data[3])
                model.set_score(parsed_data[4])
                model.set_views(parsed_data[5])
                model.set_rating(parsed_data[6])
                model.set_content_link(last_link[2:-1].strip())
                _movies.append(model)
                parsed_data = []
            
            # Find the link to the movie title
            if "Attr: href = /title/tt" in line and "_=chttp_t_" in line:
                last_link = line.replace("Attr: href = ", "https://www.imdb.com")
                target_line_counter = 6
                
            # Get a set amount of data | The rest was not useful
            elif (target_line_counter > 0  
                and last_link is not None 
                and "Data: " in line 
                and "Data: (" not in line 
                and "Data: )" not in line 
                and "Data: Rate" not in line 
                and "Data: Mark as watched" not in line):

                # All parsed data is added to a list and is mapped to an object by index at the end of this method
                parse_data = line[line.index("Data:")+len("Data:"):-1].strip()
                parsed_data.append("N/A" if parse_data is None and len(parse_data) == 0 else parse_data)
                
                # All data for this movie has been collected. Add parsed content to list and stop tracking
                target_line_counter -= 1
                if (target_line_counter == 0):
                    movie_counter += 1
                    parsed_data.append(str(movie_counter))
        
        return _movies


    @staticmethod
    def missing_property_trivia(movie: Movie, trivia_questions: list[(str, list[str])]):
        
        # Parse property names
        properties = [property for property in dir(Movie) 
            if not (property.startswith("__") and property.endswith("__")) 
                and not (property.startswith("set_") 
                    or property.startswith("get_") 
                    or property.startswith("add_") 
                    or property.endswith("_link") 
                    or property.endswith("_id")
                    or "trivia" in property)]
        
        question: str = "With the provided information below, fill in the missing data:<>"

        # Setup a missing property question where each property can make 1 question
        for missing_property_index in range(len(properties)):
            question_options: str = ""
            answers: list[str] = []
            
            # exception case
            if properties[missing_property_index] == "cast_members":
                question_options += f"<>{"Name of a cast member: "}"
                answers = movie.cast_members
            
            for index, property_name in enumerate(properties):
                property_value = getattr(movie, property_name)
                parsed_name = property_name.capitalize().replace("_", " ")
                
                # exception case
                if property_name == "cast_members":
                    continue
                
                # Setup question options
                question_options += f"<>{parsed_name}: "
                
                # Set the answer for the given permutation
                if index == missing_property_index:
                    answers.append(property_value.lower())
                    continue
                
                # Display the property value because it is not the answer for this question
                question_options += f"{property_value}"
            
            trivia_questions.append((question + question_options, answers))
    


                    
# https://www.imdb.com/title/tt0111161/?ref_=chttp_t_1
# title: 1. The Shawshank Redemption
# year: 1994
# runtime: 2h 22m
# content_rating: R
# score: 9.3
# views: 3.1M
# rating: #1