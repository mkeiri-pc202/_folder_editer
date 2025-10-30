import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import configuration
from helpers import change_folder
from organize import classify_files

class MainGui():
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

        # # 優先順位
        # self.priority_label = tk.Label(self.frame1,text="優先順位(日付＋拡張子選択時に使用)",font=font2)
        # module = list(json_config["priority_options"].keys())
        # self.priority_combobox1 = ttk.Combobox(self.frame1,height=10, width=35,values=module)
        # self.priority_combobox1.set(json_config["options"]["priority"])
        # priority = self.priority_combobox1.get()
        # # コンボボックス変更時の処理
        # def on_select_priority(event): 
        #     nonlocal priority
        #     priority = json_config["priority_options"][self.priority_combobox1.get()]
        # self.priority_combobox1.bind("<<ComboboxSelected>>", on_select_priority)
        
        # ファイルの分け方
        self.organize_label = tk.Label(self.frame1,text="ファイルの分け方",font=font2) 
        module = list(json_config["organize_options"].keys())
        self.organize_combobox1 = ttk.Combobox(self.frame1,height=10, width=35,values=module)
        self.organize_combobox1.set(json_config["options"]["organize"])
        # 実行時のボタンにパラメータを渡すときの初期値
        organize = self.organize_combobox1.get()
        # コンボボックス変更時の処理
        def on_select_organize(event): 
            nonlocal organize
            organize = json_config["organize_options"][self.organize_combobox1.get()]
        self.organize_combobox1.bind("<<ComboboxSelected>>", on_select_organize)
        
        # チェックボックス
        check_var = tk.BooleanVar(value=json_config["options"]["option1"])
        self.option1_label  = tk.Label(self.frame1,text="実行前にバックアップを取得するか",font=font2)
        self.option1_checkbox = tk.Checkbutton(self.frame1, text="取得する", variable=check_var)
        
        ## 実行ボタン
        # 振り分けをする拡張子を取得
        extensions = json_config["config"]["extension"]
        # ファイルの作成日時でフォルダを分けるか、拡張子で分けるかの選択
        # organize = self.organize_combobox1.get()
        # option = json_config["organize_options"][organize]
        self.execute_button = tk.Button(self.frame1,text="実行",width=15,command=lambda: classify_files(self.folder_entry.get(),extensions,organize))

        # レイアウト
        self.title.grid(row=0,column=0, padx=10,pady=margin_bottom)
        self.folder_entry_label.grid(row=1, column=0)
        self.folder_entry.grid(row=1, column=1)
        self.folder_entry_button.grid(row=1, column=2,padx=margin_bottom)
        # self.priority_label.grid(row=2, column=0)
        # self.priority_combobox1.grid(row=2, column=1)
        self.organize_label.grid(row=3, column=0)
        self.organize_combobox1.grid(row=3, column=1) 
        self.option1_label.grid(row=4,column=0)
        self.option1_checkbox.grid(row=4,column=1)
        
        self.execute_button.grid(row=6,column=2)

        self.frame1.grid(row=0, column=0)
        self.root.mainloop()


app = MainGui()


