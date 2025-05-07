import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from feedback import Admin, Feedback, FeedbackManager, FeedbackStorage
from datetime import datetime


# Function to test admin's reply_feedback
def test_admin_reply_feedback():
    # Setup test environment
    storage = FeedbackStorage()
    manager = FeedbackManager(limit=5, storage=storage)
    admin = Admin("admin", "adminpass")
    
    # Clear any existing feedback
    storage._FeedbackStorage__feedback_list = []
    
    # Add test feedback
    test_feedback = Feedback("test_user", "Test feedback message", category="Suggestions")
    storage.save_feedback(test_feedback)
    feedbacks = storage.get_feedback_list()
    
    # Test Case 1: Successful reply
    reply_message = "Thank you for your feedback!"
    result = admin.reply_feedback(feedbacks[0], reply_message, manager)
    if result == "Reply added successfully!" and feedbacks[0].get_admin_reply() == reply_message:
        print("Test Case 1 (Reply): ✅ Passed")
    else:
        print(f"Test Case 1 (Reply): ❌ Failed. Result: {result}, Reply: {feedbacks[0].get_admin_reply()}")
    
    # Test Case 2: Empty reply
    result = admin.reply_feedback(feedbacks[0], "", manager)
    if result == "Reply failed: Please enter a reply message." and feedbacks[0].get_admin_reply() == reply_message:  # Should preserve previous reply
        print("Test Case 2 (Reply): ✅ Passed")
    else:
        print(f"Test Case 2 (Reply): ❌ Failed. Result: {result}, Reply: {feedbacks[0].get_admin_reply()}")
    
    # Test Case 3: Reply persistence
    new_storage = FeedbackStorage()  # Simulate program restart
    persisted_feedbacks = new_storage.get_feedback_list()
    if len(persisted_feedbacks) > 0 and persisted_feedbacks[0].get_admin_reply() == reply_message:
        print("Test Case 3 (Reply): ✅ Passed")
    else:
        print(f"Test Case 3 (Reply): ❌ Failed. Persisted reply: {persisted_feedbacks[0].get_admin_reply() if len(persisted_feedbacks) > 0 else 'None'}")

if __name__ == "__main__":
    print("\n=== Testing reply_feedback ===")
    test_admin_reply_feedback()