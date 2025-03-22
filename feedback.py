import csv
from datetime import datetime

class Feedback:
    def __init__(self, username: str, message: str, timestamp=None, admin_reply=""):
        self.__username = username
        self.__message = message
        self.__timestamp = timestamp if timestamp else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.__admin_reply = admin_reply

    def to_list(self):
        return [self.__username, self.__message, self.__timestamp, self.__admin_reply]

    def get_username(self):
        return self.__username

    def get_message(self):
        return self.__message

    def get_timestamp(self):
        return self.__timestamp

    def get_admin_reply(self):
        return self.__admin_reply

    def set_admin_reply(self, reply: str):
        self.__admin_reply = reply

class FeedbackStorage:
    FILE_NAME = "feedback.csv"

    def __init__(self):
        self.__feedback_list = []
        self.__load_feedback()

    def save_feedback(self, feedback: Feedback):
        self.__feedback_list.append(feedback)
        with open(FeedbackStorage.FILE_NAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(feedback.to_list())

    def __load_feedback(self):
        self.__feedback_list = []
        try:
            with open(FeedbackStorage.FILE_NAME, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 4: 
                        continue
                    self.__feedback_list.append(Feedback(row[0], row[1], row[2], row[3]))
        except FileNotFoundError:
            pass

    def get_feedback_list(self):
        return self.__feedback_list

    def update_feedback(self):
        with open(FeedbackStorage.FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            for fb in self.__feedback_list:
                writer.writerow(fb.to_list())

class FeedbackManager:
    def __init__(self, limit: int, storage: FeedbackStorage):
        self.__limit = limit
        self.__storage = storage

    def __limit_feedback(self):
        feedbacks = self.__storage.get_feedback_list()
        today = datetime.now().strftime('%Y-%m-%d')
        todays_feedbacks = [fb for fb in feedbacks if fb.get_timestamp().startswith(today)]
        return len(todays_feedbacks) < self.__limit

    def submit_feedback(self, username: str, message: str):
        if not self.__limit_feedback():
            print("Daily feedback limit reached! Please try again tomorrow.")
            return
        feedback = Feedback(username, message)
        self.__storage.save_feedback(feedback)
        print("Feedback submitted successfully!")

    def view_feedback(self):
        return self.__storage.get_feedback_list()

    def update_feedback(self):
        self.__storage.update_feedback()
   
class Admin:
    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password

    def get_password(self, input_password: str):
        return self.__password == input_password

    def search_feedback(self, keyword: str, feedbacks: list):
        return [fb for fb in feedbacks if keyword.lower() in fb.get_message().lower()]

    def reply_feedback(self, feedback_index: int, reply: str, manager: FeedbackManager):
        feedbacks = manager.view_feedback()
        if 0 <= feedback_index < len(feedbacks):
            feedbacks[feedback_index].set_admin_reply(reply)
            manager.update_feedback()
            print("Reply added successfully!")
        else:
            print("Invalid feedback selection.")

if __name__ == "__main__":
    storage = FeedbackStorage()
    manager = FeedbackManager(limit=5, storage=storage)
    admin = Admin(username="Admin", password="adminpass")
   
    while True:
        print("\n1. Submit Feedback")
        print("2. View Feedback")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter your username: ")
            message = input("Enter your feedback: ")
            manager.submit_feedback(username, message)

        elif choice == "2":
            feedbacks = manager.view_feedback()
            if feedbacks:
                for i, fb in enumerate(feedbacks, 1):
                    print(f"{i}. User - {fb.get_username()}: {fb.get_message()} (Reply - {admin.__username}: {fb.get_admin_reply()})")
            else:
                print("No feedback available.")
       
        elif choice == "3":
            password = input("Enter admin password: ")
            if admin.get_password(password):

                while True:
                    print("\nAdmin Panel:")
                    print("1. Search Feedback")
                    print("2. Reply to Feedback")
                    print("3. Exit Admin Panel")
                    admin_choice = input("Enter your choice: ")

                    if admin_choice == "1":
                        keyword = input("Enter keyword to search: ")
                        feedbacks = manager.view_feedback()
                        results = admin.search_feedback(keyword, feedbacks)
                        if results:
                            for i, fb in enumerate(results, 1):
                                print(f"{i}. User - {fb.get_username()}: {fb.get_message()} (Reply - {admin.__username}: {fb.get_admin_reply()})")
                        else:
                            print("No matching feedback found.")
                   
                    elif admin_choice == "2":
                        feedbacks = manager.view_feedback()
                        if feedbacks:
                            for i, fb in enumerate(feedbacks, 1):
                                print(f"{i}. User - {fb.get_username()}: {fb.get_message()} (Reply - {admin.__username}: {fb.get_admin_reply()})")
                            try:
                                index = int(input("Enter feedback number to reply: ")) - 1
                                if 0 <= index < len(feedbacks):
                                    reply = input("Enter your reply: ")
                                    admin.reply_feedback(index, reply, manager)
                                else:
                                    print("Invalid feedback selection.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                        else:
                            print("No feedback available to reply to.")

                    elif admin_choice == "3":
                        break
                    else:
                        print("Invalid choice.")
            else:
                print("Incorrect password!")

        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")
