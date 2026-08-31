from openai import OpenAI
from datetime import datetime
import json
import os

# ==========================================
# AI STUDY ASSISTANT
# ==========================================

client = OpenAI()
HISTORY_FILE = "study_history.json"


# ==========================================
# HISTORY DATA
# ==========================================

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


study_history = load_history()


def save_history():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(
                study_history,
                file,
                indent=4,
                ensure_ascii=False
            )
    except OSError:
        print("\nCould not save study history.")


def add_history(activity_type, topic, score=None, total=None):
    activity = {
        "type": activity_type,
        "topic": topic,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    if score is not None and total is not None:
        activity["score"] = score
        activity["total"] = total

    study_history.append(activity)
    save_history()


# ==========================================
# AI FUNCTION
# ==========================================

def ask_ai(prompt):
    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception:
        return None


# ==========================================
# QUIZ QUESTIONS
# ==========================================

quiz_questions = {
    "python": [
        {
            "question": "Which symbol is used to create a comment in Python?",
            "options": ["//", "#", "/*", "--"],
            "answer": 2
        },
        {
            "question": "Which function is used to display text in Python?",
            "options": ["show()", "display()", "print()", "write()"],
            "answer": 3
        },
        {
            "question": "Which data type stores True or False?",
            "options": ["String", "Boolean", "Integer", "Float"],
            "answer": 2
        },
        {
            "question": "Which keyword is used to define a function?",
            "options": ["function", "define", "def", "func"],
            "answer": 3
        },
        {
            "question": "Which symbol is used for multiplication?",
            "options": ["x", "*", "%", "^"],
            "answer": 2
        }
    ],

    "artificial intelligence": [
        {
            "question": "What does AI stand for?",
            "options": [
                "Automated Internet",
                "Artificial Intelligence",
                "Advanced Information",
                "Automatic Intelligence"
            ],
            "answer": 2
        },
        {
            "question": "Which field is closely related to AI?",
            "options": [
                "Machine Learning",
                "Photography",
                "Accounting",
                "Architecture"
            ],
            "answer": 1
        },
        {
            "question": "What is machine learning?",
            "options": [
                "A type of computer hardware",
                "A method where computers learn from data",
                "A programming language",
                "A web browser"
            ],
            "answer": 2
        },
        {
            "question": "Which is an example of AI?",
            "options": [
                "A calculator doing 2 + 2",
                "A simple light switch",
                "A recommendation system",
                "A USB cable"
            ],
            "answer": 3
        },
        {
            "question": "What is training data used for?",
            "options": [
                "Teaching a machine learning model",
                "Charging a computer",
                "Installing Windows",
                "Creating a keyboard"
            ],
            "answer": 1
        }
    ]
}


# ==========================================
# LOCAL QUIZ
# ==========================================

def run_local_quiz(topic):
    topic_key = topic.lower().strip()

    if topic_key not in quiz_questions:
        print("\nWe don't have a local quiz for this topic yet.")
        print("Try: Python")
        print("or: Artificial Intelligence")
        return

    questions = quiz_questions[topic_key]
    score = 0

    print("\n================================")
    print("          QUIZ START")
    print("================================")

    for number, question in enumerate(questions, start=1):
        print(f"\nQuestion {number}:")
        print(question["question"])

        for index, option in enumerate(
            question["options"],
            start=1
        ):
            print(f"{index}. {option}")

        while True:
            answer = input("\nYour answer (1-4): ")

            if answer in ["1", "2", "3", "4"]:
                answer = int(answer)
                break

            print("Please enter a number from 1 to 4.")

        if answer == question["answer"]:
            print("Correct! ✅")
            score += 1
        else:
            correct_answer = question["options"][
                question["answer"] - 1
            ]

            print("Incorrect ❌")
            print(f"Correct answer: {correct_answer}")

    total = len(questions)
    percentage = (score / total) * 100

    print("\n================================")
    print("          QUIZ RESULT")
    print("================================")

    print(f"\nYour score: {score}/{total}")
    print(f"Percentage: {percentage:.0f}%")

    if percentage == 100:
        print("Excellent! 🏆")
    elif percentage >= 80:
        print("Great job! 🎉")
    elif percentage >= 60:
        print("Good effort! Keep practicing. 💪")
    else:
        print("Keep studying and try again! 📚")

    add_history(
        "Quiz",
        topic,
        score,
        total
    )


# ==========================================
# SUMMARY
# ==========================================

def summarize_topic():
    topic = input(
        "\nEnter the topic you want to summarize: "
    )

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

    if result:
        print(result)
    else:
        print("AI service is currently unavailable.")
        print("This feature requires API access.")

    add_history("Summary", topic)


# ==========================================
# QUIZ
# ==========================================

def generate_quiz():
    topic = input(
        "\nEnter the topic for your quiz: "
    )

    if not topic.strip():
        print("\nPlease enter a valid topic.")
        return

    topic_key = topic.lower().strip()

    if topic_key in quiz_questions:
        run_local_quiz(topic)
        return

    print("\nGenerating AI quiz...")

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

    if result:
        print(result)
        add_history("Quiz", topic)
    else:
        print("AI service is currently unavailable.")
        print("\nAvailable offline quiz topics:")
        print("- Python")
        print("- Artificial Intelligence")


# ==========================================
# EXPLANATION
# ==========================================

def explain_concept():
    concept = input(
        "\nEnter the concept you want explained: "
    )

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

    if result:
        print(result)
    else:
        print("AI service is currently unavailable.")
        print("This feature requires API access.")

    add_history("Explanation", concept)


# ==========================================
# STUDY HISTORY
# ==========================================

def show_history():
    print("\n================================")
    print("         STUDY HISTORY")
    print("================================")

    if not study_history:
        print("\nNo study activities yet.")
        return

    for number, activity in enumerate(
        study_history,
        start=1
    ):
        print(f"\n{number}. {activity['type']}")
        print(f"   Topic: {activity['topic']}")
        print(f"   Time: {activity['time']}")

        if "score" in activity:
            print(
                f"   Score: "
                f"{activity['score']}/{activity['total']}"
            )


# ==========================================
# STATISTICS
# ==========================================

def show_statistics():
    print("\n================================")
    print("        STUDENT STATISTICS")
    print("================================")

    if not study_history:
        print("\nNo study data available yet.")
        return

    total_activities = len(study_history)

    summaries = 0
    explanations = 0
    quizzes = 0

    quiz_percentages = []
    topics = set()

    for activity in study_history:
        activity_type = activity.get("type")
        topic = activity.get("topic")

        if topic:
            topics.add(topic.lower())

        if activity_type == "Summary":
            summaries += 1

        elif activity_type == "Explanation":
            explanations += 1

        elif activity_type == "Quiz":
            quizzes += 1

            if (
                "score" in activity
                and "total" in activity
                and activity["total"] > 0
            ):
                percentage = (
                    activity["score"]
                    / activity["total"]
                ) * 100

                quiz_percentages.append(percentage)

    print(f"\nTotal study activities: {total_activities}")
    print(f"Summaries: {summaries}")
    print(f"Explanations: {explanations}")
    print(f"Quizzes: {quizzes}")
    print(f"Different topics studied: {len(topics)}")

    if quiz_percentages:
        average = sum(quiz_percentages) / len(
            quiz_percentages
        )

        best = max(quiz_percentages)

        print(f"Average quiz score: {average:.0f}%")
        print(f"Best quiz score: {best:.0f}%")
    else:
        print("Average quiz score: No quiz results yet.")
        print("Best quiz score: No quiz results yet.")


# ==========================================
# LEARNING PROGRESS
# ==========================================

def show_progress():
    print("\n================================")
    print("        LEARNING PROGRESS")
    print("================================")

    quiz_results = []

    for activity in study_history:
        if (
            activity.get("type") == "Quiz"
            and "score" in activity
            and "total" in activity
        ):
            total = activity["total"]

            if total > 0:
                percentage = (
                    activity["score"] / total
                ) * 100

                quiz_results.append({
                    "topic": activity["topic"],
                    "score": activity["score"],
                    "total": total,
                    "percentage": percentage,
                    "time": activity["time"]
                })

    if not quiz_results:
        print("\nNo completed quiz results yet.")
        return

    print("\nQuiz Performance")
    print("----------------")

    for number, quiz in enumerate(
        quiz_results,
        start=1
    ):
        print(f"\nQuiz {number}: {quiz['topic']}")
        print(
            f"Score: "
            f"{quiz['score']}/{quiz['total']}"
        )
        print(
            f"Percentage: "
            f"{quiz['percentage']:.0f}%"
        )
        print(f"Date: {quiz['time']}")

    percentages = [
        quiz["percentage"]
        for quiz in quiz_results
    ]

    average = sum(percentages) / len(percentages)
    best = max(percentages)
    worst = min(percentages)

    print("\n================================")
    print("          OVERALL PROGRESS")
    print("================================")

    print(f"\nQuizzes completed: {len(quiz_results)}")
    print(f"Average score: {average:.0f}%")
    print(f"Best score: {best:.0f}%")
    print(f"Worst score: {worst:.0f}%")

    if len(quiz_results) >= 2:
        first = quiz_results[0]["percentage"]
        latest = quiz_results[-1]["percentage"]

        improvement = latest - first

        print(
            f"\nProgress since first quiz: "
            f"{improvement:+.0f}%"
        )

        if improvement > 0:
            print("You're improving! 📈🔥")
        elif improvement == 0:
            print("Your performance is stable. 💪")
        else:
            print("Keep practicing! You can improve. 📚")


# ==========================================
# CLEAR HISTORY
# ==========================================

def clear_history():
    confirmation = input(
        "\nAre you sure you want to clear your history? "
        "(yes/no): "
    )

    if confirmation.lower() == "yes":
        study_history.clear()
        save_history()
        print("\nStudy history cleared. 🗑️")
    else:
        print("\nHistory was not changed.")


# ==========================================
# MAIN MENU
# ==========================================

def main():
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
        print("5. View statistics")
        print("6. View learning progress")
        print("7. Clear study history")
        print("8. Exit")

        choice = input(
            "\nChoose an option (1-8): "
        )

        if choice == "1":
            summarize_topic()

        elif choice == "2":
            generate_quiz()

        elif choice == "3":
            explain_concept()

        elif choice == "4":
            show_history()

        elif choice == "5":
            show_statistics()

        elif choice == "6":
            show_progress()

        elif choice == "7":
            clear_history()

        elif choice == "8":
            print("\n================================")
            print("Thank you for using")
            print("AI Study Assistant!")
            print("================================")
            break

        else:
            print("\nInvalid choice.")
            print("Please choose a number from 1 to 8.")


if __name__ == "__main__":
    main()