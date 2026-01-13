import random
import heapq
from collections import defaultdict

class HeuristicQuestionGenerator:
    def __init__(self):
        self.questions = []
    
    def dijkstra(self, nodes, edges, goal):
        graph = defaultdict(list)
        for edge in edges:
            graph[edge['to']].append((edge['from'], edge['cost']))
            graph[edge['from']].append((edge['to'], edge['cost']))
        
        distances = {node: float('inf') for node in nodes}
        distances[goal] = 0
        pq = [(0, goal)]
        visited = set()
        
        while pq:
            curr_dist, curr_node = heapq.heappop(pq)
            
            if curr_node in visited:
                continue
            visited.add(curr_node)
            
            for neighbor, cost in graph[curr_node]:
                new_dist = curr_dist + cost
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return distances
    
    def generate_graph(self, force_admissible=None, force_consistent=None):
        """Generează un graf aleatoriu cu euristică."""
        num_nodes = random.randint(6, 8)
        nodes = [chr(65 + i) for i in range(num_nodes)]
        goal_node = nodes[-1]
        edges = []
        
        # Generăm muchii pentru a asigura conectivitatea
        for i in range(num_nodes - 1):
            cost = random.randint(1, 5)
            edges.append({
                'from': nodes[i],
                'to': nodes[i + 1],
                'cost': cost
            })
            
            # Adăugăm câteva muchii suplimentare
            if random.random() > 0.5 and i < num_nodes - 2:
                target_idx = random.randint(i + 2, num_nodes - 1)
                cost = random.randint(2, 6)
                edges.append({
                    'from': nodes[i],
                    'to': nodes[target_idx],
                    'cost': cost
                })
        
        # Calculăm costurile reale
        real_costs = self.dijkstra(nodes, edges, goal_node)
        
        # Determinăm ce proprietăți să aibă euristica
        if force_admissible is None:
            is_admissible = random.random() > 0.5
        else:
            is_admissible = force_admissible
            
        if force_consistent is None:
            is_consistent = is_admissible and random.random() > 0.4
        else:
            is_consistent = force_consistent
            if is_consistent:
                is_admissible = True  # Consistentă implică admisibilă
        
        heuristic = {}
        for node in nodes:
            if node == goal_node:
                heuristic[node] = 0
            else:
                real_cost = real_costs[node]
                if is_admissible:
                    heuristic[node] = max(0, real_cost - random.randint(0, 2))
                else:
                    if random.random() > 0.6:
                        heuristic[node] = real_cost + random.randint(1, 3)
                    else:
                        heuristic[node] = max(0, real_cost - random.randint(0, 2))
        
        # Dacă vrem consistentă, trebuie să ajustăm manual
        if is_consistent:
            # Regenerăm euristica pentru a fi sigur consistentă
            heuristic = self.generate_consistent_heuristic(nodes, edges, goal_node, real_costs)
        
        return {
            'nodes': nodes,
            'edges': edges,
            'heuristic': heuristic,
            'goal_node': goal_node,
            'real_costs': real_costs
        }
    
    def generate_consistent_heuristic(self, nodes, edges, goal, real_costs):
        """Generează o euristică garantat consistentă."""
        heuristic = {}
        for node in nodes:
            if node == goal:
                heuristic[node] = 0
            else:
                # Pentru a fi consistentă, luăm o fracțiune din costul real
                heuristic[node] = max(0, int(real_costs[node] * random.uniform(0.5, 0.9)))
        return heuristic
    
    def check_admissibility(self, graph_data):
        """Verifică dacă euristica este admisibilă."""
        heuristic = graph_data['heuristic']
        real_costs = graph_data['real_costs']
        
        for node in graph_data['nodes']:
            if heuristic[node] > real_costs[node]:
                return False
        return True
    
    def check_consistency(self, graph_data):
        """Verifică dacă euristica este consistentă."""
        heuristic = graph_data['heuristic']
        edges = graph_data['edges']
        
        for edge in edges:
            from_node = edge['from']
            to_node = edge['to']
            cost = edge['cost']
            
            h_from = heuristic[from_node]
            h_to = heuristic[to_node]
            
            # Verificăm h(n) <= cost(n, n') + h(n')
            if h_from > cost + h_to:
                return False
            
            # Verificăm și în cealaltă direcție
            if h_to > cost + h_from:
                return False
        
        return True
    
    def format_question(self, graph_data, question_type):
        """Formatează întrebarea în text."""
        nodes = graph_data['nodes']
        edges = graph_data['edges']
        heuristic = graph_data['heuristic']
        goal = graph_data['goal_node']
        
        question = f"Considerăm un graf cu {len(nodes)} noduri: {', '.join(nodes)}\n"
        question += f"Nodul scop este: {goal}\n\n"
        question += "Muchiile grafului (cu costurile asociate):\n"
        for edge in edges:
            question += f"  {edge['from']} → {edge['to']}: cost = {edge['cost']}\n"
        
        question += "\nEuristica h(n) pentru fiecare nod:\n"
        for node in nodes:
            question += f"  h({node}) = {heuristic[node]}\n"
        
        question += "\n"
        if question_type == 'admissible':
            question += "Întrebare: Euristica h este admisibilă?"
        else:  # consistent
            question += "Întrebare: Euristica h este consistentă (monotonă)?"
        
        return question
    
    def generate_questions(self, num_questions=10):
        """Generează întrebări (jumătate admisibilitate, jumătate consistență)."""
        self.questions = []
        
        for i in range(num_questions):
            # Alternăm între întrebări de admisibilitate și consistență
            if i % 2 == 0:
                question_type = 'admissible'
            else:
                question_type = 'consistent'
            
            graph_data = self.generate_graph()
            question_text = self.format_question(graph_data, question_type)
            
            # Determinăm răspunsul
            if question_type == 'admissible':
                answer = "DA" if self.check_admissibility(graph_data) else "NU"
            else:
                answer = "DA" if self.check_consistency(graph_data) else "NU"
            
            self.questions.append({
                'question': question_text,
                'answer': answer,
                'type': question_type,
                'graph_data': graph_data
            })
        
        return self.questions
    
    def print_questions(self):
        """Afișează toate întrebările cu răspunsurile."""
        for i, q in enumerate(self.questions, 1):
            print(f"ÎNTREBAREA {i}")
            print(q['question'])
            print(f"\nRăspuns: {q['answer']}")
            print()
    
    def save_to_file(self, filename='euristici_intrebari.txt'):
        """Salvează întrebările în fișier."""
        with open(filename, 'w', encoding='utf-8') as f:
            for i, q in enumerate(self.questions, 1):
                f.write(f"{'='*70}\n")
                f.write(f"ÎNTREBAREA {i}\n")
                f.write(f"{'='*70}\n\n")
                f.write(q['question'])
                f.write(f"\n\nRăspuns: {q['answer']}\n\n")
        
    
    def get_question_answer_pairs(self):
        """Returnează perechi (întrebare, răspuns) pentru evaluare."""
        return [(q['question'], q['answer']) for q in self.questions]


# Exemplu de utilizare
if __name__ == "__main__":
    generator = HeuristicQuestionGenerator()
    
    # Generează 10 întrebări (5 admisibilitate, 5 consistență)
    questions = generator.generate_questions(10)
    
    # Afișează toate întrebările
    generator.print_questions()
    
    # Salvează în fișier
    generator.save_to_file('euristici_intrebari.txt')
  