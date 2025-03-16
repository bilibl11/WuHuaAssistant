# 开发时间:2025/3/2 13:53
import pyautogui

from DataPack.FilePath import image_JudgeMainPage_path, image_home_path, image_back_path
from Utils import get_xy, auto_click


# 判断是否在游戏主界面
def JudgeMainPage():
    avg = get_xy(image_JudgeMainPage_path)
    if avg is not None:
        return True
    else:
        return False


def ReturnMainPage():
    print("返回主页")
    if JudgeMainPage() is False:
        screenSize = pyautogui.size()
        pyautogui.click(screenSize.width * 0.265, screenSize.height * 0.175)
        return True

def Back():
    print("返回上一级")
    avg = get_xy(image_back_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False
