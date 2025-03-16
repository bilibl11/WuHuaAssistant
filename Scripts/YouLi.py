# 开发时间:2025/3/11 12:59
import pyautogui

from DataPack.FilePath import image_youli_path, image_getAll_path, image_task_path, \
    image_reward_path
from Utils import get_xy, auto_click


def GoYouLi():
    print("点击游历")
    avg = get_xy(image_youli_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def GetAll():
    print("点击全部领取")
    avg = get_xy(image_getAll_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

# 950 530
def ClickChallenge():
    print("点击挑战")
    pyautogui.click(pyautogui.size().width * 0.371, pyautogui.size().height * 0.368)

def ClickTask():
    print("点击任务")
    avg = get_xy(image_task_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def ClickReward():
    print("点击任务")
    avg = get_xy(image_reward_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False