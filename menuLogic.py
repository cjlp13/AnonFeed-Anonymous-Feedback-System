print("\n1. Submit Feedback")
print("2. View Feedback")
print("3. Admin Login")
print("4. Exit")
choice = input("Enter your choice: ")
        
if choice == "1":
    print("Submit feedback")
        
elif choice == "2":
    print("View Feedback")

elif choice == "3":
    #password required
    print("\nAdmin Panel:")
    print("1. Search Feedback")
    print("2. Reply to Feedback")
    print("3. Exit Admin Panel")
    admin_choice = input("Enter your choice: ")
             
    if admin_choice == "1":
        print("Search for feedbacks")
                        
    elif admin_choice == "2":
        print("Reply to feedback")

    elif admin_choice == "3":
        print("Exiting...")

    else:
        print("Invalid choice")

elif choice == "4":
    print("Exiting...")
else:
    print("Invalid choice.")