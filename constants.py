from werkzeug.security import generate_password_hash
import random
import os

# CONFIG SETTINGS
HOST_IP = "0.0.0.0"
SECRET_KEY = os.getenv("OPENAI_API_KEY")

# DB SETTINGS
PRESENTATION_PASS_KEY = os.getenv("PRESENTATION_PASS_KEY")
PRESENTATION_PASS_KEY_HASH = generate_password_hash(PRESENTATION_PASS_KEY)
HUMAN_ROOM_LIST = ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20']
NUMBER_OF_ROOMS = 20

# GPT-3 SETTINGS
TT_ENGINE = 'babbage'
TT_MAX_TOKENS = 1000
TT_TEMPERATURE = .9
TT_TOP_P = 1
TT_n = 1
TT_STREAM = False
TT_LOGPROBS = None
TT_STOP = ["\n", "Person 2"]
TT_PRESENCE_PENALTY = 1.5
TT_FREQUENCY_PENALTY = 1.5
TT_BEST_OF = 3
TT_PROMPT_BEGINNING = "Two people are talking to each other for the first time in an online chat room. \"Person 1\" is suspicious that the other person may be a chatbot. \"Person 2\" is a friendly human with a sarcastic yet wholesome sense of humor. Here is their conversation:\n"

DB_PROMPT_BEGINNING = "Dwight is a nerdy office worker who loves farming, Battlestar Galactica, and beets. This is a conversation between Dwight and his coworker, Jim, who Dwight is annoyed with:\n"
DB_FINE_TUNE_MODEL_ID = os.getenv("FINETUNE_MODELl_ID")
DB_STOP = ["\n", "Jim:", '[']
DB_PRESENCE_PENALTY = 0.7
DB_FREQUENCY_PENALTY = 1.5
DB_TEMPERATURE = 0.7
DB_MAX_TOKENS = 180

GB_PROMPT_BEGINNING = "George is an extremely intelligent person who loves to answer questions thoroughly and correctly. Here is a conversation between George and a friend of his:\n"
GB_STOP = ["Friend:"]
GB_ENGINE = "davinci"

WAIT_TIME_PER_CHARACTER_MULTIPLIER = 0.2 * (random.randint(85,115) / 100)    # Delay response from GPT-3 for realism

file = open("static/trainingdata.jsonl", "r")
stringdata =''
for row in file:
    stringdata += (row + "\n")
RAW_TRAINING_DATA = stringdata

# USER MESSAGES
USER_ALREADY_LOGGED_IN_MESSAGE = 'You\'re already logged in! Redirecting back to your chat room...'
LOGIN_FAILED_MESSAGE = "Login failed - username and password combo not recognized."
WRONG_PASSKEY_MESSAGE = "Wrong presentation key used. Did those darn presenters forget to tell you the presentation key?!"
USERNAME_TAKEN_MESSAGE = "Whoops - somebody already took that name!"
UNKNOWN_SIGN_IN_ERROR = "Sorry, an unknown error has occurred while you attempted to sign in. Let a presenter know!"
USER_HAS_BEEN_LOGGED_OUT_MESSAGE = "You have been logged out of your temporary account, but you can make a new one if you want."
