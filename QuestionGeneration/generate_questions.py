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
            if q['title']!='CSP':
                ranking = q["answer"]["ranking"]
                f.write("Strategii:\n")
                for j, strategy in enumerate(ranking, 1):
                    f.write(f"   {j}. {strategy}\n")
                f.write("\n")
            else:
                f.write("Asignare:\n")
                f.write(f" {q["solution"]}\n")
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

    for i in range(count):
        # Alegem aleator dacă generăm o întrebare CSP sau din cele existente
        if random.random() < 0.3 or not available:  # 30% șanse sau dacă nu mai avem disponibile
            # Generare întrebări CSP
            num_vars = random.randint(4, 6)
            domain_size = random.randint(2, 5)
            num_constraints = random.randint(num_vars-1, num_vars*(num_vars-1)//2)
            csp_question = generate_csp_question_with_solution(num_vars=num_vars,
                                                 domain_size=domain_size,
                                                 num_constraints=num_constraints,
                                                 lang=lang)
            if csp_question is None:
                continue
            # Împachetăm întrebarea CSP ca un dicționar compatibil cu generate_one
           
            wrapped_csp = {
                "title": f"CSP",
                "question": csp_question["question"],
                "variables": csp_question["variables"],
                "domains": csp_question["domains"],
                "constraints": csp_question["constraints"],
                "constraint_ops": csp_question["constraint_ops"],
                "partial_assignment": csp_question["partial_assignment"],
                "optimization": csp_question["optimization"],
                "solution":csp_question["solution"]
            }
            results.append(wrapped_csp)
            print(csp_question["solution"])
        else:
            # Generare întrebări existente
            name, entry = random.choice(available)
            results.append(generate_one(name, entry, lang=lang))

    return results


import random

def generate_csp_question(num_vars=4, domain_size=3, num_constraints=None, lang="ro"):
    # 1. Variabilele
    variables = [f"X{i+1}" for i in range(num_vars)]

    # 2. Domeniile
    domains = {v: list(range(1, domain_size+1)) for v in variables}

    # 3. Alegere perechi variabile pentru constrângeri
    all_pairs = [(v1, v2) for i, v1 in enumerate(variables) for v2 in variables[i+1:]]
    if num_constraints is None:
        num_constraints = random.randint(num_vars, len(all_pairs))

    chosen_pairs = random.sample(all_pairs, num_constraints)

    constraints = {}
    constraint_ops = {}

    # Operatorii inversi pentru afisare
    inverse_op = {"!=": "!=", "<": ">", ">": "<"}

    for v1, v2 in chosen_pairs:
        op = random.choice(["!=", "<", ">"])

        # definim funcția (evităm late binding prin f=func)
        if op == "!=":
            def f(a, b): return a != b
        elif op == "<":
            def f(a, b): return a < b
        else:
            def f(a, b): return a > b

        # stocăm ambele direcții pentru AC-3 și forward checking
        constraints[(v1, v2)] = f
        constraints[(v2, v1)] = lambda b, a, f=f: f(a, b)

        constraint_ops[(v1, v2)] = op
        constraint_ops[(v2, v1)] = inverse_op[op]

    # 4. Asignare parțială
    num_assigned = random.randint(1, max(1, num_vars // 2))
    assigned_vars = random.sample(variables, num_assigned)
    partial_assignment = {v: random.choice(domains[v]) for v in assigned_vars}

    # 5. Alegere optimizare
    optimizations = ["MRV", "FC", "AC-3"]
    chosen_opt = random.choice(optimizations)

    opt_text_ro = {
        "MRV": "Minimum Remaining Values (MRV)",
        "FC": "Forward Checking (FC)",
        "AC-3": "AC-3 (Arc Consistency)"
    }

    opt_text_en = {
        "MRV": "Minimum Remaining Values (MRV)",
        "FC": "Forward Checking (FC)",
        "AC-3": "AC-3 (Arc Consistency)"
    }

    # 6. Textul pentru constrângeri
    constraints_text = [
        f"{v1} {op} {v2}" for (v1, v2), op in constraint_ops.items()
        if (v1 < v2)  # evităm duplicarea
    ]

    # 7. Construirea întrebării
    if lang.lower() == "ro":
        question_text = (
            f"Având variabilele {variables}, domeniile {domains}, "
            f"constrângerile {constraints_text},\n"
            f"și asignarea parțială {partial_assignment}, determinați "
            f"asignarea variabilelor rămase folosind Backtracking cu optimizarea "
            f"{opt_text_ro[chosen_opt]}."
        )
    else:
        question_text = (
            f"Given the variables {variables}, domains {domains}, "
            f"constraints {constraints_text},\n"
            f"and the partial assignment {partial_assignment}, determine the "
            f"remaining assignment using Backtracking with the "
            f"{opt_text_en[chosen_opt]} optimization."
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
    # selectează variabila cu cel mai mic domeniu (număr de valori posibile)
    return min(unassigned, key=lambda var: len(domains[var]))

def forward_check(var, value, domains, constraints, assignment):
    pruned = []  # listă de valori eliminate (pentru backtrack)
    
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

    # dacă un domeniu devine gol → inconsistență
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
        # x trebuie să aibă măcar o valoare y în domeniul lui xj care satisface constrângerea
        if not any(func(x, y) for y in domains[xj]):
            domains[xi].remove(x)
            revised = True
    return revised

def backtrack_engine(variables, domains, constraints, assignment, optimization):
    if len(assignment) == len(variables):
        return assignment

    # MRV
    if optimization == "MRV":
        var = select_unassigned_variable_MRV(variables, domains, assignment)
    else:
        var = next(v for v in variables if v not in assignment)

    for value in domains[var][:]:
        if is_consistent(var, value, assignment, constraints):
            assignment[var] = value

            # Forward Checking
            if optimization == "FC":
                ok, pruned = forward_check(var, value, domains, constraints, assignment)
                if ok:
                    result = backtrack_engine(variables, domains, constraints, assignment, optimization)
                    if result:
                        return result
                restore_domains(domains, pruned)

            else:
                # Backtracking normal
                result = backtrack_engine(variables, domains, constraints, assignment, optimization)
                if result:
                    return result

            del assignment[var]

    return None

def solve_csp(variables, domains, constraints, partial_assignment, optimization):
    # copie separate pentru a nu distruge domeniile inițiale
    domains = {v: domains[v][:] for v in domains}

    # aplică AC-3 înainte dacă este cerut
    if optimization == "AC-3":
        if not ac3(domains, constraints):
            return None

    return backtrack_engine(variables, domains, constraints, partial_assignment, optimization)


def is_consistent(var, value, assignment, constraints):
    """
    Verifică dacă atribuirea value lui var respectă toate constrângerile
    cu variabilele deja asignate.
    """
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

    # Dacă toate variabilele sunt asignate, returnăm soluția
    if len(assignment) == len(variables):
        return assignment

    # Alegem o variabilă neasignată (MRV dacă vrem)
    unassigned = [v for v in variables if v not in assignment]
    var = unassigned[0]  # aici putem implementa MRV dacă vrem

    for value in domains[var]:
        if is_consistent(var, value, assignment, constraints):
            assignment[var] = value
            result = backtracking(variables, domains, constraints, assignment)
            if result:
                return result
            del assignment[var]  # backtrack

    return None  # nu există soluție

def generate_csp_question_with_solution(num_vars=4, domain_size=3, num_constraints=None, lang="ro"):
    for _ in range(15):  # maxim 15 încercări
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

    # dacă nu găsește soluție în 3 încercări → returnăm ultima întrebare fără soluție
    csp["solution"] = None
    return csp

# # Exemplu de utilizare
# csp_question = generate_csp_question()
# print(csp_question["question"])


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
        #print(q["answer"])
        user_answer = input("Răspunsul tău: ").strip()
        score = 0
        if(q["title"]!="CSP"):
            if q["answer"]["best_strategy"].lower() in user_answer.lower() or user_answer.lower() in q["answer"]["best_strategy"].lower():
                score = 100
            else:
                ranking = q["answer"]["ranking"]
                n = len(ranking)

                for idx, strategy in enumerate(ranking):
                    if strategy.lower() in user_answer.lower() and idx != 0 or user_answer.lower() in strategy.lower():
                        score = 100 - idx * (100 / n)
                        break

                    if strategy.lower() in user_answer.lower() and idx == 0 or user_answer.lower() in strategy.lower():
                        score = 100
                        break

        score = str(int (score)) + '%'
        print(f"   Scorul tau: {score}")
        answers.append({
            "title": q["title"],
            "question": q["question"],
            "user_answer": user_answer,
            "score": score
        })

    with open(filename, "w", encoding="utf-8") as f:
        for i, a in enumerate(answers, 1):
            f.write(f"{i}. [{a['title']}] {a['question']}\n")
            f.write(f"   Răspunsul tău: {a['user_answer']}\n")
            f.write(f"   Scorul tau: {a['score']}\n\n")

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

    # csp_question = generate_csp_question(4, 3, None, lang)
    # print(csp_question["question"])

    # Afișează și scrie în fișier

    write_questions_to_file(questions, filename=filename)
    write_strategies_to_file(questions, filename="strategies.txt")

    # Utilizatorul răspunde la întrebări
    ask_user_for_answers(questions)

    input("\n Apasati \"Enter\" pentru a inchide aplicatia")
