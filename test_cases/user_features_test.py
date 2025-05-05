import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from feedback import FeedbackManager, FeedbackStorage, Feedback

# Mocking FeedbackStorage to avoid file I/O
class MockFeedbackStorage:
    def __init__(self):
        self.saved_feedback = []

    def save_feedback(self, feedback: Feedback):
        self.saved_feedback.append(feedback)

    def get_feedback_list(self):
        return self.saved_feedback

    def update_feedback(self):
        pass  # No-op for testing

# Use mocked storage
mock_storage = MockFeedbackStorage()
feedback_manager = FeedbackManager(limit=3, storage=mock_storage)

# Unit Test Cases
test_cases = [
    {
        # Test Case 1: Normal case = Normal inputs
        "input": {"username": "user1", "message": "Great platform!", "category": "Positive Feedbacks"},
        "expected": "Feedback submitted successfully!"
    },
    {
        # Test Case 2: Invalid case = Missing input field (message)
        "input": {"username": "user2", "message": "", "category": "Suggestions"},
        "expected": "Submission failed: Please enter your feedback."
    },
    {
        # Test Case 3: Normal case = Limit of feedback 
        "input": {"username": "user3", "message": "Spam", "category": "Policy Issues"},
        "expected": "Feedback submitted successfully!"
    },
]

# Run the test cases
for i, test_case in enumerate(test_cases, 1):
    result = feedback_manager.submit_feedback(
        test_case["input"]["username"],
        test_case["input"]["message"],
        test_case["input"]["category"]
    )
    if result == test_case["expected"]:
        print(f"Test Case {i}: ✅ Passed")
    else:
        print(f"Test Case {i}: ❌ Failed")
        print(f"\tExpected: {test_case['expected']}")
        print(f"\tGot     : {result}")
