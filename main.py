import tkinter as tk
from tkinter import font
from gf_utils.stc_data import GameData
from typing import *

class GunPresetHeader(tk.Frame):
    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args, **kwargs)
        for i in range(12):
            self.columnconfigure(i,weight=1,minsize=40)
        tk.Label(self,text='编号',relief='groove').grid(sticky='nsew',column=0,row=0,rowspan=2)
        tk.Label(self,text='星级',relief='groove').grid(sticky='ew',column=1,row=0)
        tk.Label(self,text='枪种',relief='groove').grid(sticky='ew',column=2,row=0)
        tk.Label(self,text='人形',relief='groove').grid(sticky='ew',column=3,row=0,columnspan=3)
        tk.Label(self,text='等级',relief='groove').grid(sticky='ew',column=6,row=0)
        tk.Label(self,text='编制',relief='groove').grid(sticky='ew',column=7,row=0)
        tk.Label(self,text='Mod',relief='groove').grid(sticky='ew',column=8,row=0)
        tk.Label(self,text='技能1',relief='groove').grid(sticky='ew',column=9,row=0)
        tk.Label(self,text='技能2',relief='groove').grid(sticky='ew',column=10,row=0)
        tk.Label(self,text='好感',relief='groove').grid(sticky='ew',column=11,row=0)
        tk.Label(self,text='装备1',relief='groove').grid(sticky='ew',column=1,row=1,columnspan=3)
        tk.Label(self,text='装备2',relief='groove').grid(sticky='ew',column=4,row=1,columnspan=3)
        tk.Label(self,text='装备3',relief='groove').grid(sticky='ew',column=7,row=1,columnspan=3)
        tk.Label(self,text='皮肤',relief='groove').grid(sticky='ew',column=10,row=1,columnspan=2)


