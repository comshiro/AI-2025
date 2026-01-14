import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re

from generate_questions import generate_questions


class AIQuestionsGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI Question Generator – GUI")
        self.geometry("1200x800")

        self.questions = []
        self.current_index = 0
        self.checked = False
        self.total_score = 0

        self.create_widgets()

    # ================= UI =================
    def create_widgets(self):
        # Notebook pentru tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tab 1: Generator de întrebări (existent)
        tab_generator = self.create_generator_tab()
        notebook.add(tab_generator, text="📝 Generator Întrebări")
        
        # Tab 2: Solver custom (NOU)
        tab_solver = self.create_solver_tab()
        notebook.add(tab_solver, text="🔧 Rezolvare Problemă")
        
        # Tab 3: Parser întrebări în limbaj natural (NOU)
        tab_parser = self.create_parser_tab()
        notebook.add(tab_parser, text="💬 Întrebare în Text")
    
    def create_generator_tab(self):
        """Tab-ul original cu generatorul de întrebări"""
        main_frame = ttk.Frame(self)
        
        # ---------- CONFIG ----------
        config = ttk.LabelFrame(main_frame, text="Configurare")
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
        q_frame = ttk.LabelFrame(main_frame, text="Întrebare")
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
        r_frame = ttk.LabelFrame(main_frame, text="Rezultat")
        r_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_box = scrolledtext.ScrolledText(
            r_frame, height=8, wrap=tk.WORD, font=("Consolas", 11)
        )
        self.result_box.pack(fill="both", expand=True, padx=5, pady=5)
        
        return main_frame
    
    def create_solver_tab(self):
        """Tab nou pentru rezolvare probleme custom"""
        solver_frame = ttk.Frame(self)
        
        # ---------- PROBLEM SELECTION ----------
        select_frame = ttk.LabelFrame(solver_frame, text="Selectare Problemă")
        select_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(select_frame, text="Tip problemă:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.solver_problem_type = ttk.Combobox(
            select_frame,
            values=[
                "N-Queens",
                "Graph Coloring", 
                "Sudoku 4x4",
                "Job Scheduling",
                "A* Pathfinding"
            ],
            state="readonly",
            width=25
        )
        self.solver_problem_type.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.solver_problem_type.current(0)
        self.solver_problem_type.bind("<<ComboboxSelected>>", self.update_solver_params)
        
        # ---------- PARAMETERS ----------
        self.params_frame = ttk.LabelFrame(solver_frame, text="Parametri")
        self.params_frame.pack(fill="x", padx=10, pady=5)
        
        # Acest frame va fi populat dinamic
        self.param_widgets = {}
        
        # ---------- ALGORITHM SELECTION ----------
        algo_frame = ttk.LabelFrame(solver_frame, text="Algoritm de Rezolvare")
        algo_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(algo_frame, text="Algoritm:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.solver_algorithm = ttk.Combobox(algo_frame, state="readonly", width=25)
        self.solver_algorithm.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Button(
            algo_frame,
            text="🚀 Rezolvă Problema",
            command=self.solve_custom_problem
        ).grid(row=0, column=2, padx=20, pady=5)
        
        # ---------- OUTPUT ----------
        output_frame = ttk.LabelFrame(solver_frame, text="Rezultat")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.solver_output = scrolledtext.ScrolledText(
            output_frame,
            height=25,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.solver_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Inițializare parametri pentru prima problemă
        self.update_solver_params()
        
        return solver_frame
    
    def update_solver_params(self, event=None):
        """Actualizează câmpurile de parametri în funcție de problema selectată"""
        # Șterge widget-urile existente
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        self.param_widgets.clear()
        
        problem = self.solver_problem_type.get()
        
        if problem == "N-Queens":
            ttk.Label(self.params_frame, text="N (dimensiune tablă):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.param_widgets['n'] = ttk.Spinbox(self.params_frame, from_=4, to=15, width=10)
            self.param_widgets['n'].set(8)
            self.param_widgets['n'].grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            self.solver_algorithm['values'] = ["Backtracking", "Forward Checking", "Min-Conflicts"]
            self.solver_algorithm.current(0)
            
        elif problem == "Graph Coloring":
            ttk.Label(self.params_frame, text="Număr noduri:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.param_widgets['nodes'] = ttk.Spinbox(self.params_frame, from_=4, to=12, width=10)
            self.param_widgets['nodes'].set(6)
            self.param_widgets['nodes'].grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            ttk.Label(self.params_frame, text="Muchii (ex: 0-1,1-2,2-3):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.param_widgets['edges'] = ttk.Entry(self.params_frame, width=40)
            self.param_widgets['edges'].insert(0, "0-1,1-2,2-3,3-4,4-0,1-4")
            self.param_widgets['edges'].grid(row=1, column=1, padx=5, pady=5, sticky="w")
            
            self.solver_algorithm['values'] = ["Backtracking", "Forward Checking", "Arc Consistency"]
            self.solver_algorithm.current(0)
            
        elif problem == "Sudoku 4x4":
            ttk.Label(self.params_frame, text="Grid inițial (0 = celulă goală):").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
            
            self.param_widgets['grid'] = scrolledtext.ScrolledText(self.params_frame, width=30, height=6, font=("Consolas", 10))
            self.param_widgets['grid'].insert("1.0", "0 2 0 0\n0 0 0 3\n4 0 0 0\n0 0 1 0")
            self.param_widgets['grid'].grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            self.solver_algorithm['values'] = ["Backtracking", "Forward Checking"]
            self.solver_algorithm.current(0)
            
        elif problem == "Job Scheduling":
            ttk.Label(self.params_frame, text="Număr mașini:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.param_widgets['machines'] = ttk.Spinbox(self.params_frame, from_=2, to=5, width=10)
            self.param_widgets['machines'].set(3)
            self.param_widgets['machines'].grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            ttk.Label(self.params_frame, text="Număr joburi:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.param_widgets['jobs'] = ttk.Spinbox(self.params_frame, from_=3, to=10, width=10)
            self.param_widgets['jobs'].set(6)
            self.param_widgets['jobs'].grid(row=1, column=1, padx=5, pady=5, sticky="w")
            
            self.solver_algorithm['values'] = ["Backtracking", "Hill-Climbing", "Min-Conflicts"]
            self.solver_algorithm.current(0)
            
        elif problem == "A* Pathfinding":
            ttk.Label(self.params_frame, text="Dimensiune grid:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.param_widgets['grid_size'] = ttk.Spinbox(self.params_frame, from_=5, to=15, width=10)
            self.param_widgets['grid_size'].set(8)
            self.param_widgets['grid_size'].grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            ttk.Label(self.params_frame, text="Start (ex: 0,0):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.param_widgets['start'] = ttk.Entry(self.params_frame, width=15)
            self.param_widgets['start'].insert(0, "0,0")
            self.param_widgets['start'].grid(row=1, column=1, padx=5, pady=5, sticky="w")
            
            ttk.Label(self.params_frame, text="Goal (ex: 7,7):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.param_widgets['goal'] = ttk.Entry(self.params_frame, width=15)
            self.param_widgets['goal'].insert(0, "7,7")
            self.param_widgets['goal'].grid(row=2, column=1, padx=5, pady=5, sticky="w")
            
            self.solver_algorithm['values'] = ["A*", "Greedy Best-First", "Dijkstra"]
            self.solver_algorithm.current(0)
    
    def solve_custom_problem(self):
        """Rezolvă problema selectată cu algoritmul ales"""
        problem = self.solver_problem_type.get()
        algorithm = self.solver_algorithm.get()
        
        self.solver_output.delete("1.0", tk.END)
        self.solver_output.insert(tk.END, f"🔄 Rezolvare {problem} cu {algorithm}...\n")
        self.solver_output.insert(tk.END, "=" * 60 + "\n\n")
        
        try:
            if problem == "N-Queens":
                n = int(self.param_widgets['n'].get())
                self.solve_n_queens(n, algorithm)
                
            elif problem == "Graph Coloring":
                nodes = int(self.param_widgets['nodes'].get())
                edges_str = self.param_widgets['edges'].get()
                self.solve_graph_coloring(nodes, edges_str, algorithm)
                
            elif problem == "Sudoku 4x4":
                grid_str = self.param_widgets['grid'].get("1.0", tk.END)
                self.solve_sudoku(grid_str, algorithm)
                
            elif problem == "Job Scheduling":
                machines = int(self.param_widgets['machines'].get())
                jobs = int(self.param_widgets['jobs'].get())
                self.solve_job_scheduling(machines, jobs, algorithm)
                
            elif problem == "A* Pathfinding":
                grid_size = int(self.param_widgets['grid_size'].get())
                start = self.param_widgets['start'].get()
                goal = self.param_widgets['goal'].get()
                self.solve_pathfinding(grid_size, start, goal, algorithm)
                
        except Exception as e:
            self.solver_output.insert(tk.END, f"\n❌ EROARE: {str(e)}")
    
    def solve_n_queens(self, n, algorithm):
        """Rezolvă problema N-Queens"""
        self.solver_output.insert(tk.END, f"📋 Problemă: Plasarea a {n} regine pe o tablă {n}×{n}\n")
        self.solver_output.insert(tk.END, f"🎯 Obiectiv: Nicio regină să nu se atace reciproc\n")
        self.solver_output.insert(tk.END, f"⚙️  Algoritm: {algorithm}\n\n")
        
        # Funcție simplă de verificare
        def is_safe(board, row, col):
            # Verifică coloana
            for i in range(row):
                if board[i] == col:
                    return False
            
            # Verifică diagonala principală
            for i in range(row):
                if abs(board[i] - col) == abs(i - row):
                    return False
            
            return True
        
        # Backtracking
        steps = []
        def backtrack(board, row):
            if row == n:
                return board[:]
            
            for col in range(n):
                if is_safe(board, row, col):
                    board[row] = col
                    steps.append(f"Plasare regină: rând {row}, coloană {col}")
                    
                    result = backtrack(board, row + 1)
                    if result:
                        return result
                    
                    steps.append(f"Backtrack de la ({row}, {col})")
                    board[row] = -1
            
            return None
        
        solution = backtrack([-1] * n, 0)
        
        if solution:
            self.solver_output.insert(tk.END, "✅ SOLUȚIE GĂSITĂ!\n\n")
            self.solver_output.insert(tk.END, f"Poziții regine (rând, coloană):\n")
            for row, col in enumerate(solution):
                self.solver_output.insert(tk.END, f"  Regină {row + 1}: ({row}, {col})\n")
            
            self.solver_output.insert(tk.END, f"\n📊 Statistici:\n")
            self.solver_output.insert(tk.END, f"  - Pași explorați: {len(steps)}\n")
            self.solver_output.insert(tk.END, f"  - Backtrack-uri: {sum(1 for s in steps if 'Backtrack' in s)}\n")
            
            # Vizualizare tablă
            self.solver_output.insert(tk.END, f"\n🎨 Vizualizare tablă:\n")
            for i in range(n):
                line = ""
                for j in range(n):
                    if solution[i] == j:
                        line += " ♛ "
                    else:
                        line += " · " if (i + j) % 2 == 0 else " ○ "
                self.solver_output.insert(tk.END, f"  {line}\n")
        else:
            self.solver_output.insert(tk.END, "❌ Nu există soluție!\n")
    
    def solve_graph_coloring(self, nodes, edges_str, algorithm):
        """Rezolvă problema Graph Coloring"""
        self.solver_output.insert(tk.END, f"📋 Problemă: Colorare graf cu {nodes} noduri\n")
        
        # Parse edges
        edges = []
        try:
            for edge in edges_str.split(','):
                a, b = map(int, edge.strip().split('-'))
                edges.append((a, b))
        except:
            self.solver_output.insert(tk.END, "❌ Format muchii invalid! Folosește: 0-1,1-2,2-3\n")
            return
        
        self.solver_output.insert(tk.END, f"🔗 Muchii: {edges}\n")
        self.solver_output.insert(tk.END, f"⚙️  Algoritm: {algorithm}\n\n")
        
        # Construiește lista de adiacență
        adj = [[] for _ in range(nodes)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        
        # Backtracking colorare
        colors = [-1] * nodes
        
        def is_safe_color(node, color):
            for neighbor in adj[node]:
                if colors[neighbor] == color:
                    return False
            return True
        
        def backtrack(node):
            if node == nodes:
                return True
            
            for color in range(nodes):  # Max nodes culori posibile
                if is_safe_color(node, color):
                    colors[node] = color
                    if backtrack(node + 1):
                        return True
                    colors[node] = -1
            
            return False
        
        if backtrack(0):
            self.solver_output.insert(tk.END, "✅ SOLUȚIE GĂSITĂ!\n\n")
            
            num_colors = max(colors) + 1
            self.solver_output.insert(tk.END, f"🎨 Număr culori folosite: {num_colors}\n\n")
            
            self.solver_output.insert(tk.END, "Colorare noduri:\n")
            for node in range(nodes):
                self.solver_output.insert(tk.END, f"  Nod {node}: Culoare {colors[node]}\n")
        else:
            self.solver_output.insert(tk.END, "❌ Nu există soluție!\n")
    
    def solve_sudoku(self, grid_str, algorithm):
        """Rezolvă Sudoku 4x4"""
        self.solver_output.insert(tk.END, "📋 Problemă: Sudoku 4×4\n")
        self.solver_output.insert(tk.END, f"⚙️  Algoritm: {algorithm}\n\n")
        
        # Parse grid
        try:
            grid = []
            for line in grid_str.strip().split('\n'):
                row = [int(x) for x in line.split()]
                if len(row) != 4:
                    raise ValueError("Fiecare rând trebuie să aibă 4 numere")
                grid.append(row)
            
            if len(grid) != 4:
                raise ValueError("Grid-ul trebuie să aibă 4 rânduri")
        except Exception as e:
            self.solver_output.insert(tk.END, f"❌ Format grid invalid: {e}\n")
            return
        
        self.solver_output.insert(tk.END, "Grid inițial:\n")
        for row in grid:
            self.solver_output.insert(tk.END, f"  {' '.join(str(x) if x != 0 else '·' for x in row)}\n")
        
        self.solver_output.insert(tk.END, "\n")
        
        def is_valid(grid, row, col, num):
            # Verifică rând
            if num in grid[row]:
                return False
            
            # Verifică coloană
            if num in [grid[r][col] for r in range(4)]:
                return False
            
            # Verifică subgrid 2x2
            subgrid_row = (row // 2) * 2
            subgrid_col = (col // 2) * 2
            for r in range(subgrid_row, subgrid_row + 2):
                for c in range(subgrid_col, subgrid_col + 2):
                    if grid[r][c] == num:
                        return False
            
            return True
        
        def solve():
            for row in range(4):
                for col in range(4):
                    if grid[row][col] == 0:
                        for num in range(1, 5):
                            if is_valid(grid, row, col, num):
                                grid[row][col] = num
                                if solve():
                                    return True
                                grid[row][col] = 0
                        return False
            return True
        
        if solve():
            self.solver_output.insert(tk.END, "✅ SOLUȚIE GĂSITĂ!\n\n")
            self.solver_output.insert(tk.END, "Grid rezolvat:\n")
            for row in grid:
                self.solver_output.insert(tk.END, f"  {' '.join(str(x) for x in row)}\n")
        else:
            self.solver_output.insert(tk.END, "❌ Nu există soluție!\n")
    
    def solve_job_scheduling(self, machines, jobs, algorithm):
        """Rezolvă Job Scheduling (simplificat)"""
        import random
        
        self.solver_output.insert(tk.END, f"📋 Problemă: Alocare {jobs} joburi pe {machines} mașini\n")
        self.solver_output.insert(tk.END, f"⚙️  Algoritm: {algorithm}\n\n")
        
        # Generează durate random pentru joburi
        job_durations = [random.randint(1, 10) for _ in range(jobs)]
        
        self.solver_output.insert(tk.END, "Durate joburi:\n")
        for i, duration in enumerate(job_durations):
            self.solver_output.insert(tk.END, f"  Job {i}: {duration} unități\n")
        
        self.solver_output.insert(tk.END, "\n")
        
        # Greedy allocation
        machine_loads = [0] * machines
        allocation = [0] * jobs
        
        for job_id, duration in enumerate(job_durations):
            # Găsește mașina cu încărcarea minimă
            min_machine = machine_loads.index(min(machine_loads))
            allocation[job_id] = min_machine
            machine_loads[min_machine] += duration
        
        self.solver_output.insert(tk.END, "✅ ALOCARE GĂSITĂ!\n\n")
        self.solver_output.insert(tk.END, "Alocare joburi:\n")
        for job_id, machine_id in enumerate(allocation):
            self.solver_output.insert(tk.END, f"  Job {job_id} → Mașina {machine_id} (durată: {job_durations[job_id]})\n")
        
        self.solver_output.insert(tk.END, f"\n📊 Încărcări mașini:\n")
        for machine_id, load in enumerate(machine_loads):
            self.solver_output.insert(tk.END, f"  Mașina {machine_id}: {load} unități\n")
        
        self.solver_output.insert(tk.END, f"\n⏱️  Makespan (timp total): {max(machine_loads)} unități\n")
    
    def solve_pathfinding(self, grid_size, start_str, goal_str, algorithm):
        """Rezolvă A* Pathfinding"""
        import heapq
        import random
        
        self.solver_output.insert(tk.END, f"📋 Problemă: Găsire cale în grid {grid_size}×{grid_size}\n")
        self.solver_output.insert(tk.END, f"⚙️  Algoritm: {algorithm}\n\n")
        
        # Parse coordonate
        try:
            start = tuple(map(int, start_str.split(',')))
            goal = tuple(map(int, goal_str.split(',')))
        except:
            self.solver_output.insert(tk.END, "❌ Format coordonate invalid!\n")
            return
        
        self.solver_output.insert(tk.END, f"🎯 Start: {start}\n")
        self.solver_output.insert(tk.END, f"🏁 Goal: {goal}\n\n")
        
        # Generează obstacole random
        obstacles = set()
        for _ in range(grid_size * 2):
            obs = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
            if obs != start and obs != goal:
                obstacles.add(obs)
        
        # Heuristică Manhattan
        def heuristic(pos):
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        
        # A* search
        open_set = [(heuristic(start), 0, start, [start])]
        visited = set()
        
        while open_set:
            f, g, current, path = heapq.heappop(open_set)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == goal:
                self.solver_output.insert(tk.END, f"✅ CALE GĂSITĂ!\n\n")
                self.solver_output.insert(tk.END, f"📏 Lungime cale: {len(path)} pași\n")
                self.solver_output.insert(tk.END, f"🔍 Noduri explorate: {len(visited)}\n\n")
                
                self.solver_output.insert(tk.END, "Cale:\n")
                for i, pos in enumerate(path):
                    self.solver_output.insert(tk.END, f"  {i}. {pos}\n")
                
                # Vizualizare grid
                self.solver_output.insert(tk.END, f"\n🗺️  Grid:\n")
                path_set = set(path)
                for r in range(grid_size):
                    line = "  "
                    for c in range(grid_size):
                        pos = (r, c)
                        if pos == start:
                            line += "S "
                        elif pos == goal:
                            line += "G "
                        elif pos in path_set:
                            line += "· "
                        elif pos in obstacles:
                            line += "█ "
                        else:
                            line += "  "
                    self.solver_output.insert(tk.END, line + "\n")
                
                return
            
            # Explorează vecini
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                if (0 <= neighbor[0] < grid_size and 
                    0 <= neighbor[1] < grid_size and
                    neighbor not in obstacles and
                    neighbor not in visited):
                    
                    new_g = g + 1
                    new_f = new_g + heuristic(neighbor)
                    heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))
        
        self.solver_output.insert(tk.END, "❌ Nu există cale!\n")

    # ================= LOGIC GENERATOR (existent) =================
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
    
    def create_parser_tab(self):
        """Tab pentru parsare întrebări în limbaj natural"""
        parser_frame = ttk.Frame(self)
        
        # ---------- INSTRUCTION ----------
        instruction = ttk.LabelFrame(parser_frame, text="📖 Instrucțiuni")
        instruction.pack(fill="x", padx=10, pady=5)
        
        info_text = """Scrie o întrebare în text liber și aplicația va încerca să o rezolve automat.

Exemple de întrebări acceptate:
• "Verifică dacă euristica este admisibilă"
• "Testează consistența euristicii"
• "Rezolvă N-Queens cu 8 regine folosind backtracking"
• "Colorează un graf cu 6 noduri și muchiile 0-1,1-2,2-3,3-4,4-5,5-0"
• "Găsește calea de la (0,0) la (5,5) într-un grid 10x10 cu A*"
• "Rezolvă sudoku 4x4: 0 2 0 0, 0 0 0 3, 4 0 0 0, 0 0 1 0"
• "Aloca 5 joburi pe 3 mașini cu hill climbing"
• "Aplică MinMax cu alpha-beta pe arborele [[[9,7],[10,1]],[[7,6],[1,5]]]"
• "Există Nash equilibrium pentru joc 3x3?"
"""
        
        info_label = tk.Label(instruction, text=info_text, justify="left", font=("Arial", 9))
        info_label.pack(padx=10, pady=5, anchor="w")
        
        # ---------- INPUT ----------
        input_frame = ttk.LabelFrame(parser_frame, text="✍️ Întrebarea ta")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        self.parser_input = scrolledtext.ScrolledText(
            input_frame,
            height=5,
            wrap=tk.WORD,
            font=("Arial", 11)
        )
        self.parser_input.pack(fill="x", padx=5, pady=5)
        
        # Buton rezolvare
        ttk.Button(
            input_frame,
            text="🚀 Analizează și Rezolvă",
            command=self.parse_and_solve
        ).pack(pady=5)
        
        # ---------- OUTPUT ----------
        output_frame = ttk.LabelFrame(parser_frame, text="💡 Răspuns")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.parser_output = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.parser_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        return parser_frame
    
    def parse_and_solve(self):
        """Parsează întrebarea și rezolvă problema"""
        question = self.parser_input.get("1.0", tk.END).strip().lower()
        
        if not question:
            messagebox.showwarning("Atenție", "Introdu o întrebare!")
            return
        
        self.parser_output.delete("1.0", tk.END)
        self.parser_output.insert(tk.END, f"📝 Întrebare: {question}\n")
        self.parser_output.insert(tk.END, "=" * 70 + "\n\n")
        
        # ---------- DETECTARE TIP PROBLEMĂ ----------
        problem_type = None
        algorithm = "Backtracking"  # default
        
        # Heuristics (admisibilitate/consistență) - verificăm PRIMUL pentru că folosește "graf"
        if any(keyword in question for keyword in ["euristic", "heuristic", "admisibil", "admissible", "consisten", "monoton"]):
            problem_type = "Heuristics"
            
            # Detectează tipul de verificare
            if "admisibil" in question or "admissible" in question:
                check_type = "admissible"
            else:
                check_type = "consistent"
            
            self.parser_output.insert(tk.END, f"🔍 Detectat: Verificare Euristică\n")
            self.parser_output.insert(tk.END, f"📊 Tip: {'Admisibilitate' if check_type == 'admissible' else 'Consistență'}\n\n")
            self._solve_heuristics_internal(check_type)
        
        # N-Queens
        elif any(keyword in question for keyword in ["queen", "regine", "regină", "n-queens"]):
            problem_type = "N-Queens"
            n = self._extract_number(question, default=8)
            
            if "forward" in question or "fc" in question:
                algorithm = "Forward Checking"
            elif "min-conflict" in question or "conflicts" in question:
                algorithm = "Min-Conflicts"
            
            self.parser_output.insert(tk.END, f"🔍 Detectat: Problema N-Queens\n")
            self.parser_output.insert(tk.END, f"📊 Parametri: N={n}, Algoritm={algorithm}\n\n")
            self._solve_n_queens_internal(n, algorithm)
        
        # Graph Coloring
        elif any(keyword in question for keyword in ["colorare", "coloring", "graf", "graph", "muchii", "edges"]):
            problem_type = "Graph Coloring"
            
            # Extrage număr noduri
            nodes = self._extract_number(question, default=6)
            
            # Extrage muchii
            edges_str = self._extract_edges(question)
            
            if "forward" in question or "fc" in question:
                algorithm = "Forward Checking"
            elif "arc" in question or "ac3" in question or "consistency" in question:
                algorithm = "Arc Consistency"
            
            self.parser_output.insert(tk.END, f"🔍 Detectat: Graph Coloring\n")
            self.parser_output.insert(tk.END, f"📊 Parametri: Noduri={nodes}, Muchii={edges_str}, Algoritm={algorithm}\n\n")
            self._solve_graph_coloring_internal(nodes, edges_str, algorithm)
        
        # Sudoku
        elif any(keyword in question for keyword in ["sudoku"]):
            problem_type = "Sudoku"
            
            grid_str = self._extract_sudoku_grid(question)
            
            if "forward" in question:
                algorithm = "Forward Checking"
            
            self.parser_output.insert(tk.END, f"🔍 Detectat: Sudoku 4×4\n")
            self.parser_output.insert(tk.END, f"📊 Algoritm: {algorithm}\n\n")
            self._solve_sudoku_internal(grid_str, algorithm)
        
        # Job Scheduling
        elif any(keyword in question for keyword in ["job", "joburi", "mașini", "machines", "alocare", "scheduling"]):
            problem_type = "Job Scheduling"
            
            # Extrage mașini și joburi
            numbers = re.findall(r'\d+', question)
            jobs = int(numbers[0]) if len(numbers) > 0 else 5
            machines = int(numbers[1]) if len(numbers) > 1 else 3
            
            if "hill" in question or "climbing" in question:
                algorithm = "Hill-Climbing"
            elif "min-conflict" in question:
                algorithm = "Min-Conflicts"
            
            self.parser_output.insert(tk.END, f"🔍 Detectat: Job Scheduling\n")
            self.parser_output.insert(tk.END, f"📊 Parametri: Joburi={jobs}, Mașini={machines}, Algoritm={algorithm}\n\n")
            self._solve_job_scheduling_internal(machines, jobs, algorithm)
        
        # Pathfinding (A*)
        elif any(keyword in question for keyword in ["cale", "path", "a*", "astar", "dijkstra", "grid"]):
            problem_type = "Pathfinding"
            
            # Extrage dimensiune grid
            grid_size = self._extract_number(question, default=8)
            
            # Extrage coordonate start/goal
            coords = re.findall(r'\((\d+)\s*,\s*(\d+)\)', question)
            start = coords[0] if len(coords) > 0 else ("0", "0")
            goal = coords[1] if len(coords) > 1 else (str(grid_size-1), str(grid_size-1))
            
            start_str = f"{start[0]},{start[1]}"
            goal_str = f"{goal[0]},{goal[1]}"
            
            algorithm = "A*"
            if "greedy" in question or "best-first" in question:
                algorithm = "Greedy Best-First"
            elif "dijkstra" in question:
                algorithm = "Dijkstra"
            
            self.parser_output.insert(tk.END, f"🔍 Detectat: Pathfinding\n")
            self.parser_output.insert(tk.END, f"📊 Parametri: Grid={grid_size}×{grid_size}, Start={start_str}, Goal={goal_str}, Algoritm={algorithm}\n\n")
            self._solve_pathfinding_internal(grid_size, start_str, goal_str, algorithm)
        
        # Nash Equilibrium (verificăm ÎNAINTE de MinMax pentru că ambele folosesc "joc"/"game")
        elif any(keyword in question for keyword in ["nash", "echilibru", "equilibrium", "matrice", "payoff", "formă normală", "normal form"]):
            problem_type = "Nash"
            
            # Extrage dimensiunile matricei
            numbers = re.findall(r'\d+', question)
            rows = int(numbers[0]) if len(numbers) > 0 else 3
            cols = int(numbers[1]) if len(numbers) > 1 else 3
            
            # Extrage matricea dacă e prezentă
            game_matrix = self._extract_game_matrix(question, rows, cols)
            
            self.parser_output.insert(tk.END, f"🔍 Detectat: Nash Equilibrium\n")
            self.parser_output.insert(tk.END, f"📊 Parametri: Joc {rows}×{cols}\n\n")
            self._solve_nash_internal(game_matrix, rows, cols)
        
        # MinMax Alpha-Beta
        elif any(keyword in question for keyword in ["minmax", "minimax", "alpha", "beta", "arbore", "tree"]):
            problem_type = "MinMax"
            
            # Extrage arborele din text
            tree = self._extract_minmax_tree(question)
            
            self.parser_output.insert(tk.END, f"🔍 Detectat: MinMax Alpha-Beta\n")
            self.parser_output.insert(tk.END, f"📊 Arbore: {tree}\n\n")
            self._solve_minmax_internal(tree)
        
        else:
            self.parser_output.insert(tk.END, "❌ Nu am putut detecta tipul de problemă!\n\n")
            self.parser_output.insert(tk.END, "Încearcă să folosești cuvinte cheie precum:\n")
            self.parser_output.insert(tk.END, "  • 'euristică' sau 'admisibilă' pentru Verificare Euristică\n")
            self.parser_output.insert(tk.END, "  • 'regine' sau 'queens' pentru N-Queens\n")
            self.parser_output.insert(tk.END, "  • 'colorare' sau 'graf' pentru Graph Coloring\n")
            self.parser_output.insert(tk.END, "  • 'minmax' sau 'alpha-beta' pentru MinMax\n")
            self.parser_output.insert(tk.END, "  • 'nash' sau 'echilibru' pentru Nash Equilibrium\n")
            self.parser_output.insert(tk.END, "  • 'sudoku' pentru Sudoku\n")
            self.parser_output.insert(tk.END, "  • 'joburi' sau 'mașini' pentru Job Scheduling\n")
            self.parser_output.insert(tk.END, "  • 'cale' sau 'path' sau 'A*' pentru Pathfinding\n")
    
    def _extract_number(self, text, default=8):
        """Extrage primul număr din text"""
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else default
    
    def _extract_edges(self, text):
        """Extrage muchii din format '0-1,1-2,2-3' sau '(0,1),(1,2)'"""
        # Format: 0-1,1-2
        match1 = re.search(r'(\d+-\d+(?:,\s*\d+-\d+)*)', text)
        if match1:
            return match1.group(1)
        
        # Format: (0,1),(1,2)
        coords = re.findall(r'\((\d+)\s*,\s*(\d+)\)', text)
        if coords:
            return ','.join([f"{a}-{b}" for a, b in coords])
        
        # Default
        return "0-1,1-2,2-3,3-4,4-5,5-0"
    
    def _extract_sudoku_grid(self, text):
        """Extrage grid Sudoku din text"""
        # Caută pattern-uri ca: "0 2 0 0, 0 0 0 3, 4 0 0 0, 0 0 1 0"
        # sau linii separate
        lines = text.split('\n')
        grid_lines = []
        
        for line in lines:
            # Caută linii cu 4 numere
            numbers = re.findall(r'\d+', line)
            if len(numbers) == 4:
                grid_lines.append(' '.join(numbers))
        
        if len(grid_lines) == 4:
            return '\n'.join(grid_lines)
        
        # Încearcă să găsești toate numerele și împarte-le în 4 linii
        all_numbers = re.findall(r'\d+', text)
        if len(all_numbers) >= 16:
            return '\n'.join([
                ' '.join(all_numbers[0:4]),
                ' '.join(all_numbers[4:8]),
                ' '.join(all_numbers[8:12]),
                ' '.join(all_numbers[12:16])
            ])
        
        # Default grid
        return "0 2 0 0\n0 0 0 3\n4 0 0 0\n0 0 1 0"
    
    def _extract_minmax_tree(self, text):
        """Extrage arbore MinMax din text - din liste sau din vizualizare"""
        import ast
        
        # Metoda 1: Caută liste Python explicite: [[1,2],[3,4]]
        list_pattern = r'\[[\[\],\-\d\s]+\]'
        matches = re.findall(list_pattern, text)
        
        for match in matches:
            try:
                tree = ast.literal_eval(match)
                if isinstance(tree, list) and len(tree) > 0:
                    return tree
            except:
                continue
        
        # Metoda 2: Parsează din vizualizare text "frunză: 0", "frunză: 6", etc.
        leaf_values = re.findall(r'frunz[ăa]:\s*(-?\d+)', text, re.IGNORECASE)
        
        if len(leaf_values) >= 4:
            # Convertește la int
            leaves = [int(v) for v in leaf_values]
            
            # Construiește arbore binar complet
            # Presupunem structura: nivel 0 (MAX) -> nivel 1 (MIN) -> nivel 2 (MAX) -> nivel 3 (frunze)
            
            if len(leaves) == 4:
                # Arbore simplu: 2 noduri MIN, fiecare cu 2 frunze
                return [[leaves[0], leaves[1]], [leaves[2], leaves[3]]]
            
            elif len(leaves) == 8:
                # Arbore complex: 2 noduri MIN, fiecare cu 2 noduri MAX, fiecare cu 2 frunze
                return [
                    [[leaves[0], leaves[1]], [leaves[2], leaves[3]]],
                    [[leaves[4], leaves[5]], [leaves[6], leaves[7]]]
                ]
            
            elif len(leaves) == 16:
                # Arbore foarte complex: 2->4->8->16
                return [
                    [
                        [[leaves[0], leaves[1]], [leaves[2], leaves[3]]],
                        [[leaves[4], leaves[5]], [leaves[6], leaves[7]]]
                    ],
                    [
                        [[leaves[8], leaves[9]], [leaves[10], leaves[11]]],
                        [[leaves[12], leaves[13]], [leaves[14], leaves[15]]]
                    ]
                ]
        
        # Default tree (arbore simplu 2 nivele)
        return [[[9, 7], [10, 1]], [[7, 6], [1, 5]]]
    
    def _extract_game_matrix(self, text, rows, cols):
        """Extrage matrice de joc pentru Nash"""
        # Caută perechi de numere (u1,u2)
        pairs = re.findall(r'\((-?\d+)\s*,\s*(-?\d+)\)', text)
        
        if len(pairs) >= rows * cols:
            matrix = []
            idx = 0
            for r in range(rows):
                row = []
                for c in range(cols):
                    if idx < len(pairs):
                        u1, u2 = int(pairs[idx][0]), int(pairs[idx][1])
                        row.append((u1, u2))
                        idx += 1
                matrix.append(row)
            return matrix
        
        # Încearcă să detecteze automat dimensiunile din perechi
        if pairs:
            # Numără câte perechi sunt per rând (caută pattern-uri "row X:")
            row_markers = re.findall(r'row\s+\d+', text.lower())
            col_markers = re.findall(r'col\s+\d+', text.lower())
            
            if row_markers and col_markers:
                detected_rows = len(row_markers)
                detected_cols = len(col_markers)
                
                if len(pairs) == detected_rows * detected_cols:
                    rows = detected_rows
                    cols = detected_cols
                    
                    matrix = []
                    idx = 0
                    for r in range(rows):
                        row = []
                        for c in range(cols):
                            u1, u2 = int(pairs[idx][0]), int(pairs[idx][1])
                            row.append((u1, u2))
                            idx += 1
                        matrix.append(row)
                    return matrix
        
        # Generează matrice random
        import random
        return [
            [(random.randint(-5, 5), random.randint(-5, 5)) for _ in range(cols)]
            for _ in range(rows)
        ]
    
    # Wrapper methods care folosesc codul existent
    def _solve_n_queens_internal(self, n, algorithm):
        """Wrapper pentru solve_n_queens care scrie în parser_output"""
        original_output = self.solver_output
        self.solver_output = self.parser_output
        self.solve_n_queens(n, algorithm)
        self.solver_output = original_output
    
    def _solve_graph_coloring_internal(self, nodes, edges_str, algorithm):
        """Wrapper pentru solve_graph_coloring"""
        original_output = self.solver_output
        self.solver_output = self.parser_output
        self.solve_graph_coloring(nodes, edges_str, algorithm)
        self.solver_output = original_output
    
    def _solve_sudoku_internal(self, grid_str, algorithm):
        """Wrapper pentru solve_sudoku"""
        original_output = self.solver_output
        self.solver_output = self.parser_output
        self.solve_sudoku(grid_str, algorithm)
        self.solver_output = original_output
    
    def _solve_job_scheduling_internal(self, machines, jobs, algorithm):
        """Wrapper pentru solve_job_scheduling"""
        original_output = self.solver_output
        self.solver_output = self.parser_output
        self.solve_job_scheduling(machines, jobs, algorithm)
        self.solver_output = original_output
    
    def _solve_pathfinding_internal(self, grid_size, start_str, goal_str, algorithm):
        """Wrapper pentru solve_pathfinding"""
        original_output = self.solver_output
        self.solver_output = self.parser_output
        self.solve_pathfinding(grid_size, start_str, goal_str, algorithm)
        self.solver_output = original_output
    
    def _solve_minmax_internal(self, tree):
        """Rezolvă MinMax Alpha-Beta"""
        from QTemplates import QTemplates
        
        self.parser_output.insert(tk.END, "📋 Problemă: MinMax cu Alpha-Beta Pruning\n\n")
        
        # Vizualizare arbore
        def visualize_tree(node, indent=0, node_type="MAX"):
            lines = []
            prefix = "  " * indent
            
            if isinstance(node, int):
                lines.append(f"{prefix}└─ Frunză: {node}")
            elif isinstance(node, list):
                lines.append(f"{prefix}├─ {node_type}")
                next_type = "MIN" if node_type == "MAX" else "MAX"
                for child in node:
                    lines.extend(visualize_tree(child, indent + 1, next_type))
            
            return lines
        
        tree_viz = visualize_tree(tree)
        self.parser_output.insert(tk.END, "Structura arborelui:\n")
        for line in tree_viz:
            self.parser_output.insert(tk.END, line + "\n")
        
        self.parser_output.insert(tk.END, "\n")
        
        # Calculează MinMax
        qt = QTemplates('QTemplates.json')
        result = qt.solve_minmax_alpha_beta({"tree": tree})
        
        root_value = result["root_value"]
        leaf_count = result["leaf_count"]
        
        # Calculează total frunze
        def count_leaves(node):
            if isinstance(node, int):
                return 1
            elif isinstance(node, list):
                return sum(count_leaves(child) for child in node)
            return 0
        
        total_leaves = count_leaves(tree)
        
        self.parser_output.insert(tk.END, "✅ REZULTAT:\n\n")
        self.parser_output.insert(tk.END, f"📊 Valoare în rădăcină: {root_value}\n")
        self.parser_output.insert(tk.END, f"🍃 Frunze vizitate: {leaf_count}\n")
        self.parser_output.insert(tk.END, f"🌳 Total frunze: {total_leaves}\n")
        self.parser_output.insert(tk.END, f"✂️  Frunze tăiate (pruning): {total_leaves - leaf_count}\n")
    
    def _solve_nash_internal(self, game_matrix, rows, cols):
        """Rezolvă Nash Equilibrium"""
        self.parser_output.insert(tk.END, "📋 Problemă: Nash Equilibrium (Joc în formă normală)\n\n")
        
        # Afișează matricea
        self.parser_output.insert(tk.END, "Matricea jocului (Player 1 = rânduri, Player 2 = coloane):\n")
        self.parser_output.insert(tk.END, "     ")
        for j in range(cols):
            self.parser_output.insert(tk.END, f"  Col {j}  ")
        self.parser_output.insert(tk.END, "\n")
        
        for i in range(rows):
            self.parser_output.insert(tk.END, f"Row {i}: ")
            for j in range(cols):
                u1, u2 = game_matrix[i][j]
                self.parser_output.insert(tk.END, f"({u1:2},{u2:2})  ")
            self.parser_output.insert(tk.END, "\n")
        
        self.parser_output.insert(tk.END, "\n")
        
        # Găsește echilibre Nash pure
        def find_pure_nash(game):
            equilibria = []
            
            # Calculează best responses
            best_u1 = [max(game[i][j][0] for i in range(rows)) for j in range(cols)]
            best_u2 = [max(game[i][j][1] for j in range(cols)) for i in range(rows)]
            
            for i in range(rows):
                for j in range(cols):
                    u1, u2 = game[i][j]
                    if u1 == best_u1[j] and u2 == best_u2[i]:
                        equilibria.append((i, j))
            
            return equilibria
        
        equilibria = find_pure_nash(game_matrix)
        
        if equilibria:
            self.parser_output.insert(tk.END, "✅ DA - Există echilibru Nash pur!\n\n")
            self.parser_output.insert(tk.END, f"Echilibre Nash găsite: {len(equilibria)}\n\n")
            for i, j in equilibria:
                payoff = game_matrix[i][j]
                self.parser_output.insert(tk.END, f"  • Poziția ({i}, {j}) → Payoff {payoff}\n")
        else:
            self.parser_output.insert(tk.END, "❌ NU - Nu există echilibru Nash pur în acest joc.\n")
    
    def _solve_heuristics_internal(self, check_type):
        """Rezolvă verificare euristică (admisibilitate/consistență)"""
        from new_question import HeuristicQuestionGenerator
        
        self.parser_output.insert(tk.END, "📋 Problemă: Verificare Euristică\n")
        self.parser_output.insert(tk.END, f"🎯 Tip verificare: {'Admisibilitate' if check_type == 'admissible' else 'Consistență (Monotonie)'}\n\n")
        
        # Generează un graf și euristică
        gen = HeuristicQuestionGenerator()
        
        # Forțează tipul de euristică dorit
        if check_type == "admissible":
            graph_data = gen.generate_graph(force_admissible=True, force_consistent=False)
        else:
            graph_data = gen.generate_graph(force_admissible=True, force_consistent=True)
        
        nodes = graph_data['nodes']
        edges = graph_data['edges']
        heuristic = graph_data['heuristic']
        goal = graph_data['goal_node']
        real_costs = graph_data['real_costs']
        
        # Afișează graful
        self.parser_output.insert(tk.END, f"Graf generat cu {len(nodes)} noduri: {', '.join(nodes)}\n")
        self.parser_output.insert(tk.END, f"Nod scop: {goal}\n\n")
        
        self.parser_output.insert(tk.END, "Muchii (cu costurile asociate):\n")
        for edge in edges:
            self.parser_output.insert(tk.END, f"  {edge['from']} → {edge['to']}: cost = {edge['cost']}\n")
        
        self.parser_output.insert(tk.END, f"\nEuristică h(n):\n")
        for node in nodes:
            self.parser_output.insert(tk.END, f"  h({node}) = {heuristic[node]}\n")
        
        self.parser_output.insert(tk.END, f"\nCosturi reale h*(n) (calculate cu Dijkstra):\n")
        for node in nodes:
            cost = real_costs.get(node, float('inf'))
            cost_str = str(cost) if cost != float('inf') else "∞"
            self.parser_output.insert(tk.END, f"  h*({node}) = {cost_str}\n")
        
        self.parser_output.insert(tk.END, "\n" + "=" * 60 + "\n\n")
        
        # Verifică admisibilitatea
        if check_type == "admissible":
            is_admissible = gen.check_admissibility(graph_data)
            
            self.parser_output.insert(tk.END, "🔍 VERIFICARE ADMISIBILITATE:\n")
            self.parser_output.insert(tk.END, "Condiție: h(n) ≤ h*(n) pentru toate nodurile\n\n")
            
            all_valid = True
            for node in nodes:
                h_val = heuristic[node]
                h_star = real_costs.get(node, float('inf'))
                is_valid = h_val <= h_star if h_star != float('inf') else True
                
                status = "✓" if is_valid else "✗"
                self.parser_output.insert(tk.END, f"  {status} {node}: h({node})={h_val} {'≤' if is_valid else '>'} h*({node})={h_star}\n")
                
                if not is_valid:
                    all_valid = False
            
            self.parser_output.insert(tk.END, f"\n{'✅ DA' if is_admissible else '❌ NU'} - Euristica {'ESTE' if is_admissible else 'NU ESTE'} admisibilă.\n")
        
        # Verifică consistența
        else:
            is_consistent = gen.check_consistency(graph_data)
            
            self.parser_output.insert(tk.END, "🔍 VERIFICARE CONSISTENȚĂ (MONOTONIE):\n")
            self.parser_output.insert(tk.END, "Condiție: h(n) ≤ cost(n,n') + h(n') pentru toate muchiile\n\n")
            
            all_valid = True
            for edge in edges:
                n1 = edge['from']
                n2 = edge['to']
                cost = edge['cost']
                h1 = heuristic[n1]
                h2 = heuristic[n2]
                
                is_valid = h1 <= cost + h2
                status = "✓" if is_valid else "✗"
                
                self.parser_output.insert(tk.END, f"  {status} {n1}→{n2}: h({n1})={h1} {'≤' if is_valid else '>'} {cost}+{h2}={cost+h2}\n")
                
                if not is_valid:
                    all_valid = False
                
                # Verifică și în sens invers
                is_valid_reverse = h2 <= cost + h1
                status_reverse = "✓" if is_valid_reverse else "✗"
                self.parser_output.insert(tk.END, f"  {status_reverse} {n2}→{n1}: h({n2})={h2} {'≤' if is_valid_reverse else '>'} {cost}+{h1}={cost+h1}\n")
                
                if not is_valid_reverse:
                    all_valid = False
            
            self.parser_output.insert(tk.END, f"\n{'✅ DA' if is_consistent else '❌ NU'} - Euristica {'ESTE' if is_consistent else 'NU ESTE'} consistentă.\n")


if __name__ == "__main__":
    AIQuestionsGUI().mainloop()
