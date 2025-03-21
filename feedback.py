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
