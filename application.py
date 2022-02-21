from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, current_user
from flask.templating import render_template_string
from flask_login.utils import login_required, logout_user
from flask_socketio import SocketIO, join_room, leave_room
from user import User
from db import calculate_vote_results, get_user, save_user, get_user_room, record_user_vote
import constants as const
from time import sleep
from pymongo import errors
import json
import rooms
import gpt3
import time

# Initiate Flask instance and wrap inside of socketio instance
application = Flask(__name__)
application.config['SECRET_KEY'] = const.SECRET_KEY
socketio = SocketIO(application)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(application)
    # Run the flask site on the server
if __name__ == '__main__':
    socketio.run(application, debug=True, host=const.HOST_IP, port="5000")
room_tracker = rooms.Room_Manager()

# Conversation objects for algorithm
room_1_convo = gpt3.Conversation()
room_3_convo = gpt3.Conversation()
room_5_convo = gpt3.Conversation()
room_7_convo = gpt3.Conversation()
room_9_convo = gpt3.Conversation()
room_11_convo = gpt3.Conversation()
room_13_convo = gpt3.Conversation()
room_15_convo = gpt3.Conversation()
room_17_convo = gpt3.Conversation()
room_19_convo = gpt3.Conversation()
room_21_convo = gpt3.Conversation()
room_22_convo = gpt3.Conversation()
room_23_convo = gpt3.Conversation()
room_24_convo = gpt3.Conversation()
room_25_convo = gpt3.Conversation()
room_26_convo = gpt3.Conversation()
room_27_convo = gpt3.Conversation()
room_28_convo = gpt3.Conversation()
room_29_convo = gpt3.Conversation()
room_30_convo = gpt3.Conversation()

good_bot_convo = gpt3.GoodBot()
dwight_bot_convo = gpt3.DwightBot()

# LANDING PAGE - QR Code links here
@application.route("/", methods=['GET', 'POST'])
def landing():
    message = ''
    if current_user.is_authenticated:
        if get_user(current_user.username).room:
            return render_template('userchat.html', username=current_user.username, room=get_user_room(current_user.username))
        else:
            pass
    if request.method == 'POST':
        user = None
        username = request.form.get('username')
        password_input = request.form.get('password')

        if password_input == const.PRESENTATION_PASS_KEY:
            try:
                room_on_deck = room_tracker.next_room()
                print("Assigned " + str(username) + " to room " + str(room_on_deck))
                room_tracker.mark_occupied(room_on_deck)
                print( "Room " + str(room_on_deck) + " marked occupied")
                save_user(username, password_input, room_on_deck)
                print("Saved user " + str(username))
            except errors.DuplicateKeyError:
                room_tracker.mark_vacant(room_on_deck)
                message = const.USERNAME_TAKEN_MESSAGE
                return render_template('landing.html', message=message)
            except Exception:
                room_tracker.mark_vacant(room_on_deck)
                message = const.UNKNOWN_SIGN_IN_ERROR
                return render_template('landing.html', message=message)
            user = get_user(username)
            user.assign_room(room_on_deck)
            login_user(user)
            return render_template('userchat.html', username=user.username, room=room_on_deck)
                
        else:
            message = const.WRONG_PASSKEY_MESSAGE
            return render_template('landing.html', message=message)

        #message = const.LOGIN_FAILED_MESSAGE
    return render_template('landing.html', message=message)

# PRESENTER LOGIN - redirects to presenter dashboard if login successful
@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.is_presenter():
        return redirect(url_for('presenterdash'))
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)

        if user and user.check_password(password_input) and user.is_presenter:
            login_user(user)
            return redirect(url_for('presenterdash'))
        else:
            message = const.LOGIN_FAILED_MESSAGE
    return render_template('login.html', message=message)

# PRESENTER DASHBOARD - general access to demos for presentation
@application.route('/presenterdash', methods=['GET', 'POST'])
def presenterdash():
    return render_template('presenterdash.html')

