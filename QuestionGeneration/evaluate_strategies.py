from collections import deque
from algorithm_runners import search_algorithms, csp_algorithms

import random
import math

strategy_runners = {
    "Depth-First Search (DFS)": search_algorithms.dfs,
    "Breadth-First Search (BFS)": search_algorithms.bfs,
    "A* Search": search_algorithms.a_star,
    "Greedy Best-First Search": search_algorithms.a_star,  # poți avea aliasuri
    "Backtracking": csp_algorithms.backtracking,
    "Forward Checking": csp_algorithms.forward_checking,
    "Arc Consistency": csp_algorithms.arc_consistency,
    "Min-Conflicts": csp_algorithms.min_conflicts
}

import time

import time
import random

def dfs(problem, problem_instance):
    return {"result": "path found", "time": time.time() }

def iterative_deepening(problem, problem_instance):
    n_pegs = problem_instance.get("n", 3)
    n_discs = problem_instance.get("m", 3)

    # Starea goal: toate discurile pe ultima tijă în ordine descrescătoare
    goal = tuple(range(n_discs, 0, -1))
    
    def is_goal(state):
        return state[-1] == goal

    def successors(state):
        succs = []
        for i in range(n_pegs):
            if not state[i]:
                continue
            disc = state[i][-1]
            for j in range(n_pegs):
                if i == j:
                    continue
                if not state[j] or disc < state[j][-1]:
                    new_state = [list(t) for t in state]
                    new_state[i].pop()
                    new_state[j].append(disc)
                    succs.append(tuple(tuple(t) for t in new_state))
        return succs

    def dls(state, depth):
        if is_goal(state):
            return [state]
        if depth == 0:
            return None
        for succ in successors(state):
            path = dls(succ, depth - 1)
            if path:
                return [state] + path
        return None

    # stare inițială: toate discurile pe prima tijă
    initial_state = tuple([tuple(range(n_discs, 0, -1))] + [() for _ in range(n_pegs - 1)])
    
    depth = 0
    while True:
        path = dls(initial_state, depth)
        if path:
            #print(path)
            return {"solution": path}
        depth += 1

def iterative_deepening1(problem, problem_instance):
    print("here")
    result = iterative_deepening(problem_instance)
    #for state in result["solution"]:
      #print(state)


def bfs(problem, problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.02, 0.06))
    return {"result": "path found", "time": time.time() - start}

def a_star(problem, problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.005, 0.02))
    return {"result": "optimal path", "time": time.time() - start}

def recursive_search(problem, problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.005, 0.02))
    return {"result": "optimal path", "time": time.time() - start}


import time
import random

