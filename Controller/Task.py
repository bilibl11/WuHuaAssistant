# 开发时间:2025/1/20 16:24
# 点击任务
import pyautogui

from DataPack.FilePath import image_weekTask_path, image_getTask_path
from Utils.Utils import get_xy, auto_click


def EntryTask():
    print("进入任务界面")
    pyautogui.click(2100, 1200)

def ClickWeekTask():
    print("点击周常任务")
    avg = get_xy(image_weekTask_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def GetTaskReward():
    print("领取奖励")
    avg = get_xy(image_getTask_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False
