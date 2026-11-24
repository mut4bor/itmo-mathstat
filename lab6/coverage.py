from pathlib import Path

from interval import DISTRIBUTIONS, studentInterval

N = 10**3
Q = 0.95
sampleSizes = [10, 20, 30, 50, 60]
OUTPUT = Path(__file__).with_suffix(".md")

markdown = ["# Доля интервалов, содержащих математическое ожидание", ""]

for title, draw, trueMean in DISTRIBUTIONS:
    print(f"{title}, Q = {Q}, N = {N}")
    print(f"{'n':>4} {'covered':>8} {'Q*':>7}")
    markdown.append(f"## {title}, Q = {Q}, N = {N}")
    markdown.append("")
    markdown.append("| n | covered | Q* |")
    markdown.append("|---|---|---|")
    for n in sampleSizes:
        lower, upper = studentInterval(draw((N, n)), Q)
        covered = ((lower <= trueMean) & (trueMean <= upper)).sum()
        print(f"{n:>4} {covered:>8} {covered / N:>7.3f}")
        markdown.append(f"| {n} | {covered} | {covered / N:.3f} |")
    print()
    markdown.append("")

OUTPUT.write_text("\n".join(markdown), encoding="utf-8")
print(f"Saved to {OUTPUT}")
