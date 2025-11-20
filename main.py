import tkinter as tk
import csv
import random


class App:
    """Main class"""

    def __init__(self):
        # Load questions
        self.data_list = self.get_questions_from_db("20_card_deck.csv")
        # To display questions
        self.wrong_questions_list = []
        random.shuffle(self.data_list)

        self.root = tk.Tk()
        self.root.title("Flash Cards")

        # State
        self.current_question = ""
        self.current_answer = ""
        # Main frame
        frame = tk.Frame(self.root)
        frame.pack(padx=5, pady=12)

        # Diplay question type
        self.question_type = tk.Label(
            frame,
            text="test",
            font=("Arial", 30, "bold"),
            wraplength=600,
            justify="left",
        )
        self.question_type.grid(row=0, column=0, sticky="w")

        # Frame for question + answer
        self.question_tk = tk.LabelFrame(frame, text="Question")
        self.question_tk.grid(row=1, column=0, padx=50, pady=30, sticky="ew")

        # Question label (keep a reference so we can update)
        self.question_label = tk.Label(
            self.question_tk,
            text="",
            font=("Arial", 24, "bold"),
            wraplength=600,
            justify="left",
        )
        self.question_label.grid(row=0, column=0, sticky="w")

        # Answer label (initially empty)
        self.answer_label = tk.Label(
            self.question_tk,
            text="",
            font=("Arial", 20),
            wraplength=600,
            justify="left",
        )
        self.answer_label.grid(row=1, column=0, sticky="w", pady=(10, 0))

        # Remaining questions label
        self.remaining_label = tk.Label(
            frame,
            text=f"Remaining: {len(self.data_list)}",
            font=("Arial", 18),
        )
        self.remaining_label.grid(row=2, column=0, sticky="w", pady=(10, 0))

        # Buttons sub frame from main
        buttons_frame = tk.Frame(frame)
        buttons_frame.grid(row=3, column=0, pady=10, sticky="ew")

        self.show_answer_btn = tk.Button(
            buttons_frame,
            text="Show answer",
            command=self.show_answer,
        )
        self.show_answer_btn.grid(row=0, column=0, padx=5, sticky="ew")

        self.next_question_btn = tk.Button(
            buttons_frame,
            text="Next question",
            command=self.next_question,
            state=tk.DISABLED,
        )
        self.next_question_btn.grid(row=0, column=1, padx=5, sticky="ew")

        self.wrong_btn = tk.Button(
            buttons_frame,
            text="Wrong",
            command=self.set_to_wrong_list,
        )

        self.wrong_btn.grid(row=0, column=2, padx=5, sticky="ew")

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

        # Show first question
        self.next_question()

    def show_answer(self):
        """Display the answer for the current question."""
        self.answer_label.config(text=self.current_answer)
        self.next_question_btn.config(state=tk.ACTIVE)

    def next_question(self):
        """Move to the next question."""
        # Save the question type
        question_type = ""
        # If question in data list and wrong list then 7.5% ish chance to get a wrong
        if self.data_list and self.wrong_questions_list:
            # If the len of questions is smaller than the wrong questions, then more wrong questions come
            if len(self.data_list) + 5 < len(self.wrong_questions_list):
                random_question_pull = random.randint(0, 3)
            else:
                random_question_pull = random.randint(0, 10)
            if random_question_pull == 2:
                self.remaining_label.config(
                    text=f"Wrong questions remaining: {len(self.wrong_questions_list)}"
                )
                self.current_question, self.current_answer = (
                    self.get_one_wrong_question()
                )
                question_type = "Question from Wrong"
            else:
                self.current_question, self.current_answer = self.get_one_question()
                question_type = "New Question from queue"
                self.remaining_label.config(text=f"Remaining: {len(self.data_list)}")

        elif self.data_list:
            # Get next question
            question_type = "New Question from queue"
            self.current_question, self.current_answer = self.get_one_question()
            self.remaining_label.config(text=f"Remaining: {len(self.data_list)}")

        elif not self.data_list and self.wrong_questions_list:
            # If data_list is done show wrong questions
            question_type = "Question from Wrong"
            self.remaining_label.config(
                text=f"Wrong questions remaining: {len(self.wrong_questions_list)}"
            )
            self.current_question, self.current_answer = self.get_one_wrong_question()

        elif not self.data_list and not self.wrong_questions_list:
            # No more questions
            self.current_question = "No more questions!"
            self.current_answer = ""
            self.question_label.config(text=self.current_question)
            self.answer_label.config(text=self.current_answer)
            self.remaining_label.config(text="Remaining: 0")
            self.show_answer_btn.config(state="disabled")
            self.next_question_btn.config(state="disabled")
            self.wrong_btn.config(state=tk.DISABLED)
            return

        # Update GUI
        self.question_type.config(text=question_type)
        self.next_question_btn.config(state=tk.DISABLED)
        self.question_label.config(text=self.current_question)
        self.answer_label.config(text="")  # clear old answer
        self.wrong_btn.config(state=tk.ACTIVE)

    def set_to_wrong_list(self):
        """Adds the question to the woring list"""
        woring_question = [self.current_question, self.current_answer]
        self.wrong_questions_list.append(woring_question)
        self.wrong_btn.config(state=tk.DISABLED)

    def get_one_question(self):
        """Pop one question from the list and return (question, answer)."""
        question = self.data_list.pop()
        return question[0], question[1]

    def get_one_wrong_question(self):
        """Pop one question for wrong list"""
        # So you dont get the last markd wrong question
        random.shuffle(self.wrong_questions_list)
        question = self.wrong_questions_list.pop()
        return question[0], question[1]

    def get_questions_from_db(self, filename):
        """Read questions from CSV (semicolon-separated)."""
        data_list = []
        with open(filename, "r", encoding="UTF-8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=";")
            for row in csv_reader:
                if row:
                    data_list.append(row)
        return data_list

    def run(self):
        """Run App window"""
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
