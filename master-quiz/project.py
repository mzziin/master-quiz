import json
import requests
import random
import html


def main():
    score = 0
    flag = 0
    while True:
        is_begin = start_or_exit_prompt(flag)
        if is_begin:
            level = get_level()
            results = get_api_data(level)

            for i, data in enumerate(results):
                answer_options, correct_answer_index = get_options(data)

                # question = re.sub(r"&[^;]*;", "", data["question"])
                question = html.unescape(data["question"])
                print(f"Q{i+1}) {question}")

                for i, option in enumerate(answer_options):
                    print(f"  {i+1} - {option}")
                print()

                user_answer = get_user_answer(answer_options)
                # correct_answer = re.sub(r"&[^;]*;", "", data["correct_answer"])
                correct_answer = html.unescape(data["correct_answer"])

                if (user_answer == correct_answer.lower() or user_answer == correct_answer_index):
                    print("correct\n")
                    score += 1
                else:
                    print(f"Wrong! correct answer is {correct_answer}\n")
                answer_options = []

            print(f"You scored {score} out of 10")
            score = 0
            flag = 1
        else:
            exit()

def start_or_exit_prompt(flag):
    desc = " again" if flag else ""
    while True:
        val = input(f"Do you want to start{desc}? (y/n)").lower().strip()
        if val == 'y':
            return True
        elif val == 'n':
            return False
        else:
            print("Enter valid input")
            continue

def get_options(data):
    options = [data["correct_answer"]] + data["incorrect_answers"]
    # options_filtered = [re.sub(r"&[^;]*;", "", x) for x in options]
    # correct_answer = re.sub(r"&[^;]*;", "", data["correct_answer"])
    options_filtered = [html.unescape(x) for x in options]
    correct_answer = html.unescape(data["correct_answer"])
    random.shuffle(options_filtered)
    crct_answer_index = str(options_filtered.index(correct_answer) + 1)
    return options_filtered, crct_answer_index


def get_api_data(level):
    quiz_api = f"https://opentdb.com/api.php?amount=10&difficulty={level}"
    try:
        response = requests.get(quiz_api)
        data = json.loads(response.text)
        # data = html.unescape(data["results"]) todo: check wheather it will work or not
        return data["results"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quiz data: {e}")
        exit()


def get_level():
    options = ["easy", "medium", "hard", "mixed", "1", "2", "3", "4"]
    while True:
        level = (
            input("Choose your level:\n1)Easy\n2)Medium\n3)Hard\n4)Mixed\n")
            .strip()
            .lower()
        )
        if level not in options:
            print("\nEnter valid input!\n")
            continue
        if level == "mixed":
            return ""
        match level:
            case "1":
                return "easy"
            case "2":
                return "medium"
            case "3":
                return "hard"
            case "4":
                return ""
        return level


def get_user_answer(answer_options):
    answer_options = [x.lower() for x in answer_options]
    while True:
        user_answer = input("Your answer: ").lower().strip()
        print()
        if user_answer in answer_options or user_answer in ["1", "2", "3", "4"]:
            return user_answer
        print("Please enter a valid answer!\n")


if __name__ == "__main__":
    main()