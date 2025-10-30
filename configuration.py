import json
import tkinter as tk
from tkinter import messagebox,filedialog

# jsonから設定を取得する
def import_json_settings():
    with open('config.json', 'r', encoding="utf-8") as f:
        json_config = json.load(f)
    return json_config

# # リストの初期値を設定する
# def set_default_value(keys):
#     config = import_json_settings()
#     try:
#         for key,value in config[keys].items():
#             if value == config["options"]["priority"]:
#                 return key
#             else:
#                 return "リストから選択してください"
#     except:
#         return "リストから選択してください"