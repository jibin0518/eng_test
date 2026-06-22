import tkinter as tk
import random
import os

# 단어 불러오기
def load_words(filename):
    words = {}

    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    text = text.replace("\n", ",")

    for item in text.split(","):
        item = item.strip()

        if ":" not in item:
            continue

        word, meaning = item.split(":", 1)

        words[word.strip()] = meaning.strip()

    return words


def choose_txt_file():
    txt_files = [
        file for file in os.listdir()
        if file.endswith(".txt")
    ]

    if not txt_files:
        raise Exception("현재 폴더에 txt 파일이 없음")

    print("불러올 수 있는 텍스트 파일:")

    for i, file in enumerate(txt_files, start=1):
        print(f"{i}. {file}")

    while True:
        choice = input("불러올 파일 번호 입력: ")

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(txt_files):
                return txt_files[choice - 1]

        print("잘못 입력함. 다시 입력")


selected_file = choose_txt_file()
words = load_words(selected_file)

print("선택한 파일:", selected_file)
print("단어 개수:", len(words))

if len(words) < 4:
    raise Exception("단어는 최소 4개 이상 필요함")

# 아직 맞추지 못한 단어
remaining_words = list(words.keys())

# 틀린 적 있는 단어
wrong_words = set()

current_word = ""
correct_meaning = ""


def next_question():
    global current_word, correct_meaning

    if not remaining_words:
        finish_quiz()
        return

    current_word = random.choice(remaining_words)
    correct_meaning = words[current_word]

    word_label.config(text=current_word)

    # 정답 제외 뜻들
    wrong_meanings = [
        meaning
        for meaning in words.values()
        if meaning != correct_meaning
    ]

    choices = random.sample(wrong_meanings, 3)
    choices.append(correct_meaning)

    random.shuffle(choices)

    for i in range(4):
        buttons[i].config(
            text=choices[i],
            state="normal",
            command=lambda x=choices[i]: check_answer(x)
        )


def check_answer(selected):
    if selected == correct_meaning:

        # 맞췄으면 목록에서 제거
        remaining_words.remove(current_word)

        result_label.config(
            text="정답!",
            fg="blue"
        )

    else:

        wrong_words.add(current_word)

        result_label.config(
            text=f"오답! 정답: {correct_meaning}",
            fg="red"
        )

    root.after(700, next_question)


def finish_quiz():

    word_label.config(text="퀴즈 종료")

    for btn in buttons:
        btn.destroy()

    if wrong_words:

        text = "틀렸던 단어\n\n"

        for word in sorted(wrong_words):
            text += f"{word} : {words[word]}\n"

    else:
        text = "전부 맞힘!"

    result_label.config(
        text=text,
        fg="black"
    )


# GUI
root = tk.Tk()
root.title("영단어 퀴즈")
root.geometry("600x500")

word_label = tk.Label(
    root,
    text="",
    font=("맑은 고딕", 30)
)
word_label.pack(pady=30)

buttons = []

for _ in range(4):
    btn = tk.Button(
        root,
        font=("맑은 고딕", 14),
        width=30,
        height=2
    )

    btn.pack(pady=5)

    buttons.append(btn)

result_label = tk.Label(
    root,
    text="",
    font=("맑은 고딕", 14)
)

result_label.pack(pady=20)

next_question()

root.mainloop()