# TURING'S CHATROOM - first demo when attendees enter.
@application.route('/userchat', methods=['GET', 'POST'])
def userchat():
    user = get_user(request.args.get("username"))
    if user.username and get_user_room(user.username):
        return render_template("userchat.html", username=user.username, room=get_user_room(user.username), host=const.HOST_IP)
    else:
        return redirect(url_for("landing", message = const.LOGIN_FAILED_MESSAGE))

# TURING DISPLAY - bigscreen graphic to show while audience is doing the Turing's Chat experiment
@application.route('/turingdisplay', methods=['GET', 'POST'])
def turingdisplay():
    return render_template('turingdisplay.html')

# HUMAN DASHBOARD - displays all open "human" chatrooms for the human participant to chat with users simultaneously.
@application.route('/humandash', methods=['GET', 'POST'])
def humanchat():
    return render_template('humandash.html', username='USER',
                                             human_room_list = [i for i in range(2, 21) if i % 2 == 0])

# TRAINING DATA DEMO - allows interaction between a well-trained and poorly-trained gpt-3 model
@application.route('/trainingdata', methods=["GET", "POST"])
def trainingdata():
    return render_template('trainingdata.html', role="presenter")

# Shows a raw dump of the dwightbot fine-tune jsonl
@application.route("/rawdata")
def raw_data():
    return const.RAW_TRAINING_DATA

# User votes "human" from userchat page
@application.route("/votehuman", methods=["GET", "POST"])
def vote_human():
    user = get_user(current_user.username)
    record_user_vote(user.username, "human")
    return render_template('trainingdata.html', role="audience", username=user.username)

# User votes "computer" from userchat page
@application.route("/votecomputer", methods=["GET", "POST"])
def vote_computer():
    user = get_user(current_user.username)
    record_user_vote(user.username, "computer")
    return render_template('trainingdata.html', role="audience", username=user.username)

# LOGOUT
@application.route("/logout")
#@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/')

################# EVENT HANDLING #################

# JOIN HUMAN ROOMS - Presenter visits /humandash to chat with multiple attendees
@socketio.on('join_human_rooms')
def handle_join_human_rooms_event(data):
    roomlist = [i for i in range(1,21) if i % 2 == 0]
    for room in roomlist:
        application.logger.info("{} has joined room {}".format(data['username'], room))
        join_room(room)
        data['message_box_id'] = 'messages' + str(room)
        socketio.emit("join_room_announcement", data)

# JOIN ROOM - Attendee visits /userchat to begin the "Turing's Chatroom" demonstration
@socketio.on('join_room')
def handle_join_room_event(data):
    application.logger.info("{} has joined room {}".format(data['username'], data['room']))
    join_room(data['room'])
    data['message_box_id'] = "messages" + str(data['room'])
    socketio.emit("join_room_announcement", data)

# ENABLE TC MESSAGE BOX - When a presenter begins the timer, users will be able to send messages
@socketio.on("tc_started")
def handle_tc_started_event():
    socketio.emit("enable_tc_message_inputs")

# DISABLE TC MESSAGE BOX - When the timer reaches zero, input boxes are disabled again and the vote buttons appear
@socketio.on("tc_ended")
def handle_tc_ended_event():
    socketio.emit("disable_tc_message_inputs")

# LEAVE ROOM - Any user leaves an active chatroom page
@socketio.on('leave_room')
def handle_leave_room_event(data):
    application.logger.info("{} has left room {}".format(data['username'], data["room"]))
    leave_room(data['room'])
    data['message_box_id'] = "messages" + str(data['room'])
    socketio.emit("leave_room_announcement", data)

# SHOW RESULTS - Presenter clicks "show results" button on big screen to reveal experiment results
@socketio.on('show_results')
def handle_show_results_event(data):
    result_list = calculate_vote_results()
    data["result_list"] = result_list
    socketio.emit('reveal_results', data)

