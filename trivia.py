import requests #module is used to make HTTP requests to Database API
import random #for generating random numbers
import html  #escaping/unescaping special characters in HTML
import json #Parsing JSON data received from web APIs into Python dictionaries

# Function to fetch trivia questions from the Open Trivia Database API
def get_trivia_questions(): 
    url = "https://opentdb.com/api.php"
    params = {
        "amount": 10,
        "category": 18, #computers
        "difficulty": "easy",
        "type": "multiple",
    }

    response = requests.get(url, params=params) #HTTP GET request to the 'Open Trivia Database' API using the specified URL and parameters
    data = response.json() #receive a JSON response from the API, which contains trivia questions and related data
    return data.get("results", []) #extract relevant information from the JSON response, including questions, answer choices, and correct answers

def decode_html_entities(text):
    html_entities = {
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&quot;": "\"",
        "&#039;": "'",
    }

    for entity, char in html_entities.items():
        text = text.replace(entity, char)

    return text

# Function to display and process a trivia question
def ask_question(question, options):
    question = decode_html_entities(question)
    options = [decode_html_entities(option) for option in options]

    print(question)
    random.shuffle(options)
    
    for i, option in enumerate(options, start=1): #built-in Python function that is used to iterate over a sequence
        print(f"{i}. {option}")

    while True:
        user_answer = input("Enter the number of your answer: ")

        try:
            user_answer = int(user_answer)
            if 1 <= user_answer <= len(options):
                return options[user_answer - 1]
            else:
                raise ValueError("Invalid input")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue 

        break

# Function to play the trivia game
def play_trivia_game():
    print("Welcome to the Open Trivia Quiz!")
    questions = get_trivia_questions()
    score = 0

    for question_data in questions:
        question = decode_html_entities(question_data["question"])
        correct_answer = decode_html_entities(question_data["correct_answer"])
        incorrect_answers = [decode_html_entities(option) for option in question_data["incorrect_answers"]]
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
