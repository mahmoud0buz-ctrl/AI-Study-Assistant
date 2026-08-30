from openai import OpenAI
from datetime import datetime
import json
import os

# ==========================================
# AI STUDY ASSISTANT
# ==========================================

client = OpenAI()

HISTORY_FILE = "study_history.json"


def load_history():
    """Load saved study history from the JSON file."""

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_history():
    """Save study history to the JSON file."""

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(study_history, file, indent=4, ensure_ascii=False)
    except OSError:
        print("\nCould not save study history.")


study_history = load_history()


def ask_ai(prompt):
    """Send a request to the AI and handle errors safely."""

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception:
        return (
            "AI service is currently unavailable.\n"
            "This may be because the API has no available credits."
        )


def add_history(activity_type, topic):
    """Add a study activity to the history."""

    activity = {
        "type": activity_type,
        "topic": topic,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    study_history.append(activity)
    save_history()


def show_history():
    """Display study history."""

    print("\n================================")
    print("         STUDY HISTORY")
    print("================================")

    if not study_history:
        print("\nNo study activities yet.")
        return

    for number, activity in enumerate(study_history, start=1):
        print(f"\n{number}. {activity['type']}")
        print(f"   Topic: {activity['topic']}")
        print(f"   Time: {activity['time']}")


def clear_history():
    """Clear all saved study history."""

    study_history.clear()
    save_history()

    print("\nStudy history cleared.")


def summarize_topic():
    """Summarize a topic using AI."""

    topic = input("\nEnter the topic you want to summarize: ")

    if not topic.strip():
        print("\nPlease enter a valid topic.")
        return

    print("\nGenerating summary...")

    result = ask_ai(
        f"""
Summarize the following topic for a student:

{topic}

Requirements:
- Use simple language.
- Explain the main ideas.
- Use short paragraphs.
- Include important points.
"""
    )

    print("\n--- AI SUMMARY ---")
    print(result)

    add_history("Summary", topic)


def generate_quiz():
    """Generate quiz questions using AI."""

    topic = input("\nEnter the topic for your quiz: ")

    if not topic.strip():
        print("\nPlease enter a valid topic.")
        return

    print("\nGenerating quiz...")

    result = ask_ai(
        f"""
Create 5 multiple-choice questions about:

{topic}

Requirements:
- Four choices for each question.
- Clearly identify the correct answer.
- Questions should test understanding.
- Suitable for a student.
"""
    )

    print("\n--- AI QUIZ ---")
    print(result)

    add_history("Quiz", topic)


def explain_concept():
    """Explain a concept using AI."""

    concept = input("\nEnter the concept you want explained: ")

    if not concept.strip():
        print("\nPlease enter a valid concept.")
        return

    print("\nGenerating explanation...")

    result = ask_ai(
        f"""
Explain the following concept to a beginner:

{concept}

Requirements:
- Use simple language.
- Explain step by step.
- Give a practical example.
- Mention why the concept is important.
"""
    )

    print("\n--- AI EXPLANATION ---")
    print(result)

    add_history("Explanation", concept)


def main():
    """Run the main application."""

    print("================================")
    print("       AI STUDY ASSISTANT")
    print("================================")

    name = input("\nWhat is your name? ")

    if not name.strip():
        name = "Student"

    print(f"\nHello {name}! 👋")
    print("Your AI Study Assistant is ready.")

    while True:
        print("\n================================")
        print("             MENU")
        print("================================")

        print("1. Summarize a topic")
        print("2. Generate quiz questions")
        print("3. Explain a concept")
        print("4. View study history")
        print("5. Clear study history")
        print("6. Exit")

        choice = input("\nChoose an option (1-6): ")

        if choice == "1":
            summarize_topic()

        elif choice == "2":
            generate_quiz()

        elif choice == "3":
            explain_concept()

        elif choice == "4":
            show_history()

        elif choice == "5":
            clear_history()

        elif choice == "6":
            print("\n================================")
            print("Thank you for using")
            print("AI Study Assistant!")
            print("================================")
            break

        else:
            print("\nInvalid choice.")
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()