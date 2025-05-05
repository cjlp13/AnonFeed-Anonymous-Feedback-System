test_cases = [
    {
        "input": {"admin_password": "adminpass"},
        "expected": True
    },
    {
        "input": {"admin_password": "wrongpass"},
        "expected": False
    },
    {
        "input": {"search_keyword": "Suggestions", "feedbacks": [
            Feedback("u1", "a", category="Suggestions"),
            Feedback("u2", "b", category="Misconducts")
        ]},
        "expected": 1
    },
    {
        "input": {"reply_to": Feedback("u3", "Needs improvement", category="Suggestions"), "reply": "Thank you"},
        "expected": "Thank you"
    }
]