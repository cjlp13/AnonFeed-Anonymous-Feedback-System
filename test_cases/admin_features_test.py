# Function to simulate admin searching for feedback
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from feedback import Admin, Feedback, FeedbackManager

# Function to test admin's search_feedback
def test_admin_search_feedback():
    # Setup: mock feedback list
    mock_feedbacks = [
        Feedback("user1", "Great app!", category="Positive Feedbacks"),
        Feedback("user2", "More dark mode options", category="Suggestions"),
        Feedback("user3", "Policy unfair", category="Policy Issues"),
        Feedback("user4", "Harassment report", category="Misconducts")
    ]

    admin = Admin("admin", "adminpass")

    # Test Case 1: Search for Suggestions
    result = admin.search_feedback("Suggestions", mock_feedbacks)
    if len(result) == 1 and result[0].get_message() == "More dark mode options":
        print("Test Case 1: ✅ Passed")
    else:
        print(f"Test Case 1: ❌ Failed. Found {[fb.get_message() for fb in result]}")

    # Test Case 2: Search for Positive Feedbacks
    result = admin.search_feedback("Positive Feedbacks", mock_feedbacks)
    if len(result) == 1 and result[0].get_username() == "user1":
        print("Test Case 2: ✅ Passed")
    else:
        print(f"Test Case 2: ❌ Failed. Found {[fb.get_username() for fb in result]}")

    # Test Case 3: Search for a category with no match
    result = admin.search_feedback("Nomination", mock_feedbacks)
    if len(result) == 0:
        print("Test Case 3: ✅ Passed")
    else:
        print(f"Test Case 3: ❌ Failed. Unexpectedly found results")

# Run the test
if __name__ == "__main__":
    test_admin_search_feedback()
