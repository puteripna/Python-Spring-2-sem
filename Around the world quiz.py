"""
Program   : Quizzes Around The World
Student 1 : Nur Izzaty binti Yaacob , 23039735
Student 2 : Puteri Nurin Aisya binti Ainul Hasni , 23035742
Date      : 20 February 2024

A quiz application to test users’ knowledge on history and places around the world
with different types of questions and levels of difficulty.
Allows users to register account, log in, take quizzes, view scores and exit the program.
"""

# Import modules
from os import path, system, name
from random import shuffle
from sys import exit
from time import sleep, time
from colorama import init, Fore, Back, Style
init(autoreset=True)

# File paths for storing user accounts and quiz attempts
USERNAME_PW_FILEPATH = "user_account.txt"
ATTEMPT_SCORE_FILEPATH = "scores.txt"

TOTAL_QUESTIONS = 9
TOTAL_MARKS = 27


# ====== UTILITY FUNCTIONS ======
# Function to clear console of screen
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux
    else:
        _ = system('clear')


# Class to represent a quiz question
class Question:
    def __init__(self, input_question, input_answer, difficulty, input_multioptions=None):
        self.question = input_question
        self.answer = input_answer
        self.difficulty = difficulty
        self.multioptions = input_multioptions

    # Method to shuffle options for multiple choice questions
    def shuffleOptions(self):
        shuffle(self.multioptions)

    # Method to get formatted options display text
    def getOptionsDisplayText(self):
        displayText = ""
        letters = ["a", "b", "c", "d"]
        for idx in range(len(self.multioptions)):
            letter = letters[idx]
            option = self.multioptions[idx]
            displayText = displayText + f"{letter}) {option}\n"

        return displayText

    # Map each letter to corresponding option in multiple choice questions
    def getOptionsWithLetters(self):
        choices = {}
        letters = ["a", "b", "c", "d"]
        for idx in range(len(self.multioptions)):
            choices[letters[idx]] = self.multioptions[idx]
        return choices


# Calculate points based on difficulty
def calc_points(difficulty):
    if difficulty == "Easy":
        return 2
    elif difficulty == "Medium":
        return 3
    elif difficulty == "Hard":
        return 5
    else:
        return 0  # return 0 points for unknown difficulty level


# Print message for correctly answered questions
def print_correct(marksCollected, totalMarksCollected):
    print(f"{Fore.GREEN}{Style.BRIGHT}Correct!")
    print(f"{Fore.GREEN}+{marksCollected} points", end="")
    print(f"\t{Fore.YELLOW}Current points: {totalMarksCollected} points\n")


# Print message for wrongly answered questions
def print_wrong(totalMarksCollected, correctAnswer):
    print(Fore.RED + Style.BRIGHT + "Wrong...")
    print(f"{Style.BRIGHT}The correct answer is: {correctAnswer}\n")
    print(f"{Fore.RED}+0 points", end="")
    print(f"\t{Fore.YELLOW}Current points: {totalMarksCollected} points\n")


