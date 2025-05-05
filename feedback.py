import csv
from datetime import datetime

class Feedback:
    def __init__(self, username: str, message: str, timestamp=None, admin_reply = "", category = "feedback"):
        self.__username = username
        self.__message = message
        self.__timestamp = timestamp if timestamp else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.__admin_reply = admin_reply
        self.__category = category

    def to_list(self):
        return [self.__username, self.__message, self.__timestamp, self.__admin_reply, self.__category]

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

    def get_category(self):
        return self.__category
    
    def set_category(self, category: str):
        self.__category = category

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
                    self.__feedback_list.append(Feedback(row[0], row[1], row[2], row[3], row[4]))
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

    def submit_feedback(self, username: str, message: str, category: str):
        if not username.strip() and not message.strip():
            return"Submission failed: Make sure to fill the necessary fields (username and message)."
            
        elif not username.strip():
            return"Submission failed: Please enter you username."
            
        elif not message.strip():
            return"Submission failed: Please enter your feedback."
            
        
        if not self.__limit_feedback():
            return"Daily feedback limit reached! Please try again tomorrow."

        feedback = Feedback(username, message, category=category)
        self.__storage.save_feedback(feedback)
        return"Feedback submitted successfully!"

    def view_feedback(self):
        return self.__storage.get_feedback_list()

    def update_feedback(self):
        self.__storage.update_feedback()
   
class Admin:
    def __init__(self, username: str, password: str):
        self.username = username
        self.__password = password

    def get_password(self, input_password: str):
        return self.__password == input_password

    def search_feedback(self, keyword: str, feedbacks: list):
        return [fb for fb in feedbacks if fb.get_category() == keyword]

    def reply_feedback(self, feedback: Feedback, reply: str, manager: FeedbackManager):
        if not reply.strip():
            return "Reply failed: Please enter a reply message."
        
        feedback.set_admin_reply(reply)
        manager.update_feedback()
        return "Reply added successfully!"



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
            category_choice = input("In what category does your feedback fall into: \n\t[1] Misconducts: includes Harassment, Abuse, Discrimination, & Bias \n\t[2] Policy Issues: includes institutional practice, rules, or policy that promotes inequality \n\t[3] Suggestions: Ideas or Recommendations \n\t[4] Positive Feedbacks: Recognition of individuals, initiatives, and practices \nCategory: ")
            match (category_choice):
                case "1":
                    category = "Misconducts"
                case "2":
                    category = "Policy Issues"
                case "3":
                    category = "Suggestions"
                case "4":
                    category = "Positive Feedbacks"
                case _:
                    print("Invalid category.")
                    continue
            
            username = input("Enter your username: ")
            message = input("Enter your feedback: ")

            confirmation = manager.submit_feedback(username, message, category)
            print(confirmation)

        elif choice == "2":
            feedbacks = manager.view_feedback()
            if feedbacks:
                for i, fb in enumerate(feedbacks, 1):
                    print(f"{i}. User - {fb.get_username()}: {fb.get_message()} (Reply - {admin.username}: {fb.get_admin_reply()})")
            else:
                print("No feedback available.")
       
        elif choice == "3":
            password = input("Enter admin password: ")
            if admin.get_password(password):
                filtered_results = []
                while True:
                    print("\nAdmin Panel:")
                    print("1. Search Feedback")
                    print("2. Reply to Feedback")
                    print("3. Exit Admin Panel")
                    admin_choice = input("Enter your choice: ")

                    if admin_choice == "1":
                        category_choice = input("Choose the category of feedbacks to be displayed: \n\t[1] Misconducts \n\t[2] Policy Issues \n\t[3] Suggestions \n\t[4] Positive Feedbacks \nCategory: ")
                        match (category_choice):
                            case "1":
                                keyword = "Misconducts"
                            case "2":
                                keyword = "Policy Issues"
                            case "3":
                                keyword = "Suggestions"
                            case "4":
                                keyword = "Positive Feedbacks"
                            case _:
                                print("Invalid category.")
                                continue

                        feedbacks = manager.view_feedback()
                        filtered_results = admin.search_feedback(keyword, feedbacks)
                        if filtered_results:
                            print(f"Feedbacks for {keyword}: \n")
                            for i, fb in enumerate(filtered_results, 1):
                                print(f"{i}. User - {fb.get_username()}: {fb.get_message()} (Reply - {admin.username}: {fb.get_admin_reply()})")
                        else:
                            print("No matching feedback found.")
                   
                    elif admin_choice == "2":
                        category_choice = input("Choose the category of feedbacks to reply to: \n\t[1] Misconducts \n\t[2] Policy Issues \n\t[3] Suggestions \n\t[4] Positive Feedbacks \nCategory: ")
                        match (category_choice):
                            case "1":
                                keyword = "Misconducts"
                            case "2":
                                keyword = "Policy Issues"
                            case "3":
                                keyword = "Suggestions"
                            case "4":
                                keyword = "Positive Feedbacks"
                            case _:
                                print("Invalid category.")
                                continue

                        feedbacks = manager.view_feedback()
                        filtered_results = admin.search_feedback(keyword, feedbacks)
                        if filtered_results:
                            print(f"Feedbacks for {keyword}: \n")
                            for i, fb in enumerate(filtered_results, 1):
                                print(f"{i}. User - {fb.get_username()}: {fb.get_message()} (Reply - {admin.username}: {fb.get_admin_reply()})")
                            try:
                                index = int(input("Enter feedback number to reply: ")) - 1
                                if 0 <= index < len(filtered_results):
                                    reply = input("Enter your reply: ")
                                    confirmation = admin.reply_feedback(filtered_results[index], reply, manager)
                                    print(confirmation)
                                else:
                                    print("Invalid feedback selection.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                        else:
                            print("No matching feedback found.")

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
