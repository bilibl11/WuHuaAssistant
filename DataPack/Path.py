#开发时间:2025/7/6 18:02
# 开发时间:2025/2/1 23:14
import json
import os

file_path = "path.json"

exe_path = ""



def Save():
    global exe_path  # 声明变量为全局变量
    try:
        data = {
            "exe_path": exe_path,
        }
        # 将字典转换为 JSON 格式，并写入本地文件
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)  # indent=4 使得 JSON 格式可读
        print("path.json已保存")
    except Exception as e:
        print(f"保存过程中发生错误: {e}")


def Get():
    global exe_path  # 声明变量为全局变量
    if not os.path.exists(file_path):
        Save()
    # 读取本地 JSON 文件并解析
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    exe_path = data["exe_path"]
    print("成功读取path.json")
