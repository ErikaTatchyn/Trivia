import requests
import random
import html 
import json

# Function to fetch trivia questions from the Open Trivia Database API
def get_trivia_questions():
    url = "https://opentdb.com/api.php"
    params = {
        "amount": 10,
        "category": 18,
        "difficulty": "easy",
        "type": "multiple",
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data.get("results", [])

# Function to decode HTML entities
def decode_html_entities(text):
    return html.unescape(text).replace("&#039;", "'")

# Function to display and process a trivia question
def ask_question(question, options):
    question = decode_html_entities(question)
    options = [decode_html_entities(option) for option in options]

    print(question)
    random.shuffle(options)
    
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    user_answer = input("Enter the number of your answer: ")

    try:
        user_answer = int(user_answer)
        if 1 <= user_answer <= len(options):
            return options[user_answer - 1]
        else:
            raise ValueError("Invalid input")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return ask_question(question, options)

# Function to play the trivia game
def play_trivia_game():
    print("Welcome to the Open Trivia Quiz!")
    questions = get_trivia_questions()
    score = 0

    for question_data in questions:
        question = question_data["question"]
        correct_answer = question_data["correct_answer"]
        incorrect_answers = question_data["incorrect_answers"]
        options = incorrect_answers + [correct_answer]

        user_choice = ask_question(question, options)
        if user_choice == correct_answer:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer is: {correct_answer}\n")

    total_questions = len(questions)
    print(f"Your final score: {score}/{total_questions}")
    save_results(total_questions, score)

# Function to save the quiz results to a file
def save_results(total_questions, user_score):
    with open("quiz_results.txt", "a") as file:
        file.write(f"Total Questions: {total_questions}\n")
        file.write(f"User Score: {user_score}\n\n")

if __name__ == "__main__":
    play_trivia_game()
