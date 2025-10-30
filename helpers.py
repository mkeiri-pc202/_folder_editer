import os
import tkinter as tk
from tkinter import filedialog

# フォルダ選択画面の呼び出し
def change_folder(entry_widget, path):
    folder = os.path.abspath(path)
    selected_folder = filedialog.askdirectory(initialdir=folder)
    if selected_folder:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, selected_folder)
