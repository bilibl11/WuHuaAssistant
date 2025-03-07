# 开发时间:2025/1/19 18:13
import subprocess
from datetime import time

import pyautogui

from DataPack.FilePath import exe_path, image_game_exe_path, image_weekTask_path, image_checkClose_path
from Scripts.GameStateServlet import JudgeMainPage
from Utils import CompareImageAndClick, get_xy, auto_click


def LaunchGame():
    process = subprocess.Popen(exe_path)
    times = 0
    while times < 20:
        if CompareImageAndClick(image_game_exe_path, "启动游戏") is False:
            print("未成功加载模拟器")
            time.sleep(5)
            times += 1
        else:
            print("启动游戏成功")
            break
    times = 0
    while times < 40:
        if JudgeMainPage():
            break
        pyautogui.click(2074, 331)
        time.sleep(5)
    print("启动游戏成功！")


def click_check_close():
    avg = get_xy(image_checkClose_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

