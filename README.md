# AI Question Generator 🤖

Generator automat de întrebări pentru examenele de Inteligență Artificială, cu suport pentru multiple categorii de probleme și evaluare automată.

## ✨ Funcționalități

### 🎯 Generare Automată de Întrebări
- **5+ Categorii de probleme**: Search, CSP, MinMax, Nash Equilibrium, Heuristics
- **Template-uri multilingve**: Suport pentru română și engleză
- **Parametri randomizați**: Fiecare întrebare este unică
- **Evaluare strategii**: Clasificare automată a algoritmilor optimi

### 🖥️ Interfață Grafică (GUI)
- Aplicație desktop cu Tkinter
- Selectare categorii și configurare parametri
- Verificare răspunsuri în timp real
- Afișare scoruri și feedback instantaneu

### 📝 Mod Consola (CLI)
- Generare batch de întrebări
- Export în fișiere text
- Salvare strategii și răspunsuri
- Evaluare automată cu scoring

### 🧩 Tipuri de Probleme Suportate

#### 1. **Search Problems** (Categoria 1)
- **Hanoi Towers**: Probleme de transfer de discuri
- **DFS Maze**: Explorare labirinturi
- **A* Route Planning**: Planificare rute cu euristici
- **Beam Search**: Alocare resurse cu beam width
- **8-Puzzle**: Puzzle glisant 3×3
- **Knight's Tour**: Parcurgerea tablei de șah

#### 2. **Constraint Satisfaction (CSP)** (Categoria 2)
- **N-Queens**: Poziționare regine pe tablă
- **Graph Coloring**: Colorare grafuri
- **Job Scheduling**: Planificare sarcini pe mașini
- **Sudoku**: Puzzle logic 9×9
- Suport pentru:
  - Backtracking
  - Forward Checking
  - Arc Consistency (AC-3)
  - MRV (Minimum Remaining Values)

#### 3. **Adversarial Search (Game)** (Categoria 3)
- **MinMax cu Alpha-Beta Pruning**
- Arbori de joc cu nivele MAX/MIN
- Calculare automată a valorii rădăcinii
- Contorizare frunze vizitate vs. tăiate (pruning)

#### 4. **Game Theory** (Categoria 4)
- **Nash Equilibrium**
- Jocuri în formă normală (matrice de payoff)
- Detectare echilibre Nash pure
- Suport pentru jocuri m×n

#### 5. **Heuristics** (Categoria 5)
- **Admisibilitate**: Verificare h(n) ≤ h*(n)
- **Consistență**: Verificare h(n) ≤ c(n,n') + h(n')
- Generare grafuri aleatorii cu costuri reale (Dijkstra)

---

## 📦 Instalare

### Cerințe
- Python 3.8+
- Tkinter (inclus în majoritatea distribuțiilor Python)

### Pași

1. **Clonează repository-ul**
```bash
git clone https://github.com/comshiro/AI-2025.git
cd AI-2025/QuestionGeneration
```

2. **Instalează dependențele** (dacă este necesar)
```bash
pip install -r requirements.txt
```
*Notă: Proiectul folosește doar biblioteci standard Python (tkinter, random, heapq)*

---

## 🚀 Utilizare

### 🖥️ Mod GUI (Recomandat)

```bash
python gui_app.py
```

**Pași:**
1. Selectează categoria de întrebări (1-5 sau Mixed)
2. Setează numărul de întrebări (1-20)
3. Alege limba (ro/en)
4. Click pe "Generează test"
5. Răspunde la întrebări și verifică scorul

### 📝 Mod CLI

```bash
python generate_questions.py
```

**Interacțiune:**
```
Alege tipurile de întrebări:
1 = Search problems
2 = CSP
3 = Game problems (MinMax)
4 = Nash Equilibrium
5 = Heuristics

Introduceți categoriile (ex: 1,2,3,4,5 sau 5): 1,3
Număr de întrebări: 5
Limba (ro/en) [implicit: ro]: ro
Seed aleator (Enter pentru random): 
Nume fișier [implicit: questions.txt]: my_test.txt
```

