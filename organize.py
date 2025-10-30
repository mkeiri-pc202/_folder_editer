import os
import shutil
from datetime import datetime


# ファイルを分類する関数
def classify_files(directory,extensions,organize):
    source_directory = directory
    destination_base = os.path.join(source_directory, 'sorted')
    
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    folder_name = 'backup' + str(now)
    backup_directory = os.path.join(source_directory, folder_name)
    
    #ファイルがあればバックアップを取得。
    if len(os.listdir(source_directory)):
        # バックアップフォルダが存在している場合は取得しない
        if not os.path.isdir(backup_directory):
            shutil.copytree(source_directory, backup_directory)
    #ファイルがないか同じ日付のバックアップがあれば警告を出したい（とりあえずはprintを出して空のreturnで終了)
    else:
        print('対象のフォルダにファイルがない')
        return
    
    # 拡張子がjsonの指定と一致したファイルについて処理を行う。一致しない場合はcontinueで処理を飛ばす。
    for filename in os.listdir(source_directory):
        if os.path.splitext(filename)[1] not in extensions:
            continue
        else:
            group_by(source_directory, filename,destination_base,organize)

# ファイルの処理
def group_by(source_directory, filename,destination_base,organize):
    file_path = os.path.join(source_directory, filename)
    if os.path.isfile(file_path):
        # ファイルのメタデータから作成日を取得
        if organize == "date":
            date_folder = date(file_path)
        elif organize == "extension":
            date_folder = extension(file_path)
        elif organize == "date_and_extension":
            date_and_extension(file_path,destination_base)
        elif organize == "extension_and_date":
            date_and_extension(file_path,destination_base)
        
        if organize in ("date","extension"):
            # 分類先のフォルダパスを生成
            destination_folder = os.path.join(destination_base, date_folder)
            
            # 分類先のフォルダが存在しない場合は作成
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            
            # ファイルを移動
            shutil.move(file_path, destination_folder)
            print(f'Moved: {file_path} -> {destination_folder}')
        
def date(file_path):
    creation_time = os.path.getctime(file_path)
    date_folder = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
    return date_folder

def extension(file_path):
    date_folder = os.path.splitext(file_path)[1]
    return date_folder

def date_and_extension(file_path,destination_base):
    creation_time = os.path.getctime(file_path)
    date_folder = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
    destination_folder = os.path.join(destination_base, date_folder)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    destination_base = destination_folder
    date_folder = os.path.splitext(file_path)[1]
    
    # 分類先のフォルダパスを生成
    destination_folder = os.path.join(destination_base, date_folder)
        
    # 分類先のフォルダが存在しない場合は作成
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        
    # ファイルを移動
    shutil.move(file_path, destination_folder)
    print(f'Moved: {file_path} -> {destination_folder}')
    return
    
# スクリプトの実行
if __name__ == '__main__':
    source_directory = "C:\\temp"
    classify_files(source_directory,[".jpeg",".png",".jpg",".gif",".bmp"],"date_and_extension")
    # result = os.listdir(source_directory)
    # print(result)