import logging
import math
import tkinter as tk
from functools import partial
from typing import *

from gf_utils.stc_data import GameData

from utils import menu_from_dict, var_min_max

logger = logging.getLogger(__name__)


class GunConfig(tk.Frame):
    def __init__(self, idx: int, gamedata: GameData, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.idx = idx
        self.gamedata = gamedata

        self.var_gun_name = tk.StringVar(value="-")
        self.var_gun_id = tk.IntVar(value=0)
        self.var_gun_id.trace_add("write", self.update_gun_opts)
        self.opt_gun = tk.Menubutton(self, textvariable=self.var_gun_name, indicatoron=False, width=1, relief="groove")
        self.opt_gun.config(
            menu=menu_from_dict(self.opt_gun, self.get_grouped_gun(), self.var_gun_name, self.var_gun_id)
        )

        self.var_skin_name = tk.StringVar(value="-")
        self.var_skin_id = tk.IntVar(value=0)
        self.opt_skin = tk.Menubutton(
            self, textvariable=self.var_skin_name, indicatoron=False, width=1, relief="groove"
        )

        self.var_level = tk.IntVar(value=100)
        self.var_level.trace_add("write", partial(var_min_max, self.var_level, 1, 120))
        self.ent_level = tk.Entry(self, textvariable=self.var_level, width=1)

        self.var_number = tk.IntVar(value=5)
        self.var_number.trace_add("write", partial(var_min_max, self.var_number, 1, 5))
        self.ent_number = tk.Entry(self, textvariable=self.var_number, width=1)

        self.var_mod = tk.IntVar(value=0)
        self.var_mod.trace_add("write", partial(var_min_max, self.var_mod, 0, 3))
        self.ent_mod = tk.Entry(self, textvariable=self.var_mod, width=1)

        self.var_skill1 = tk.IntVar(value=10)
        self.var_skill1.trace_add("write", partial(var_min_max, self.var_skill1, 1, 10))
        self.ent_skill1 = tk.Entry(self, textvariable=self.var_skill1, width=1)

        self.var_skill2 = tk.IntVar(value=0)
        self.var_skill2.trace_add("write", partial(var_min_max, self.var_skill2, 0, 10))
        self.ent_skill2 = tk.Entry(self, textvariable=self.var_skill2, width=1)

        self.var_favor = tk.IntVar(value=100)
        self.var_favor.trace_add("write", partial(var_min_max, self.var_favor, 0, 200))
        self.ent_favor = tk.Entry(self, textvariable=self.var_favor, width=1)

        self.var_equip_name: dict[int, tk.StringVar] = {}
        self.var_equip_id: dict[int, tk.IntVar] = {}
        self.var_equip_lv: dict[int, tk.IntVar] = {}
        self.opt_equip: dict[int, tk.Menubutton] = {}
        self.ent_equip_lv: dict[int, tk.Menubutton] = {}
        for i in range(1, 4):
            self.var_equip_name[i] = tk.StringVar(value="-")
            self.var_equip_id[i] = tk.IntVar(value=0)
            self.opt_equip[i] = tk.Menubutton(
                self, textvariable=self.var_equip_name[i], indicatoron=False, width=1, relief="groove"
            )
            self.var_equip_lv[i] = tk.IntVar(value=10)
            self.var_equip_lv[i].trace_add("write", partial(var_min_max, self.var_equip_lv[i], 1, 10))
            self.ent_equip_lv[i] = tk.Entry(self, textvariable=self.var_equip_lv[i], width=1)

        self.columnconfigure(0, minsize=30)
        self.columnconfigure(1, minsize=60)
        self.columnconfigure(2, minsize=30)
        self.columnconfigure(3, minsize=60)
        tk.Label(self, text=_("人形") + f"{self.idx}").grid(row=0, column=0, sticky="e")
        self.opt_gun.grid(row=0, column=1, columnspan=3, sticky="we")
        tk.Label(self, text=_("皮肤")).grid(row=1, column=0, sticky="e")
        self.opt_skin.grid(row=1, column=1, columnspan=3, sticky="we")
        tk.Label(self, text=_("LV")).grid(row=2, column=0, sticky="e")
        self.ent_level.grid(row=2, column=1, sticky="we")
        tk.Label(self, text=_("编制")).grid(row=2, column=2, sticky="e")
        self.ent_number.grid(row=2, column=3, sticky="we")
        tk.Label(self, text=_("Mod")).grid(row=3, column=0, sticky="e")
        self.ent_mod.grid(row=3, column=1, sticky="we")
        tk.Label(self, text=_("好感")).grid(row=3, column=2, sticky="e")
        self.ent_favor.grid(row=3, column=3, sticky="we")
        tk.Label(self, text=_("技能1")).grid(row=4, column=0, sticky="e")
        self.ent_skill1.grid(row=4, column=1, sticky="we")
        tk.Label(self, text=_("技能2")).grid(row=4, column=2, sticky="e")
        self.ent_skill2.grid(row=4, column=3, sticky="we")
        tk.Label(self, text=_("装备")).grid(row=5, column=1)
        tk.Label(self, text=_("LV")).grid(row=5, column=3)
        for i in range(1, 4):
            self.opt_equip[i].grid(row=5 + i, column=0, columnspan=3, sticky="we")
            self.ent_equip_lv[i].grid(row=5 + i, column=3, sticky="we")

    def get_grouped_gun(self) -> dict:
        type_map = {1: "HG", 2: "SMG", 3: "RF", 4: "AR", 5: "MG", 6: "SG"}
        rank_map = {7: "1☆", 2: "2☆", 3: "3☆", 4: "4☆", 5: "5☆", 6: "6☆", 1: "..."}
        grouped = {"-": 0} | {t: {r: {} for r in rank_map.values()} for t in type_map.values()}
        for gun in self.gamedata["gun"].values():
            if 9000 <= gun["id"] <= 20000 or gun["id"] >= 30000:
                grouped[type_map[gun["type"]]]["..."][str(gun["id"]) + " " + gun["name"]] = gun["id"]
            else:
                gun_name = gun["name"] if gun["id"] <= 20000 else "[MOD]" + gun["name"]
                grouped[type_map[gun["type"]]][rank_map[gun["rank_display"]]][gun_name] = gun["id"]
        return grouped

    def update_gun_opts(self, *_):
        gun_id = self.var_gun_id.get()
        gun_info = self.gamedata["gun"][gun_id]
        logger.debug(f"{gun_id} {gun_info['name']}")
        for i in range(1, 4):
            logger.debug(f'{i} {gun_info[f"type_equip{i}"]}')
            valid_types = [int(s) for s in gun_info[f"type_equip{i}"][2:].split(",")]
            grouped: dict[str, int | dict] = {"-": 0, "...": {}}
            for equip in self.gamedata["equip"].values():
                equip_name = f"{equip['rank']}☆-{equip['name']}"
                type_name = self.gamedata["equip_type"][equip["type"]]["name"]
                if (
                    (equip["type"] not in valid_types)
                    or (equip["is_show"] == 0)
                    or (equip["fit_guns"] and str(gun_id) not in equip["fit_guns"].split(","))
                ):
                    grouped["..."].setdefault(type_name, {})
                    grouped["..."][type_name][equip_name] = equip["id"]
                else:
                    grouped.setdefault(type_name, {})
                    grouped[type_name][equip_name] = equip["id"]
            logger.debug(grouped)
            self.opt_equip[i].config(
                menu=menu_from_dict(self.opt_equip[i], grouped, self.var_equip_name[i], self.var_equip_id[i])
            )

        grouped = {"-": 0} | {
            skin["name"]: skin["id"]
            for skin in self.gamedata["skin"].values()
            if skin["fit_gun"] in [gun_id, gun_id % 20000]
        }
        self.opt_skin.config(menu=menu_from_dict(self.opt_skin, grouped, self.var_skin_name, self.var_skin_id))

    def generate_records(self, position) -> Tuple[dict, dict]:
        gun_id = self.var_gun_id.get()
        gun_info = self.gamedata["gun"][gun_id]
        gun_record = {
            "id": self.idx,
            "user_id": "123456",
            "gun_id": gun_id,
            "gun_exp": self.gun_exp(self.var_level.get()),
            "gun_level": self.var_level.get(),
            "team_id": "1",
            "if_modification": self.var_mod.get(),
            "location": self.idx,
            "position": position,
            "life": calculate(self.var_level.get(), "hp", gun_info) * self.var_number.get(),
            "ammo": "5",
            "mre": "10",
            "pow": calculate(self.var_level.get(), "pow", gun_info),
            "hit": calculate(self.var_level.get(), "hit", gun_info),
            "dodge": calculate(self.var_level.get(), "dodge", gun_info),
            "rate": calculate(self.var_level.get(), "rate", gun_info),
            "skill1": self.var_skill1.get(),
            "skill2": self.var_skill2.get(),
            "fix_end_time": "0",
            "is_locked": "1",
            "number": self.var_number.get(),
            "equip1": self.idx,
            "equip2": self.idx + 5,
            "equip3": self.idx + 10,
            "equip4": "0",
            "favor": 10000 * self.var_favor.get(),
            "max_favor": 2000000 if gun_id > 20000 else 1500000,
            "favor_toplimit": 2000000 if gun_id > 20000 else 1500000,
            "soul_bond": 0 if self.var_favor.get() <= 100 else 1,
            "skin": self.var_skin_id.get(),
            "can_click": "0",
            "soul_bond_time": "0",
            "special_effect": "0",
        }
        for k in gun_record:
            gun_record[k] = str(gun_record[k])

        equip_records = {}
        for i in range(1, 4):
            equip_id = self.var_equip_id[i].get()
            if equip_id == 0:
                continue
            record = {
                "id": 5 * i - 5 + self.idx,
                "user_id": "123456",
                "gun_with_user_id": self.idx,
                "equip_id": equip_id,
                "equip_exp": "0",
                "equip_level": self.var_equip_lv[i].get(),
                "pow": "10000",
                "hit": "10000",
                "dodge": "10000",
                "speed": "10000",
                "rate": "10000",
                "critical_harm_rate": "10000",
                "critical_percent": "10000",
                "armor_piercing": "10000",
                "armor": "10000",
                "shield": "10000",
                "damage_amplify": "10000",
                "damage_reduction": "10000",
                "night_view_percent": "10000",
                "bullet_number_up": "10000",
                "adjust_count": "13",
                "is_locked": "1",
                "last_adjust": "",
            }
            for k in record:
                record[k] = str(record[k])
            equip_records[record["id"]] = record

        return gun_record, equip_records

    def gun_exp(self, lv):
        if lv == 1:
            return 0
        ei = int(self.gamedata["gun_exp_info"][str(lv - 1)]["exp"])
        return self.gun_exp(lv - 1) + ei


BASIC = [16, 45, 5, 5]
BASIC_LIFE_ARMOR = [[[55, 0.555], [2, 0.161]], [[96.283, 0.138], [13.979, 0.04]]]
BASE_ATTR = [
    [0.60, 0.60, 0.80, 1.20, 1.80, 0.00],
    [1.60, 0.60, 1.20, 0.30, 1.60, 0.00],
    [0.80, 2.40, 0.50, 1.60, 0.80, 0.00],
    [1.00, 1.00, 1.00, 1.00, 1.00, 0.00],
    [1.50, 1.80, 1.60, 0.60, 0.60, 0.00],
    [2.00, 0.70, 0.40, 0.30, 0.30, 1.00],
]
GROW = [
    [[0.242, 0], [0.181, 0], [0.303, 0], [0.303, 0]],
    [[0.06, 18.018], [0.022, 15.741], [0.075, 22.572], [0.075, 22.572]],
]
TYPE_ENUM = {"HG": 0, "SMG": 1, "RF": 2, "AR": 3, "MG": 4, "SG": 5}
ATTR_ENUM = {"hp": 0, "pow": 1, "rate": 2, "hit": 3, "dodge": 4, "armor": 5}


def calculate(lv, attr_type, doll):
    mod = 1
    if lv <= 100:
        mod = 0
    guntype = doll["type"] - 1
    attr = ATTR_ENUM[attr_type]
    ratio = doll[f"ratio_{attr_type}"] if attr_type != "hp" else doll[f"ratio_life"]
    growth = doll["eat_ratio"]

    if attr == 0 or attr == 5:
        return math.ceil(
            (BASIC_LIFE_ARMOR[mod][attr & 1][0] + (lv - 1) * BASIC_LIFE_ARMOR[mod][attr & 1][1])
            * BASE_ATTR[guntype][attr]
            * (ratio / 100)
        )
    else:
        return math.ceil(
            (GROW[mod][attr - 1][1] + (lv - 1) * GROW[mod][attr - 1][0])
            * BASE_ATTR[guntype][attr]
            * (ratio / 100)
            * (growth / 100)
        )


if __name__ == "__main__":
    logger.setLevel("DEBUG")
    window = tk.Tk()

    gamedata = GameData(r"..\GF_Data_Tools\data\ch\formatted\json")
    for i in range(5):
        gun_config = GunConfig(i + 1, gamedata, relief="groove")
        gun_config.grid(row=0, column=i, padx=10, pady=10)
    window.mainloop()
