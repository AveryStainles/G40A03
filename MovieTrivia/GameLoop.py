from MovieTriviaGame import *
from datetime import *
import random
import math

# Item 1 == question, Item 2 == answers
trivia_questions: list[(str, list[str])] = []

def main():
    try:
        # Parse game data from parsed_data.txt
        data = FileReadWriteHelper.read_data()
        
        # Flag if there was an issue setting the game questions
        if data == None or len(data) == 0:
            raise Exception("Error when loading data")
        
        is_answer = False
        question = ""
        
        for line in FileReadWriteHelper.read_data():
        
        # line is an answer
            if is_answer:
                trivia_questions.append(("\n".join(question.split("<>")), [answer for answer in line.split("~") if not (answer == None or answer == "")]))
            else:
                question = line
            
            is_answer = not is_answer
        
        run_game()
    
    except:
        # Scrape the data and try again
        print(f"\nThere were issues trying to load up the game. Do you wish to attempt generating game data?\n")
        is_scraping_data = input("Press \'Y\' to scrape data: ").lower().strip() == "y"
        
        if is_scraping_data:
            generate_data()

        print("\n...Please restart the game...")
        
def run_game():
    print("\n====================================================================\n")
    
    print("\nWelcome to the game!\n")
    questions_count = 5
    current_game_questions = []
    total_correct_answers = 0
    
    for _ in range(5):
        # Get a random trivia question
        index = random.randint(0, len(trivia_questions)-1)
        current_game_questions.append(trivia_questions[index])

        # Ensure the question does not reappear
        trivia_questions.pop(index)
        
    for question in current_game_questions:
        
        # All 5 questions were answered
        if questions_count == 0:
            break
        
        trivia_question = question[0]
        trivia_answers = question[1]    
        
        # Display question
        print(f"\n\n{trivia_question}\n")
        correct_answers = 0

        for answer_index, answer in enumerate(trivia_answers):
            # Prompt user for answers
            user_input = input(f" > Answer {answer_index+1}:").lower().strip()
            is_correct = user_input == answer.lower().strip()
            
            # Tally up partial correct answers for the question
            correct_answers += 1 if is_correct else 0
        
        # Tally up current score
        val = (correct_answers / len(trivia_answers))
        total_correct_answers += (1 - val if val > 1 else val) if correct_answers > 0 else 0
        questions_count -= 1
    
    print(f"\nWell played! Your score is {total_correct_answers} / 5\n")
    is_playing_again = input("Press \'Y\' to play again: ").lower().strip() == "y"
    
    # Run game again with 1 less trivia question
    if is_playing_again:
        run_game()
        

def generate_data():
    movies = MovieTriviaGame.parse_top_25_movies()
    print("\n\n...Initializing game data...\n")
    print("This takes about 3-5 minutes during testing. However, this makes the game significantly faster to launch in subsequent games.")
    
    for index, movie in enumerate(movies):
        # Progress report
        print(f"{int(math.floor(index * 100 / len(movies)))}%")
        
        # add missing content to movie objects
        MovieTriviaGame.parse_movie(movie)
        MovieTriviaGame.parse_trivia(movie)
        
        # Add scraped trivia questions
        [trivia_questions.append(questions) for questions in movie.trivia_questions]
        
        # Add missing property trivia question for the movie
        MovieTriviaGame.missing_property_trivia(movie, trivia_questions)
        
    # Write data to file so that it doesn't need to be scraped again
    [FileReadWriteHelper.write_data(f"{question[0]}\n{"~".join(question[1])}", is_encoding=False) for question in trivia_questions]


if __name__ == "__main__":
    main()