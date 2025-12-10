import random
import sys
from pathlib import Path
from evaluate_strategies import evaluate_problem

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

CATEGORY_MAP = {
    "1": "SearchIdentification",
    "2": "CSP"
}


def write_strategies_to_file(questions, filename="strategies.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, q in enumerate(questions, 1):
            f.write(f"Problema {i}: {q['title']}\n")
            if q['title'] != 'CSP':
                ranking = q["answer"]["ranking"]
                f.write("Strategii:\n")
                for j, strategy in enumerate(ranking, 1):
                    f.write(f"   {j}. {strategy}\n")
                f.write("\n")
            else:
                f.write("Asignare:\n")
                f.write(f" {q['solution']}\n")
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

    title = entry.get("title")

    if title in ["N-Queens", "Coloring", "Knight's Tour"]:
        results = evaluate_problem(entry, params)
        best = results[0][0] if results else None
        ranking = [r[0] for r in results]
    else:
        results = entry.get("strategies")
        best = results[0] if results else "N/A"
        ranking = results or []

    return {
        "title": title,
        "question": text,
        "params": params,
        "answer": {
            "best_strategy": best,
            "ranking": ranking
        },
        "category": entry.get("category")
    }


def generate_questions(count=1, choices=None, seed=None, lang="ro"):
    if seed is not None:
        random.seed(seed)

    selected_categories = None
    selected_names = None

    if choices:
        selected_categories = set()
        selected_names = []

        for c in choices:
            c = c.strip()
            if c in CATEGORY_MAP:
                selected_categories.add(CATEGORY_MAP[c])
            elif c in search_problems:
                selected_names.append(c)

    if selected_categories:
        available = [
            (n, e) for n, e in search_problems.items()
            if e.get("category") in selected_categories
        ]
    elif selected_names:
        available = [(n, search_problems[n]) for n in selected_names]
    else:
        available = list(search_problems.items())

    csp_only = selected_categories == {"CSP"}

    results = []

    for _ in range(count):
        if csp_only:
            num_vars = random.randint(4, 6)
            domain_size = random.randint(2, 5)
            num_constraints = random.randint(num_vars - 1, num_vars * (num_vars - 1) // 2)

            csp = generate_csp_question_with_solution(
                num_vars=num_vars,
                domain_size=domain_size,
                num_constraints=num_constraints,
                lang=lang
            )

            wrapped = {
                "title": "CSP",
                "question": csp["question"],
                "variables": csp["variables"],
                "domains": csp["domains"],
                "constraints": csp["constraints"],
                "constraint_ops": csp["constraint_ops"],
                "partial_assignment": csp["partial_assignment"],
                "optimization": csp["optimization"],
                "solution": csp["solution"],
                "category": "CSP"
            }

            results.append(wrapped)
            continue

        if "CSP" in (selected_categories or []) and random.random() < 0.3:
            num_vars = random.randint(4, 6)
            domain_size = random.randint(2, 5)
            num_constraints = random.randint(num_vars - 1, num_vars * (num_vars - 1) // 2)

            csp = generate_csp_question_with_solution(
                num_vars=num_vars,
                domain_size=domain_size,
                num_constraints=num_constraints,
                lang=lang
            )

            wrapped = {
                "title": "CSP",
                "question": csp["question"],
                "variables": csp["variables"],
                "domains": csp["domains"],
                "constraints": csp["constraints"],
                "constraint_ops": csp["constraint_ops"],
                "partial_assignment": csp["partial_assignment"],
                "optimization": csp["optimization"],
                "solution": csp["solution"],
                "category": "CSP"
            }

            results.append(wrapped)
            continue

        if available:
            name, entry = random.choice(available)
            results.append(generate_one(name, entry, lang))

    return results


import random


def generate_csp_question(num_vars=4, domain_size=3, num_constraints=None, lang="ro"):
    variables = [f"X{i + 1}" for i in range(num_vars)]
    domains = {v: list(range(1, domain_size + 1)) for v in variables}

    all_pairs = [(v1, v2) for i, v1 in enumerate(variables) for v2 in variables[i + 1:]]

    if num_constraints is None:
        num_constraints = random.randint(num_vars, len(all_pairs))

    chosen_pairs = random.sample(all_pairs, num_constraints)

    constraints = {}
    constraint_ops = {}
    inverse_op = {"!=": "!=", "<": ">", ">": "<"}

    for v1, v2 in chosen_pairs:
        op = random.choice(["!=", "<", ">"])

        if op == "!=":
            def f(a, b):
                return a != b
        elif op == "<":
            def f(a, b):
                return a < b
        else:
            def f(a, b):
                return a > b

        constraints[(v1, v2)] = f
        constraints[(v2, v1)] = lambda b, a, f=f: f(a, b)

        constraint_ops[(v1, v2)] = op
        constraint_ops[(v2, v1)] = inverse_op[op]

    num_assigned = random.randint(1, max(1, num_vars // 2))
    assigned_vars = random.sample(variables, num_assigned)
    partial_assignment = {v: random.choice(domains[v]) for v in assigned_vars}

    optimizations = ["MRV", "FC", "AC-3"]
    chosen_opt = random.choice(optimizations)

    constraints_text = [
        f"{v1} {op} {v2}" for (v1, v2), op in constraint_ops.items()
        if (v1 < v2)
    ]

    if lang.lower() == "ro":
        question_text = (
            f"Având variabilele {variables}, domeniile {domains}, "
            f"constrângerile {constraints_text},\n"
            f"și asignarea parțială {partial_assignment}, determinați asignarea finală "
            f"folosind Backtracking cu {chosen_opt}."
        )
    else:
        question_text = (
            f"Given variables {variables}, domains {domains}, constraints {constraints_text},\n"
            f"and partial assignment {partial_assignment}, determine the final assignment "
            f"using Backtracking with {chosen_opt}."
        )

    return {
        "variables": variables,
        "domains": domains,
        "constraints": constraints,
        "constraint_ops": constraint_ops,
        "partial_assignment": partial_assignment,
        "optimization": chosen_opt,
        "question": question_text
    }


def select_unassigned_variable_MRV(variables, domains, assignment):
    unassigned = [v for v in variables if v not in assignment]
    return min(unassigned, key=lambda var: len(domains[var]))


def forward_check(var, value, domains, constraints, assignment):
    pruned = []

    for (v1, v2), func in constraints.items():
        if v1 == var and v2 not in assignment:
            for val2 in domains[v2][:]:
                if not func(value, val2):
                    domains[v2].remove(val2)
                    pruned.append((v2, val2))

        elif v2 == var and v1 not in assignment:
            for val1 in domains[v1][:]:
                if not func(val1, value):
                    domains[v1].remove(val1)
                    pruned.append((v1, val1))

    for v in domains:
        if not domains[v]:
            return False, pruned

    return True, pruned


def restore_domains(domains, pruned):
    for var, val in pruned:
        domains[var].append(val)


from collections import deque


def ac3(domains, constraints):
    queue = deque(constraints.keys())

    while queue:
        (xi, xj) = queue.popleft()
        if revise(domains, xi, xj, constraints):
            if not domains[xi]:
                return False
            for (xk, xl) in constraints:
                if xl == xi:
                    queue.append((xk, xi))
                if xk == xi:
                    queue.append((xl, xi))
    return True


def revise(domains, xi, xj, constraints):
    revised = False
    func = constraints[(xi, xj)]
    for x in domains[xi][:]:
        if not any(func(x, y) for y in domains[xj]):
            domains[xi].remove(x)
            revised = True
    return revised


def backtrack_engine(variables, domains, constraints, assignment, optimization):
    if len(assignment) == len(variables):
        return assignment

    if optimization == "MRV":
        var = select_unassigned_variable_MRV(variables, domains, assignment)
    else:
        var = next(v for v in variables if v not in assignment)

    for value in domains[var][:]:
        if is_consistent(var, value, assignment, constraints):
            assignment[var] = value

            if optimization == "FC":
                ok, pruned = forward_check(var, value, domains, constraints, assignment)
                if ok:
                    result = backtrack_engine(variables, domains, constraints, assignment, optimization)
                    if result:
                        return result
                restore_domains(domains, pruned)
            else:
                result = backtrack_engine(variables, domains, constraints, assignment, optimization)
                if result:
                    return result

            del assignment[var]

    return None


def solve_csp(variables, domains, constraints, partial_assignment, optimization):
    domains = {v: domains[v][:] for v in domains}

    if optimization == "AC-3":
        if not ac3(domains, constraints):
            return None

    return backtrack_engine(variables, domains, constraints, partial_assignment, optimization)


def is_consistent(var, value, assignment, constraints):
    for (v1, v2), func in constraints.items():
        if var == v1 and v2 in assignment:
            if not func(value, assignment[v2]):
                return False
        elif var == v2 and v1 in assignment:
            if not func(assignment[v1], value):
                return False
    return True


def backtracking(variables, domains, constraints, assignment=None):
    if assignment is None:
        assignment = {}

    if len(assignment) == len(variables):
        return assignment

    unassigned = [v for v in variables if v not in assignment]
    var = unassigned[0]

    for value in domains[var]:
        if is_consistent(var, value, assignment, constraints):
            assignment[var] = value
            result = backtracking(variables, domains, constraints, assignment)
            if result:
                return result
            del assignment[var]

    return None


def generate_csp_question_with_solution(num_vars=4, domain_size=3, num_constraints=None, lang="ro"):
    for _ in range(15):
        csp = generate_csp_question(num_vars, domain_size, num_constraints, lang)

        sol = solve_csp(
            csp["variables"],
            csp["domains"],
            csp["constraints"],
            csp["partial_assignment"].copy(),
            csp["optimization"]
        )

        if sol is not None:
            csp["solution"] = sol
            return csp

    csp["solution"] = None
    return csp


def write_questions_to_file(questions, filename="questions.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, q in enumerate(questions, 1):
            f.write(f"{i}. [{q['title']}] {q['question']}\n")
            if q.get("strategy"):
                f.write(f"   Strategie recomandată: {q['strategy']}\n")
            f.write("\n")
    print(f"\nÎntrebările au fost salvate în fișierul '{filename}'")


def ask_user_for_answers(questions, filename="raspunsuri.txt"):
    answers = []
    print("\n-------------------------------------------------------")
    print("Scrieți mai jos răspunsurile la întrebări.")
    print("---------------------------------------------------------")

    for i, q in enumerate(questions, 1):
        print(f"\n{i}. [{q['title']}]")
        print(q["question"])
        user_answer = input("Răspunsul tău la întrebare: ").strip()
        score = 0

        if q["title"] != "CSP":
            correct_answer = q["answer"]["best_strategy"]

            if correct_answer.lower() in user_answer.lower() or user_answer.lower() in correct_answer.lower():
                score = 100
            else:
                ranking = q["answer"]["ranking"]
                n = len(ranking)
                for idx, strategy in enumerate(ranking):
                    if strategy.lower() in user_answer.lower() or user_answer.lower() in strategy.lower():
                        score = 100 - idx * (100 / n)
                        break

        else:
            if q["solution"] is None:
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

        score = str(int(score)) + '%'
        print(f"Scorul tău obținut la întrebare: {score}")

        answers.append({
            "title": q["title"],
            "question": q["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "score": score
        })

    with open(filename, "w", encoding="utf-8") as f:
        for i, a in enumerate(answers, 1):
            f.write(f"{i}. [{a['title']}] {a['question']}\n")
            f.write(f"   Răspunsul tău: {a['user_answer']}\n")
            f.write(f"   Răspuns corect: {a['correct_answer']}\n")
            f.write(f"   Scorul tău: {a['score']}\n\n")

    print(f"\nRăspunsurile au fost salvate în fișierul '{filename}'.")


if __name__ == "__main__":
    print("Alege tipurile de întrebări:")
    print("1 = Search problem identification")
    print("2 = CSP")

    problems_input = input("Introduceți problemele sau categoriile (ex: 1,2 sau WaterJugs,N-Queens): ").strip()
    problems = [p.strip() for p in problems_input.split(",")] if problems_input else None

    try:
        count = int(input("Introduceți numărul de întrebări de generat: "))
    except ValueError:
        count = 5
        print("Valoare invalidă, se va folosi count = 5")

    lang = input("Introduceți limba (ro/en) [implicit: ro]: ").strip().lower() or "ro"

    seed_input = input("Introduceți seed aleator (sau Enter pentru random): ").strip()
    seed = int(seed_input) if seed_input.isdigit() else None

    filename = input("Introduceți numele fișierului pentru salvare [implicit: questions.txt]: ").strip() or "questions.txt"

    questions = generate_questions(count=count, choices=problems, seed=seed, lang=lang)

    write_questions_to_file(questions, filename=filename)
    write_strategies_to_file(questions, filename="strategies.txt")

    ask_user_for_answers(questions)

    input("\n Apasati \"Enter\" pentru a inchide aplicatia")
