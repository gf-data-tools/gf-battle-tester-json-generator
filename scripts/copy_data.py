import os
import shutil

src_dir = R"..\GF_Data_Tools\data\{region}\formatted\json\{table}.json"
regions = ["ch", "tw", "jp", "kr", "us"]
tables = ["gun", "gun_exp_info", "skin", "equip", "equip_type", "fairy", "fairy_exp_info", "fairy_talent"]

for region in regions:
    dst_dir = f"data/{region}"
    os.makedirs(dst_dir, exist_ok=True)
    for table in tables:
        shutil.copy(src_dir.format(region=region, table=table), dst_dir)
