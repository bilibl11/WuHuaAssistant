import sys
import threading
import time
import subprocess
import webbrowser

import pyautogui
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QToolButton, QFrame, QWidget, QComboBox, \
    QCheckBox, QMessageBox
from pynput import mouse

from Controller.BoWu import click_bowu, click_zhuti, click_qicheng, choose_boss, choose_diffculty, click_jinyinjixing, \
    add_role, click_ok, choose_fuzhu, entry_yanxue, click_rest, add_role2, click_ok2, click_ok3, \
    enter_battleUI, click_start_battle, click_ok4, click_ok5, click_role, click_battle, click_hardBattle, click_boss, \
    finish_yanxue, click_reward, get_reward, get_own_position, continue_yanxue
from Controller.WaiQin import enter_waiqin, start_waiqin, zhengzaiwaiqin
from DataPack import Level, CompleteSetting, Path
from DataPack.FilePath import image_game_exe_path, image_KaoHe_path
from Controller import Shop, MainUIServlet, BoWu, WaiQin
from Controller.CleanHP import (
    ClickYanXun, ChooseLevel, ClickSuTong,
    AddTimes, ClickOK, ClickFinish, ClickStartTrain, ChooseRank, ChangeLevelPath, ChangeRankPath, ChangeKaoHeLevelPath
)
from Controller.DispatchCompany import (
    EntryCompany, CollectDunShe, CollectMaterial,
    ClickGift, ClickCoin, GetGanYing, GoToDunShe, GetHP, ReturnCompany
)
from Controller.GameStateServlet import ReturnMainPage, JudgeMainPage, Back
from Controller.MainUIServlet import click_check_close, get_all_json_data, click_update
from Controller.Shop import GoShop, ClickXunShi, Gobuy, BuyGift
from Controller.Task import EntryTask, ClickWeekTask, GetTaskReward
from Controller.YIWUSUO import EntryYiWuSuo, ConfirmBuy, Buy
from Controller.YouLi import GoYouLi, ClickTask, GetAll, ClickChallenge, ClickReward
from DataPack.Level import level_type
from UI import SettingUI, HelpUI
from Utils.Utils import CompareImageAndClick

# 控制线程停止 True代表停止线程
stop_thread = False
# 显示屏尺寸
ScreenSize = pyautogui.size()
# 是否是完整运行
is_complete_execution = False
# 当前页面
now_page = "MainPage"