**Fișiere generate:**
- `questions.txt` - Întrebările generate
- `strategies.txt` - Răspunsurile corecte și strategiile
- `raspunsuri.txt` - Răspunsurile tale și scorurile

---

## 📂 Structura Proiectului

```
QuestionGeneration/
├── gui_app.py                    # Aplicație GUI (Tkinter)
├── generate_questions.py         # Generator principal + CLI
├── QTemplates.py                 # Sistem de template-uri
├── QTemplates.json               # Definiții probleme
├── new_question.py               # Generator euristici
├── evaluate_strategies.py        # Evaluare strategii CSP/Search
├── algorithm_runners/            # Algoritmi de rezolvare
│   ├── __init__.py
│   ├── csp_algorithms.py        # Backtracking, FC, AC-3
│   └── search_algorithms.py     # DFS, BFS, A*
├── questions.txt                 # Output: întrebări
├── strategies.txt                # Output: răspunsuri
├── raspunsuri.txt                # Output: evaluare utilizator
└── README.md                     # Acest fișier
```

---

## 🔧 Configurare

### Modificarea Template-urilor

Editează `QTemplates.json` pentru a adăuga/modifica probleme:

```json
{
  "problems": {
    "My Custom Problem": {
      "title": "MyProblem",
      "category": "search",
      "templates": {
        "ro": ["Întrebarea în română cu {param}"],
        "en": ["Question in English with {param}"]
      },
      "param_types": {
        "param": {"type": "randint", "min": 1, "max": 10}
      },
      "strategies": ["Algorithm1", "Algorithm2"],
      "types": ["search", "planning"]
    }
  }
}
```

### Tipuri de Parametri Suportați

- `randint`: Număr întreg aleatoriu în interval
- `choice`: Selecție dintr-o listă
- `fixed`: Valoare constantă
- `custom`: Funcție Python personalizată

---

## 📊 Exemple

### Exemplu 1: Generare MinMax

**Întrebare:**
```
Se dă un arbore de joc în care nivelurile alternează între MAX și MIN.
Aplicând MinMax cu Alpha-Beta, care este valoarea finală din rădăcină 
și câte noduri frunză sunt evaluate?

Arborele:
├─ MAX
  ├─ MIN
    ├─ MAX
      └─ Frunză: 9
      └─ Frunză: 7
    ├─ MAX
      └─ Frunză: 10
      └─ Frunză: 1
  ├─ MIN
    ├─ MAX
      └─ Frunză: 7
      └─ Frunză: 6
    ├─ MAX
      └─ Frunză: 1
      └─ Frunză: 5
```

**Răspuns Corect:**
- Valoare rădăcină: 9
- Frunze vizitate: 5 (din 8 total)
- Frunze tăiate (pruning): 3

---

### Exemplu 2: Nash Equilibrium

**Întrebare:**
```
Pentru jocul dat în formă normală, există echilibru Nash pur?

Matricea jocului:
     Col 0   Col 1   Col 2
Row 0: ( 3, 2)  (-1, 4)  ( 5,-2)
Row 1: ( 1, 3)  ( 4, 1)  ( 2, 5)
Row 2: (-2, 0)  ( 3, 2)  ( 1, 3)
```

**Răspuns:**
DA. Echilibru Nash pur: (1, 1) → payoff (4, 1)

---

### Exemplu 3: CSP cu Forward Checking

**Întrebare:**
```
Având variabilele [X1, X2, X3, X4], domeniile {X1:[1,2,3], ...},
constrângerile [X1 != X2, X1 < X3, X2 < X4, X3 < X4],
și asignarea parțială {X1: 1}, determinați asignarea finală 
folosind Backtracking cu Forward Checking.
```

**Răspuns:**
`{X1: 1, X2: 2, X3: 3, X4: 4}`

## 🤝 Contribuții

Contribuțiile sunt binevenite! Pentru a adăuga noi tipuri de probleme:

1. Adaugă definiția în `QTemplates.json`
2. Implementează funcția de generare parametri în `QTemplates.py`
3. Actualizează logica de scoring în `generate_questions.py` și `gui_app.py`