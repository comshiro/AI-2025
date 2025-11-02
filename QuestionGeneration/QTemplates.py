import random

search_problems = {
    "N-Queens": {
        "template": "Problema: N-Queens. Instanță: o tablă de dimensiune {n}×{n}. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"n": random.randint(4, 12)},
        "strategy": "Backtracking / CSP Search"
    },
    "Graph Coloring": {
        "template": "Problema: Graph Coloring. Instanță: un graf cu {n} noduri și {m} muchii. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"n": random.randint(5, 12), "m": random.randint(10, 25)},
        "strategy": "Backtracking / Constraint Satisfaction Search"
    },
    "Knight's Tour": {
        "template": "Problema: Knight's Tour. Instanță: o tablă de dimensiune {n}×{n}. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"n": random.choice([5, 6, 7, 8])},
        "strategy": "Backtracking / Heuristic Search (Warnsdorff’s Rule)"
    },
    "Generalized Hanoi": {
        "template": "Problema: Generalized Hanoi. Instanță: {n} discuri și {pegs} țăruși. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"n": random.randint(3, 8), "pegs": random.choice([3, 4])},
        "strategy": "Recursive Search / State-Space Search"
    },
    "Missionaries and Cannibals": {
        "template": "Problema: Missionaries and Cannibals. Instanță: {missionaries} misionari și {cannibals} canibali, barca poate transporta {boat_capacity} persoane. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"missionaries": 3, "cannibals": 3, "boat_capacity": 2},
        "strategy": "State-Space Search / BFS"
    },
    "8-Puzzle": {
        "template": "Problema: 8-Puzzle. Instanță: configurație inițială a unui puzzle {n}×{n}. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"n": 3},
        "strategy": "Heuristic Search (A*)"
    },
    "Water Jug Problem": {
        "template": "Problema: Water Jug Problem. Instanță: vase de {jug1} și {jug2} litri, scop: {target} litri. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"jug1": 3, "jug2": 5, "target": 4},
        "strategy": "State-Space Search / BFS"
    },
    "Robot Pathfinding": {
        "template": "Problema: Robot Pathfinding. Instanță: robot pe o grilă {n}×{n} cu start ({start_x},{start_y}) și țintă ({goal_x},{goal_y}), cu obstacole. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"n": random.randint(5, 15), "start_x": 0, "start_y": 0, "goal_x": random.randint(1, 14), "goal_y": random.randint(1, 14)},
        "strategy": "Heuristic Search (A* / Dijkstra)"
    },
    "Maze Solving": {
        "template": "Problema: Maze Solving. Instanță: labirint {n}×{m} cu start și final. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"n": random.randint(5, 15), "m": random.randint(5, 15)},
        "strategy": "DFS / BFS / A* Search"
    },
    "TSP (Traveling Salesman Problem)": {
        "template": "Problema: Traveling Salesman. Instanță: {n} orașe de vizitat o singură dată. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"n": random.randint(4, 10)},
        "strategy": "Heuristic Search / Branch and Bound"
    },
    "Vacuum World": {
        "template": "Problema: Vacuum World. Instanță: {rooms} camere de curățat. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"rooms": random.randint(2, 4)},
        "strategy": "Uninformed Search / State-Space Search"
    },
    "Blocks World": {
        "template": "Problema: Blocks World. Instanță: {blocks} blocuri într-o configurație inițială și finală. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"blocks": random.randint(3, 6)},
        "strategy": "Heuristic Search / STRIPS Planning"
    },
    "Fox-Goose-Beans": {
        "template": "Problema: Fox-Goose-Beans. Instanță: traversarea unui râu cu fermier, vulpe, gâscă și boabe. Barca poate transporta doar fermierul și un obiect. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {},
        "strategy": "State-Space Search / BFS"
    },
    "Knight’s Covering Problem": {
        "template": "Problema: Knight’s Covering. Instanță: tablă {n}×{n}. Determinați un set minim de poziții de cal pentru a acoperi toate pătratele. Care este cea mai potrivită strategie de rezolvare?",
        "params": lambda: {"n": random.choice([5, 6, 7, 8])},
        "strategy": "Heuristic Search / Optimization"
    }
}
