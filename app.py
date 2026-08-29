print("================================")
print("       AI STUDY ASSISTANT")
print("================================")

name = input("\nWhat is your name? ")

print(f"\nHello {name}! 👋")

while True:
    print("\nWhat would you like to do?")
    print("1. Summarize a topic")
    print("2. Generate quiz questions")
    print("3. Explain a concept")
    print("4. Exit")

    choice = input("\nChoose an option (1-4): ")

    if choice == "1":
        topic = input("\nEnter the topic you want to summarize: ")
        print(f"\nYour topic: {topic}")
        print("Summary feature coming soon...")

    elif choice == "2":
        topic = input("\nEnter the topic for your quiz: ")
        print(f"\nCreating quiz questions about: {topic}")
        print("Quiz feature coming soon...")

    elif choice == "3":
        concept = input("\nEnter the concept you want explained: ")
        print(f"\nExplaining: {concept}")
        print("Explanation feature coming soon...")

    elif choice == "4":
        print("\nThank you for using AI Study Assistant!")
        break

    else:
        print("\nInvalid choice. Please choose 1, 2, 3, or 4.")