class GunPreset(tk.Frame):
    def __init__(self,idx:int,gamedata:GameData,*args,**kwargs) -> None:
        super().__init__(*args, **kwargs)
        for i in range(12):
            self.columnconfigure(i,weight=1,minsize=60)
        self.gamedata = gamedata
        self.idx = idx
        tk.Label(self,text=idx,relief='groove').grid(sticky='nsew',column=0,row=0,rowspan=2)

        self.var_rank = tk.StringVar(value='-')
        self.opt_rank = tk.OptionMenu(self,self.var_rank,'-','2','3','4','5','6','7',command=self.opt_update)
        self.opt_rank.config(width=1)
        self.opt_rank.grid(sticky='ew',column=1,row=0)

        self.var_type = tk.StringVar(value='-')
        self.opt_type = tk.OptionMenu(self,self.var_type,'-','HG','SMG','RF','AR','MG','SG',command=self.opt_update)
        self.opt_type.config(width=1)
        self.opt_type.grid(sticky='ew',column=2,row=0)

        self.var_gun = tk.StringVar(value='-')
        self.opt_gun = tk.OptionMenu(self,self.var_gun,'-')
        self.opt_gun.config(width=1)
        self.opt_gun.grid(sticky='ew',column=3,row=0,columnspan=3)
        
        self.var_level = tk.IntVar(value=100)
        self.ent_level = tk.Entry(self,textvariable=self.var_level)
        self.ent_level.config(width=1)
        self.ent_level.grid(sticky='ew',column=6,row=0)

        self.var_number = tk.IntVar(value=5)
        self.ent_number = tk.Entry(self,textvariable=self.var_number)
        self.ent_number.config(width=1)
        self.ent_number.grid(sticky='ew',column=7,row=0)

        self.var_mod = tk.IntVar(value=0)
        self.ent_mod = tk.Entry(self,textvariable=self.var_mod)
        self.ent_mod.config(width=1)
        self.ent_mod.grid(sticky='ew',column=8,row=0)

        self.var_skill1 = tk.IntVar(value=10)
        self.ent_skill1 = tk.Entry(self,textvariable=self.var_skill1)
        self.ent_skill1.config(width=1)
        self.ent_skill1.grid(sticky='ew',column=9,row=0)

        self.var_skill2 = tk.IntVar(value=0)
        self.ent_skill2 = tk.Entry(self,textvariable=self.var_skill2)
        self.ent_skill2.config(width=1)
        self.ent_skill2.grid(sticky='ew',column=10,row=0)

        self.var_favor = tk.IntVar(value=100)
        self.ent_favor = tk.Entry(self,textvariable=self.var_favor)
        self.ent_favor.config(width=1)
        self.ent_favor.grid(sticky='ew',column=11,row=0)

        self._gun_table = {
            ('' if gun['id']<=20000 else '[MOD]')+gun['name']:(gun['id'], gun['type'], gun['rank_display'])
            for gun in self.gamedata['gun'].values() if gun['id']<=9000 or 20000<=gun['id']<=30000
        }

        self.equip:dict[int,Equip] = {}
        for i in range(3):
            var_type = tk.StringVar(value='-')
            opt_type = tk.OptionMenu(self,var_type,'-')
            opt_type.config(width=1)
            opt_type.grid(sticky='ew',column=1+i*3,row=1,columnspan=2)

            var_level = tk.IntVar(value=10)
            ent_level = tk.Entry(self,textvariable=var_level)
            ent_level.config(width=1)
            ent_level.grid(sticky='ew',column=3+i*3,row=1)
            self.equip[i] = Equip(var_type, opt_type, var_level, ent_level)

        self.var_skin = tk.StringVar(value='-')
        self.opt_skin = tk.OptionMenu(self,self.var_skin,'-')
        self.opt_skin.config(width=1)
        self.opt_skin.grid(sticky='ew',column=10,row=1,columnspan=2)

    def opt_update(self,_):
        gun_rank = {'-':0,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7}[self.var_rank.get()]
        gun_type = {'-':0,'HG':1,'SMG':2,'RF':3,'AR':4,'MG':5,'SG':6}[self.var_type.get()]
        options = ['-']+[name for name,info in self._gun_table.items() if info[1]==gun_type and info[2]==gun_rank] if gun_rank and gun_type else ['-']
        
        self.opt_gun['menu'].delete(0, "end")
        for v in options: self.opt_gun['menu'].add_command(label=v, command=lambda v=v: self.gun_select(v))
    
    def gun_select(self,gun_name):
        self.var_gun.set(gun_name)
        gun_id = self._gun_table[gun_name][0]
        gun_info = self.gamedata['gun'][gun_id]
        self._equip_table = {}
        for i in range(3):
            self.equip[i].opt_type['menu'].delete(0, "end")
            self.equip[i].opt_type['menu'].add_command(label='-', command=lambda i=i: self.equip[i].var_type.set('-'))
            equip_str = gun_info[f'type_equip{i+1}']
            equip_types = [int(t) for t in equip_str[2:].split(',')]
            for equip_info in self.gamedata['equip'].values():
                if equip_info['is_show']==0: continue
                if equip_info['type'] not in equip_types: continue
                fit_guns = equip_info['fit_guns']
                if not fit_guns or str(gun_id) in fit_guns.split(','):
                    equip_name = f"{equip_info['rank']}-{equip_info['name']}"
                    self._equip_table[equip_name] = equip_info['id']
                    self.equip[i].opt_type['menu'].add_command(label=equip_name, command=lambda v=equip_name,i=i: self.equip[i].var_type.set(v))
        
        self._skin_table = {'-':0}
        for skin_info in self.gamedata['skin'].values():
            if skin_info['fit_gun'] in [gun_id, gun_id%20000]:
                self._skin_table[skin_info['name']] = skin_info['id']
        
        self.opt_skin['menu'].delete(0, "end")
        for v in self._skin_table: self.opt_skin['menu'].add_command(label=v, command=lambda v=v: self.var_skin.set(v))
    
    def generate_records(self,position)->Tuple[dict,dict]:
        gun_id = self._gun_table[self.var_gun.get()][0]
        gun_info = self.gamedata['gun'][gun_id]
        gun_record = {
            "id": self.idx, "user_id": "123456",
            "gun_id": gun_id,
            "gun_exp": self.gun_exp(self.var_level.get()), 
            "gun_level": self.var_level.get(),
            "team_id": "1",
            "if_modification": self.var_mod.get(),
            "location": self.idx,
            "position": position,
            "life": calculate(self.var_level.get(),'hp',gun_info)*self.var_number.get(),
            "ammo": "5", "mre": "10",
            "pow": calculate(self.var_level.get(),'pow',gun_info),
            "hit": calculate(self.var_level.get(),'hit',gun_info),
            "dodge": calculate(self.var_level.get(),'dodge',gun_info),
            "rate": calculate(self.var_level.get(),'rate',gun_info),
            "skill1": self.var_skill1.get(),"skill2": self.var_skill2.get(),
            "fix_end_time": "0","is_locked": "1",
            "number": self.var_number.get(),
            "equip1": self.idx,"equip2": self.idx+5,"equip3": self.idx+10, "equip4": "0",
            "favor": 10000*self.var_favor.get(),
            "max_favor": 2000000 if gun_id>20000 else 1500000, 
            "favor_toplimit": 2000000 if gun_id>20000 else 1500000, 
            "soul_bond": 0 if self.var_favor.get()<=100 else 1,
            "skin": self._skin_table[self.var_skin.get()],
            "can_click": "0","soul_bond_time": "0","special_effect": "0"
        }
        for k in gun_record:
            gun_record[k] = str(gun_record[k])

        equip_records = {}
        for i in range(3):
            if self.equip[i].var_type.get()=='-':continue
            equip_id = self._equip_table[self.equip[i].var_type.get()]
            record = {
                "id": 5*i+self.idx, "user_id": "123456",
                "gun_with_user_id": self.idx, 
                "equip_id": equip_id,
                "equip_exp": "0",
                "equip_level": self.equip[i].var_level.get(),
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
                "last_adjust": ""
            }
            for k in record:
                record[k] = str(record[k])
            equip_records[record['id']]=record
        
        return gun_record, equip_records

    def gun_exp(self,lv):
        ei = int(self.gamedata['gun_exp_info'][str(lv)]['exp'])
        print(lv,ei)
        return ei if lv==1 else self.gun_exp(lv-1)+ei

