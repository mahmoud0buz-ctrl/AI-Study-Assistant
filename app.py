from openai import OpenAI

client = OpenAI()


def ask_ai(prompt):
    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )
        return response.output_text

    except Exception:
        return (
            "\n[AI service is currently unavailable.]"
            "\nThe feature will work when API access is available."
        )


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

        result = ask_ai(
            f"Summarize this topic for a student "
            f"in a clear and simple way:\n\n{topic}"
        )

        print("\n--- AI SUMMARY ---")
        print(result)

    elif choice == "2":
        topic = input("\nEnter the topic for your quiz: ")

        result = ask_ai(
            f"Create 5 multiple-choice quiz questions "
            f"about {topic}. Include the correct answer."
        )

        print("\n--- AI QUIZ ---")
        print(result)

    elif choice == "3":
        concept = input("\nEnter the concept you want explained: ")

        result = ask_ai(
            f"Explain {concept} to a beginner "
            f"using simple language and an example."
        )

        print("\n--- AI EXPLANATION ---")
        print(result)

    elif choice == "4":
        print("\nThank you for using AI Study Assistant!")
        break

    else:
        print("\nInvalid choice. Please choose 1, 2, 3, or 4.")