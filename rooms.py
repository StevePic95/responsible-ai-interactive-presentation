import pandas as pd
import constants as const

class Room_Manager:
    '''Handles the way users are placed into rooms upon logging in'''
    def __init__(self):
        def human_or_ai(i):
            if i % 2 == 0 and i < 21:
                return "human"
            else:
                return "ai"
        def rtn_false(i):
            return False
        room_dict = {
            'room_id': [str(i) for i in range(1, 31)],
            'room_type': [human_or_ai(i) for i in range(1,31)],
            'occupied': [rtn_false(i) for i in range(1, 31)]
        }
        self.df = pd.DataFrame(room_dict, columns=['room_id', 'room_type', 'occupied'])
        self.human_rooms_available = True
    
    # Flag a room as occupied by changing 'occupied' value to False
    def mark_occupied(self, room_number):
        self.df.iloc[[int(room_number) - 1], [2]] = True

    # Flag a room as available by changing 'occupied' value to True
    def mark_vacant(self, room_number):
        self.df.iloc[[int(room_number) - 1], [2]] = False

    def next_room(self):
        # Create subsets for active rooms and vacant rooms
        active_room_subset = self.df[self.df.iloc[:, 2]==True]
        vacant_room_subset = self.df[self.df.iloc[:, 2]==False]
        
        # Create sub-subsets for ai and human rooms
        vacant_human_chat_subset = vacant_room_subset[vacant_room_subset.iloc[:, 1]=="human"]
        vacant_ai_chat_subset = vacant_room_subset[vacant_room_subset.iloc[:, 1]=="ai"]
        active_ai_chat_subset = active_room_subset[active_room_subset.iloc[:, 1]=="ai"]
        active_human_chat_subset = active_room_subset[active_room_subset.iloc[:, 1]=="human"]
        
        # Count how many of each
        number_of_active_ai_chats = active_ai_chat_subset.shape[0]
        number_of_active_human_chats = active_human_chat_subset.shape[0]
        
        # Return the lowest vacant room of type with fewer active participants (tie goes to ai)
        # To avoid overloading the human volunteer with messages, rooms 21 and up are ai rooms only
        lowest_available_ai_room_number = vacant_ai_chat_subset.iloc[:, 0].astype(int).min()
        if number_of_active_human_chats == 10:
            self.human_rooms_available = False
        if self.human_rooms_available:
            lowest_available_human_room_number = vacant_human_chat_subset.iloc[:, 0].astype(int).min()
            if number_of_active_ai_chats <= number_of_active_human_chats:
                return str(lowest_available_ai_room_number)
            else:
                return str(lowest_available_human_room_number)
        else:
            return str(lowest_available_ai_room_number)

        


