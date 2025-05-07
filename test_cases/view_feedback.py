import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from feedback import FeedbackManager, Feedback, FeedbackStorage

# Mocking feedback
class MockFeedbackStorage:
    def __init__(self):
        self.saved_feedback = []
    
    def save_feedback(self, feedback: Feedback):
        self.saved_feedback.append(feedback)
    
    def get_feedback_list(self):
        return self.saved_feedback.copy()  # Return copy to prevent modification
    
    def update_feedback(self):
        pass  # No-op for testing

def test_view_feedback():
    """Test cases for view_feedback functionality"""
    print("\n=== Testing View Feedback ===")
    
    # Setup
    storage = MockFeedbackStorage()
    manager = FeedbackManager(limit=3, storage=storage)
    
    # Test Case 1: View empty feedback list
    empty_result = manager.view_feedback()
    assert len(empty_result) == 0, f"Expected 0 feedbacks, got {len(empty_result)}"
    print("Test Case 1 (Empty List): ✅ Passed")
    
    # Test Case 2: View single feedback
    test_fb = Feedback("user1", "Test feedback", category="Suggestions")
    storage.save_feedback(test_fb)
    single_result = manager.view_feedback()
    assert len(single_result) == 1, "Expected 1 feedback"
    assert single_result[0].get_username() == "user1", "Username mismatch"
    print("Test Case 2 (Single Feedback): ✅ Passed")
    
    # Test Case 3: View multiple feedbacks
    storage.save_feedback(Feedback("user2", "Second", category="Policy Issues"))
    storage.save_feedback(Feedback("user3", "Third", admin_reply="Test reply", category="Misconducts"))
    multi_result = manager.view_feedback()
    
    assert len(multi_result) == 3, f"Expected 3 feedbacks, got {len(multi_result)}"
    assert multi_result[2].get_admin_reply() == "Test reply", "Admin reply missing"
    print("Test Case 3 (Multiple Feedbacks): ✅ Passed")

if __name__ == "__main__":
    test_view_feedback()