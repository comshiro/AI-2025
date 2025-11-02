import time
import random

# Mock pentru Backtracking
def backtracking(problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.01, 0.05))  # simulare timp execuție
    return {"result": "backtracking done", "time": time.time() - start}

# Mock pentru Forward Checking
def forward_checking(problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.02, 0.06))
    return {"result": "forward checking done", "time": time.time() - start}

# Mock pentru Arc Consistency
def arc_consistency(problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.01, 0.03))
    return {"result": "arc consistency done", "time": time.time() - start}

# Mock pentru Min-Conflicts Heuristic
def min_conflicts(problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.005, 0.02))
    return {"result": "min conflicts done", "time": time.time() - start}

# Mock pentru Hill-Climbing (CSP heuristic)
def hill_climbing(problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.01, 0.04))
    return {"result": "hill climbing done", "time": time.time() - start}

# Warnsdorff's Heuristic (de obicei pentru Knight's Tour)
def warnsdorff(problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.005, 0.03))
    return {"result": "warnsdorff done", "time": time.time() - start}