class MainPage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.start_global_mouse_listener()

        self.dragging = False
        self.start_pos = QPoint()  # 鼠标按下时的位置
        self.last_pos = QPoint()  # 上次移动的位置

    # 全局鼠标监听（即使窗口不在前台）
    def start_global_mouse_listener(self):
        def on_click(x, y, button, pressed):
            global stop_thread
            if pressed and button == mouse.Button.right:  # 鼠标右键按下
                print("进程终止")
                stop_thread = True

        listener = mouse.Listener(on_click=on_click)
        listener_thread = threading.Thread(target=listener.start, daemon=True)
        listener_thread.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and 0 <= event.y() <= 30:
            self.dragging = True
            # 获取鼠标在屏幕坐标系中的绝对位置（例如：屏幕左上角为原点，向右为 x 正方向，向下为 y 正方向）
            self.start_pos = event.globalPos()
            self.last_pos = self.pos()
        # 再调用父类的同名方法，保留默认行为
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            # 实时更新目标位置，但不立即移动窗口
            self.target_pos = self.last_pos + (event.globalPos() - self.start_pos)
            self.move(self.target_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
        super().mouseReleaseEvent(event)

    # 顶部区域
    def create_header(self):
        # Icon
        self.icon_label = QLabel(self.central_widget)
        self.icon_label.setGeometry(10, 5, 30, 30)
        self.icon_label.setPixmap(QPixmap("picture/icon.jpg"))
        self.icon_label.setScaledContents(True)

        # Title
        self.title_label = QLabel("WuHua Assistant v1.4", self.central_widget)
        self.title_label.setGeometry(55, 5, 200, 30)
        self.title_label.setFont(QFont('Arial', 10, QFont.Bold))

        # 最小化按钮
        self.minimize_button = MainUIServlet.header_button_model(self, 1080, 0, "picture/minimize.png", self.showMinimized)

        # 关闭按钮
        self.close_button = MainUIServlet.header_button_model(self, 1140, 0, "picture/close.png", self.close)

    # 左侧区域
    def create_left_area(self):
        self.main_page_button = MainUIServlet.left_area_button_model(
            self, 0, 40, "picture/MainPage.png", "主页", lambda: self.show_main_frame()
        )
        self.help_page_button = MainUIServlet.left_area_button_model(
            self, 0, 120, "picture/help.png", "使用指南", lambda: self.show_help_frame()
        )
        self.wiki_button = MainUIServlet.left_area_button_model(
            self, 0, 200, "picture/wiki.png", "打开wiki", lambda: self.open_wiki()
        )
        self.start_button = MainUIServlet.left_area_button_model(
            self, 0, 760, "picture/launch.png", "启动游戏", lambda: self.launch_game()
        )
        self.setting_page_button = MainUIServlet.left_area_button_model(
            self, 0, 840, "picture/install.png", "设置", lambda: self.show_setting_frame()
        )

    # 主界面(右侧界面)
    def create_main_frame(self):
        self.main_frame = QFrame(self.central_widget)
        self.main_frame.setGeometry(80, 40, 1120, 910)

        # 主界面图片
        self.image_label = QLabel(self.main_frame)
        self.image_label.setGeometry(0, 0, 1120, 600)
        self.image_label.setPixmap(QPixmap("picture/MainPageImage.jpg"))
        self.image_label.setScaledContents(True)

        # 右侧按钮
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.all_process_button = MainUIServlet.right_area_button_model(
            self, 70, 630, "picture/AllProcess.jpg", "完整运行",
            lambda: self.complete_execution()
        )
        self.clean_hp_button = MainUIServlet.right_area_button_model(
            self, 320, 630, "picture/CleanHP.jpg", "清理体力",
            lambda: self.clean_hp()
        )
        self.company_button = MainUIServlet.right_area_button_model(
            self, 570, 630, "picture/Company.jpg", "派遣公司",
            lambda: self.dispatch_company()
        )
        self.bowu_button = MainUIServlet.right_area_button_model(
            self, 820, 630, "picture/BoWU.jpg", "博物研学",
            lambda: self.bowu()
        )

    # ui初始化
    def setup_ui(self):
        self.setFixedSize(1200, 950)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('picture/icon.jpg'))
        get_all_json_data()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.create_header()
        self.create_left_area()
        self.create_main_frame()
        self.help_frame = HelpUI.create_help_frame(self)
        self.setting_frame = SettingUI.create_setting_frame(self)

        self.setting_frame.hide()
        self.help_frame.hide()
        self.show_main_frame()

    def show_main_frame(self):
        if self.main_frame.isVisible() is False:
            global now_page
            last_page = now_page
            now_page = "MainPage"
            self.page_switch(last_page)

    def show_setting_frame(self):
        if self.setting_frame.isVisible() is False:
            # 切换界面
            global now_page
            last_page = now_page
            now_page = "SettingPage"
            self.page_switch(last_page)
            # 读取当前选择的数据
            Level.Get()

    def show_help_frame(self):
        if self.help_frame.isVisible() is False:
            # 切换界面
            global now_page
            last_page = now_page
            now_page = "HelpPage"
            self.page_switch(last_page)

    def page_switch(self, last_page):
        if last_page == "MainPage":
            self.main_frame.hide()
            self.main_page_button.setStyleSheet("""
                 QToolButton {
                     border-left: 0px solid rgba(255, 105, 180, 255);
                     border-radius: 0px;  /* 圆角 */
                     background-color: rgba(255, 255, 255, 255);  /* 背景颜色 */
                 }
                 QToolButton:hover { 
                 }
                 QToolButton:pressed {
                     background-color: rgba(255, 105, 180, 100);  /* 按下时背景颜色 */
                 }
             """)
        elif last_page == "SettingPage":
            self.setting_frame.hide()
            self.setting_page_button.setStyleSheet("""
                 QToolButton {
                     border-left: 0px solid rgba(255, 105, 180, 255);
                     border-radius: 0px;  /* 圆角 */
                     background-color: rgba(255, 255, 255, 255);  /* 背景颜色 */
                 }
                 QToolButton:hover { 
                 }
                 QToolButton:pressed {
                     background-color: rgba(255, 105, 180, 100);  /* 按下时背景颜色 */
                 }
             """)
        elif last_page == "HelpPage":
            self.help_frame.hide()
            self.help_page_button.setStyleSheet("""
                 QToolButton {
                     border-left: 0px solid rgba(255, 105, 180, 255);
                     border-radius: 0px;  /* 圆角 */
                     background-color: rgba(255, 255, 255, 255);  /* 背景颜色 */
                 }
                 QToolButton:hover { 
                 }
                 QToolButton:pressed {
                     background-color: rgba(255, 105, 180, 100);  /* 按下时背景颜色 */
                 }
             """)
        if now_page == "MainPage":
            self.main_frame.show()
            self.main_page_button.setStyleSheet("""
                 QToolButton {
                     border-left: 5px solid rgba(255, 105, 180, 255);  /* 粉色左边边框 */
                     border-radius: 0px;  /* 圆角 */
                     background-color: rgba(255, 255, 255, 255);  /* 背景颜色 */
                 }
                 QToolButton:hover { 
                 }
                 QToolButton:pressed {
                     background-color: rgba(255, 105, 180, 100);  /* 按下时背景颜色 */
                 }
             """)
        elif now_page == "SettingPage":
            self.setting_frame.show()
            self.setting_page_button.setStyleSheet("""
                  QToolButton {
                     border-left: 5px solid rgba(255, 105, 180, 255);  /* 粉色左边边框 */
                     border-radius: 0px;  /* 圆角 */
                     background-color: rgba(255, 255, 255, 255);  /* 背景颜色 */
                 }
                 QToolButton:hover { 
                 }
                 QToolButton:pressed {
                     background-color: rgba(255, 105, 180, 100);  /* 按下时背景颜色 */
                 }
             """)
        elif now_page == "HelpPage":
            self.help_frame.show()
            self.help_page_button.setStyleSheet("""
                 QToolButton {
                     border-left: 5px solid rgba(255, 105, 180, 255);  /* 粉色左边边框 */
                     border-radius: 0px;  /* 圆角 */
                     background-color: rgba(255, 255, 255, 255);  /* 背景颜色 */
                 }
                 QToolButton:hover { 
                 }
                 QToolButton:pressed {
                     background-color: rgba(255, 105, 180, 100);  /* 按下时背景颜色 */
                 }
             """)

    # 打开wiki
    def open_wiki(self):
        url = "https://wiki.biligame.com/whmx/%E9%A6%96%E9%A1%B5"
        # 方式3：在新标签页中打开（如果浏览器支持）
        webbrowser.open_new_tab(url)

    # 启动并进入游戏
    def launch_game(self):
        global stop_thread
        stop_thread = False
        for i in range(3):
            if stop_thread is True:
                break
            time.sleep(1)
        if stop_thread is True:
            time.sleep(1)
            self.raise_()  # 让窗口置顶
            self.activateWindow()  # 激活窗口
            time.sleep(1)
            QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
        print("启动游戏")
        if Path.exe_path == "":
            self.raise_()  # 让窗口置顶
            self.activateWindow()  # 激活窗口
            time.sleep(1)
            QMessageBox.information(self, '', '模拟器路径为空，进程已停止', QMessageBox.Ok)
            return
        subprocess.Popen(Path.exe_path)
        self.start_button.setEnabled(False)
        time.sleep(1)
        # 如果游戏已经启动
        if JudgeMainPage():
            print("启动游戏成功！")
            return
        times = 0
        while times < 20 and stop_thread is False:
            if CompareImageAndClick(image_game_exe_path, "启动游戏") is False:
                print("未成功加载模拟器")
                time.sleep(5)
                times += 1
            else :
                print("成功点击游戏图标")
                break
        if times >= 20:
            QMessageBox.information(self, '', '未找到游戏，进程已停止', QMessageBox.Ok)
            return
        time.sleep(15)
        times = 0
        while times < 40 and stop_thread is False:
            # 判断是否成功启动游戏
            if JudgeMainPage():
                time.sleep(1)
                print("启动游戏成功！")
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '启动游戏成功！', QMessageBox.Ok)
                return
            # 检测游戏是否需要更新
            if times >= 5 and click_update() is True:
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '检测到游戏需要更新，进程已停止', QMessageBox.Ok)
                return
            time.sleep(1)
            # 2560 1440
            pyautogui.click(ScreenSize.width * 0.81, ScreenSize.height * 0.229)
            time.sleep(1)
            if JudgeMainPage():
                time.sleep(1)
                print("启动游戏成功！")
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '启动游戏成功！', QMessageBox.Ok)
                return
            time.sleep(2)
            click_check_close()
            times += 1
        self.raise_()  # 让窗口置顶
        self.activateWindow()  # 激活窗口
        time.sleep(1)
        QMessageBox.information(self, '', '启动游戏失败，进程已停止', QMessageBox.Ok)

    # 完整运行
    def complete_execution(self):
        if Path.exe_path == "":
            self.raise_()  # 让窗口置顶
            self.activateWindow()  # 激活窗口
            time.sleep(1)
            QMessageBox.information(self, '', '模拟器路径为空，进程已停止', QMessageBox.Ok)
        subprocess.Popen(Path.exe_path)
        global stop_thread, is_complete_execution
        is_complete_execution = True
        stop_thread = False
        for i in range(3):
            if stop_thread is True:
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
                return
            time.sleep(1)
        # 检查是否在主界面
        print("检查是否在主界面")
        if JudgeMainPage() is False:
            self.raise_()  # 让窗口置顶
            self.activateWindow()  # 激活窗口
            time.sleep(1)
            QMessageBox.information(self, '', '请将游戏打开到主界面再启动脚本，进程已停止', QMessageBox.Ok)
            return
        if CompleteSetting.state_dict["company"] is True and stop_thread is False:
            print("dispatch_company")
            self.dispatch_company()
            time.sleep(3)
            if JudgeMainPage() is False:
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '脚本运行异常，错误函数：dispatch_company，进程已停止', QMessageBox.Ok)
                return
        if CompleteSetting.state_dict["cleanhp"] is True and stop_thread is False:
            self.clean_hp()
            time.sleep(3)
            if JudgeMainPage() is False:
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '脚本运行异常，错误函数：clean_hp，进程已停止', QMessageBox.Ok)
                return
        if CompleteSetting.state_dict["yiwusuo"] is True and stop_thread is False:
            self.yiwusuo()
            time.sleep(3)
            if JudgeMainPage() is False:
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '脚本运行异常，错误函数：yiwusuo，进程已停止', QMessageBox.Ok)
                return
        if  CompleteSetting.state_dict["task"] is True and stop_thread is False:
            self.get_task()
            time.sleep(3)
            if JudgeMainPage() is False:
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '脚本运行异常，错误函数：get_task，进程已停止', QMessageBox.Ok)
                return
        if  CompleteSetting.state_dict["shop"] is True and stop_thread is False:
            self.youli()
            time.sleep(3)
            if JudgeMainPage() is False:
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '脚本运行异常，错误函数：youli，进程已停止', QMessageBox.Ok)
                return
        if  CompleteSetting.state_dict["youli"]is True and stop_thread is False:
            self.shop()
            time.sleep(3)
            if JudgeMainPage() is False:
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '脚本运行异常，错误函数：shop，进程已停止', QMessageBox.Ok)
                return
        if  CompleteSetting.state_dict["waiqin"]is True and stop_thread is False:
            self.waiqin()
            time.sleep(3)
            if JudgeMainPage() is False:
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '脚本运行异常，错误函数：waiqin，进程已停止', QMessageBox.Ok)
                return
        is_complete_execution = False
        self.raise_()  # 让窗口置顶
        self.activateWindow()  # 激活窗口
        time.sleep(1)
        if stop_thread is True:
            QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
        else:
            QMessageBox.information(self, '', '完整运行结束', QMessageBox.Ok)

    # 派遣公司
    def dispatch_company(self):
        global stop_thread
        stop_thread = False
        for i in range(3):
            if stop_thread is True:
                QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
                return
            time.sleep(1)
        print("派遣公司")
        subprocess.Popen(Path.exe_path)  # 打开游戏界面
        time.sleep(1)
        # 检查是否在主界面
        print("检查是否在主界面")
        if JudgeMainPage() is False:
            QMessageBox.information(self, '', '请将游戏打开到主界面再启动脚本，进程已停止', QMessageBox.Ok)
            return
        else:
            time.sleep(2.5)
        EntryCompany()
        time.sleep(5)
        GetGanYing()
        time.sleep(2)
        # 1200 400（空白处）
        pyautogui.click(ScreenSize.width * 0.469, ScreenSize.height * 0.156)
        time.sleep(1)
        CollectMaterial()
        time.sleep(2)
        pyautogui.click(ScreenSize.width * 0.469, ScreenSize.height * 0.278)
        CollectDunShe()
        time.sleep(2)
        pyautogui.click(ScreenSize.width * 0.469, ScreenSize.height * 0.278)
        time.sleep(1)
        # 顿舍
        GoToDunShe()
        time.sleep(2)
        GetHP()
        time.sleep(1)
        ReturnCompany()
        time.sleep(1)
        # 办公室
        pyautogui.click(ScreenSize.width * 0.41, ScreenSize.height * 0.33)
        time.sleep(1)                                       
        if ClickGift() is False:
            ReturnMainPage()
        time.sleep(1)
        ClickCoin()
        time.sleep(3)
        pyautogui.click(ScreenSize.width * 0.469, ScreenSize.height * 0.417)
        time.sleep(3)
        pyautogui.click(ScreenSize.width * 0.469, ScreenSize.height * 0.417)
        ReturnMainPage()
        time.sleep(1)
        if is_complete_execution is False:
            self.raise_()  # 让窗口置顶
            self.activateWindow()  # 激活窗口
            time.sleep(1)
            QMessageBox.information(self, '', '脚本运行结束', QMessageBox.Ok)

    # 博物研学
    def bowu(self):
        global stop_thread
        stop_thread = False
        for i in range(3):
            if stop_thread is True:
                QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
                return
            time.sleep(1)
        subprocess.Popen(Path.exe_path)  # 打开游戏界面
        time.sleep(1)
        # 检查是否在主界面
        print("检查是否在主界面")
        if JudgeMainPage() is False:
            self.raise_()  # 让窗口置顶
            self.activateWindow()  # 激活窗口
            time.sleep(1)
            QMessageBox.information(self, '', '请将游戏打开到主界面再启动脚本，进程已停止', QMessageBox.Ok)
            return
        # 操作开始, 进入博物研学关卡
        click_bowu()
        time.sleep(0.5)
        pyautogui.click(ScreenSize.width * 0.49, ScreenSize.height * 0.3125)
        time.sleep(1)
        click_jinyinjixing()
        time.sleep(0.5)
        click_zhuti()
        time.sleep(0.5)
        if continue_yanxue() is True:
            time.sleep(1)
        else:
            click_qicheng()
            time.sleep(0.5)
            choose_boss()
            time.sleep(0.5)
            choose_diffculty()
            time.sleep(0.5)
            add_role()
            time.sleep(0.5)
            #选择角色 width=2560, height=1440
            pyautogui.click(ScreenSize.width * 0.45, ScreenSize.height * 0.3125)
            time.sleep(0.5)
            pyautogui.click(ScreenSize.width * 0.45, ScreenSize.height * 0.659)
            time.sleep(0.5)
            pyautogui.click(ScreenSize.width * 0.527, ScreenSize.height * 0.29)
            time.sleep(0.5)
            pyautogui.click(ScreenSize.width * 0.527, ScreenSize.height * 0.625)
            time.sleep(0.5)
            click_ok()
            time.sleep(0.5)
            choose_fuzhu()
            time.sleep(0.5)
            entry_yanxue()
            time.sleep(3)
        # 进行关卡挂机
        self.bowu_level_strategy()

    # 博物研学关卡策略
    def bowu_level_strategy(self):
        # 策略：先补满队伍的人
        for i in range(20):
            time.sleep(2)
            own_position = get_own_position()
            print(f"own_position = {own_position}")
            if own_position is None:
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', 'own_position为空，进程已停止', QMessageBox.Ok)
                return
            if own_position[0] > ScreenSize.width * 0.5:
                print("需要滑动窗口：")
                target_x = own_position[0] - 200
                target_y = own_position[1]
                pyautogui.mouseDown(x=own_position[0], y=own_position[1], button='left')
                # 可选：添加短暂延迟，确保鼠标按下动作完成
                time.sleep(0.1)
                pyautogui.moveTo(target_x, target_y, duration=0.2)
                pyautogui.mouseUp(button='left')
            time.sleep(1)
            if click_role() is True:
                print("选择添加角色：")
                time.sleep(1)
                # 点击添加角色
                click_ok2()
                time.sleep(0.5)
                add_role2()
                time.sleep(0.5)
                pyautogui.click(ScreenSize.width * 0.45, ScreenSize.height * 0.3125)
                time.sleep(1)
                click_ok()
                time.sleep(1)
                # 点击确认
                click_ok3()
                time.sleep(1)
                BoWu.roles += 1
                continue
            if click_battle() is True:
                print("选择战斗：")
                time.sleep(1)
                click_ok2()
                time.sleep(1)
                enter_battleUI()
                time.sleep(15)
                for j in range(6):
                    time.sleep(3)
                    if click_start_battle() is True:
                        print("成功开始战斗")
                        break
                for k in range(100):
                    time.sleep(5)
                    if click_ok4() is True:
                        break
                    else:
                        print(f"还在战斗中{k}")
                time.sleep(5)
                pyautogui.click(ScreenSize.width * 0.5, ScreenSize.height * 0.5)
                time.sleep(0.5)
                click_ok5()
                time.sleep(1)
                click_ok5()
                continue
            if click_hardBattle() is True:
                print("选择精英战：")
                time.sleep(1)
                click_ok2()
                time.sleep(3)
                enter_battleUI()
                for j in range(6):
                    time.sleep(3)
                    if click_start_battle() is True:
                        print("成功开始战斗")
                        break
                for k in range(100):
                    time.sleep(5)
                    if click_ok4() is True:
                        break
                    else:
                        print(f"还在战斗中{k}")
                time.sleep(5)
                pyautogui.click(ScreenSize.width * 0.5, ScreenSize.height * 0.5)
                time.sleep(1)
                click_ok5()
                time.sleep(1)
                pyautogui.click(ScreenSize.width * 0.5, ScreenSize.height * 0.5)
                time.sleep(1)
                click_ok5()
                time.sleep(1)
                pyautogui.click(ScreenSize.width * 0.5, ScreenSize.height * 0.5)
                time.sleep(1)
                click_ok5()
                continue
            if click_rest() is True:
                print("选择休息：")
                time.sleep(1)
                click_ok2()
                time.sleep(1)
                click_ok5()
                time.sleep(1)
                continue
            if click_boss() is True:
                print("选择boss战：")
                time.sleep(1)
                click_ok2()
                time.sleep(3)
                enter_battleUI()
                for j in range(6):
                    time.sleep(3)
                    if click_start_battle() is True:
                        print("成功开始战斗")
                        break
                for k in range(100):
                    time.sleep(5)
                    if click_ok4() is True:
                        break
                    else:
                        print(f"还在战斗中{k}")
                time.sleep(3)
                finish_yanxue()
                time.sleep(2)
                click_reward()
                time.sleep(1)
                get_reward()
                time.sleep(1)
                pyautogui.click(ScreenSize.width * 0.515, ScreenSize.height * 0.29)
                time.sleep(1)
                pyautogui.click(ScreenSize.width * 0.515, ScreenSize.height * 0.29)
                ReturnMainPage()
                time.sleep(1)
                self.raise_()  # 让窗口置顶
                self.activateWindow()  # 激活窗口
                time.sleep(1)
                QMessageBox.information(self, '', '博物研学挂机结束', QMessageBox.Ok)
                return


    # 易物所
    def yiwusuo(self):
        global stop_thread
        stop_thread = False
        for i in range(3):
            if stop_thread is True:
                QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
                return
            time.sleep(1)
        EntryYiWuSuo()
        time.sleep(0.5)
        for i in range(2):
            Buy()
            time.sleep(0.5)
            ConfirmBuy()
            time.sleep(1.5)
            pyautogui.click(ScreenSize.width * 0.469, ScreenSize.height * 0.417)
            time.sleep(0.5)
        ReturnMainPage()

    # 领取任务奖励
    def get_task(self):
        global stop_thread
        stop_thread = False
        for i in range(3):
            if stop_thread is True:
                QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
                return
            time.sleep(1)
        print("领取任务")
        #进入任务界面
        EntryTask()
        time.sleep(0.5)
        GetTaskReward()
        time.sleep(1)
        pyautogui.click(ScreenSize.width*0.515, ScreenSize.height*0.29)
        time.sleep(1)
        pyautogui.click(ScreenSize.width*0.515, ScreenSize.height*0.29)
        time.sleep(1)
        ClickWeekTask()
        time.sleep(0.5)
        GetTaskReward()
        time.sleep(1)
        pyautogui.click(ScreenSize.width*0.515, ScreenSize.height*0.29)
        time.sleep(1)
        pyautogui.click(ScreenSize.width*0.515, ScreenSize.height*0.29)
        time.sleep(1)
        ReturnMainPage()

    # 清理体力
    def clean_hp(self):
        global stop_thread
        stop_thread = False
        for i in range(3):
            if stop_thread is True:
                QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
                return
            time.sleep(1)
        level_path = ChangeLevelPath()
        rank_path = ChangeRankPath(level_path)
        times = Level.level_times
        print("清理体力")
        process = subprocess.Popen(Path.exe_path)  # 打开游戏界面
        time.sleep(1)
        ClickYanXun()
        time.sleep(1)
        ClickStartTrain()
        time.sleep(1)
        ChooseLevel(level_path)
        time.sleep(1)
        # 如果是考核本，需要多点一下
        if level_path == image_KaoHe_path:
            print("考核本")
            level_path = ChangeKaoHeLevelPath()
            ChooseLevel(level_path)
            time.sleep(1)
        ChooseRank(level_path, rank_path)
        time.sleep(1)
        # 速通
        ClickSuTong()
        time.sleep(2)
        # 选择次数
        AddTimes(times)
        time.sleep(0.5)
        ClickOK()
        time.sleep(1)
        # 可能出现器者好感度已满提醒
        ClickOK()
        time.sleep(2)
        pyautogui.click(1200, 600)
        time.sleep(1)
        ClickFinish()
        time.sleep(2)
        if times > 10:
            ClickSuTong()
            time.sleep(2)
            # 选择次数
            AddTimes((times - 10))
            time.sleep(0.5)
            ClickOK()
            time.sleep(1)
            # 可能出现器者好感度已满提醒
            ClickOK()
            time.sleep(1)
            pyautogui.click(1200, 600)
            time.sleep(1)
            ClickFinish()
            time.sleep(2)
        ReturnMainPage()
        time.sleep(1)
        if is_complete_execution is False:
            self.raise_()  # 让窗口置顶
            self.activateWindow()  # 激活窗口
            time.sleep(1)
            QMessageBox.information(self, '', '清理体力成功！', QMessageBox.Ok)

    # 商亭
    def shop(self):
        global stop_thread
        stop_thread = False
        for i in range(3):
            if stop_thread is True:
                QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
                return
            time.sleep(1)
        GoShop()
        time.sleep(1)
        Shop.ClickGift()
        time.sleep(1)
        ClickXunShi()
        time.sleep(1)
        Gobuy()
        time.sleep(1)
        BuyGift()
        time.sleep(3)
        pyautogui.click(ScreenSize.width * 0.515, ScreenSize.height * 0.29)
        time.sleep(1)
        ReturnMainPage()

    # 游历
    def youli(self):
        global stop_thread
        stop_thread = False
        for i in range(3):
            if stop_thread is True:
                QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
                return
            time.sleep(1)
        GoYouLi()
        time.sleep(1)
        ClickTask()
        time.sleep(1)
        GetAll()
        time.sleep(1)
        # 1200 400（空白处）
        pyautogui.click(ScreenSize.width * 0.469, ScreenSize.height * 0.156)
        time.sleep(1)
        ClickChallenge()
        time.sleep(1)
        GetAll()
        time.sleep(1)
        # 1200 400（空白处）
        pyautogui.click(ScreenSize.width * 0.469, ScreenSize.height * 0.156)
        time.sleep(1)
        ClickReward()
        time.sleep(1)
        GetAll()
        time.sleep(1)
        # 1200 400（空白处）
        pyautogui.click(ScreenSize.width * 0.469, ScreenSize.height * 0.156)
        Back()

    # 外勤
    def waiqin(self):
        global stop_thread
        stop_thread = False
        for i in range(3):
            if stop_thread is True:
                QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
                return
            time.sleep(1)
        ClickYanXun()
        time.sleep(1)
        enter_waiqin()
        time.sleep(1)
        if zhengzaiwaiqin() is True:
            time.sleep(1)
            ReturnMainPage()
            return
        start_waiqin()
        time.sleep(1)
        WaiQin.click_ok()
        time.sleep(1.5)
        ReturnMainPage()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec())
