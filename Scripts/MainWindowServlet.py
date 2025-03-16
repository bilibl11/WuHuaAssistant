# 开发时间:2025/1/19 18:13
import subprocess
from datetime import time

import pyautogui

from DataPack.FilePath import exe_path, image_game_exe_path, image_weekTask_path, image_checkClose_path
from Scripts.GameStateServlet import JudgeMainPage
from Utils import CompareImageAndClick, get_xy, auto_click



def click_check_close():
    avg = get_xy(image_checkClose_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

