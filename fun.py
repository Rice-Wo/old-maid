import sys
import os
import json

# 定義全域變數
main_script_path = os.path.abspath(sys.argv[0])
main_script_directory = os.path.dirname(main_script_path)

def writeJson(file, item):
    file_path = os.path.join(main_script_directory, file + '.json')
    with open(file_path, "w+") as f:
        f.write(json.dumps(item, ensure_ascii=False, indent=4))

def readJson(file):
    file_path = os.path.join(main_script_directory, file + '.json')
    with open(file_path, "r", encoding='utf-8') as f:
        data = json.load(f)
    return data
