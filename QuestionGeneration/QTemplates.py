import json
import random
from collections import deque


class QTemplates:
    def __init__(self, json_file_path):
        """Initialize the QTemplates with JSON file."""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # ATENȚIE: cheia din JSON trebuie să fie 'search_problems'
        # Dacă în fișier este 'problems', schimbă aici în consecință.

        self.search_problems = {}

        if 'problems' in self.data:
            self.search_problems.update(self.data['problems'])
        
        if 'search_problems' in self.data:
            self.search_problems.update(self.data['search_problems'])
            

    # ============================================================
    # PARAM GENERATION
    # ============================================================
    def generate_params(self, param_types):
        """Generate actual parameter values based on param_types specification."""
        params = {}
        for param_name, param_config in param_types.items():
            param_type = param_config['type']

            if param_type == 'choice':
                params[param_name] = random.choice(param_config['values'])

            elif param_type == 'randint':
                params[param_name] = random.randint(
                    param_config['min'], param_config['max']
                )

            elif param_type == 'fixed':
                params[param_name] = param_config['value']

            elif param_type == 'custom':
                function_name = param_config['function']
                params[param_name] = self._call_custom_function(function_name, params)

        return params

    def _call_custom_function(self, function_name, existing_params):
        """Call custom parameter generation functions."""

        if function_name == 'graph_edges':
            n = existing_params.get('n', random.randint(4, 8))
            edges = []
            for i in range(n):
                for j in range(i + 1, n):
                    if random.random() < 0.4:
                        edges.append([i, j])
            return edges

        elif function_name == 'puzzle_state':
            state = list(range(9))
            random.shuffle(state)
            return state

        elif function_name == 'goal_state':
            return list(range(1, 9)) + [0]

        elif function_name == 'sudoku_grid':
            n = existing_params.get('n', 9)
            sqrt_n = int(n ** 0.5)
            grid = [[0 for _ in range(n)] for _ in range(n)]

            def fill_diagonal_blocks():
                for block_row in range(0, n, sqrt_n):
                    nums = list(range(1, n + 1))
                    random.shuffle(nums)
                    idx = 0
                    for i in range(block_row, block_row + sqrt_n):
                        for j in range(block_row, block_row + sqrt_n):
                            grid[i][j] = nums[idx]
                            idx += 1

            def is_safe(row, col, num):
                for j in range(n):
                    if grid[row][j] == num:
                        return False
                for i in range(n):
                    if grid[i][col] == num:
                        return False
                start_row = row - row % sqrt_n
                start_col = col - col % sqrt_n
                for i in range(sqrt_n):
                    for j in range(sqrt_n):
                        if grid[i + start_row][j + start_col] == num:
                            return False
                return True

            fill_diagonal_blocks()
            attempts = 0
            filled_cells = n * sqrt_n

            while filled_cells < n * n * 0.3 and attempts < 100:
                row = random.randint(0, n - 1)
                col = random.randint(0, n - 1)
                if grid[row][col] == 0:
                    num = random.randint(1, n)
                    if is_safe(row, col, num):
                        grid[row][col] = num
                        filled_cells += 1
                attempts += 1

            grid_lines = [" ".join(str(cell) for cell in row) for row in grid]
            return "\n".join(grid_lines)

        elif function_name == 'minmax_tree':
            """
            Generează un arbore MinMax aleatoriu.
            Structură: [[frunze_subarbore1], [frunze_subarbore2], ...]
            """
            # Generam un arbore binar complet
            # Nivel 0: radacina (MAX)
            # Nivel 1: 2 noduri (MIN)
            # Nivelul 2: 4 noduri (MAX)
            # Nivelul 3: 8 frunze (valori)
            
            # Optiunea 1: Arbore fix cu 8 frunze (ca in exemplu)
            num_leaves = 8
            leaves = [random.randint(-1, 10) for _ in range(num_leaves)]

            # Construim arborele de jos in sus
            # Nivelul 3 : 8 frunze grupate cate 2
            level_2 = []
            for i in range(0, len(leaves), 2):
                level_2.append([leaves[i], leaves[i + 1]])
            
            # Nivelul 1: grupam level_2 cate 2
            level_1 = []
            for i in range(0, len(level_2), 2):
                level_1.append([level_2[i], level_2[i + 1]])

            # Radacina: grupam level_1
            tree = level_1

            return tree

        return None
    def _minmax_alpha_beta_with_count(self, node, maximizing, alpha, beta):
        """
        Returnează un tuple: (valoare_MinMax, număr_frunze_vizitate)
        """
        # Frunză numerică
        if isinstance(node, int):
            return node, 1

        # Nod MAX
        if maximizing:
            value = float("-inf")
            visited = 0
            for child in node:
                child_value, child_visited = self._minmax_alpha_beta_with_count(
                    child, False, alpha, beta
                )
                visited += child_visited
                value = max(value, child_value)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, visited

        # Nod MIN
        else:
            value = float("inf")
            visited = 0
            for child in node:
                child_value, child_visited = self._minmax_alpha_beta_with_count(
                    child, True, alpha, beta
                )
                visited += child_visited
                value = min(value, child_value)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value, visited

    def solve_minmax_alpha_beta(self, params):
        tree = params["tree"]
        value, leaves = self._minmax_alpha_beta_with_count(
            tree, True, float("-inf"), float("inf")
        )
        return {
            "root_value": value,
            "leaf_count": leaves
        }

    # ============================================================
    # QUESTION GENERATION (direct, nu legacy)
    # ============================================================
    def generate_question(self, problem_name, language='en', template_index=None):
        if problem_name not in self.search_problems:
            raise ValueError(f"Problem '{problem_name}' not found")

        problem = self.search_problems[problem_name]
        params = self.generate_params(problem['param_types'])

        # Adaptare pentru Graph Coloring
        if problem_name == 'Graph Coloring':
            params['m'] = len(params['edges'])

        templates = problem['templates'][language]
        if template_index is None:
            template_index = random.randint(0, len(templates) - 1)
        elif template_index >= len(templates):
            template_index = 0

        template = templates[template_index]
        question = template.format(**params)

        # Answer (doar pentru MinMax aici, dacă vrei)
        answer = None
        if problem['title'] == "MinMax":
            answer = self.solve_minmax_alpha_beta(params)

        return {
            'question': question,
            'problem_name': problem_name,
            'title': problem['title'],
            'params': params,
            'answer': answer,
            'strategies': problem['strategies'],
            'types': problem['types'],
            'language': language,
            'template_index': template_index
        }

    # Helpers
    def get_problem_names(self):
        return list(self.search_problems.keys())

    def get_problem(self, problem_name):
        return self.search_problems.get(problem_name)

    def generate_random_question(self, language='en'):
        problem_name = random.choice(self.get_problem_names())
        return self.generate_question(problem_name, language)

    def generate_questions_by_type(self, problem_type, language='en', count=1):
        matching_problems = [
            name for name, problem in self.search_problems.items()
            if problem_type in problem['types']
        ]
        if not matching_problems:
            raise ValueError(f"No problems found with type '{problem_type}'")

        questions = []
        for _ in range(count):
            problem_name = random.choice(matching_problems)
            questions.append(self.generate_question(problem_name, language))
        return questions


# ============================================================
# LEGACY FORMAT (pentru generate_questions.py)
# ============================================================
def convert_to_legacy_format():
    qt = QTemplates('QTemplates.json')
    legacy_problems = {}

    for name, problem in qt.search_problems.items():
        # Sari peste aliasurile CSP generice, dacă există
        if name == "CSP" and "alias_for" in problem:
            continue

        def make_param_function(param_types):
            def param_function():
                return qt.generate_params(param_types)
            return param_function

        legacy_problems[name] = {
            'title': problem['title'],
            'templates': problem['templates'],
            'params': make_param_function(problem['param_types']),
            'strategies': problem['strategies'],
            'types': problem['types'],
            'category': problem.get('category')  # IMPORTANT pentru filtrarea pe categorie
        }

    return legacy_problems


try:
    search_problems = convert_to_legacy_format()
except Exception as e:
    print(f"Warning: Could not load search_problems: {e}")
    search_problems = {}
