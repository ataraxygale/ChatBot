import json
from difflib import get_close_matches

# Load knowledge base pull from JSON
def load_knowledge_base(file_paths: list) -> dict:
    knowledge_base = {"questions": []}

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            knowledge_base["questions"].extend(data.get("questions", []))

    return knowledge_base

# Need to save old responses in memory
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Finds best one from the dictionary
# Will return a string or nothing if it doesn't exist
# n=1 best answer possible - cutoff accuracy, .6 60% accurate or nothing without accuracy specified
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    # array looking for q in index questions
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chat_bot():
    global kbfile_paths  # Access the global variable

    # type dictionary
    knowledge_base: dict = load_knowledge_base(kbfile_paths)

    # need an infinite loop for this to run here
    while True:
        user_input: str = input('You:')
        # this is how to end the chatbot program
        if user_input.lower() == 'quit':
            break

        # loads user input, checks q of question in the json knowledge base through the question index loaded
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        # checks if there is a matching answer in the index here in any form
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        # if no matching answer in the index
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            new_answer: str = input('Type the answer or "skip" to skip: ')

            # if the user doesn't type skip then do the following
            # then the new answer will be appended
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base(kbfile_paths[0], knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    kbfile_paths = ['knowledge_base.json', 'dialogues_act.txt', 'dialogues_emotion.txt', 'dialogues_text.txt', 'dialogues_topic.txt']
    chat_bot()
