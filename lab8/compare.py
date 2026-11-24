from pathlib import Path

from clopperPearson import METHODS

Q = 0.95
CASES = [(10, 0), (10, 1), (10, 5), (10, 9), (10, 10)] + [
    (100, 0),
    (100, 1),
    (100, 10),
    (100, 50),
    (100, 90),
    (100, 99),
    (100, 100),
]
OUTPUT = Path(__file__).with_suffix(".md")


def formatInterval(lower, upper):
    return f"[{lower:.4f}, {upper:.4f}]"


markdown = [f"# Доверительные интервалы для вероятности, Q = {Q}", ""]
markdown.append("| n | m | " + " | ".join(name for name, _ in METHODS) + " |")
markdown.append("|" + "---|" * (2 + len(METHODS)))

for n, m in CASES:
    intervals = [formatInterval(*interval(m, n, Q)) for _, interval in METHODS]
    print(f"n = {n}, m = {m}")
    for (name, _), interval in zip(METHODS, intervals):
        print(f"  {name:>18} {interval}")
    markdown.append(f"| {n} | {m} | " + " | ".join(intervals) + " |")

markdown.append("")
OUTPUT.write_text("\n".join(markdown), encoding="utf-8")
print(f"Saved to {OUTPUT}")
