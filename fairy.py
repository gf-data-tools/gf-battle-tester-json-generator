import logging
import math
import tkinter as tk
from functools import cache, partial
from typing import *

from gf_utils.stc_data import GameData

from utils import menu_from_dict, var_min_max


class FairyConfig(tk.Frame):
    def __init__(self, gamedata: GameData, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.gamedata = gamedata

        self.var_fairy_name = tk.StringVar(value="-")
        self.var_fairy_id = tk.IntVar(value=0)
        self.opt_fairy = tk.Menubutton(
            self, textvariable=self.var_fairy_name, indicatoron=False, width=1, relief="groove"
        )
        fairy_dict = {fairy["name"]: fairy["id"] for fairy in self.gamedata["fairy"].values()}
        self.opt_fairy.config(menu=menu_from_dict(self.opt_fairy, fairy_dict, self.var_fairy_name, self.var_fairy_id))

        self.var_talent_name = tk.StringVar(value="-")
        self.var_talent_id = tk.IntVar(value=0)
        self.opt_talent = tk.Menubutton(
            self, textvariable=self.var_talent_name, indicatoron=False, width=1, relief="groove"
        )
        talent_dict = {talent["name"]: talent["id"] for talent in self.gamedata["fairy_talent"].values()}
        self.opt_talent.config(
            menu=menu_from_dict(self.opt_talent, talent_dict, self.var_talent_name, self.var_talent_id)
        )

        self.var_level = tk.IntVar(value=100)
        self.var_level.trace_add("write", partial(var_min_max, self.var_level, 1, 100))
        self.ent_level = tk.Entry(self, textvariable=self.var_level, width=1)

        self.var_rank = tk.IntVar(value=5)
        self.var_rank.trace_add("write", partial(var_min_max, self.var_rank, 1, 5))
        self.ent_rank = tk.Entry(self, textvariable=self.var_rank, width=1)

        self.var_skill1 = tk.IntVar(value=10)
        self.var_skill1.trace_add("write", partial(var_min_max, self.var_skill1, 1, 10))
        self.ent_skill1 = tk.Entry(self, textvariable=self.var_skill1, width=1)

        self.columnconfigure(0, minsize=30)
        self.columnconfigure(1, minsize=60)
        tk.Label(self, text=f"妖精").grid(row=0, column=0, sticky="e")
        self.opt_fairy.grid(row=0, column=1, sticky="we")
        tk.Label(self, text=f"天赋").grid(row=1, column=0, sticky="e")
        self.opt_talent.grid(row=1, column=1, sticky="we")
        tk.Label(self, text=f"Lv").grid(row=2, column=0, sticky="e")
        self.ent_level.grid(row=2, column=1, sticky="we")
        tk.Label(self, text=f"星级").grid(row=3, column=0, sticky="e")
        self.ent_rank.grid(row=3, column=1, sticky="we")
        tk.Label(self, text=f"技能").grid(row=4, column=0, sticky="e")
        self.ent_skill1.grid(row=4, column=1, sticky="we")

    def generate_record(self):
        fairy_id = self.var_fairy_id.get()
        level = self.var_level.get()
        rank = self.var_rank.get()
        fairy_info = self.gamedata["fairy"][fairy_id]
        quality_exp = eval(f"{{{fairy_info['quality_need_number']}}}")[rank]
        record = {
            "id": "1",
            "user_id": "123456",
            "fairy_id": fairy_id,
            "team_id": "1",
            "fairy_lv": level,
            "fairy_exp": self.gamedata["fairy_exp_info"][str(level)]["exp"],
            "quality_lv": rank,
            "quality_exp": quality_exp,
            "skill_lv": self.var_skill1.get(),
            "passive_skill": self.var_talent_id.get(),
            "is_locked": "1",
            "equip_id": "0",
            "adjust_count": "0",
            "last_adjust": "0",
            "passive_skill_collect": "0",
            "skin": "0",
        }
        for k in record:
            record[k] = str(record[k])
        return record

    def fairy_exp(self, lv):
        if lv == 1:
            return 0
        ei = int(self.gamedata["fairy_exp_info"][str(lv - 1)]["exp"])
        return self.fairy_exp(lv - 1) + ei
