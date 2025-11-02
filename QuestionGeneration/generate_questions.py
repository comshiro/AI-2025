"""Generate question instances from templates in QTemplates.py.

Usage examples:
    python generate_questions.py --count 5
    python generate_questions.py --count 3 --format json --out questions.json
    python generate_questions.py --count 10 --problems "N-Queens,8-Puzzle" --seed 42

The script finds `QTemplates.py` in the same directory and uses its `search_problems` dict.
"""
import argparse
import json
import csv
import random
import sys
from pathlib import Path

# Make sure the script can import QTemplates located in the same folder
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    import QTemplates
except Exception as e:
    print("Failed to import QTemplates.py from the script directory:", e)
    raise

search_problems = getattr(QTemplates, "search_problems", None)
if search_problems is None:
    raise RuntimeError("QTemplates.py does not define `search_problems`")


def generate_one(name, entry):
    """Generate one question dict for a given template entry."""
    # entry['params'] is expected to be a callable returning a dict
    params_fn = entry.get("params")
    params = params_fn() if callable(params_fn) else {}
    template = entry.get("template", "")
    try:
        text = template.format(**params)
    except Exception:
        # If formatting fails, fall back to the raw template and include params
        text = template + "\n(Params: {})".format(params)
    return {
        "title": name,
        "question": text,
        "params": params,
        "strategy": entry.get("strategy")
    }


def generate_questions(count=1, choices=None, seed=None):
    """Generate `count` questions. If `choices` is a list of problem names, pick from them.
    Otherwise use all available templates.
    """
    if seed is not None:
        random.seed(seed)

    available = list(search_problems.items())
    if choices:
        # filter by provided names (case-sensitive match)
        names = [s.strip() for s in ",".join(choices).split(",") if s.strip()]
        available = [(n, search_problems[n]) for n in names if n in search_problems]
        if not available:
            raise ValueError("None of the requested problem names were found in QTemplates.search_problems")

    results = []
    for _ in range(count):
        name, entry = random.choice(available)
        results.append(generate_one(name, entry))
    return results


def write_output(items, fmt="text", outpath=None):
    if outpath:
        outpath = Path(outpath)

    if fmt == "json":
        s = json.dumps(items, ensure_ascii=False, indent=2)
        if outpath:
            outpath.write_text(s, encoding="utf-8")
            print(f"Wrote {len(items)} questions to {outpath}")
        else:
            print(s)
    elif fmt == "csv":
        # Flatten to rows: title, question, strategy, params(JSON)
        if outpath:
            with outpath.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["title", "question", "strategy", "params"])
                for it in items:
                    writer.writerow([it["title"], it["question"], it.get("strategy"), json.dumps(it.get("params", {}), ensure_ascii=False)])
            print(f"Wrote {len(items)} questions to {outpath}")
        else:
            # print CSV to stdout
            writer = csv.writer(sys.stdout)
            writer.writerow(["title", "question", "strategy", "params"])
            for it in items:
                writer.writerow([it["title"], it["question"], it.get("strategy"), json.dumps(it.get("params", {}), ensure_ascii=False)])
    else:
        # plain text
        out_lines = []
        for i, it in enumerate(items, 1):
            out_lines.append(f"{i}. [{it['title']}] {it['question']}")
            if it.get("strategy"):
                out_lines.append(f"   Strategy: {it['strategy']}")
            out_lines.append("")
        out_text = "\n".join(out_lines)
        if outpath:
            outpath.write_text(out_text, encoding="utf-8")
            print(f"Wrote {len(items)} questions to {outpath}")
        else:
            print(out_text)


def main(argv=None):
    p = argparse.ArgumentParser(description="Generate questions from QTemplates.search_problems")
    p.add_argument("--count", "-c", type=int, default=5, help="How many questions to generate")
    p.add_argument("--format", "-f", choices=["text", "json", "csv"], default="text", help="Output format")
    p.add_argument("--out", "-o", help="Write output to file")
    p.add_argument("--problems", "-p", help="Comma-separated list of problem names to draw from (exact names)")
    p.add_argument("--seed", type=int, help="Random seed for reproducible generation")

    args = p.parse_args(argv)

    choices = None
    if args.problems:
        choices = [s.strip() for s in args.problems.split(",") if s.strip()]

    items = generate_questions(count=args.count, choices=choices, seed=args.seed)
    write_output(items, fmt=args.format, outpath=args.out)


if __name__ == "__main__":
    main()