def backtracking(problem, problem_instance):
    """
    problem: numele problemei (ex: "N-Queens")
    problem_instance: dict cu parametrii instanței (ex: {"n": 8})
    returnează dict cu rezultatul și timpul de execuție
    """
    
    if problem == "N-Queens":
        n = problem_instance["n"]
        print("n:", n)
        solutions = []

        def solve(board=None, row=0):
            if board is None:
                board = []
            if row == n:
                solutions.append(board[:])
                return
            for col in range(n):
                if all(col != c and abs(row - r) != abs(col - c) for r, c in enumerate(board)):
                    board.append(col)
                    solve(board, row + 1)
                    board.pop()

        solve()  # apelăm funcția pentru a genera soluțiile
        #print(solutions)  # acum lista conține soluțiile
    elif problem=="Hanoi":
            n_pegs = problem_instance.get("n", 3)
            n_discs = problem_instance.get("m", 3)
            moves = []

            # Soluție recursivă pentru 3 tije (generalizare la >3 tije e mai complicată)
            def move(discs, source, target, auxiliary):
                if discs == 0:
                    return
                move(discs - 1, source, auxiliary, target)
                moves.append((discs, source, target))
                move(discs - 1, auxiliary, target, source)

            if n_pegs == 3:
                move(n_discs, 0, 2, 1)
            else:
                # Pentru n_pegs > 3 ai nevoie de algoritmi de tip Frame-Stewart
                # Ca mock, doar sleep și generăm mutări fictive
                time.sleep(0.01 * n_discs)
            #print(moves)
        
            return {"moves": moves}
    elif problem == "Coloring":
            n = problem_instance["n"]
            edges = problem_instance["edges"]
            colors = ["red", "green", "blue"]  # putem extinde dacă vrem mai multe culori
            solutions = []

            # creează o mapă de vecini pentru acces rapid
            neighbors = {i: set() for i in range(n)}
            for a, b in edges:
                if a != b:
                    neighbors[a].add(b)
                    neighbors[b].add(a)

            # recursive backtracking
            def assign(node=0, assignment=None):
                if assignment is None:
                    assignment = {}
                if node == n:
                    solutions.append(assignment.copy())
                    return
                for color in colors:
                    # verifică dacă nodul poate fi colorat fără conflict
                    if all(assignment.get(neigh) != color for neigh in neighbors[node]):
                        assignment[node] = color
                        assign(node + 1, assignment)
                        assignment.pop(node)

            assign()
            #print(solutions)
            return {"solutions": solutions}
    elif problem=="Knight's Tour":
            n = problem_instance["n"]
            start_x = problem_instance["start_x"]
            start_y = problem_instance["start_y"]

            # toate cele 8 mutări posibile ale calului
            moves = [
                (2, 1), (1, 2), (-1, 2), (-2, 1),
                (-2, -1), (-1, -2), (1, -2), (2, -1)
            ]

            solution = []
            visited = [[False] * n for _ in range(n)]

            def is_valid(x, y):
                return 0 <= x < n and 0 <= y < n and not visited[x][y]

            def solve(x, y, step):
                visited[x][y] = True
                solution.append((x, y))

                if step == n * n:
                    return True  # toate pătratele vizitate

                # încercăm toate mutările
                for dx, dy in moves:
                    nx, ny = x + dx, y + dy
                    if is_valid(nx, ny):
                        if solve(nx, ny, step + 1):
                            return True

                # backtracking
                visited[x][y] = False
                solution.pop()
                return False

            start_time = time.time()
            if solve(start_x, start_y, 1):
                elapsed = time.time() - start_time
                print(solution)
                return {"solution": solution,}
            else:
                elapsed = time.time() - start_time
                return {"solution": None, "time": elapsed}
    
    
    # fallback mock pentru alte probleme
    time.sleep(random.uniform(0.005, 0.02))
    return {"result": "mock result"}


def greedy_best_first(problem, problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.005, 0.02))
    return {"result": "optimal path", "time": time.time() - start}

def forward_checking(problem, problem_instance):
    if problem == "N-Queens":
        n = problem_instance["n"]
        start_time = time.time()
        solutions = []

        # Domeniile disponibile pentru fiecare rând (coloane posibile)
        domains = [set(range(n)) for _ in range(n)]

        def is_safe(row, col, board):
            # Verifică dacă coloana și diagonalele sunt libere
            for r, c in enumerate(board):
                if c == col or abs(row - r) == abs(col - c):
                    return False
            return True

        def solve(board=[], row=0):
            if row == n:
                solutions.append(board[:])
                return
            for col in domains[row]:
                if is_safe(row, col, board):
                    # forward check: elimină coloanele și diagonalele afectate de plasare
                    original_domains = [d.copy() for d in domains]
                    board.append(col)
                    # elimină coloană și diagonale pentru următorii rânduri
                    for r in range(row + 1, n):
                        domains[r] -= {col, col + (r - row), col - (r - row)}
                    solve(board, row + 1)
                    board.pop()
                    domains[:] = original_domains  # restore domains

        solve()
        #print(solutions)
        return {"solutions": solutions}
    elif problem=="Coloring":
            n = problem_instance["n"]
            edges = problem_instance.get("edges", [])
            max_colors = n  # upper bound
            solutions = []

            # lista de vecini pentru fiecare nod
            neighbors = {i: [] for i in range(n)}
            for u, v in edges:
                neighbors[u].append(v)
                neighbors[v].append(u)

            def solve(assignment=None, domains=None, node=0):
                if assignment is None:
                    assignment = {}
                if domains is None:
                    domains = {i: list(range(max_colors)) for i in range(n)}

                if node == n:
                    solutions.append(assignment.copy())
                    return

                for color in domains[node]:
                    # verificăm dacă este valid
                    if all(assignment.get(nei) != color for nei in neighbors[node]):
                        assignment[node] = color
                        # salvăm domeniile curente pentru backtracking
                        local_domains = {nei: domains[nei][:] for nei in neighbors[node] if nei not in assignment}
                        # eliminăm culoarea curentă din domeniile vecinilor nevizitați
                        for nei in neighbors[node]:
                            if nei not in assignment and color in domains[nei]:
                                domains[nei].remove(color)

                        solve(assignment, domains, node + 1)

                        # backtracking
                        assignment.pop(node)
                        for nei in local_domains:
                            domains[nei] = local_domains[nei]

            solve()
            #print(solutions)
            return {"solutions": solutions}
   
    time.sleep(random.uniform(0.005, 0.02))
    return {"result": "optimal path", "time": time.time() }

