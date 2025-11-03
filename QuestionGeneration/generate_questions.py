import random
import sys
from pathlib import Path
from evaluate_strategies import evaluate_problem

# asigură că directorul curent este în path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    import QTemplates
except ImportError as e:
    print("Nu s-a putut importa QTemplates.py:", e)
    raise

search_problems = getattr(QTemplates, "search_problems", None)
if search_problems is None:
    raise RuntimeError("QTemplates.py nu definește `search_problems`")


def write_strategies_to_file(questions, filename="strategies.txt"):
    """Scrie listele de strategii pentru fiecare problemă într-un fișier separat."""
    with open(filename, "w", encoding="utf-8") as f:
        for i, q in enumerate(questions, 1):
            f.write(f"Problema {i}: {q['title']}\n")
            ranking = q["answer"]["ranking"]
            f.write("Strategii:\n")
            for j, strategy in enumerate(ranking, 1):
                f.write(f"   {j}. {strategy}\n")
            f.write("\n")
    print(f"\nListele de strategii au fost salvate în fișierul '{filename}'")


def generate_one(name, entry, lang="ro"):
    params_fn = entry.get("params")
    params = params_fn() if callable(params_fn) else {}

    templates = entry.get("templates", {})
    lang_templates = templates.get(lang) or templates.get("ro") or []
    if not lang_templates:
        text = f"[No template available for {name}]"
    else:
        text = random.choice(lang_templates)
        try:
            text = text.format(**params)
        except Exception:
            text += f"\n(Params: {params})"

    name = entry.get("title")

    if name in ["N-Queens", "Coloring", "Knight's Tour"]:
        results = evaluate_problem(entry, params)
        best = results[0][0] if results else None
        ranking = [r[0] for r in results]
    else:
        results = entry.get("strategies")
        best = results[0] if results else "N/A"
        ranking = results or []

    return {
        "title": name,
        "question": text,
        "params": params,
        "answer": {
            "best_strategy": best,
            "ranking": ranking
        }
    }


def generate_questions(count=1, choices=None, seed=None, lang="ro"):
    if seed is not None:
        random.seed(seed)

    available = list(search_problems.items())
    if choices:
        names = [s.strip() for s in ",".join(choices).split(",") if s.strip()]
        available = [(n, search_problems[n]) for n in names if n in search_problems]
        if not available:
            raise ValueError("None of the requested problem names were found in QTemplates.search_problems")

    results = []

    if count <= len(available):
        selected = random.sample(available, count)
        for name, entry in selected:
            results.append(generate_one(name, entry, lang=lang))
    else:
        results.extend(generate_one(name, entry, lang=lang) for name, entry in random.sample(available, len(available)))
        remaining = count - len(available)
        for _ in range(remaining):
            name, entry = random.choice(available)
            results.append(generate_one(name, entry, lang=lang))

    return results


def write_questions_to_file(questions, filename="questions.txt"):
    """Scrie întrebările într-un fișier text."""
    with open(filename, "w", encoding="utf-8") as f:
        for i, q in enumerate(questions, 1):
            f.write(f"{i}. [{q['title']}] {q['question']}\n")
            if q.get("strategy"):
                f.write(f"   Strategie recomandată: {q['strategy']}\n")
            f.write("\n")
    print(f"\nÎntrebările au fost salvate în fișierul '{filename}'")


def ask_user_for_answers(questions, filename="raspunsuri.txt"):
    answers = []
    print("\n------------------")
    print("   Scrie răspunsurile tale   ")
    print("---------------------")

    for i, q in enumerate(questions, 1):
        print(f"\n{i}. [{q['title']}]")
        print(q["question"])
       # print(q["answer"])
        user_answer = input("Răspunsul tău: ").strip()
        score = 0

        if q["answer"]["best_strategy"].lower() in user_answer.lower():
            score = 100
        else:
            ranking = q["answer"]["ranking"]
            n = len(ranking)

            for idx, strategy in enumerate(ranking):
                if strategy.lower() in user_answer.lower() and idx != 0:
                    score = 100 - idx * (100 / n)
                    break

                if strategy.lower() in user_answer.lower() and idx == 0:
                    score = 100
                    break

        score = str(score) + '%'
        answers.append({
            "title": q["title"],
            "question": q["question"],
            "user_answer": user_answer,
            "score": score
        })

    with open(filename, "w", encoding="utf-8") as f:
        for i, a in enumerate(answers, 1):
            f.write(f"{i}. [{a['title']}] {a['question']}\n")
            f.write(f"   Răspunsul tău: {a['user_answer']}\n\n")
            f.write(f"   Scorul tau: {a['score']}\n")

    print(f"\n Răspunsurile au fost salvate în fișierul '{filename}'.")


if __name__ == "__main__":
    # Citește datele de la tastatură
    try:
        count = int(input("Introduceți numărul de întrebări de generat: "))
    except ValueError:
        count = 5
        print("Valoare invalidă, se va folosi count = 5")

    lang = input("Introduceți limba (ro/en) [implicit: ro]: ").strip().lower() or "ro"

    problems_input = input("Introduceți problemele separate prin virgulă (sau Enter pentru toate): ").strip()
    problems = [p.strip() for p in problems_input.split(",")] if problems_input else None

    seed_input = input("Introduceți seed aleator (sau Enter pentru random): ").strip()
    seed = int(seed_input) if seed_input.isdigit() else None

    filename = input(
        "Introduceți numele fișierului pentru salvare [implicit: questions.txt]: ").strip() or "questions.txt"

    # Generează întrebările
    questions = generate_questions(count=count, choices=problems, seed=seed, lang=lang)

    # Afișează și scrie în fișier

    write_questions_to_file(questions, filename=filename)
    write_strategies_to_file(questions, filename="strategies.txt")

    # Utilizatorul răspunde la întrebări
    ask_user_for_answers(questions)
