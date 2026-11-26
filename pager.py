"""Collect every figure passed to show() and display them in ONE window.

Use Left/Right arrow keys or the Prev/Next buttons to flip pages.
Usage in a lab script (import before matplotlib.pyplot):

    import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from pager import show
    ...
    show()   # instead of plt.show()
"""

import atexit
import tkinter as tk

import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.backends.backend_tkagg import (  # noqa: E402
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,
)

_figures = []
_registered = False


def show():
    global _registered
    for num in plt.get_fignums():
        _figures.append(plt.figure(num))
        plt.close(num)  # drop the per-figure window, keep the Figure object
    if not _registered:
        _registered = True
        atexit.register(_run)


def _run():
    if not _figures:
        return
    root = tk.Tk()
    root.title("Graphs")

    bar = tk.Frame(root)
    bar.pack(side=tk.BOTTOM, fill=tk.X)
    stage = tk.Frame(root)
    stage.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    pages = []
    for fig in _figures:
        frame = tk.Frame(stage)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar=False)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.get_tk_widget().pack(side=tk.TOP)  # natural figsize, no stretching
        pages.append(frame)

    state = {"i": 0}
    label = tk.Label(bar)

    def go(i):
        i = max(0, min(len(pages) - 1, i))
        pages[state["i"]].pack_forget()
        state["i"] = i
        pages[i].pack(fill=tk.BOTH, expand=True)
        label.config(text=f"{i + 1} / {len(pages)}")
        pages[i].update_idletasks()
        _figures[i].canvas.draw_idle()

    tk.Button(bar, text="◀ Prev", command=lambda: go(state["i"] - 1)).pack(side=tk.LEFT)
    label.pack(side=tk.LEFT, expand=True)
    tk.Button(bar, text="Next ▶", command=lambda: go(state["i"] + 1)).pack(side=tk.RIGHT)

    root.bind("<Left>", lambda e: go(state["i"] - 1))
    root.bind("<Right>", lambda e: go(state["i"] + 1))
    root.bind("<Escape>", lambda e: root.destroy())

    pages[0].pack(fill=tk.BOTH, expand=True)
    label.config(text=f"1 / {len(pages)}")
    # size the window to the largest figure (same size as plain plt.show())
    root.update_idletasks()
    w = max(p.winfo_reqwidth() for p in pages)
    h = max(p.winfo_reqheight() for p in pages) + bar.winfo_reqheight()
    root.geometry(f"{w}x{h}")
    root.mainloop()