# CONNECT TRAININGDATA - "Dwightbot" demonstration page is opened
@socketio.on('connect_trainingdata')
def handle_connect_trainingdata_event():
    pass

# SEND TRAININGDATA MESSAGE - A message is passed to either of the trainingdata models
@socketio.on("send_trainingdata_message")
def handle_send_trainingdata_message_event(data):
    global good_bot_convo
    global dwight_bot_convo
    message_from_human = data['message']
    socketio.emit('receive_trainingdata_message', data)
    good_response = good_bot_convo.get_response_to(message_from_human)
    time.sleep(1.5)
    data['message'] = good_response
    data['username'] = "GOOD MODEL"
    socketio.emit('receive_trainingdata_message', data)
    dwight_response = dwight_bot_convo.get_response_to(message_from_human)
    time.sleep(1.5)
    data['message'] = dwight_response
    data['username'] = "DWIGHT MODEL"
    socketio.emit('receive_trainingdata_message', data)

# 15s Delay for trainingdata demo
@socketio.on("15s_delay")
def handle_15s_delay_event():
    socketio.emit("start_delay")
    time.sleep(15)
    socketio.emit("end_delay")

# SEND MESSAGE - Any user hits "submit" on the message input form
@socketio.on("send_message")
def handle_send_message_event(data):
    def chatbot_response_sequence(data):
        global room_1_convo 
        global room_3_convo
        global room_5_convo 
        global room_7_convo 
        global room_9_convo 
        global room_11_convo
        global room_13_convo
        global room_15_convo 
        global room_17_convo 
        global room_19_convo 
        global room_21_convo
        global room_22_convo
        global room_23_convo
        global room_24_convo
        global room_25_convo
        global room_26_convo
        global room_27_convo
        global room_28_convo
        global room_29_convo
        global room_30_convo

        if int(data['room']) == 1:
            conversation = room_1_convo
        elif int(data['room']) == 3:
            conversation = room_3_convo
        elif int(data['room']) == 5:
            conversation = room_5_convo
        elif int(data['room']) == 7:
            conversation = room_7_convo
        elif int(data['room']) == 9:
            conversation = room_9_convo
        elif int(data['room']) == 11:
            conversation = room_11_convo
        elif int(data['room']) == 13:
            conversation = room_13_convo
        elif int(data['room']) == 15:
            conversation = room_15_convo
        elif int(data['room']) == 17:
            conversation = room_17_convo
        elif int(data['room']) == 19:
            conversation = room_19_convo
        elif int(data['room']) == 21:
            conversation = room_21_convo
        elif int(data['room']) == 22:
            conversation = room_22_convo
        elif int(data['room']) == 23:
            conversation = room_23_convo
        elif int(data['room']) == 24:
            conversation = room_24_convo
        elif int(data['room']) == 25:
            conversation = room_25_convo
        elif int(data['room']) == 26:
            conversation = room_26_convo
        elif int(data['room']) == 27:
            conversation = room_27_convo
        elif int(data['room']) == 28:
            conversation = room_28_convo
        elif int(data['room']) == 29:
            conversation = room_29_convo
        elif int(data['room']) == 30:
            conversation = room_30_convo

        socketio.emit('receive_message', data)
        response = conversation.get_response_to(data['message'])
        time.sleep(1.5)
        print(data['message'])
        data['message'] = response
        data['username'] = "USER"
        socketio.emit('receive_message', data)
        print(data)
        print(response)

    application.logger.info("{} has sent message to room {}: {}".format(data['username'],
                                                                data['room'],
                                                                data['message']))
    data['message_box_id'] = "messages" + str(data['room'])
    if int(data['room']) % 2 == 1 or int(data['room']) > 20:
        chatbot_response_sequence(data)
    else:
        socketio.emit('receive_message', data)

# Allows login manager to access authenticated users
@login_manager.user_loader
def load_user(username):
    return get_user(username)
