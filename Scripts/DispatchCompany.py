# 开发时间:2024/10/4 23:40
import subprocess
import sys
import time

import pyautogui

from DataPack.FilePath import image_game_exe_path, image_company_path, image_collect_path, image_DunShe_path, \
    image_office_path, image_gift_path, image_coin_path, image_getGanYing_path, image_enterDunShe_path, \
    image_getHP_path, image_return_path
from Scripts.GameStateServlet import ReturnMainPage
from Utils import get_xy, auto_click


def EntryCompany():
    print("进入派遣公司")
    avg = get_xy(image_company_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def GetGanYing():
    print("获取感应")
    avg = get_xy(image_getGanYing_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def CollectMaterial():
    print("收取所有资源")
    avg = get_xy(image_collect_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


# 0.454 0.772
def CollectDunShe():
    print("收取顿舍资源")
    screenSize = pyautogui.size()
    pyautogui.click(1166, 1129)


def GoToDunShe():
    print("进入顿舍")
    avg = get_xy(image_enterDunShe_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def GetHP():
    print("收获体力")
    avg = get_xy(image_getHP_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def ReturnCompany():
    print("进入顿舍")
    avg = get_xy(image_return_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def GoToOffice():
    print("进入办公室")
    avg = get_xy(image_office_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def ClickGift():
    print("点击礼物")
    avg = get_xy(image_gift_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        ReturnMainPage()
        return False


def ClickCoin():
    print("投币")
    avg = get_xy(image_coin_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False
