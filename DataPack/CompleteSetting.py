# 开发时间:2025/3/8 14:02
# 开发时间:2025/2/1 23:14
import json
import os

file_path = "complete_setting_data.json"
state_dict = {
    "company": True,
    "yiwusuo": True,
    "cleanhp": True,
    "task": True,
    "shop": True,
    "youli": True,
}

def Save():
    global state_dict # 声明变量为全局变量
    try:
        # 将字典转换为 JSON 格式，并写入本地文件
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(state_dict, json_file, indent=4)  # indent=4 使得 JSON 格式可读
        # print("complete_setting_data.json已保存")
    except Exception as e:
        print(f"保存过程中发生错误: {e}")


def Get():
    global state_dict  # 声明变量为全局变量
    # 如果不存在，就创建一个
    if not os.path.exists(file_path):
        Save()
    # 读取本地 JSON 文件并解析
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            state_dict = json.load(json_file)
            print_dict()
    except:
        print("读取complete_setting_data.json失败")

def Revise(key, value):
    # 看看是不是bool类型
    if isinstance(value, bool) is False:
        return False
    if key in state_dict:
        state_dict[key] = value
        Save()
        print("修改state_dict成功")
        return True
    else:
        return False


def print_dict():
    for key, value in state_dict.items():
        print(f"{key} {value}")