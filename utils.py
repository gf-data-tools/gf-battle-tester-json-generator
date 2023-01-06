import tkinter as tk


def menu_from_dict(master: tk.Widget, options: dict, var_key: tk.Variable, var_value: tk.Variable):
    menu = tk.Menu(master, tearoff=False)
    for k, v in options.items():
        if isinstance(v, dict):
            menu.add_cascade(label=k, menu=menu_from_dict(menu, v, var_key, var_value))
        else:
            menu.add_radiobutton(
                label=k, indicatoron=False, command=lambda k=k, v=v: (var_key.set(k), var_value.set(v))
            )
    return menu


def var_min_max(var: tk.IntVar, min: int, max: int, *_):
    v = var.get()
    if v < min:
        var.set(min)
    if v > max:
        var.set(max)
