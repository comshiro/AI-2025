import random

def generate_graph_coloring_params():
    n = random.randint(5, 7)  # număr de noduri
    m = random.randint(n, n*2)  # număr de muchii
    edges = []

    while len(edges) < m:
        a = random.randint(0, n-1)
        b = random.randint(0, n-1)
        if a != b and (a, b) not in edges and (b, a) not in edges:
            edges.append((a, b))

    return {"n": n, "m": m, "edges": edges}

search_problems = {
    "Hanoi Towers": {
        "title":"Hanoi",
        "templates": {
            "ro": [
                "Există {n} tije metalice și {m} discuri de dimensiuni diferite stivuite pe prima tijă, de la cel mai mare la cel mai mic. Scopul este mutarea întregului turn pe a n-a tijă, respectând regulile: se mută un singur disc o dată și nu se poate așeza un disc mai mare peste unul mai mic. Care este strategia optimă pentru a planifica mutările astfel încât numărul total de pași să fie minim?",

                "O macara automatizată trebuie să mute {m} containere de diferite dimensiuni între {m} zone de depozitare, fără a încălca regula de greutate (un container mai greu nu poate fi plasat peste unul mai ușor). Cum se poate planifica succesiunea mutărilor pentru a atinge scopul final în cel mai scurt timp posibil?"
            ],
            "en": [
                "There are {n} metal rods and {m} discs of different sizes stacked on the first rod, from largest to smallest. The goal is to move the entire tower to the third rod, following the rules: only one disc can be moved at a time, and no larger disc may be placed on a smaller one. What is the optimal strategy to plan the moves with the minimum number of steps?",

                "An automated crane must move {m} containers of varying sizes between {n} storage areas without violating weight constraints (a heavier container cannot be placed on top of a lighter one). How should the sequence of moves be planned to reach the goal configuration as efficiently as possible?"
            ]
        },
        "params": lambda: {"n": random.choice([3, 4]), "m":random.randint(5, 10)},
        "strategies": ["Recursive Search", "Backtracking", "Iterative Deepening"],
        "types": ["search", "planning", "puzzle"]
    },

    "DFS Maze Exploration": {
        "title":"DFS Maze",
        "templates": {
            "ro": [
                "Un robot autonom pornește din colțul stânga-sus al unui labirint de dimensiune {n}×{m} și trebuie să ajungă la o ieșire amplasată aleatoriu. Robotul explorează mereu cea mai adâncă cale posibilă înainte de a reveni la un nod anterior. Cum ar trebui implementată strategia de căutare pentru a explora complet labirintul?",

                "Un agent de salvare trebuie să găsească ieșirea dintr-un labirint cu {n} coridoare și {m} intersecții. El urmează întotdeauna cea mai adâncă cale înainte de a reveni. Cum se numește strategia potrivită pentru această abordare?"
            ],
            "en": [
                "An autonomous robot starts from the top-left corner of a {n}×{m} maze and must reach a randomly placed exit. The robot always explores the deepest possible path before backtracking. How should the search strategy be implemented to explore the maze completely?",

                "A rescue agent must find the exit in a maze with {n} corridors and {m} intersections. The agent always follows the deepest path before backtracking. What search strategy best fits this approach?"
            ]
        },
        "params": lambda: {"n": random.randint(5, 12), "m": random.randint(5, 12)},
        "strategies": ["Depth-First Search (DFS)", "Iterative Deepening DFS", "Backtracking"],
        "types": ["search", "uninformed", "exploration", "robotics"]
    },

    "N-Queens": {
        "title":"N-Queens",
        "templates": {
            "ro": [
                "Să se plaseze {n} regine pe o tablă de șah de dimensiune {n}×{n} astfel încât niciuna să nu se atace reciproc pe linie, coloană sau diagonală. Care ar fi cea mai potrivita strategie pentru a determina o solutie a acestei probleme?",

                "O companie trebuie să poziționeze {n} antene de comunicație pe o grilă {n}×{n} astfel încât să nu interfereze între ele 2 cate 2 pe linie, coloana sau diagonala. Fiecare poziție corespunde unui canal radio distinct. Care ar fi cea mai potrivita strategie pentru a determina o solutie a acestei probleme?"
            ],
            "en": [
                "Place {n} queens on a {n}×{n} chessboard so that no two queens attack each other along rows, columns, or diagonals. Find all possible configurations. Which is the best strategy to solve this problem?",

                "A telecom company must place {n} communication towers on an {n}×{n} grid such that no two interfere with each other along rows, columns or diagonals. Each grid cell represents a frequency zone. Which is the best strategy to solve this problem?"
            ]
        },
        "params": lambda: {"n": random.choice([4, 5, 6, 7, 8, 9, 10])},
        "strategies": ["Backtracking", "Forward Checking", "Arc Consistency", "Min-Conflicts"],
        "types": ["CSP", "constraint-satisfaction", "search"]
    },

    "A* Route Planning": {
         "title":"A*",
        "templates": {
            "ro": [
                "Un sistem GPS trebuie să determine ruta optimă între orașele {start} și {goal} dintr-o rețea de {cities} orașe. Fiecare drum are un cost (distanță, timp sau consum). Algoritmul trebuie să combine costul parcurs (g) cu o estimare a distanței rămase (h). Care este strategia optimă de căutare?",

                "Un serviciu de livrări planifică traseul unui curier între {start} și {goal} pe o hartă cu {cities} locații conectate. Costurile pot fi afectate de trafic și distanță. Cum se poate calcula ruta cea mai eficientă folosind o funcție euristică?"
            ],
            "en": [
                "A GPS system must determine the optimal route between cities {start} and {goal} in a network of {cities} cities. Each road has an associated cost (distance, time, or energy). The algorithm should combine the traveled cost (g) with a heuristic estimate (h). What search strategy is most suitable?",

                "A delivery company plans a courier route from {start} to {goal} across {cities} connected locations. Costs depend on traffic and distance. How can the most efficient route be computed using a heuristic function?"
            ]
        },
        "params": lambda: {
            "start": random.choice(["Iași", "Cluj", "Timișoara", "București", "Brașov"]),
            "goal": random.choice(["Constanța", "Oradea", "Sibiu", "Galați", "Arad"]),
            "cities": random.randint(6, 12)
        },
        "strategies": ["A* Search", "Greedy Best-First", "Uniform Cost Search"],
        "types": ["search", "informed", "heuristic", "route-planning"]
    },

    "Beam Search Job Allocation": {
         "title":"Beam",
        "templates": {
            "ro": [
                "O companie IT trebuie să aloce {employees} angajați către {projects} proiecte. Fiecare proiect are un scor estimativ de profit și un termen limită. Deoarece spațiul soluțiilor este foarte mare, se vor păstra doar cele mai bune {beam_width} combinații la fiecare nivel al căutării. Ce strategie de căutare se aplică în acest caz?",

                "Un sistem automat de planificare trebuie să asigneze {employees} ingineri la {projects} sarcini, evaluând eficiența totală. Din motive de timp, algoritmul păstrează doar cele mai promițătoare {beam_width} stări la fiecare pas. Care este strategia utilizată?"
            ],
            "en": [
                "An IT company must allocate {employees} employees to {projects} projects. Each project has an estimated profit score and a deadline. Because the search space is huge, only the top {beam_width} combinations are retained at each search level. What search strategy applies here?",

                "An automated planning system assigns {employees} engineers to {projects} tasks, evaluating total efficiency. For time constraints, the algorithm keeps only the {beam_width} most promising states at each step. What strategy is used here?"
            ]
        },
        "params": lambda: {"employees": random.randint(6, 12), "projects": random.randint(3, 6), "beam_width": random.choice([2, 3, 4])},
        "strategies": ["Beam Search", "Greedy Best-First", "Hill-Climbing"],
        "types": ["search", "informed", "planning"]
    },

    "Job Scheduling": {
         "title":"Job",
        "templates": {
            "ro": [
                "O fabrică are {machines} mașini și {jobs} comenzi, fiecare cu un timp de procesare specific. Unele comenzi depind de altele (de exemplu, piesele trebuie prelucrate într-o ordine). Obiectivul este minimizarea timpului total de producție. Cum se poate aborda această problemă respectând toate constrângerile?",

                "Un sistem de planificare trebuie să atribuie {jobs} sarcini pe {machines} echipamente, ținând cont de durata fiecărei operații și de relațiile de dependență. Cum se poate optimiza ordonarea execuțiilor?"
            ],
            "en": [
                "A factory has {machines} machines and {jobs} tasks, each with a specific processing time. Some jobs depend on others (e.g., certain parts must be finished before others). The goal is to minimize total completion time. How can this constraint-based scheduling problem be solved?",

                "A planning system must assign {jobs} tasks to {machines} machines, considering task durations and dependencies. How can the task execution order be optimized under these constraints?"
            ]
        },
        "params": lambda: {
            "jobs": random.randint(4, 8),
            "machines": random.randint(2, 5),
            "dependencies": [(i, i + 1) for i in range(random.randint(1, 3))]
        },
        "strategies": ["Backtracking", "Forward Checking", "Arc Consistency", "Hill-Climbing", "Min-Conflicts"],
        "types": ["CSP", "constraint-satisfaction", "planning"]
    },

    "Graph Coloring": {
    "title": "Coloring",
    "templates": {
        "ro": [
            "Fie o hartă cu {n} regiuni și {m} granițe, unde vecinătățile sunt date de lista {edges}. Trebuie să atribui fiecărei regiuni o culoare astfel încât două regiuni adiacente să nu aibă aceeași culoare și să folosești cât mai puține culori. Cum poate fi modelată această problemă și ce metode de rezolvare sunt eficiente?",
            
            "Se dă un graf cu {n} noduri și {m} muchii, cu vecinătățile specificate în lista {edges}. Atribuie culori fiecărui nod astfel încât nodurile adiacente să aibă culori diferite, minimizând numărul total de culori utilizate. Ce strategii și euristici pot fi aplicate pentru a găsi o soluție?"
        ],
        "en": [
            "Given a map with {n} regions and {m} borders, where adjacency is defined by the list {edges}, assign a color to each region so that no two adjacent regions share the same color while minimizing the number of colors used. How can this problem be modeled, and what solving techniques are effective?",
            
            "Consider a graph with {n} nodes and {m} edges, with adjacency given by the list {edges}. Assign colors to each node such that adjacent nodes have different colors, minimizing the total number of colors. What strategies and heuristics can help find a solution efficiently?"
        ]
    },
  "params": lambda: generate_graph_coloring_params(),
    "strategies": ["Backtracking", "Forward Checking", "Arc Consistency", "MRV + Least Constraining Value"],
    "types": ["CSP", "search", "constraint-satisfaction", "heuristic"]
},

    "Knight's Tour": {
         "title":"Knight's Tour",
        "templates": {
            "ro": [
                "Un cal de șah trebuie să viziteze toate cele {n}×{n} pătrate ale tablei exact o dată, pornind din poziția ({start_x}, {start_y}). Planifică traseul complet astfel încât calul să ajungă pe fiecare pătrat o singură dată. Cum se poate genera o astfel de secvență de mutări?",

                "Un robot mobil se mișcă în forma literei L pe o tablă {n}×{n} și trebuie să acopere toate celulele fără a reveni pe una deja vizitată. Cum se poate implementa strategia care maximizează eficiența explorării?"
            ],
            "en": [
                "A knight must visit every square on an {n}×{n} chessboard exactly once, starting from ({start_x}, {start_y}). Plan the full path so that each square is visited only once. How can such a sequence of moves be generated?",

                "A mobile robot moves in an 'L' pattern on an {n}×{n} grid and must visit all cells without revisiting any. How can the strategy be designed to maximize exploration efficiency?"
            ]
        },
        "params": lambda: {"n": random.choice([5, 6]), "start_x": random.randint(0, 3), "start_y": random.randint(0, 3)},
        "strategies": ["Backtracking", "Simulated Annealing"],
        "types": ["search", "heuristic", "game"]
    },

    "8-Puzzle": {
         "title":"8-Puzzle",
        "templates": {
            "ro": [
                "Se dă un puzzle glisant {n}×{n} cu 8 piese numerotate și un spațiu liber. Configurația inițială este {start_state}, iar scopul este să ajungi la {goal_state}. Determină secvența optimă de mutări care minimizează numărul total de pași, folosind o funcție de cost f(n)=g(n)+h(n). Ce algoritm este cel mai potrivit?",

                "Un puzzle numeric {n}×{n} trebuie rearanjat din starea {start_state} în starea {goal_state}. Care este cea mai eficientă strategie de căutare informată pentru a obține soluția?"
            ],
            "en": [
                "Given a {n}×{n} sliding puzzle with 8 numbered tiles and one empty space. The initial configuration is {start_state}, and the goal is {goal_state}. Find the optimal sequence of moves minimizing total cost, using f(n)=g(n)+h(n). Which algorithm is most appropriate?",

                "A {n}×{n} tile puzzle must be rearranged from {start_state} to {goal_state}. What is the most efficient informed search strategy to find the solution?"
            ]
        },
        "params": lambda: {
            "n": 3,
            "start_state": random.sample(range(9), 9),
            "goal_state": list(range(1, 9)) + [0]
        },
        "strategies": ["A*", "Greedy Best-First", "Uniform Cost Search"],
        "types": ["search", "heuristic", "puzzle"]
    },

    "Sudoku": {
         "title":"Sudoku",
    "templates": {
        "ro": [
            "Rezolvă următorul puzzle Sudoku {n}×{n}: completează grila astfel încât fiecare rând, coloană și subgrilă {sqrt_n}×{sqrt_n} să conțină toate numerele de la 1 la {n} fără repetări. Grila inițială este:\n{grid}\nCare este cea mai potrivită strategie de rezolvare?",

            "Se dă o grilă Sudoku parțial completată de dimensiune {n}×{n}. Completează spațiile libere respectând regulile jocului: fiecare număr de la 1 la {n} trebuie să apară exact o dată pe rând, coloană și în fiecare bloc {sqrt_n}×{sqrt_n}. Grila este:\n{grid}\nCe strategie de rezolvare consideri mai eficientă?"
        ],
        "en": [
            "Solve the following {n}×{n} Sudoku puzzle: fill the grid so that each row, column, and {sqrt_n}×{sqrt_n} subgrid contains all numbers from 1 to {n} without repetition. The initial grid is:\n{grid}\nWhat is the most suitable solving strategy?",

            "Given a partially filled {n}×{n} Sudoku grid, complete the missing cells so that every number from 1 to {n} appears exactly once in each row, column, and {sqrt_n}×{sqrt_n} block. The grid is:\n{grid}\nWhich solving strategy do you find most efficient?"
        ]
    },
    "params": lambda: (
        lambda n=9: {
            "n": n,
            "sqrt_n": int(n ** 0.5),
            "grid": "\n".join(
                " ".join(str(random.choice(range(1, n + 1))) if random.random() < 0.25 else "0" for _ in range(n))
                for _ in range(n)
            )
        }
    )(),
    "strategies": [
        "Backtracking",
        "Constraint Propagation (Forward Checking)",
        "Arc Consistency",
        "MRV",
        "Simulated Annealing (for approximate solutions)"
    ],
    "types": ["CSP", "search", "constraint-satisfaction", "puzzle"]
}
}
