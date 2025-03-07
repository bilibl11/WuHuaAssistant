# 开发时间:2024/10/3 15:25
import time
from os import getcwd

import cv2
import pyautogui

from DataPack.FilePath import image_game_exe_path, image_home_path, image_YanXun_path

shot_path = "screenshot.png"


def get_xy(image_model_path):
    # 将屏幕截图保存
    pyautogui.screenshot().save(shot_path)
    # 载入截图
    image = cv2.imread(shot_path)
    # 图像模板
    image_model = cv2.imread(image_model_path)
    # 读取模板的宽度和高度
    height, width, channels = image_model.shape
    # 进行模板匹配
    result = cv2.matchTemplate(image_model, image, cv2.TM_SQDIFF_NORMED)
    # 找到最小值和它的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print("匹配值:" + "%.3f" % min_val)
    if min_val <= 0.1:
        # 解析出匹配区域的左上角坐标
        upper_left = cv2.minMaxLoc(result)[2]
        # 计算匹配区域右下角的坐标
        lower_right = (upper_left[0] + width, upper_left[1] + height)
        # 计算中心区域的坐标并且返回
        avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))
        return avg
    else:
        return None


def auto_click(avg):
    pyautogui.click(avg[0], avg[1], button='left')
    time.sleep(1)


def CompareImageAndClick(model_path, action):
    avg = get_xy(model_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def ShowPosition():
    print(pyautogui.size())
    time.sleep(3)
    print(pyautogui.position())



