from feedback import Feedback, Admin
def submit_feedback(self, username: str, message: str, category: str):
        if not self.__limit_feedback():
            print("Daily feedback limit reached! Please try again tomorrow.")
            return
        feedback = Feedback(username, message, category=category)
        self.__storage.save_feedback(feedback)
        print("Feedback submitted successfully!")

# Unit Test Cases
test_cases = [
    {
        "input": {"username": "user1", "message": "Great platform!", "category": "Positive Feedbacks"},
        "expected": "Feedback submitted successfully!"
    },
    {
        "input": {"username": "user2", "message": "", "category": "Suggestions"},
        "expected": "Feedback submitted successfully!"  # No message validation in current code
    },
    {
        "input": {"username": "user3", "message": "Spam", "category": "Policy Issues"},
        "expected": "Feedback submitted successfully!"  # Repeats allowed unless limit exceeded
    },
]

# Run the test cases
for test_case in test_cases:
    print(f"Running test case: {test_case}")

