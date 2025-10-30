import tkinter as tk
from tkinter import font, scrolledtext
import tkinter.ttk as ttk
import logging
import queue
import threading

import configuration
from helpers import change_folder
from organize import classify_files


# ------------------------------------------------------------
# QueueHandler: ログをGUIに送るためのハンドラ
# ------------------------------------------------------------
class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(self.format(record))  # フォーマット済み文字列を送る


# ------------------------------------------------------------
# Main GUI
# ------------------------------------------------------------
class MainGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("900x600")
        self.root.title("ファイル操作用プログラム")

        self.frame1 = tk.Frame(self.root)
        font1 = font.Font(family='Helvetica', size=20, weight='bold')
        font2 = font.Font(family='Helvetica', size=15, weight='bold')
        margin_bottom = 20

        self.title = tk.Label(self.frame1, text="ファイル操作用プログラム", font=font1)
        json_config = configuration.import_json_settings()

        # フォルダ指定
        self.folder_entry_label = tk.Label(self.frame1, text="操作対象のフォルダ", font=font2)
        self.folder_entry = tk.Entry(self.frame1, width=50)
        self.folder_entry.insert(tk.END, json_config['options']['path'])
        self.folder_entry_button = tk.Button(
            self.frame1,
            width=15,
            text="フォルダの指定",
            command=lambda: change_folder(self.folder_entry, self.folder_entry.get())
        )

        # ファイルの分け方
        self.organize_label = tk.Label(self.frame1, text="ファイルの分け方", font=font2)
        module = list(json_config["organize_options"].keys())
        self.organize_combobox1 = ttk.Combobox(self.frame1, height=10, width=35, values=module)
        self.organize_combobox1.set(json_config["options"]["organize"])
        organize = self.organize_combobox1.get()

        def on_select_organize(event):
            nonlocal organize
            organize = json_config["organize_options"][self.organize_combobox1.get()]

        self.organize_combobox1.bind("<<ComboboxSelected>>", on_select_organize)

        # 実行ボタン
        extensions = json_config["config"]["extension"]
        self.execute_button = tk.Button(
            self.frame1,
            text="実行",
            width=15,
            command=lambda: self.run_classify(self.folder_entry.get(), extensions,json_config["organize_options"][self.organize_combobox1.get()])
        )

        # ログ表示エリア
        self.log_queue = queue.Queue()
        handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger = logging.getLogger()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        # 定期的にログをチェックしてTextに反映
        self.root.after(100, self.poll_log_queue)
        
        e = ''
        for i in extensions:
            e += i.replace('.','') + ' '
                    
        self.extension_text = tk.Label(self.frame1, text=f'分類対象の拡張子  {e}', font=('Consolas', 10))

        # ---- レイアウト---- 
        self.title.grid(row=0, column=0, padx=10, pady=margin_bottom)
        self.folder_entry_label.grid(row=1, column=0)
        self.folder_entry.grid(row=1, column=1)
        self.folder_entry_button.grid(row=1, column=2, padx=margin_bottom)
        self.organize_label.grid(row=3, column=0)
        self.organize_combobox1.grid(row=3, column=1)
        self.execute_button.grid(row=6, column=2)
        self.frame1.grid(row=0, column=0)

        # ログ表示エリア
        self.log_text = scrolledtext.ScrolledText(self.frame1, height=20, width=110, state='disabled', font=('Consolas', 10))
        self.log_text.grid(row=7, column=0, columnspan=3, pady=10)

        self.extension_text.grid(row=8, column=0, columnspan=3)
        
        self.root.mainloop()

    # ------------------------------------------------------------
    # ログキュー監視
    # ------------------------------------------------------------
    def poll_log_queue(self):
        while not self.log_queue.empty():
            record = self.log_queue.get()
            self.log_text.configure(state='normal')
            self.log_text.insert(tk.END, record + '\n')
            self.log_text.configure(state='disabled')
            self.log_text.yview(tk.END)
        self.root.after(100, self.poll_log_queue)

    # ------------------------------------------------------------
    # 実行ボタン押下時の動作（別スレッド）
    # ------------------------------------------------------------
    def run_classify(self, folder, extensions, organize):
        threading.Thread(
            target=self._run_classify_thread, 
            args=(folder, extensions, organize),
            daemon=True
        ).start()

    def _run_classify_thread(self, folder, extensions, organize):
        self.logger.info("分類処理を開始します...")
        try:
            classify_files(folder, extensions, organize)
            self.logger.info("分類処理が完了しました。")
        except Exception as e:
            self.logger.error(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    app = MainGui()
