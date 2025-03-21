import csv
from datetime import datetime

class Feedback:
    def __init__(self, user_id: str, message: str, timestamp=None, admin_reply=""):
        self.user_id = user_id
        self.message = message
        self.timestamp = timestamp if timestamp else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.admin_reply = admin_reply

    def to_list(self):
        return [self.user_id, self.message, self.timestamp, self.admin_reply]

class FeedbackStorage:
    FILE_NAME = "feedback.csv"

    def save_feedback(feedback: Feedback):
        with open(FeedbackStorage.FILE_NAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(feedback.to_list())

    def load_feedback():
        feedback_list = []
        try:
            with open(FeedbackStorage.FILE_NAME, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 4:  # Ensuring correct number of columns
                        continue
                    feedback_list.append(Feedback(row[0], row[1], row[2], row[3]))
        except FileNotFoundError:
            pass
        return feedback_list

class FeedbackManager:
    def __init__(self, limit: int):
        self.limit = limit

    def limit_feedback(self):
        feedbacks = FeedbackStorage.load_feedback()
        today = datetime.now().strftime('%Y-%m-%d')
        todays_feedbacks = [fb for fb in feedbacks if fb.timestamp.startswith(today)]
        return len(todays_feedbacks) < self.limit

    def submit_feedback(self, user_id: str, message: str):
        if not self.limit_feedback():
            print("Daily feedback limit reached! Please try again tomorrow.")
            return
        
        feedback = Feedback(user_id, message)
        FeedbackStorage.save_feedback(feedback)
        print("Feedback submitted successfully!")

    def view_feedback(self):
        return FeedbackStorage.load_feedback()
    
    class Admin:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def authenticate(self, input_password: str):
        return self.password == input_password

    def search_feedback(self, keyword: str, feedbacks: list):
        return [fb for fb in feedbacks if keyword.lower() in fb.message.lower()]
    
    def reply_feedback(self, feedback_index: int, reply: str):
        feedbacks = FeedbackStorage.load_feedback()
        if 0 <= feedback_index < len(feedbacks):
            feedbacks[feedback_index].admin_reply = reply
            with open(FeedbackStorage.FILE_NAME, mode='w', newline='') as file:
                writer = csv.writer(file)
                for fb in feedbacks:
                    writer.writerow(fb.to_list())
            print("Reply added successfully!")
        else:
            print("Invalid feedback selection.")


