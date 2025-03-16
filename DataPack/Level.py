# 开发时间:2025/2/1 23:14
import json
import os

file_path = "level_data.json"
level_type = "冬谷币"
level_rank = "辰"
level_times = 10


def Save():
    global level_type, level_rank, level_times  # 声明变量为全局变量
    print(f"types: {level_type}, rank: {level_rank}, times: {level_times}")
    try:
        data = {
            "level_type": level_type,
            "level_rank": level_rank,
            "level_times": level_times
        }
        # 将字典转换为 JSON 格式，并写入本地文件
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)  # indent=4 使得 JSON 格式可读
        print("level_data.json已保存")
    except Exception as e:
        print(f"保存过程中发生错误: {e}")


def Get():
    global level_type, level_rank, level_times  # 声明变量为全局变量
    if not os.path.exists(file_path):
        Save()
        level_type = "冬谷币"
        level_rank = "辰"
        level_times = 10
    # 读取本地 JSON 文件并解析
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    level_type = data["level_type"]
    level_rank = data["level_rank"]
    level_times = data["level_times"]
    print("成功读取level_data.json")
