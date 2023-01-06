import logging
import tkinter as tk

from gf_utils.stc_data import GameData

from gun import GunConfig
from position import Positioning

logger = logging.getLogger(__name__)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        gamedata = GameData(r"..\GF_Data_Tools\data\ch\formatted\json")
        self.gun_config: dict[int, GunConfig] = {}
        for i in range(1, 6):
            gun_config = GunConfig(i, gamedata, master=self)
            gun_config.any_equip = False
            gun_config.grid(row=0, column=i - 1, padx=10, pady=10)
            self.gun_config[i] = gun_config
        self.positioning = Positioning(master=self)
        self.positioning.grid(row=1, column=0, sticky="nwse", padx=10, pady=10)

        self.btn_generate = tk.Button(self, text="生成JSON", command=self.generate_json)
        self.btn_generate.grid(row=1, column=4, sticky="se", padx=10, pady=10)

    def generate_json(self):
        pos_dict = self.positioning.get_pos_dict()
        gun_full = []
        equip_full = {}
        for idx, pos in pos_dict.items():
            gun_record, equip_records = self.gun_config[idx].generate_records(pos)
            gun_full.append(gun_record)
            equip_full.update(equip_records)
        import json
        from pathlib import Path

        json.dump(gun_full, Path("gun_with_user_info.json").open("w"))
        json.dump(equip_full, Path("equip_with_user_info.json").open("w"))


if __name__ == "__main__":
    logger.setLevel("DEBUG")
    App().mainloop()