# Generate and shuffle quiz questions
def questions():
    q1 = Question("A home to all federal-level government ministries and national level civil servants,\n"
                  "Putrajaya is the administrative capital of Malaysia (2m) ",
                  "Yes",
                  "Easy",
                  ["Yes", "No"])
    q2 = Question("Let’s take a ride north! But we’ll need to get a car first.\n"
                  "Which of the following is the first Malaysian car? (2m)",
                  "Proton Saga",
                  "Easy",
                  ["Proton Kancil", "Perodua Kelisa", "Perodua Saga", "Proton Saga"])
    q3 = Question("Let’s head to the most northern part of Malaysia, Perlis!\n"
                  "While the capital of Perlis is Kangar, the royal capital is ____. (5m) ",
                  "arau",
                  "Hard")
    q4 = Question("Nothing speaks of adventure like kayaking on a long river!\n"
                  "Which one of these is the longest river in the world? (3m) ",
                  "Nile River",
                  "Medium",
                  ["Mekong River", "Yangtze River", "Nile River", "Amazon River"])
    q5 = Question("You are on summer break and would like to go camping with your friend.\n"
                  "While scrolling on Tiktok, you saw a mountain with face carvings called Mount Rushmore.\n"
                  "Is Mount Rushmore located in California? (3m) ",
                  "No",
                  "Medium",
                  ["Yes", "No"])
    q6 = Question("You follow your dad outstation to Laos.\n"
                  "Your father is asking you, what is the currency of Laos? (5m) \n"
                  "Hint: It’s a three-letter word!",
                  "kip",
                  "Hard")
    q7 = Question("On your journey, you saw a certain country’s flag which has 6 stars on it.\n"
                  "Which country is this flag from? (3m) ",
                  "Australia",
                  "Medium",
                  ["New Zealand", "Australia", "China", "United States of America"])
    q8 = Question("How many wonders of the world are there?\n"
                  "Enter your answer in numerical form. (2m) ",
                  "7",
                  "Easy")
    q9 = Question("Let's travel through the oceans!\n"
                  "Which of the following is a name of the oceans? (2m)\n"
                  " I. Atlantic\n II. Asia\n III. Europe\n IV. Indian\n",
                  "I and IV",
                  "Easy",
                  ["I and II", "I and IV", "II and III", "III and IV"])

    questions = [q1, q2, q3, q4, q5, q6, q7, q8, q9]
    # Shuffle the list of questions before output
    shuffle(questions)
    return questions

# Display rules and guide for answering the different types of questions
def guide():
    # Guide
    print("GUIDE TO ANSWER QUIZ".center(40))
    print(("-"*30).center(40))
    print("For MCQ: Enter your answer from a, b, c or d")
    print("For YES/NO Question: Enter your answer from a or b")
    print("For Fill in the Blank Question: Type in your answer")
    print("For Numerical Question: Only enter number value as answer")
    print("\n[Press Enter to start quiz!]")
    input()
    clear()



# ====== QUIZ FUNCTIONS  ======
# Conduct the quiz
def quiz(username):
    guide()

    # Load attempts for the given username
    attempts = load_attempts(username)

    # Check if attempts exist for the user
    # If yes, calculate next attempt number by adding 1 to previous attempt number
    # If no, set attempt number to 1
    if attempts:
        attemptNumber = max(attempt[0] for attempt in attempts) + 1
    else:
        attemptNumber = 1


    # Initialize variables to track quiz progress and scores
    totalMarksCollected = 0
    correctCount = 0

    # Start timer
    startTime = time()

    # Get a shuffled list of questions
    shuffledQuestions = questions()


    for idx, q in enumerate(shuffledQuestions, 1):
        print(f"Q{idx}. {q.question}")

        # Handle multiple choice questions
        if q.multioptions is not None:
            q.shuffleOptions()
            print(q.getOptionsDisplayText())

            choices = q.getOptionsWithLetters()
            given_answer = input("Answer: ").lower()

            # Loop to handle user input if input is not from the list of available options
            while given_answer not in choices:
                print("Invalid input. Please choose from the provided options!")
                given_answer = input("Answer: ").lower()

            if choices[given_answer] == q.answer:
                correctCount += 1
                marksCollected = calc_points(q.difficulty)
                totalMarksCollected += marksCollected

                print_correct(marksCollected, totalMarksCollected)


            else:
                correctCount += 0

                print_wrong(totalMarksCollected, q.answer)


        # Handle non-multiple choice questions
        else:
            print()
            given_answer = input("Answer: ").lower()
            if given_answer == q.answer.lower():
                correctCount += 1
                marksCollected = calc_points(q.difficulty)
                totalMarksCollected += marksCollected

                print_correct(marksCollected, totalMarksCollected)

            else:
                correctCount += 0

                print_wrong(totalMarksCollected, q.answer)

    # End timer and calculate time taken to answer quiz
    endTime = time()
    totalTime = endTime - startTime

    # Save attempt and score to file
    save_score(username, attemptNumber, totalMarksCollected)

    # Display total marks, number of correct answers, accuracy percentage, and top 3 scores
    print(f"{Fore.YELLOW}-------------------------------------")
    print(f"Attempt {attemptNumber}")
    print(f"{Style.BRIGHT}Total marks : %d  out of %d " % (totalMarksCollected, TOTAL_MARKS))
    print(f"{Style.BRIGHT}You answered %d correct out of %d questions in %.2f seconds." % \
          (correctCount, TOTAL_QUESTIONS, totalTime))

    percentage = (totalMarksCollected / TOTAL_MARKS) * 100
    print(f"{Style.BRIGHT}Final score : ", int(percentage), "%")
    print(f"{Fore.YELLOW}-------------------------------------")
    top3scores(username)
    print(f"{Fore.YELLOW}-------------------------------------")

    # Loop to handle retake option
    while True:
        print("Do you want to retake the quiz? < Y / N > ")
        optionRetake = input("Answer : ").strip().upper()
        print()

        if optionRetake in ["Y", "N"]:
            if optionRetake == "Y":
                attemptNumber += 1  # Update attempt number by incrementing by 1
                clear()
                quiz(username)  # Retake quiz with updated attempt number
                break
            else:
                print("Returning to main page...")
                sleep(2)
                clear()
                break

        else:
            print("Please only choose from < Y / N >!")


