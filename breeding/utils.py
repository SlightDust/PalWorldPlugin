import json
import os
from typing import Dict, List

from .pal_class import PalChar


# 读取文件并解析
def read_data() -> Dict[str, PalChar]:
    characters = {}
    with open(os.path.join(os.path.dirname(__file__), 'base_data', 'pal_data.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
        for key, value in data.items():
            character = PalChar(
                value['pal_id'], value['number'], value['en_name'], value['cn_name'], value['power'], value['alias']
            )
            characters[key] = character
    return characters


# 获取角色索引
def read_index() -> list:
    with open(os.path.join(os.path.dirname(__file__), 'base_data', 'char_index.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
    return list(data)


# 获取特殊配表
def read_special() -> dict:
    with open(os.path.join(os.path.dirname(__file__), 'base_data', 'special_data.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
    return dict(data)


# 寻找最接近的前后两条数据
def find_nearest_power(special_data: dict, pal_data: Dict[str, PalChar], power: float) -> (PalChar, PalChar):
    sorted_data = sorted(pal_data.values(), key=lambda x: x.power)
    # 寻找最接近的前一条数据
    prev_data = None
    for data in sorted_data:
        # 去除特殊
        if data.pal_id in special_data:
            continue
        if data.power <= power:
            prev_data = data
        else:
            break
    # 寻找最接近的后一条数据
    next_data = None
    for data in sorted_data[::-1]:
        # 去除特殊
        if data.pal_id in special_data:
            continue
        if data.power >= power:
            next_data = data
        else:
            break
    return prev_data, next_data


# 先找特殊表
def find_child_by_special(
        special_data: Dict[str, List[str]],
        pal_data: Dict[str, PalChar],
        mother_id: str,
        father_id: str) -> PalChar:
    pal_char = None
    for key, value_list in special_data.items():
        if mother_id in value_list and father_id in value_list:
            pal_char = pal_data.get(key, None)
            break
    return pal_char


# 根据名字和别称寻找唯一
def find_char_by_raw_name(raw_name: str) -> PalChar:
    pal_data = read_data()
    pal_char = None
    for _, value in pal_data.items():
        if raw_name == value.en_name or raw_name == value.cn_name:
            pal_char = value
            break
        for alias in value.alias:
            if raw_name == alias:
                pal_char = value
                break
    return pal_char