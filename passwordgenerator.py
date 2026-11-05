import math
import secrets
import string
import tkinter as tk
from tkinter import ttk

SETS = {
    "Uppercase (A-Z)": string.ascii_uppercase,
    "Lowercase (a-z)": string.ascii_lowercase,
    "Numbers (0-9)": string.digits,
    "Symbols": string.punctuation,
}
SYMBOLS = "Symbols"
AMBIGUOUS = set("Il1O0o|`'\"")


def strength(length, pool):
    bits = length * math.log2(pool) if pool > 1 else 0
    if bits < 40:
        return "Weak", "#d9534f"
    if bits < 60:
        return "Fair", "#f0ad4e"
    if bits < 90:
        return "Strong", "#5cb85c"
    return "Very strong", "#2e8b57"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.resizable(False, False)
        pad = {"padx": 16, "pady": 6}

        # Output + copy
        self.out = tk.StringVar()
        row = ttk.Frame(self)
        row.pack(fill="x", **pad)
        ttk.Entry(row, textvariable=self.out, font=("Menlo", 14), state="readonly", width=32).pack(
            side="left", fill="x", expand=True, ipady=6
        )
        self.copy_btn = ttk.Button(row, text="Copy", command=self.copy)
        self.copy_btn.pack(side="left", padx=(8, 0))

        # Strength
        self.strength = tk.Label(self, text="", font=("Helvetica", 12, "bold"))
        self.strength.pack(anchor="w", padx=16)

        # Length
        self.length = tk.IntVar(value=16)
        lrow = ttk.Frame(self)
        lrow.pack(fill="x", **pad)
        ttk.Label(lrow, text="Length").pack(side="left")
        self.len_label = ttk.Label(lrow, text="16", width=3)
        self.len_label.pack(side="right")
        ttk.Scale(lrow, from_=4, to=64, variable=self.length, command=self.on_length).pack(
            side="left", fill="x", expand=True, padx=10
        )

        # Options
        self.opts = {name: tk.BooleanVar(value=True) for name in SETS}
        for name, var in self.opts.items():
            ttk.Checkbutton(self, text=name, variable=var, command=self.generate).pack(anchor="w", padx=16)
        srow = ttk.Frame(self)
        srow.pack(fill="x", padx=16)
        ttk.Label(srow, text="Symbols to use").pack(side="left")
        self.symbols = tk.StringVar(value=SETS[SYMBOLS])
        ttk.Button(srow, text="Reset", width=6, command=lambda: self.symbols.set(SETS[SYMBOLS])).pack(side="right")
        ttk.Entry(srow, textvariable=self.symbols, font=("Menlo", 12)).pack(
            side="left", fill="x", expand=True, padx=8
        )
        self.symbols.trace_add("write", lambda *_: self.generate())
        self.no_ambig = tk.BooleanVar(value=False)
        self.no_repeat = tk.BooleanVar(value=False)
        ttk.Checkbutton(self, text="Avoid look-alike characters (I l 1 O 0)", variable=self.no_ambig,
                        command=self.generate).pack(anchor="w", padx=16)
        ttk.Checkbutton(self, text="No repeated characters", variable=self.no_repeat,
                        command=self.generate).pack(anchor="w", padx=16)

        self.msg = ttk.Label(self, text="", foreground="#d9534f")
        self.msg.pack(anchor="w", padx=16)
        ttk.Button(self, text="Generate", command=self.generate).pack(fill="x", padx=16, pady=(6, 16), ipady=4)

        self.generate()

    def on_length(self, _=None):
        self.len_label.config(text=str(self.length.get()))
        self.generate()

    def generate(self):
        n = self.length.get()
        self.len_label.config(text=str(n))
        pools = []
        for name, var in self.opts.items():
            if var.get():
                source = self.symbols.get() if name == SYMBOLS else SETS[name]
                chars = [c for c in dict.fromkeys(source) if not c.isspace() and not (self.no_ambig.get() and c in AMBIGUOUS)]
                if chars:
                    pools.append(chars)
        self.msg.config(text="")
        if not pools:
            self.out.set("")
            self.strength.config(text="")
            self.msg.config(text="Pick at least one character type.")
            return
        allchars = sorted({c for p in pools for c in p})
        if self.no_repeat.get() and n > len(allchars):
            self.out.set("")
            self.strength.config(text="")
            self.msg.config(text=f"No-repeat max length is {len(allchars)} for these options.")
            return

        rng = secrets.SystemRandom()
        # Guarantee one char from each selected type, then fill the rest.
        if self.no_repeat.get():
            picked = [rng.choice(p) for p in pools]
            while len(set(picked)) < len(pools):
                picked = [rng.choice(p) for p in pools]
            rest = [c for c in allchars if c not in picked]
            picked += rng.sample(rest, n - len(picked))
        else:
            picked = [rng.choice(p) for p in pools] + [rng.choice(allchars) for _ in range(n - len(pools))]
        rng.shuffle(picked)
        self.out.set("".join(picked))
        label, color = strength(n, len(allchars))
        self.strength.config(text=label, fg=color)
        self.copy_btn.config(text="Copy")

    def copy(self):
        if self.out.get():
            self.clipboard_clear()
            self.clipboard_append(self.out.get())
            self.copy_btn.config(text="Copied!")


if __name__ == "__main__":
    App().mainloop()
