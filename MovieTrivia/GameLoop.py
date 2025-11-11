from MovieTriviaGame import *
from datetime import *
import random

def main():
    movies: list[Movie] = generate_data()    
    run_game(movies)
    
        
def run_game(movies: list[Movie]):
    print("\n====================================================================\n")
    
    print("\nWelcome to the game!\n")
    questions_count = 5
    total_correct_answers = 0
    
    for movie in movies:
        if questions_count == 0:
            break
            
        # Get a random trivia question
        index = random.randint(0, len(movie.trivia_questions)-1)
        trivia_question_and_answers = movie.trivia_questions[index]
        trivia_question = trivia_question_and_answers[0]
        trivia_answers = trivia_question_and_answers[1]
        
        # Display question
        print(f"\nQuestion:\n{trivia_question}\n")
        correct_answers = 0

        # Prompt user for answers
        for answer_index, answer in enumerate(trivia_answers):
            user_input = input(f" > Answer {answer_index+1}:").lower().strip()
            correct_answers += 1 if user_input == answer.lower().strip() else 0
        
        # Tally up current score
        total_correct_answers += 1 - (correct_answers / len(trivia_answers)) if correct_answers > 0 else 0
        questions_count -= 1
        
        # Ensure the question doesn't get asked again
        movie.trivia_questions.pop(index)
        index -= 1
        if len(movie.trivia_questions) == 0:
            movie_index = [target_index for target_index, target_movie in enumerate(movies) if target_movie.movie_id == movie.movie_id][0]
            movies.pop(movie_index)
            continue
    
    print(f"\nWell played! Your score is {total_correct_answers} / 5\n")
    is_playing_again = input("Press \'Y\' to play again: ").lower().strip() == "y"
    
    # Run game again with 1 less trivia question
    if is_playing_again:
        run_game(movies)
        


def generate_data():
    movies = MovieTriviaGame.parse_top_25_movies()[:5]
    print("\n\n...Initializing game...\n")
    
    for movie in movies:
        # Progress report
        print(f"{movie.movie_id*4}%")
        
        # add missing content to movie objects
        MovieTriviaGame.parse_movie(movie)
        MovieTriviaGame.parse_trivia(movie)
        
    return movies


if __name__ == "__main__":
    main()