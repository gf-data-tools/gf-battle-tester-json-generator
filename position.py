import tkinter as tk


class Positioning(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for i in range(3):
            self.columnconfigure(i, weight=1, minsize=60)
        tk.Label(self, text=_("站位")).grid(row=0, column=0, columnspan=3)
        self.posvar = {}
        for i in range(3):
            for j in range(3):
                var = tk.IntVar(value=0)
                ent = tk.Entry(self, textvariable=var)
                ent.config(width=1)
                ent.grid(sticky="ew", row=i + 1, column=j)
                self.posvar[(i, j)] = var

    def get_pos_dict(self):
        ret = {}
        for i in range(3):
            for j in range(3):
                v = self.posvar[(i, j)].get()
                if v != 0:
                    ret[v] = j * 5 - i + 9
        return ret
