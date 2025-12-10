import json
import random
import itertools
from collections import deque


class QTemplates:
    def __init__(self, json_file_path):
        """Initialize the QTemplates with JSON file."""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.search_problems = self.data['search_problems']

    def generate_params(self, param_types):
        """Generate actual parameter values based on param_types specification."""
        params = {}
        for param_name, param_config in param_types.items():
            param_type = param_config['type']
            if param_type == 'choice':
                params[param_name] = random.choice(param_config['values'])
            elif param_type == 'randint':
                params[param_name] = random.randint(param_config['min'], param_config['max'])
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

        return None

    def get_problem_names(self):
        """Get list of all available problem names."""
        return list(self.search_problems.keys())

    def get_problem(self, problem_name):
        """Get a specific problem by name."""
        return self.search_problems.get(problem_name)

    def generate_question(self, problem_name, language='en', template_index=None):
        """Generate a question with substituted parameters."""
        if problem_name not in self.search_problems:
            raise ValueError(f"Problem '{problem_name}' not found")
        problem = self.search_problems[problem_name]
        params = self.generate_params(problem['param_types'])
        if problem_name == 'Graph Coloring':
            params['m'] = len(params['edges'])
        templates = problem['templates'][language]
        if template_index is None:
            template_index = random.randint(0, len(templates) - 1)
        elif template_index >= len(templates):
            template_index = 0
        template = templates[template_index]
        question = template.format(**params)
        return {
            'question': question,
            'problem_name': problem_name,
            'title': problem['title'],
            'params': params,
            'strategies': problem['strategies'],
            'types': problem['types'],
            'language': language,
            'template_index': template_index
        }

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

# Conversie legacy format (pentru generate_questions.py)
def convert_to_legacy_format():
    qt = QTemplates('QTemplates.json')
    legacy_problems = {}
    for name, problem in qt.search_problems.items():
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
            'types': problem['types']
        }
    return legacy_problems

# Modul-level variable pentru backward compatibility
try:
    search_problems = convert_to_legacy_format()
except Exception as e:
    print(f"Warning: Could not load search_problems: {e}")
    search_problems = {}
