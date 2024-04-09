import requests
import html

# this defines the url for fetching questions
QUESTIONS_URL = "https://opentdb.com/api.php"

# this defines the quiz class
class QuizApp:
    def __init__(self, num_questions):
        self.category = 31 # this is the category id for "anime" in the opentdb
        self.num_question = num_questions # this sets the number of questions
        self.question = [] # this creates a list that stores the fetch questions
   
    # this is the func to fetch questions from teh api
    def get_question(self):
        # this sets params from the api request
        params = {
            "amount": self.num_question,
            "category": self.category,
            "type": "multiple"
        }
        try: 
            response = requests.get(QUESTIONS_URL, params = params) # this sends a get request to the api and fetchs the questions
            json_data = response.json() # this converts the json data
            self.question = json_data['results'] # this extract questions from the response and store them
            # this decodes html symbols into actual symbols
            for question in self.question:
                question['question'] = html.unescape(question['question']) # this decodes question text
                question['incorrect_answers'] = [html.unescape(answer) for answer in question['incorrect_answers']]# this decodes incorrect answer
                question['correct_answer'] = html.unescape(question['correct_answer']) # this decodes correct answer
        except ValueError as e: # this handles errors if the api call fails
            print(f"API call failed: {e}")

    # this is the func to ask questions to the user
    def ask_questions(self):
        score = 0 # this initializes the score counter
        # this iterate through each question
        for question in self.question:
            print("\nQuestion:", question['question'])
            options = question['incorrect_answers'] + [question['correct_answer']]
            for i, option in enumerate(options, 1): # this enumerate options starting from 1
                print(f"{i}. {option}")
            # thus gets the users input
            while True:
                user_input = input("Your answer (enter the option number): ")
                if user_input.isdigit():  # this checks if input is a digit
                    user_answer = int(user_input) # this converts the user input into a integer
                    if 1 <= user_answer <= len(options):  # this checks if input is within valid range
                        break
                print("Invalid input. Please enter a valid option number.")
            if options[user_answer - 1] == question['correct_answer']: # this checks if users answer is correct
                print("Correct!")
                score += 1
            else:
                print("Incorrect!")
                print("Correct answer:", question['correct_answer'])  
        print("\nQuiz complete!") # this prints out quiz completion message with the score
        print("Your score:", score, "/", len(self.question))

# this is the func to start the quiz, with  parameters for minimum and maximum number of questions  
def start_quiz(min_val=1, max_val=10):  
    print("Welcome to the sugoi anime test!") 
    while True:  # this while loop start an infinite loop for user interaction
        try:  # this try and except handles potential errors
            num_questions = int(input("Enter number of questions you want to do: "))  
            if not (min_val <= num_questions <= max_val):  # this checks if the input number of questions is within the specified range
                print(f'The number must be a whole number between {min_val} and {max_val}.')  # this prints out an error message if the input is out of range
            else:  
                quiz = QuizApp(num_questions)  # this creates a new quiz with the specified number of questions
                quiz.get_question()  # this calls the func to fetch questions for the quiz
                quiz.ask_questions()  # this calls the func to ask questions to the user
                break  
        except ValueError as e:  
            print(f"{e} is an invalid input. Must be a whole positive integer.")  

if __name__ == "__main__":
    start_quiz()