import math

BASIC = [16, 45, 5, 5]
BASIC_LIFE_ARMOR = [
    [[55, 0.555], [2, 0.161]],
    [[96.283, 0.138], [13.979, 0.04]]
]
BASE_ATTR = [
    [0.60, 0.60, 0.80, 1.20, 1.80, 0.00],
    [1.60, 0.60, 1.20, 0.30, 1.60, 0.00],
    [0.80, 2.40, 0.50, 1.60, 0.80, 0.00],
    [1.00, 1.00, 1.00, 1.00, 1.00, 0.00],
    [1.50, 1.80, 1.60, 0.60, 0.60, 0.00],
    [2.00, 0.70, 0.40, 0.30, 0.30, 1.00]
]
GROW = [
    [[0.242, 0], [0.181, 0], [0.303, 0], [0.303, 0]],
    [[0.06, 18.018], [0.022, 15.741], [0.075, 22.572], [0.075, 22.572]]
]
TYPE_ENUM = {"HG": 0, "SMG": 1, "RF": 2, "AR": 3, "MG": 4, "SG": 5}
ATTR_ENUM = {"hp": 0, "pow": 1, "rate": 2, "hit": 3, "dodge": 4, "armor": 5}


def calculate(lv, attr_type, doll):
    mod = 1
    if lv <= 100:
        mod = 0
    guntype = doll['type'] - 1
    attr = ATTR_ENUM[attr_type]
    ratio = doll[f'ratio_{attr_type}'] if attr_type!='hp' else doll[f'ratio_life']
    growth = doll['eat_ratio']

    if attr == 0 or attr == 5:
        return math.ceil(
            (BASIC_LIFE_ARMOR[mod][attr & 1][0] + (lv-1)*BASIC_LIFE_ARMOR[mod][attr & 1][1]) * BASE_ATTR[guntype][attr] * ratio / 100
        )
    else:
        accretion = (GROW[mod][attr-1][1] + (lv-1)*GROW[mod][attr-1][0]) * BASE_ATTR[guntype][attr] * ratio * growth / 100 / 100
        return math.ceil(accretion)

class Equip(NamedTuple):
    var_type: tk.StringVar
    opt_type: tk.OptionMenu
    var_level: tk.IntVar
    ent_level: tk.Entry

class Positioning(tk.Frame):
    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args, **kwargs)
        for i in range(3):
            self.columnconfigure(i,weight=1,minsize=60)
        tk.Label(self, text='站位').grid(row=0,column=0,columnspan=3)
        self.posvar = {}
        for i in range(3):
            for j in range(3):
                var = tk.IntVar(value=0)
                ent = tk.Entry(self,textvariable=var)
                ent.config(width=1)
                ent.grid(sticky='ew',row=i+1,column=j)
                self.posvar[(i,j)]=var
    
    def get_pos_dict(self):
        ret = {}
        for i in range(3):
            for j in range(3):
                v = self.posvar[(i,j)].get()
                if v!=0:
                    ret[v] = j*5-i+9
        return ret

class Interface(tk.Frame):
    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args, **kwargs)
        gamedata = GameData(r'..\GF_Data_Tools\data\ch\formatted\json')

        GunPresetHeader(master=self).grid(sticky='ew')
        self.guns = {i:GunPreset(i,gamedata,master=self) for i in range(1,6)}
        for gun in self.guns.values(): gun.grid(sticky='ew')

        self.pos = Positioning(master=self)
        self.pos.grid(sticky='w',row=6)
        tk.Button(self,text='生成',command=self.generate_json).grid(sticky='e',row=6)
    
    def generate_json(self):
        pos_dict = self.pos.get_pos_dict()
        gun_full = []
        equip_full = {}
        for idx,pos in pos_dict.items():
            gun_record,equip_records = self.guns[idx].generate_records(pos)
            gun_full.append(gun_record)
            equip_full.update(equip_records)
        import json
        from pathlib import Path
        json.dump(gun_full,Path('gun_with_user_info.json').open('w'))
        json.dump(equip_full,Path('equip_with_user_info.json').open('w'))


if __name__=='__main__':
    gamedata = GameData(r'..\GF_Data_Tools\data\ch\formatted\json')
    window = tk.Tk(screenName='JsonGenerator')
    Interface().pack()
    window.mainloop()