import time
import random

def dfs(problem, problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.01, 0.05))  # simulează timp de execuție
    return {"result": "path found", "time": time.time() - start}

def bfs(problem, problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.02, 0.06))
    return {"result": "path found", "time": time.time() - start}

def a_star(problem, problem_instance):
    start = time.time()
    time.sleep(random.uniform(0.005, 0.02))
    return {"result": "optimal path", "time": time.time() - start}
