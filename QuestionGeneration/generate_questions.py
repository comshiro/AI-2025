import random
import sys
from pathlib import Path
from evaluate_strategies import evaluate_problem
from new_question import HeuristicQuestionGenerator

# !!! Pentru intrebari de tipul 2!!!
def generate_game(rows, cols, payoff_range=(-5, 5)):
    """
    Generează un joc m×n în formă normală
    A[i][j] = (u1, u2)
    """
    return [
        [
            (random.randint(*payoff_range), random.randint(*payoff_range))
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]


def find_pure_nash_equilibria(game):
    """
    Găsește toate echilibrele Nash pure
    """
    rows = len(game)
    cols = len(game[0])
    equilibria = []

    # precomputăm best responses
    best_u1 = [
        max(game[i][j][0] for i in range(rows))
        for j in range(cols)
    ]

    best_u2 = [
        max(game[i][j][1] for j in range(cols))
        for i in range(rows)
    ]

    for i in range(rows):
        for j in range(cols):
            u1, u2 = game[i][j]
            if u1 == best_u1[j] and u2 == best_u2[i]:
                equilibria.append((i, j))

    return equilibria


def print_game(game):
    print("Matricea jocului (u1, u2):")
    for row in game:
        print(row)


def generate_question(rows, cols):
    game = generate_game(rows, cols)
    equilibria = find_pure_nash_equilibria(game)

    print(f"\nÎNTREBARE ({rows}×{cols}):")
    print("Pentru jocul dat în formă normală, există echilibru Nash pur?")
    print_game(game)

    print("\nREZOLVARE:")
    if equilibria:
        print("DA. Echilibre Nash pure:")
        for i, j in equilibria:
            print(f"  ({i}, {j}) → payoff {game[i][j]}")
    else:
        print("NU. Jocul nu are echilibru Nash pur.")
        # if __name__ == "__main__":
        #     for i in range(0, 10):
        #      generate_question(random.randint(3, 5), random.randint(3, 5))

#!! Intrebari tipul 2! 

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

# Alias pentru MinMax
if "MinMax Alpha-Beta" in search_problems:
    search_problems["MinMax"] = search_problems["MinMax Alpha-Beta"]

CATEGORY_MAP = {
    "1": "search",
    "2": "CSP",
    "3": "game",
    "4": "nash",
    "5": "heuristics"
}


# ---------------------------------------------------
# Fișier strategii
# ---------------------------------------------------
def write_strategies_to_file(questions, filename="strategies.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, q in enumerate(questions, 1):
            f.write(f"Problema {i}: {q['title']}\n")
            if q['title'] != 'CSP':
                if q['title'] in ['MinMax', 'MinMax Alpha-Beta']:
                    f.write("Rezultat MinMax Alpha-Beta:\n")
                    answer = q['answer']
                    if isinstance(answer, dict):
                        f.write(f"   Valoare în rădăcină: {answer.get('root_value', 'N/A')}\n")
                        f.write(f"   Frunze vizitate: {answer.get('leaf_count', 'N/A')}\n")
                        f.write(f"   Total frunze: {answer.get('total_leaves', 'N/A')}\n")
                        f.write(f"   Frunze tăiate (pruning): {answer.get('pruned_leaves', 'N/A')}\n")
                    else:
                        f.write(f"   {answer}\n")
                else:
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


# ---------------------------------------------------
# Vizualizare arbore MinMax
# ---------------------------------------------------
def visualize_tree(tree, indent=0, node_type="MAX"):
    """Vizualizează arborele MinMax într-un format lizibil."""
    lines = []
    prefix = "  " * indent

    if isinstance(tree, int):
        lines.append(f"{prefix}└─ Frunză: {tree}")
    elif isinstance(tree, list):
        lines.append(f"{prefix}├─ {node_type}")
        next_type = "MIN" if node_type == "MAX" else "MAX"
        for i, child in enumerate(tree):
            is_last = (i == len(tree) - 1)
            lines.extend(visualize_tree(child, indent + 1, next_type))

    return lines

def visualize_tree_with_names(tree, indent=0, node_name="A", node_type="MAX"):
    """Vizualizeaza arborele MinMax cu nume de noduri(A, B, C, etc)"""
    lines = []
    prefix = "  " * indent

    if isinstance(tree, int):
        lines.append(f"{prefix}{node_name} = {tree}")
    
    elif isinstance(tree, list):
        lines.append(f"{prefix}{node_name} ({node_type})")
        next_type = "MIN" if node_type == "MAX" else "MAX"

        # Generam litere pentru copii
        if node_name == "A":
            child_names = ["B", "C"]
        elif node_name == "B":
            child_names = ["D", "E"]
        elif node_name == "C":
            child_names = ["F", "G"]
        elif node_name == "D":
            child_names = ["H", "I"]
        elif node_name == "E":
            child_names = ["J", "K"]
        elif node_name == "F":
            child_names = ["L", "M"]
        elif node_name == "G":
            child_names = ["N", "O"]
        else:
            # Fallback pentru structuri mai adânci
            start_ord = ord(node_name) + 1
            child_names = [chr(start_ord + i) for i in range(len(tree))]
        
        for child, name in zip(tree, child_names):
            lines.extend(visualize_tree(child, indent + 1, name, next_type))
    return lines

# ---------------------------------------------------
# Generare întrebare
# ---------------------------------------------------
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
        except Exception as e:
            text += f"\n(Params error: {e})"

    title = entry.get("title")

    # Probleme unde chiar evaluăm strategiile (N-Queens, Coloring, Knight's Tour)
    if title in ["N-Queens", "Coloring", "Knight's Tour"]:
        results = evaluate_problem(entry, params)
        best = results[0][0] if results else None
        ranking = [r[0] for r in results]

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

    # Probleme Nash Equilibrium
    elif title == "Nash":
        rows = params.get("rows", random.randint(2, 4))
        cols = params.get("cols", random.randint(2, 4))
        game = generate_game(rows, cols)
        equilibria = find_pure_nash_equilibria(game)
        
        # Format game matrix for display
        game_str = "\nMatricea jocului (Player 1 = rânduri, Player 2 = coloane):\n"
        game_str += "     "
        for j in range(cols):
            game_str += f"  Col {j}  "
        game_str += "\n"
        
        for i in range(rows):
            game_str += f"Row {i}: "
            for j in range(cols):
                u1, u2 = game[i][j]
                game_str += f"({u1:2},{u2:2})  "
            game_str += "\n"
        
        text += game_str
        
        return {
            "title": "Nash",
            "question": text,
            "params": {"rows": rows, "cols": cols},
            "game": game,
            "answer": {
                "equilibria": equilibria,
                "has_nash": len(equilibria) > 0
            },
            "category": "nash"
        }

    # Probleme MinMax / joc
    elif title in ["MinMax", "MinMax Alpha-Beta"]:
        tree = params.get("tree")

        if tree is None:
            print(f"[EROARE] Nu s-a putut genera arborele pentru {title}")
            return None

        # Vizualizare arbore pentru debugging
        print(f"\n{'=' * 60}")
        print(f"[DEBUG] Generare întrebare MinMax")
        print(f"{'=' * 60}")
        print(f"Structură arbore: {tree}")
        print(f"\nVizualizare arbore:")
        tree_viz = visualize_tree(tree)
        tree_text = "\n".join(tree_viz)

        text += "\n\nArborele jocului:\n" + tree_text

        qt = QTemplates.QTemplates('QTemplates.json')
        minmax_result = qt.solve_minmax_alpha_beta({"tree": tree})

        root_value = minmax_result["root_value"]
        leaf_count = minmax_result["leaf_count"]

        # Calculăm numărul total de frunze
        def count_leaves(node):
            if isinstance(node, int):
                return 1
            elif isinstance(node, list):
                return sum(count_leaves(child) for child in node)
            return 0

        total_leaves = count_leaves(tree)

        print(f"\n[REZULTATE]")
        print(f"Valoare rădăcină: {root_value}")
        print(f"Frunze vizitate: {leaf_count}")
        print(f"Total frunze: {total_leaves}")
        print(f"Frunze tăiate: {total_leaves - leaf_count}")
        print(f"{'=' * 60}\n")

        return {
            "title": title,
            "question": text,
            "params": params,
            "answer": {
                "root_value": root_value,
                "leaf_count": leaf_count,
                "total_leaves": total_leaves,
                "pruned_leaves": total_leaves - leaf_count
            },
            "category": entry.get("category")
        }

    # Restul problemelor
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


# ---------------------------------------------------
# Generare listă de întrebări
# ---------------------------------------------------
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

    print(f"\n[INFO] Categorii selectate: {selected_categories}")
    print(f"[INFO] Probleme selectate: {selected_names}")

    # Check if Nash or CSP-only mode
    nash_only = selected_categories == {"nash"}
    csp_only = selected_categories == {"CSP"}
    heuristics_only = selected_categories == {"heuristics"}

    if selected_categories:
        available = [
            (n, e) for n, e in search_problems.items()
            if e.get("category") in selected_categories
        ]
        print(f"[INFO] Probleme disponibile pentru categoriile selectate: {[n for n, _ in available]}")
    elif selected_names:
        available = [(n, search_problems[n]) for n in selected_names]
    else:
        available = list(search_problems.items())

    # Allow empty available list if we're generating Nash, CSP, or Heuristics questions
    if not available and not nash_only and not csp_only and not heuristics_only:
        print("[EROARE] Nu s-au găsit probleme pentru selecția ta!")
        return []

    results = []

    for i in range(count):
        print(f"\n[INFO] Generare întrebare {i + 1}/{count}")

        # generare explicită de Nash Equilibrium
        if nash_only or (selected_categories and "nash" in selected_categories and random.random() < 0.3):
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            game = generate_game(rows, cols)
            equilibria = find_pure_nash_equilibria(game)
            
            # Format game matrix
            game_str = "\nMatricea jocului (Player 1 = rânduri, Player 2 = coloane):\n"
            game_str += "     "
            for j in range(cols):
                game_str += f"  Col {j}  "
            game_str += "\n"
            
            for row_idx in range(rows):
                game_str += f"Row {row_idx}: "
                for col_idx in range(cols):
                    u1, u2 = game[row_idx][col_idx]
                    game_str += f"({u1:2},{u2:2})  "
                game_str += "\n"
            
            if lang == "ro":
                question_text = f"Pentru jocul dat în formă normală, există echilibru Nash pur?\nDacă da, identificați toate echilibrele Nash pure.{game_str}"
            else:
                question_text = f"For the given normal form game, does a pure Nash equilibrium exist?\nIf yes, identify all pure Nash equilibria.{game_str}"
            
            wrapped = {
                "title": "Nash",
                "question": question_text,
                "game": game,
                "answer": {
                    "equilibria": equilibria,
                    "has_nash": len(equilibria) > 0
                },
                "category": "nash"
            }
            
            results.append(wrapped)
            continue

        # generare explicită de Heuristics (admisibilitate/consistență)
        heuristics_only = selected_categories == {"heuristics"}
        if heuristics_only or (selected_categories and "heuristics" in selected_categories and random.random() < 0.3):
            heuristic_gen = HeuristicQuestionGenerator()
            heuristic_gen.generate_questions(1)
            hq = heuristic_gen.questions[0]
            
            wrapped = {
                "title": "Heuristics",
                "question": hq['question'],
                "answer": {
                    "correct_answer": hq['answer'],
                    "question_type": hq['type']
                },
                "category": "heuristics"
            }
            
            results.append(wrapped)
            continue

        # generare explicită de CSP/Backtracking
        if csp_only or (selected_categories and "CSP" in selected_categories and random.random() < 0.3):
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
            print(f"[INFO] Generare întrebare pentru: {name} (categoria: {entry.get('category')})")
            question = generate_one(name, entry, lang)
            if question:
                results.append(question)
            else:
                print(f"[EROARE] Nu s-a putut genera întrebarea pentru {name}")

    return results


# ---------------- CSP Helpers ------------------

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
            f = lambda a, b: a != b
        elif op == "<":
            f = lambda a, b: a < b
        else:
            f = lambda a, b: a > b

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
        f"{v1} {op} {v2}" for (v1, v2), op in constraint_ops.items() if (v1 < v2)
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


def is_consistent(var, value, assignment, constraints):
    for (v1, v2), func in constraints.items():
        if var == v1 and v2 in assignment:
            if not func(value, assignment[v2]):
                return False
        elif var == v2 and v1 in assignment:
            if not func(assignment[v1], value):
                return False
    return True


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


# ---------------- File Handling ------------------

def write_questions_to_file(questions, filename="questions.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, q in enumerate(questions, 1):
            f.write(f"{i}. [{q['title']}] {q['question']}\n")

            # Pentru MinMax, adaugă vizualizarea arborelui
            if q['title'] in ['MinMax', 'MinMax Alpha-Beta'] and 'params' in q:
                tree = q['params'].get('tree')
                if tree:
                    f.write(f"\n   Structura arborelui: {tree}\n")
                    f.write(f"   Vizualizare:\n")
                    tree_viz = visualize_tree(tree)
                    for line in tree_viz:
                        f.write(f"   {line}\n")

            if q.get("strategy"):
                f.write(f"   Strategie recomandată: {q['strategy']}\n")
            f.write("\n")
    print(f"\nÎntrebările au fost salvate în fișierul '{filename}'")


def ask_user_for_answers(questions, filename="raspunsuri.txt"):
    answers = []
    print("\n" + "=" * 60)
    print("Scrieți mai jos răspunsurile la întrebări.")
    print("=" * 60)

    for i, q in enumerate(questions, 1):
        print(f"\n{i}. [{q['title']}]")
        print(q["question"])

        # Pentru MinMax, arată structura arborelui
        if q['title'] in ['MinMax', 'MinMax Alpha-Beta'] and 'params' in q:
            tree = q['params'].get('tree')
            if tree:
                print(f"\nStructura arborelui: {tree}")
                print("Vizualizare:")
                tree_viz = visualize_tree(tree)
                for line in tree_viz:
                    print(line)

        user_answer = input("\nRăspunsul tău: ").strip()
        score = 0
        correct_answer = None

        # CSP
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

        # MinMax
        elif q["title"] in ["MinMax", "MinMax Alpha-Beta"]:
            answer_dict = q["answer"]
            correct_root = answer_dict.get("root_value")
            correct_leaves = answer_dict.get("leaf_count")

            correct_answer = f"Valoare rădăcină: {correct_root}, Frunze vizitate: {correct_leaves}"

            score = 0
            user_lower = user_answer.lower()

            mentions_algo = any(x in user_lower for x in ["alpha", "beta", "minmax", "alpha-beta"])

            import re
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

        # Nash Equilibrium
        elif q["title"] == "Nash":
            equilibria = q["answer"]["equilibria"]
            has_nash = q["answer"]["has_nash"]
            
            if not has_nash:
                correct_answer = "NU există echilibru Nash pur"
                if "nu" in user_answer.lower() or "no" in user_answer.lower():
                    score = 100
                else:
                    score = 0
            else:
                correct_answer = f"DA. Echilibre Nash: {equilibria}"
                
                said_yes = "da" in user_answer.lower() or "yes" in user_answer.lower()
                
                pattern = r'\((\d+)\s*,\s*(\d+)\)'
                matches = re.findall(pattern, user_answer)
                user_equilibria = [(int(i), int(j)) for i, j in matches]
                
                if not said_yes and not user_equilibria:
                    score = 0
                else:
                    if said_yes and not user_equilibria:
                        score = 30
                    else:
                        correct_set = set(equilibria)
                        user_set = set(user_equilibria)
                        
                        correct_found = len(user_set & correct_set)
                        total_correct = len(correct_set)
                        false_positives = len(user_set - correct_set)
                        
                        if user_set == correct_set:
                            score = 100
                        elif correct_found > 0:
                            base_score = (correct_found / total_correct) * 80
                            penalty = false_positives * 10
                            score = max(0, int(base_score - penalty))
                        else:
                            score = 10 if said_yes else 0

        # Heuristics (Admisibilitate/Consistență)
        elif q["title"] == "Heuristics":
            correct_answer = q["answer"]["correct_answer"]
            question_type = q["answer"]["question_type"]
            
            user_lower = user_answer.lower().strip()
            
            # Verificăm dacă răspunsul conține DA sau NU
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
            
            correct_answer = f"{correct_answer} (Euristica este {'admisibilă' if question_type == 'admissible' else 'consistentă'}" if correct_answer == "DA" else f"{correct_answer} (Euristica NU este {'admisibilă' if question_type == 'admissible' else 'consistentă'})"

        # Restul problemelor
        else:
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

        score = str(int(score)) + '%'
        print(f"Scorul tău: {score}")

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

    print(f"\nRăspunsurile au fost salvate în '{filename}'.")


# ---------------- Main ------------------

if __name__ == "__main__":
    print("=" * 60)
    print("GENERATOR DE ÎNTREBĂRI - AI STRATEGIES")
    print("=" * 60)
    print("Alege tipurile de întrebări:")
    print("1 = Search problems (DFS, A*, Beam, etc.)")
    print("2 = CSP (N-Queens, Sudoku, Graph Coloring)")
    print("3 = Game problems (MinMax Alpha-Beta)")
    print("4 = Nash Equilibrium (Pure strategy Nash)")
    print("5 = Heuristics (Admissibility/Consistency)")

    problems_input = input("\nIntroduceți categoriile (ex: 1,2,3,4,5 sau 5): ").strip()
    problems = [p.strip() for p in problems_input.split(",")] if problems_input else None

    try:
        count = int(input("Număr de întrebări: "))
    except ValueError:
        count = 5
        print("Valoare invalidă, se folosește count = 5")

    lang = input("Limba (ro/en) [implicit: ro]: ").strip().lower() or "ro"

    seed_input = input("Seed aleator (Enter pentru random): ").strip()
    seed = int(seed_input) if seed_input.isdigit() else None

    filename = input("Nume fișier [implicit: questions.txt]: ").strip() or "questions.txt"

    questions = generate_questions(count=count, choices=problems, seed=seed, lang=lang)

    if questions:
        write_questions_to_file(questions, filename=filename)
        write_strategies_to_file(questions, filename="strategies.txt")
        ask_user_for_answers(questions)
    else:
        print("\n[EROARE] Nu s-au putut genera întrebări!")

    input("\nApăsați Enter pentru a închide...")