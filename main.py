import sys
import pyautogui as gui
import time

while True:
    time.sleep(3)  # 等待3秒
    x, y = gui.position()  # 获取当前鼠标位置
    print(x, y)
    time.sleep(0.3)  # 等待0.3秒