def arc_consistency(problem, problem_instance):
    if problem == "N-Queens":
            n = problem_instance["n"]
            solutions = []

            # Domeniile pentru fiecare rând: coloanele posibile
            domains = [set(range(n)) for _ in range(n)]

            def revise(i, j):
                """Elimină din domeniul i valorile care nu au suport în j"""
                revised = False
                to_remove = set()
                for vi in domains[i]:
                    if not any(vi != vj and abs(i - j) != abs(vi - vj) for vj in domains[j]):
                        to_remove.add(vi)
                        revised = True
                if revised:
                    domains[i] -= to_remove
                return revised

            def ac3():
                """Aplică AC-3 pe toate arcele (i,j)"""
                queue = deque((i, j) for i in range(n) for j in range(n) if i != j)
                while queue:
                    i, j = queue.popleft()
                    if revise(i, j):
                        for k in range(n):
                            if k != i and k != j:
                                queue.append((k, i))

            ac3()  # reducerea domeniilor

            def solve(board=[]):
                row = len(board)
                if row == n:
                    solutions.append(board[:])
                    return
                for col in domains[row]:
                    if all(col != c and abs(row - r) != abs(col - c) for r, c in enumerate(board)):
                        board.append(col)
                        solve(board)
                        board.pop()

            solve()
            #print(solutions)
            return {"solutions": solutions}
    elif problem=="Coloring":
            import copy
            n = problem_instance["n"]
            edges = problem_instance["edges"]
            colors = ["red", "green", "blue"]  # poți extinde dacă vrei mai multe culori
            solutions = []

            # creează vecinii
            neighbors = {i: set() for i in range(n)}
            for a, b in edges:
                if a != b:
                    neighbors[a].add(b)
                    neighbors[b].add(a)

            # inițializează domeniile
            domains = {i: set(colors) for i in range(n)}

            # AC-3: funcție care elimină valori imposibile
            def ac3(domains):
                queue = [(xi, xj) for xi in range(n) for xj in neighbors[xi]]
                while queue:
                    xi, xj = queue.pop(0)
                    if revise(xi, xj, domains):
                        if not domains[xi]:
                            return False  # domeniu gol => inconsistență
                        for xk in neighbors[xi] - {xj}:
                            queue.append((xk, xi))
                return True

            def revise(xi, xj, domains):
                revised = False
                to_remove = set()
                for val in domains[xi]:
                    if all(val == v for v in domains[xj]):
                        to_remove.add(val)
                        revised = True
                domains[xi] -= to_remove
                return revised

            # backtracking cu arc consistency
            def assign(assignment=None, domains=None, node=0):
                if assignment is None:
                    assignment = {}
                if domains is None:
                    domains = copy.deepcopy(domains)

                if node == n:
                    solutions.append(assignment.copy())
                    return

                for color in domains[node]:
                    if all(assignment.get(nei) != color for nei in neighbors[node]):
                        assignment[node] = color
                        local_domains = copy.deepcopy(domains)
                        local_domains[node] = {color}
                        # propaga consistența arcelor
                        if ac3(local_domains):
                            assign(assignment, local_domains, node + 1)
                        assignment.pop(node)

            assign(domains=domains)
            #print(solutions)
            return {"solutions": solutions}
    start = time.time()
    time.sleep(random.uniform(0.005, 0.02))
    return {"result": "optimal path", "time": time.time() - start}
