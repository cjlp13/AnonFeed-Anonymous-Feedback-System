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
    Feedback("user1", "Add dark mode", category="Suggestions"),
    Feedback("user2", "Policy Y is unfair", category="Policy Issues"),
    Feedback("user3", "Great service!", category="Positive Feedbacks")
]

for fb in test_feedbacks:
    mock_storage.save_feedback(fb)


def test_admin_search_invalid_category():
    print("\nTest Case: Admin attempts to search feedback under invalid category")
    
    
    invalid_keyword = "InvalidCategory"
    feedbacks = feedback_manager.view_feedback()
    filtered_results = admin.search_feedback(invalid_keyword, feedbacks)
    
    
    print(f"Expected: 0 feedbacks found for category '{invalid_keyword}'")
    print(f"Found: {len(filtered_results)} feedbacks")
    
    if len(filtered_results) == 0:
        print("✅ Passed - No feedbacks returned for invalid category")
    else:
        print("❌ Failed - Feedback(s) returned for invalid category")
        print("Found feedbacks:")
        for fb in filtered_results:
            print(f"- {fb.get_category()}: {fb.get_message()}")


test_admin_search_invalid_category()