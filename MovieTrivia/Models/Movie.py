class Movie:

    
    def __init__(self):
        self._movie_id = -1
        self._content_link = ""
        self._trivia_link = ""
        self._trivia_questions = []
        self._title = ""
        self._year = ""
        self._runtime = ""
        self._score = ""
        self._views = ""
        self._rating = ""
        self._content_rating = ""
        self._director = ""
        self._cast_members = []
    
    
    # Movie ID
    def set_movie_id(self, movie_movie_id: int) -> None:
        self._movie_id: int = movie_movie_id
    
    def get_movie_id(self) -> int:
        return self._movie_id
    
         
        
    # Content link | To get the information on a specific title
    def set_content_link(self, content_link: str) -> None:
        self._content_link: str = content_link
    
    def get_content_link(self) -> str:
        return self._content_link
    
         
        
    # Trivia link | To get a list of trivia questions for a specific title
    def set_trivia_link(self, trivia_link: str) -> None:
        self._trivia_link: str = trivia_link
    
    def get_trivia_link(self) -> str:
        return self._trivia_link
    
 

    # Trivia Questions | List of tuples, Item 1 is the question, Item 2 is a list of the answers in order
    def set_trivia_questions(self, trivia_questions: list[(str, list[str])]) -> None:
        self._trivia_questions: list[(str, list[str])] = trivia_questions
    
    def get_trivia_questions(self) -> list[(str, list[str])]:
        return self._trivia_questions

    def add_trivia_question(self, trivia_question: str) -> None:
        self._trivia_questions.append(trivia_question)
            
     
    
    # Title
    def set_title(self, title: str) -> None:
        self._title: str = title
    
    def get_title(self) -> str:
        return self._title
    
     
    
    # Year
    def set_year(self, year: str) -> None:
        self._year: str = year
    
    def get_year(self) -> str:
        return self._year
    
 

    # Runtime
    def set_runtime(self, runtime: str) -> None:
        self._runtime: str = runtime
    
    def get_runtime(self) -> str:
        return self._runtime
    
 

    # Score | e.g.  9.1 out of 10
    def set_score(self, score: str) -> None:
        self._score: str = score
    
    def get_score(self) -> str:
        return self._score
    
     
    
    # Views
    def set_views(self, views: str) -> None:
        self._views: str = views
    
    def get_views(self) -> str:
        return self._views
    
     
    
    # Rating
    def set_rating(self, rating: str) -> None:
        self._rating: str = rating
    
    def get_rating(self) -> str:
        return self._rating
    
    
    # Content rating
    def set_content_rating(self, content_rating: str) -> None:
        self._content_rating: str = content_rating
    
    def get_content_rating(self) -> str:
        return self._content_rating 
    
    
    # First director I saw (I forgot there could be more than one)
    def set_director(self, director: str) -> None:
        self._director: str = director
    
    def get_director(self) -> str:
        return self._director
    
     
    
    # Top 10 cast members
    def set_cast_members(self, cast_members: list[str]) -> None:
        self._cast_members: list[str] = cast_members
    
    def get_cast_members(self) -> list[str]:
        return self._cast_members

    def add_cast_member(self, cast_member: str) -> None:
        self._cast_members.append(cast_member)
            
 
    movie_id: int = property(get_movie_id, set_movie_id)
    
    content_link: str = property(get_content_link, set_content_link)
    trivia_link: str = property(get_trivia_link, set_trivia_link)
    
    trivia_questions: list[(str, list[str])] = property(get_trivia_questions, set_trivia_questions)
    title: str = property(get_title, set_title)
    year: str = property(get_year, set_year)
    runtime: str = property(get_runtime, set_runtime)
    score: str = property(get_score, set_score)
    views: str = property(get_views, set_views)
    rating: str = property(get_rating, set_rating)
    content_rating: str = property(get_content_rating, set_content_rating)
    director: str = property(get_director, set_director)
    cast_members: list[str] = property(get_cast_members, set_cast_members)


    def __repr__(self):
        return f"{self.movie_id}\n{self.content_link}\n{self.trivia_link}\n{self.trivia_questions}\n{self.title}\n{self.year}\n{self.runtime}\n{self.score}\n{self.views}\n{self.rating}\n{self.director}\n{self.cast_members}\n"