# Save user attempt and score to file
def save_score(username, attemptNumber, score):
    with open(ATTEMPT_SCORE_FILEPATH, 'a') as user_scores:
        user_scores.write(f"{username},{attemptNumber},{score}\n")


# Load user attempts and score from file
def load_attempts(username):
    attempts = []

    if path.exists(ATTEMPT_SCORE_FILEPATH):
        with open(ATTEMPT_SCORE_FILEPATH, 'r') as user_scores:
            for line in user_scores:
                # Split the line into username, attempt number and score
                attempt_data = line.strip().split(',')
                # Check if the username from file matches the given username
                if attempt_data[0] == username:
                    # Extract user's attempt number and score, and append to attempts list
                    attemptNumber = int(attempt_data[1])
                    score = int(attempt_data[2])
                    attempts.append((attemptNumber, score))
    return attempts


# ====== SCOREBOARD FUNCTIONS ======
# Display all attempts and scores for the user
def view_scores(username):
    print(f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{Back.BLUE}========= SCOREBOARD =========\n")
    # Load attempts for given username
    attempts = load_attempts(username)

    # Check if there are no attempts for the username
    if not attempts:
        print("No attempts found.")
        print("Returning to main page...")
        sleep(3)
        return

    # Print all attempts and scores
    print(f"{Fore.GREEN}Scores for User '{username}':")
    print(f"{Fore.YELLOW}--------------------------------")
    for attemptNumber, score in attempts:
        print(f"Attempt {attemptNumber}: {score} points")
    sleep(3)

    print("\n[Press Enter to return to main page...]")
    input()


# Display only top 3 scores for the user
def top3scores(username):
    # Load attempts for given username
    attempts = load_attempts(username)

    # Check if there are no attempts for the username
    if not attempts:
        print("No attempts found.")
        print("Returning to main page...")
        sleep(3)
        return

    # Sort attempts based on scores in descending order if attempts exist
    sortedAttempts = sorted(attempts, key=lambda x: x[1], reverse=True)

    # Select the top 3 attempts
    top3 = sortedAttempts[:3]

    # Print the top 3 attempts
    print(f"{Back.MAGENTA}{Style.BRIGHT}Top 3 Scores for User '{username}':")
    print()
    for idx, (attemptNumber, score) in enumerate(top3, 1):
        print(f"{Style.BRIGHT}{idx}. Attempt {attemptNumber}: {score} points \n")



# ====== MAIN MENU PAGE ======
def main_page(username):
    print(f"\n\n{Back.CYAN}{Style.BRIGHT}Hello, {username}!")
    while True:
        print(f"\n{Fore.YELLOW}-------------------------------------")
        print(f"{Style.BRIGHT}Welcome to Quizzes Around the World!")
        print(f"{Fore.YELLOW}-------------------------------------\n")
        print(f"{Style.BRIGHT}1. START QUIZ")
        print(f"{Style.BRIGHT}2. VIEW SCORES")
        print(f"{Style.BRIGHT}3. EXIT")
        print(f"\n{Fore.YELLOW}-------------------------------------")

        optionMain = input("Enter your option < 1 / 2 / 3 >: ")
        clear()
        print()
        print()
        if optionMain == '1':
            quiz(username)
            clear()
        elif optionMain == '2':
            view_scores(username)
            clear()
        elif optionMain == '3':
            print("Thank you for playing! See you next time...\n")
            print("Exiting...")
            sleep(2)
            exit(0)
        else:
            print("Please only choose from < 1 / 2 / 3>!\n")



# ====== USER ACCOUNT MANAGEMENT FUNCTIONS ======
# Log in to existing account
def login_account():
    print(f"\n\n{Fore.LIGHTYELLOW_EX}{Back.BLUE}{Style.BRIGHT}============= LOGIN =============")

    username = (input("Enter USERNAME: ")).strip()
    password = input("Enter PASSWORD: ")

    # Check if the username and password match
    with open(USERNAME_PW_FILEPATH, 'r') as user_accounts:
        for line in user_accounts:
            existing_username, existing_pw = line.strip().split(',')
            if existing_username == username:
                if existing_pw == password:
                    print("Log in successful!")
                    sleep(2)
                    clear()
                    return username
                else:
                    print("Incorrect password. Log in unsuccessful.\n")
                    return None  # Returns value None if password is incorrect
        print("User does not exist. Log in unsuccesful. \n")
        return None  # Returns value None if username does not exist


# Create a new account
def register_account():
    print(f"\n\n{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{Back.BLUE}============= REGISTER =============")

    username = input("Enter USERNAME: ")

    # Check if the username already exists
    username_exists = False
    with open(USERNAME_PW_FILEPATH, 'r') as user_accounts:
        for line in user_accounts:
            existing_username = line.split(',')[0]
            if existing_username == username:
                username_exists = True
                break

    # If username already exists, return to home page
    if username_exists:
        print("An account with this username already exists. Registration unsuccessful.\n")
        sleep(2)
        return

    # If username is available, proceed to register password
    else:
        password = input("Enter PASSWORD: ")
        with open(USERNAME_PW_FILEPATH, 'a') as user_accounts:
            user_accounts.write(f"{username},{password}\n")
        print("Account created successfully!\n")
        sleep(2)



# ====== HOME LOGIN/REGISTER PANEL ======
def home():
    while True:
        print(f"{Fore.YELLOW}-------------------------------------")
        print(Fore.CYAN + Back.WHITE + Style.DIM + "QUIZ LOGIN PAGE".center(37))
        print(f"{Fore.YELLOW}-------------------------------------\n")
        print(f"{Style.BRIGHT} 1. LOGIN")
        print(f"{Style.BRIGHT} 2. REGISTER")
        print(f"\n{Fore.YELLOW}-------------------------------------")
        logChoice = input("ENTER YOUR OPTION < 1 / 2 > : ")
        if logChoice == '1':
            username = login_account()
            if username is not None:
                main_page(username)
                break
            else:
                print("Returning to home page...\n")
                sleep(2)
                clear()
        elif logChoice == '2':
            register_account()
            clear()
            home()
            break
        else:
            print("\nPlease only choose from < 1 / 2 >!")



# ====== ENTRY POINT ======
def main():
    # Create empty files for username details and for user's attempts and score
    if not path.exists(USERNAME_PW_FILEPATH):
        with open(USERNAME_PW_FILEPATH, 'w'):
            pass

    if not path.exists(ATTEMPT_SCORE_FILEPATH):
        with open(ATTEMPT_SCORE_FILEPATH, 'w'):
            pass
    home()


if __name__ == "__main__":
    main()
