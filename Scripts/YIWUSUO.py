# 开发时间:2025/1/20 17:56
import pyautogui

from DataPack.FilePath import image_yiwusuo_path, image_money_path, image_moneyGreen_path
from Utils import get_xy, auto_click


def EntryYiWuSuo():
    print("进入易物所")
    avg = get_xy(image_yiwusuo_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def Buy():
    print("买东西")
    avg = get_xy(image_moneyGreen_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def ConfirmBuy():
    print("确认购买")
    avg = get_xy(image_money_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        pyautogui.click(2035, 784)
        return False