def min_conflicts(problem, problem_instance):
      if problem == "N-Queens":
            n = problem_instance["n"]
            start_time = time.time()

            # Inițializare aleatoare: o regină pe fiecare rând
            state = [random.randint(0, n-1) for _ in range(n)]

            def conflicts(row, col):
                """Numără conflictele pentru o regină la poziția (row, col)"""
                count = 0
                for r, c in enumerate(state):
                    if r != row:
                        if c == col or abs(row - r) == abs(col - c):
                            count += 1
                return count

            for step in range(10000):
                # Lista reginelor care se află în conflict
                conflicted = [r for r in range(n) if conflicts(r, state[r]) > 0]
                if not conflicted:
                    # Soluție găsită
                    elapsed_time = time.time() - start_time
                    return {"solution": state, "time": elapsed_time}

                # Alege o regină conflictată aleator
                row = random.choice(conflicted)
                # Alege coloana cu cel mai mic număr de conflicte
                min_conflict_col = min(range(n), key=lambda c: conflicts(row, c))
                state[row] = min_conflict_col

            # Dacă nu găsește soluție, returnează starea curentă
            elapsed_time = time.time() - start_time
            #print()
            return {"solution": state}
      time.sleep(random.uniform(0.005, 0.02))
      return {"result": "optimal path", "time": time.time()}

def simulated_annealing(problem, problem_instance):
    if problem == "Knight's Tour":
        import math, random, time

        max_iter = 20000
        initial_temp = 100.0
        cooling_rate = 0.995
        n = problem_instance["n"]
        start_x = problem_instance["start_x"]
        start_y = problem_instance["start_y"]

        moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                 (-2, -1), (-1, -2), (1, -2), (2, -1)]

        def is_valid(x, y):
            return 0 <= x < n and 0 <= y < n

        path = [(start_x, start_y)]

        def score(p):
            return len(set(p))

        temperature = initial_temp
        start_time = time.time()

        for iteration in range(max_iter):
            if iteration % 2000 == 0:
                print(f"Iterația {iteration}, lungimea traseului: {len(path)}, temperatura={temperature:.3f}")

            if score(path) == n * n:
                print("✅ Knight's Tour complet găsit!")
                return {"solution": path, "time": time.time() - start_time}

            current = path[-1]
            dx, dy = random.choice(moves)
            nx, ny = current[0] + dx, current[1] + dy

            if is_valid(nx, ny):
                new_path = path + [(nx, ny)]
                new_score = score(new_path)
                old_score = score(path)

                if new_score > old_score or random.random() < math.exp((new_score - old_score) / temperature):
                    path.append((nx, ny))

            temperature *= cooling_rate

        print(f"❌ Tour incomplet — lungime finală: {len(path)}")
        print("Path:", path)
        return {"solution": path, "time": time.time() - start_time}

STRATEGY_IMPLEMENTATIONS = {
    "Recursive Search": lambda problem, params: recursive_search(problem, params),
    "Backtracking": lambda problem, params: backtracking(problem, params),
    "Depth-First Search (DFS)": lambda problem, params: dfs(problem, params),
    "Breadth-First Search (BFS)": lambda problem, params: bfs(problem, params),
    "A* Search": lambda problem, params: a_star(problem, params),
    "Greedy Best-First Search": lambda problem, params: greedy_best_first(problem, params),
    "Forward Checking": lambda problem, params: forward_checking(problem, params),
    "Arc Consistency": lambda problem, params: arc_consistency(problem, params),
    "Min-Conflicts": lambda problem, params: min_conflicts(problem, params),
    "Iterative-Deepening": lambda problem, params: iterative_deepening1(problem, params),
    "Simulated Annealing": lambda problem, params: simulated_annealing(problem, params),
}


def evaluate_problem(entry, params):
    strategies = entry.get("strategies", [])
    problem_name = entry.get("title")
    results = []
    print(problem_name)
    for strat in strategies:
        print(strat)
        func = STRATEGY_IMPLEMENTATIONS.get(strat)
        if func is None:
            continue

        start = time.time()
        func(problem_name, params)  # trimite și problema
        elapsed = time.time() - start
        print(elapsed)
        results.append((strat, elapsed))

    results.sort(key=lambda x: x[1])
    print()
    return results
