import sys
import os
feedback_path = "C:\Users\Ron G\Desktop\AnonFeed\AnonFeed-Anonymous-Feedback-System"
sys.path.insert(0, feedback_path)

from feedback import FeedbackManager, FeedbackStorage, Feedback, Admin


class MockFeedbackStorage:
    def __init__(self):
        self.saved_feedback = []

    def save_feedback(self, feedback: Feedback):
        self.saved_feedback.append(feedback)

    def get_feedback_list(self):
        return self.saved_feedback

    def update_feedback(self):
        pass  # No-op for testing


mock_storage = MockFeedbackStorage()
feedback_manager = FeedbackManager(limit=5, storage=mock_storage)
admin = Admin(username="Admin", password="adminpass")

test_feedbacks = [
    Feedback("user1", "Add more features", category="Suggestions"),
    Feedback("user2", "Improve UI", category="Suggestions"),
    Feedback("user3", "Bad behavior in chat", category="Misconducts"),
    Feedback("user4", "Change policy X", category="Policy Issues"),
    Feedback("user5", "Great job!", category="Positive Feedbacks")
]

for fb in test_feedbacks:
    mock_storage.save_feedback(fb)


def test_admin_search_suggestions():
    print("\nTest Case: Admin searches feedback under 'Suggestions' category")
    
   
    keyword = "Suggestions"
    feedbacks = feedback_manager.view_feedback()
    filtered_results = admin.search_feedback(keyword, feedbacks)
    

    suggestions_found = [fb for fb in filtered_results if fb.get_category() == "Suggestions"]
    non_suggestions = [fb for fb in filtered_results if fb.get_category() != "Suggestions"]
    
    print(f"Expected: 2 feedbacks in 'Suggestions' category")
    print(f"Found: {len(suggestions_found)} feedbacks in 'Suggestions' category")
    
    if len(suggestions_found) == 2 and len(non_suggestions) == 0:
        print("✅ Passed - Correct number of suggestions found and no unrelated feedbacks")
        print("Found suggestions:")
        for i, fb in enumerate(suggestions_found, 1):
            print(f"{i}. {fb.get_username()}: {fb.get_message()}")
    else:
        print("❌ Failed - Incorrect feedbacks returned")
        if len(non_suggestions) > 0:
            print("Found non-suggestion feedbacks in results:")
            for fb in non_suggestions:
                print(f"- {fb.get_category()}: {fb.get_message()}")


test_admin_search_suggestions()

