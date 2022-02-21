from werkzeug.security import check_password_hash
import rooms


class User:
    """To provide a simple experience for presentation attendees, we will
avoid having them create full user accounts - we really only need them to 
have a one-time username for the presentation. Thus, they will be given a
passkey at the demonstration to access the web app instead of being forced
to provide an email and user-set password. kwargs 'email' and 'role' will
be used by presenters only."""

    def __init__(self, username, password, email=None, role=None):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.room = None

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def is_presenter(self): # TODO
        if self.role:
            return True
        else:
            return False

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)
    
    def assign_room(self, room_id):
        self.room = room_id

