import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re

from generate_questions import generate_questions


class AIQuestionsGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI Question Generator – GUI")
        self.geometry("1000x780")

        self.questions = []
        self.current_index = 0
        self.checked = False
        self.total_score = 0

        self.create_widgets()

    # ================= UI =================
    def create_widgets(self):
        # ---------- CONFIG ----------
        config = ttk.LabelFrame(self, text="Configurare")
        config.pack(fill="x", padx=10, pady=5)

        ttk.Label(config, text="Categorie:").grid(row=0, column=0, padx=5, sticky="w")

        self.category = tk.StringVar(value="1")

        categories = [
            ("Search problem identification", "1"),
            ("Constraint satisfaction", "2"),
            ("Adversarial search (Minimax)", "3"),
            ("Game theory (normal form)", "4"),
            ("Heuristics (admissibility/consistency)", "5"),
            ("⭐ Mixed", "all")
        ]

        for i, (txt, val) in enumerate(categories):
            ttk.Radiobutton(
                config,
                text=txt,
                variable=self.category,
                value=val
            ).grid(row=i, column=1, sticky="w", padx=10, pady=2)

        ttk.Label(config, text="Nr. întrebări:").grid(row=0, column=2, padx=(20,5))
        self.count_spin = ttk.Spinbox(config, from_=1, to=20, width=5)
        self.count_spin.set(3)
        self.count_spin.grid(row=0, column=3)

        ttk.Label(config, text="Limba:").grid(row=1, column=2, padx=(20,5))
        self.lang = ttk.Combobox(config, values=["ro", "en"], width=5)
        self.lang.set("ro")
        self.lang.grid(row=1, column=3)

        ttk.Button(
            config,
            text="Generează test",
            command=self.generate_test
        ).grid(row=2, column=2, columnspan=2, pady=10)

        # ---------- QUESTION ----------
        q_frame = ttk.LabelFrame(self, text="Întrebare")
        q_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.progress_label = ttk.Label(q_frame, text="")
        self.progress_label.pack(anchor="w", padx=5)

        self.question_text = scrolledtext.ScrolledText(
            q_frame, height=10, wrap=tk.WORD, font=("Consolas", 11)
        )
        self.question_text.pack(fill="x", padx=5, pady=5)

        ttk.Label(q_frame, text="Răspunsul tău:").pack(anchor="w", padx=5)
        self.answer_box = scrolledtext.ScrolledText(q_frame, height=4)
        self.answer_box.pack(fill="x", padx=5)

        btns = ttk.Frame(q_frame)
        btns.pack(pady=5)

        ttk.Button(
            btns,
            text="Verifică răspuns",
            command=self.check_answer
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            btns,
            text="Următoarea ▶",
            command=self.next_question
        ).grid(row=0, column=1, padx=5)

        # ---------- RESULT ----------
        r_frame = ttk.LabelFrame(self, text="Rezultat")
        r_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_box = scrolledtext.ScrolledText(
            r_frame, height=8, wrap=tk.WORD, font=("Consolas", 11)
        )
        self.result_box.pack(fill="both", expand=True, padx=5, pady=5)

    # ================= LOGIC =================
    def generate_test(self):
        selected = self.category.get()

        if selected == "all":
            choices = ["1", "2", "3", "4", "5"]
        else:
            choices = [selected]

        self.questions = generate_questions(
            count=int(self.count_spin.get()),
            choices=choices,
            lang=self.lang.get()
        )

        if not self.questions:
            messagebox.showerror("Eroare", "Nu s-au generat întrebări.")
            return

        self.current_index = 0
        self.total_score = 0
        self.show_question()

    def show_question(self):
        q = self.questions[self.current_index]

        self.question_text.delete("1.0", tk.END)
        self.answer_box.delete("1.0", tk.END)
        self.result_box.delete("1.0", tk.END)

        self.checked = False

        self.question_text.insert(tk.END, q["question"])
        self.progress_label.config(
            text=f"Întrebarea {self.current_index + 1} / {len(self.questions)}"
        )

    def check_answer(self):
        if self.checked:
            return

        q = self.questions[self.current_index]
        user_answer = self.answer_box.get("1.0", tk.END).strip()
        score = 0
        correct_answer = None

        # ================= CSP =================
        if q["title"] == "CSP":
            if q.get("solution") is None:
                correct_answer = "nu există nicio soluție"
                if "nu" in user_answer.lower() or "nicio" in user_answer.lower():
                    score = 100
                else:
                    score = 0
            else:
                correct_answer = q["solution"]

                def parse_answer(s):
                    s = s.replace("{", "").replace("}", "").strip()
                    s = s.replace(" ", "")
                    parts = s.split(",")
                    result = {}
                    for p in parts:
                        if ":" in p:
                            var, val = p.split(":")
                        elif "=" in p:
                            var, val = p.split("=")
                        else:
                            continue
                        if val.isdigit():
                            val = int(val)
                        result[var.upper()] = val
                    return result

                user_dict = parse_answer(user_answer)
                correct_dict = {k.upper(): v for k, v in correct_answer.items()}

                total_vars = len(correct_dict)
                correct_count = 0
                for var, val in user_dict.items():
                    if var in correct_dict and correct_dict[var] == val:
                        correct_count += 1

                score = int((correct_count / total_vars) * 100)

        # ================= MinMax =================
        elif q["title"] in ["MinMax", "MinMax Alpha-Beta"]:
            answer_dict = q["answer"]
            correct_root = answer_dict.get("root_value")
            correct_leaves = answer_dict.get("leaf_count")

            correct_answer = (
                f"Valoare rădăcină: {correct_root}, "
                f"Frunze vizitate: {correct_leaves}"
            )

            user_lower = user_answer.lower()
            mentions_algo = any(x in user_lower for x in ["alpha", "beta", "minmax", "alpha-beta"])

            numbers = re.findall(r'\d+', user_answer)

            if len(numbers) >= 2:
                user_root = int(numbers[0])
                user_leaves = int(numbers[1])

                if user_root == correct_root and user_leaves == correct_leaves:
                    score = 100
                elif user_root == correct_root:
                    score = 60
                elif user_leaves == correct_leaves:
                    score = 40
                elif mentions_algo:
                    score = 20
            elif len(numbers) == 1:
                if int(numbers[0]) == correct_root:
                    score = 60
                elif mentions_algo:
                    score = 30
            elif mentions_algo:
                score = 20

        # ================= Nash Equilibrium =================
        elif q["title"] == "Nash":
            equilibria = q["answer"]["equilibria"]
            has_nash = q["answer"]["has_nash"]
            
            if not has_nash:
                # No Nash equilibrium exists
                correct_answer = "NU există echilibru Nash pur"
                if "nu" in user_answer.lower() or "no" in user_answer.lower():
                    score = 100
                else:
                    score = 0
            else:
                # Format correct answer
                correct_answer = f"DA. Echilibre Nash: {equilibria}"
                
                # Check if user said YES
                said_yes = "da" in user_answer.lower() or "yes" in user_answer.lower()
                
                # Extract positions from user answer: (0,0), (1,2), etc.
                pattern = r'\((\d+)\s*,\s*(\d+)\)'
                matches = re.findall(pattern, user_answer)
                user_equilibria = [(int(i), int(j)) for i, j in matches]
                
                if not said_yes and not user_equilibria:
                    score = 0
                else:
                    # Calculate score based on correctness
                    if said_yes and not user_equilibria:
                        # Said yes but didn't specify positions
                        score = 30
                    else:
                        # Compare user equilibria with correct ones
                        correct_set = set(equilibria)
                        user_set = set(user_equilibria)
                        
                        correct_found = len(user_set & correct_set)
                        total_correct = len(correct_set)
                        false_positives = len(user_set - correct_set)
                        
                        if user_set == correct_set:
                            score = 100
                        elif correct_found > 0:
                            # Partial credit
                            base_score = (correct_found / total_correct) * 80
                            # Penalty for false positives
                            penalty = false_positives * 10
                            score = max(0, int(base_score - penalty))
                        else:
                            score = 10 if said_yes else 0

        # ================= Heuristics =================
        elif q["title"] == "Heuristics":
            correct_answer = q["answer"]["correct_answer"]
            question_type = q["answer"]["question_type"]
            
            user_lower = user_answer.lower().strip()
            
            if "da" in user_lower or "yes" in user_lower:
                user_said = "DA"
            elif "nu" in user_lower or "no" in user_lower:
                user_said = "NU"
            else:
                user_said = None
            
            if user_said == correct_answer:
                score = 100
            elif user_said is not None:
                score = 0
            else:
                score = 0
            
            type_name = 'admisibilă' if question_type == 'admissible' else 'consistentă'
            if correct_answer == "DA":
                correct_answer = f"DA (Euristica este {type_name})"
            else:
                correct_answer = f"NU (Euristica NU este {type_name})"

        # ================= REST (Search / CSP strategies) =================
        else:
            correct_answer = q["answer"]["best_strategy"]

            if correct_answer.lower() in user_answer.lower() or user_answer.lower() in correct_answer.lower():
                score = 100
            else:
                ranking = q["answer"]["ranking"]
                n = len(ranking)
                for idx, strategy in enumerate(ranking):
                    if strategy.lower() in user_answer.lower() or user_answer.lower() in strategy.lower():
                        score = int(100 - idx * (100 / n))
                        break

        # ================= OUTPUT =================
        self.total_score += score
        self.checked = True

        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(
            tk.END,
            f"Răspuns corect:\n{correct_answer}\n\n"
            f"Scorul tău: {score}%"
        )

    def next_question(self):
        if not self.checked:
            messagebox.showwarning("Atenție", "Verifică răspunsul înainte de a continua!")
            return

        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self.show_question()
        else:
            avg = self.total_score // len(self.questions)
            messagebox.showinfo("Test finalizat", f"Scor final: {avg}%")


if __name__ == "__main__":
    AIQuestionsGUI().mainloop()
