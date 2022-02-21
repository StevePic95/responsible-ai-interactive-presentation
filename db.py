"""This is the program that will dictate interactions between the web app
and the mongoDB hosted on AWS (use RCSJ email to login to Atlas). If any part
of this  is confusing, visit https://www.youtube.com/watch?v=PHX1kraTTrE"""

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import ssl
from user import User
import rooms

# DATABASE ACCESS - 'demoDB'
client = MongoClient("", ssl_cert_reqs=ssl.CERT_NONE)
demoDB = client.get_database("")

# COLLECTION ACCESS - 'users'
users_collection = demoDB.get_collection('users')
def save_user(username, password, room, vote=None, email=None, role=None):
    password_hash = generate_password_hash(password)
    users_collection.insert_one({'_id': username, 'password': password_hash, 'room': room, 'role': role, 'email': email})
def get_user(username):
    user_data = users_collection.find_one({'_id': username})
    return User(user_data['_id'], user_data['password'],  email=user_data['email'], role=user_data['role']) if user_data else None

def get_user_room(username):
    user_data = users_collection.find_one({'_id': username})
    return user_data['room']

def record_user_vote(username, vote):
    users_collection.update_one({'_id': username}, {'$set': {'vote': vote}})

def delete_temp_users():
    users_collection.delete_many({"role":"audience"})
    users_collection.delete_many({"role": None})

def calculate_vote_results():
    correcthuman = users_collection.find( { "room": { '$in': ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20'] }, "vote": "human" } ).count()
    wronghuman = users_collection.find( { "room": { '$in': ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20'] }, "vote": "computer" } ).count()
    correctcomputer = users_collection.find( { "room": { '$in': ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'] }, "vote": "computer" } ).count()
    wrongcomputer = users_collection.find( { "room": { '$in': ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'] }, "vote": "human" } ).count()
    
    correct = correctcomputer + correcthuman
    wrong = wrongcomputer + wronghuman

    total_votes = correcthuman + wronghuman + correctcomputer + wrongcomputer
    percent_correct = "{}%".format((float(correct) / float(total_votes))*100)
    percent_wrong = "{}%".format((float(wrong) / float(total_votes))*100)

    result_list_temp = [total_votes, correct, percent_correct, wrong, percent_wrong, correcthuman, wronghuman, correctcomputer, wrongcomputer]
    result_list = list(map(str, result_list_temp))
    result_list[0] = "Total Votes.................... " + result_list[0]
    result_list[1] = "Correct Votes.................. " + result_list[1]
    result_list[2] = "Percent Correct................ " + result_list[2]
    result_list[3] = "Incorrect Votes................ " + result_list[3]
    result_list[4] = "Percent Incorrect.............. " + result_list[4]
    result_list[5] = "Correctly Guessed Human........ " + result_list[5]
    result_list[6] = "Incorrectly Guessed Computer... " + result_list[6]
    result_list[7] = "Correctly Guessed Computer..... " + result_list[7]
    result_list[8] = "Incorrectly Guessed Human...... " + result_list[8]
    return result_list

## COLLECTION ACCESS - 'conversations'
convo_collection = demoDB.get_collection("conversations")
def update_conversation_record():
    pass

# COLLECTION ACCESS - 'presenters'
presenters_collection = demoDB.get_collection('presenters')
def save_presenter(username, password, email=None, role=None):
    password_hash = generate_password_hash(password)
    presenters_collection.insert_one({'_id': username, 'email': email, 'password': password_hash, 'role': role})

# COLLECTION ACCESS - 'chatrooms'
chatrooms_collection = demoDB.get_collection('chatrooms')
