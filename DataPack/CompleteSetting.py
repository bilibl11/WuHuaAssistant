# 开发时间:2025/3/8 14:02
# 开发时间:2025/2/1 23:14
import json
import os

file_path = "complete_setting_data.json"
company: bool = True
yiwusuo: bool = True
cleanhp: bool = True
task: bool = True


def Save():
    global company, yiwusuo, cleanhp, task  # 声明变量为全局变量
    try:
        data = {
            "company": company,
            "yiwusuo": yiwusuo,
            "cleanhp": cleanhp,
            "task": task
        }
        # 将字典转换为 JSON 格式，并写入本地文件
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)  # indent=4 使得 JSON 格式可读
        print("complete_setting_data.json已保存")
    except Exception as e:
        print(f"保存过程中发生错误: {e}")


def Get():
    global company, yiwusuo, cleanhp, task  # 声明变量为全局变量
    # 如果不存在，就创建一个
    if not os.path.exists(file_path):
        Save()
    # 读取本地 JSON 文件并解析
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    company = data["company"]
    yiwusuo = data["yiwusuo"]
    cleanhp = data["cleanhp"]
    task = data["task"]
    print("成功读取complete_setting_data.json")
