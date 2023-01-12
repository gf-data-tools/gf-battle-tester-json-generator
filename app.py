import gettext
import logging
import tkinter as tk
from pathlib import Path

from gf_utils.stc_data import GameData

from fairy import FairyConfig
from gun import GunConfig
from position import Positioning
from utils import menu_from_dict

gettext.translation("app", localedir="locales", languages=["ch", "us"]).install()
logger = logging.getLogger(__name__)


class App(tk.Tk):
    def __init__(self, region="ch", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup(region)

    def setup(self, region="ch"):
        for widget in self.winfo_children():
            widget.destroy()
        self.region = region
        self.output_path = Path("outputs")
        gettext.translation("app", localedir="locales", languages=[region]).install()
        gamedata = GameData(Rf"data\{region}")
        self.gun_config: dict[int, GunConfig] = {}
        for i in range(1, 6):
            gun_config = GunConfig(i, gamedata, master=self)
            gun_config.grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=10, pady=10)
            self.gun_config[i] = gun_config
        self.positioning = Positioning(master=self)
        self.positioning.grid(row=1, column=2, sticky="nwse", padx=10, pady=10)
        self.fairy = FairyConfig(gamedata, master=self)
        self.fairy.grid(row=1, column=2, sticky="ws", padx=10, pady=10)

        self.controller = tk.Frame(self)

        self.var_region = tk.StringVar(value=region)
        self.opt_region = tk.OptionMenu(
            self.controller, self.var_region, "ch", "tw", "jp", "kr", "us", command=lambda var: self.setup(var)
        )

        self.btn_generate = tk.Button(self.controller, text=_("生成JSON"), command=self.generate_json)

        self.opt_region.grid(row=0, column=0, sticky="we")
        self.btn_generate.grid(row=1, column=0, sticky="we")

        self.controller.grid(row=1, column=2, sticky="se", padx=10, pady=10)

    def generate_json(self):
        pos_dict = self.positioning.get_pos_dict()
        gun_full = []
        equip_full = {}
        for idx, pos in pos_dict.items():
            gun_record, equip_records = self.gun_config[idx].generate_records(pos)
            gun_full.append(gun_record)
            equip_full.update(equip_records)
        fairy_full = {"1": self.fairy.generate_record()}
        import json
        from pathlib import Path

        json.dump(gun_full, (self.output_path / "gun_with_user_info.json").open("w"))
        json.dump(equip_full, (self.output_path / "equip_with_user_info.json").open("w"))
        json.dump(fairy_full, (self.output_path / "fairy_with_user_info.json").open("w"))

    def change_region(self, region):
        raise RuntimeError(region)


if __name__ == "__main__":
    logger.setLevel("DEBUG")
    App().mainloop()
