import sys
import threading
import time
import subprocess

import pyautogui
from PyQt5.QtCore import Qt, QSize, QEvent, QPoint, QObject
from PyQt5.QtGui import QPixmap, QIcon, QFont, QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QToolButton, QFrame, QWidget, QComboBox, \
    QCheckBox, QMessageBox
from pynput import mouse

from DataPack import Level, CompleteSetting
from DataPack.FilePath import exe_path, image_game_exe_path, image_PeiYang_Chen_path, image_KaoHe_path
from Scripts import Shop
from Scripts.CleanHP import (
    ClickYanXun, ChooseLevel, ClickSuTong,
    AddTimes, ClickOK, ClickFinish, ClickStartTrain, ChooseRank, ChangeLevelPath, ChangeRankPath, ChangeKaoHeLevelPath
)
from Scripts.DispatchCompany import (
    EntryCompany, CollectDunShe, CollectMaterial,
    ClickGift, ClickCoin, GetGanYing, GoToDunShe, GetHP, ReturnCompany
)
from Scripts.GameStateServlet import ReturnMainPage, JudgeMainPage, Back
from Scripts.MainWindowServlet import click_check_close
from Scripts.Shop import GoShop, ClickXunShi, Gobuy, BuyGift
from Scripts.Task import EntryTask, ClickWeekTask, GetTaskReward
from Scripts.YIWUSUO import EntryYiWuSuo, ConfirmBuy, Buy
from Scripts.YouLi import GoYouLi, ClickTask, GetAll, ClickChallenge, ClickReward
from Utils import CompareImageAndClick

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
        self.dragging = False  # 是否正在拖动
        self.offset = QPoint()  # 鼠标按下时的偏移量
        self.start_global_mouse_listener()

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

    # 重写拖动事件
    def mousePressEvent(self, event):
        # 如果鼠标按下的是左键
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()  # 记录鼠标按下时的位置

    def mouseMoveEvent(self, event):
        # 如果正在拖动，则移动窗口
        if self.dragging:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        # 鼠标释放时停止拖动
        if event.button() == Qt.LeftButton:
            self.dragging = False

    # 顶部区域
    def create_header(self):
        # Icon
        self.icon_label = QLabel(self.central_widget)
        self.icon_label.setGeometry(10, 5, 30, 30)
        self.icon_label.setPixmap(QPixmap("picture/icon.jpg"))
        self.icon_label.setScaledContents(True)

        # Title
        self.title_label = QLabel("WuHua Assistant v1.3", self.central_widget)
        self.title_label.setGeometry(55, 5, 200, 30)
        self.title_label.setFont(QFont('Arial', 10, QFont.Bold))

        # 最小化按钮
        self.minimize_button = self.header_button_model(1080, 0, "picture/minimize.png", self.showMinimized)

        # 关闭按钮
        self.close_button = self.header_button_model(1140, 0, "picture/close.png", self.close)

    # 最小化和关闭按钮模板
    def header_button_model(self, x, y, picture_path, callback=None):
        button = QPushButton(self.central_widget)
        button.setGeometry(x, y, 60, 40)
        button.setIcon(QIcon(picture_path))
        if callback:
            button.clicked.connect(callback)
        button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;  /* 圆角 */
                border: none;  /* 去掉边框 */
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: white;  /* 悬停时背景透明 */
            }
        """)
        return button

    # 左侧区域
    def create_left_area(self):
        self.main_page_button = self.left_area_button_model(
            0, 40, "picture/MainPage.png", "主页", lambda: self.show_main_frame()
        )
        self.help_page_button = self.left_area_button_model(
            0, 120, "picture/help.png", "使用指南", lambda: self.show_help_frame()
        )
        self.start_button = self.left_area_button_model(
            0, 760, "picture/launch.png", "启动游戏", lambda: self.launch_game()
        )
        self.setting_page_button = self.left_area_button_model(
            0, 840, "picture/install.png", "设置", lambda: self.show_setting_frame()
        )

    # 左侧区域按钮模板
    def left_area_button_model(self, x, y, icon_path, text, callback=None):
        button = QToolButton(self.central_widget)
        button.setGeometry(x, y, 80, 80)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(50, 50))
        button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        button.setText(text)
        button.setStyleSheet("""
            QToolButton {
                padding-left: 5px;
                border-radius: 0px;  /* 圆角 */
                background-color: rgba(255, 255, 255, 255);  /* 背景颜色 */
            }
            QToolButton:hover { 
            }
        """)
        if callback:
            button.clicked.connect(callback)
        return button

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
        self.all_process_button = self.right_area_button_model(
            70, 630, "picture/AllProcess.jpg", "完整运行",
            lambda: self.complete_execution()
        )
        self.clean_hp_button = self.right_area_button_model(
            320, 630, "picture/CleanHP.jpg", "清理体力",
            lambda: self.clean_hp()
        )
        self.company_button = self.right_area_button_model(
            570, 630, "picture/Company.jpg", "派遣公司",
            lambda: self.dispatch_company()
        )
        self.bowu_button = self.right_area_button_model(
            820, 630, "picture/BoWU.jpg", "易物所和任务领取",
            lambda: self.bowu()
        )

    # 右侧区域按钮模板
    def right_area_button_model(self, x, y, icon_path, text, callback=None):
        button = QToolButton(self.main_frame)
        button.setGeometry(x, y, 200, 240)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(200, 200))
        button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        button.setText(text)
        if callback:
            button.clicked.connect(callback)
        # 设置样式表，禁用悬停效果
        button.setStyleSheet("""
            QToolButton {
                border: none;  /* 去掉边框 */
                background-color: white;
            }
            QToolButton:hover {
                background-color: white;
            }
        """)
        return button

    # 设置界面
    def create_setting_frame(self):
        # 基本布局设置
        self.setting_frame = QFrame(self.central_widget)
        self.setting_frame.raise_()
        self.setting_frame.setGeometry(85, 45, 1100, 900)
        self.left_setting_frame = QFrame(self.setting_frame)
        self.left_setting_frame.setGeometry(5, 5, 540, 865)
        self.left_setting_frame.setStyleSheet("border: 1px solid black; border-radius: 5px;")
        self.right_setting_frame = QFrame(self.setting_frame)
        self.right_setting_frame.setGeometry(560, 5, 530, 865)
        self.right_setting_frame.setStyleSheet("border: 1px solid black; border-radius: 5px;")
        big_font = QFont()
        big_font.setPointSize(14)
        normal_font = QFont()
        normal_font.setPointSize(12)
        # 左边设置界面
        self.level_label = QLabel("关卡设置:", self.setting_frame)
        self.level_label.setGeometry(15, 10, 100, 40)
        self.level_label.setFont(big_font)
        # 类型选择
        self.Level_type_label = QLabel("关卡类型选择:", self.setting_frame)
        self.Level_type_label.setGeometry(10, 60, 150, 40)
        self.Level_type_label.setFont(normal_font)
        self.type_combobox = QComboBox(self.setting_frame)
        self.type_combobox.setGeometry(420, 60, 100, 40)
        self.type_combobox.setFont(normal_font)
        type_option = ["冬谷币", "教材", "装备", "宿卫本", "构术本", "远击本", "轻锐本", "战略本"]
        self.type_combobox.addItems(type_option)
        self.type_combobox.setCurrentText(Level.level_type)
        self.type_combobox.currentIndexChanged.connect(self.type_combobox_changed)
        # rank选择
        self.Level_rank_label = QLabel("关卡选择:", self.setting_frame)
        self.Level_rank_label.setGeometry(10, 110, 150, 40)
        self.Level_rank_label.setFont(normal_font)
        self.rank_combobox = QComboBox(self.setting_frame)
        self.rank_combobox.setGeometry(420, 110, 100, 40)
        self.rank_combobox.setFont(normal_font)
        rank_option = ["子", "丑", "寅", "卯", "辰"]
        self.rank_combobox.addItems(rank_option)
        self.rank_combobox.setCurrentText(Level.level_rank)
        self.rank_combobox.currentIndexChanged.connect(self.rank_combobox_changed)
        # 次数选择
        self.Level_times_label = QLabel("速通次数选择:", self.setting_frame)
        self.Level_times_label.setGeometry(10, 160, 150, 40)
        self.Level_times_label.setFont(normal_font)
        self.times_combobox = QComboBox(self.setting_frame)
        self.times_combobox.setGeometry(420, 160, 100, 40)
        self.times_combobox.setFont(normal_font)
        times_option = [str(i) for i in range(1, 21)] # 列表推导式
        self.times_combobox.addItems(times_option)
        self.times_combobox.setCurrentText(str(Level.level_times))
        self.times_combobox.currentIndexChanged.connect(self.times_combobox_changed)
        # 完整运行设置
        self.complete_label = QLabel("完整运行设置:", self.setting_frame)
        self.complete_label.setGeometry(15, 220, 150, 40)
        self.complete_label.setFont(big_font)
        self.company_checkbox = self.checkbox_model(15, 270, "派遣公司", CompleteSetting.company)
        self.company_checkbox.stateChanged.connect(self.company_checkbox_changed)
        self.yiwusuo_checkbox = self.checkbox_model(155, 270, "易物所", CompleteSetting.yiwusuo)
        self.yiwusuo_checkbox.stateChanged.connect(self.yiwusuo_checkbox_changed)
        self.cleanhp_checkbox = self.checkbox_model(295, 270, "清理体力", CompleteSetting.cleanhp)
        self.cleanhp_checkbox.stateChanged.connect(self.cleanhp_checkbox_changed)
        self.task_checkbox = self.checkbox_model(435, 270, "领取任务", CompleteSetting.task)
        self.task_checkbox.stateChanged.connect(self.task_checkbox_changed)
        self.shop_checkbox = self.checkbox_model(15, 320, "商亭", CompleteSetting.shop)
        self.shop_checkbox.stateChanged.connect(self.shop_checkbox_changed)
        self.youli_checkbox = self.checkbox_model(155, 320, "游历", CompleteSetting.youli)
        self.youli_checkbox.stateChanged.connect(self.youli_checkbox_changed)

    # 使用指南界面(帮助界面)
    def create_help_frame(self):
        self.help_frame = QFrame(self.central_widget)
        self.help_frame.raise_()
        self.help_frame.setGeometry(85, 45, 1100, 900)
        # 中间分隔线
        line = QFrame(self.help_frame)
        line.setFrameShape(QFrame.VLine)  # 竖线
        line.setFrameShadow(QFrame.Plain)  # 样式
        line.setGeometry(520, 20, 5, 860)
        big_font = QFont()
        big_font.setPointSize(14)
        normal_font = QFont()
        normal_font.setPointSize(12)
        # 硬件要求
        self.require_title = QLabel("硬件要求:", self.help_frame)
        self.require_title.setGeometry(15, 10, 100, 40)
        self.require_title.setFont(big_font)
        self.require_text = QLabel("", self.help_frame)
        self.require_text.setGeometry(20, 55, 500, 120)
        self.require_text.setFont(normal_font)
        self.require_text.setWordWrap(True)  # 让 QLabel 自动换行
        self.require_text.setText("1.电脑显示屏分辨率16:9\n"
                                   "2.游戏需要使用雷电模拟器运行\n"
                                   "3.游戏图标需要放在桌面上\n"
                                   "4.模拟器窗口为启动大小(不是全屏)")
        # 注意事项
        self.note_title = QLabel("注意事项:", self.help_frame)
        self.note_title.setGeometry(15, 220, 100, 40)
        self.note_title.setFont(big_font)
        self.note_text = QLabel("", self.help_frame)
        self.note_text.setGeometry(20, 245, 500, 120)
        self.note_text.setFont(normal_font)
        self.note_text.setWordWrap(True)  # 让 QLabel 自动换行
        self.note_text.setText("1.脚本运行过程中请不要使用电脑\n"
                               "2.脚本运行完成会弹出通知窗口\n")
        # 功能说明
        self.description_title = QLabel("功能说明:", self.help_frame)
        self.description_title.setGeometry(535, 10, 100, 40)
        self.description_title.setFont(big_font)
        self.description_text = QLabel("", self.help_frame)
        self.description_text.setGeometry(540, 55, 500, 120)
        self.description_text.setFont(normal_font)
        self.description_text.setWordWrap(True)  # 让 QLabel 自动换行
        self.description_text.setText("1.不小心点错按钮\n"
                                   "三秒内点击鼠标右键可以取消刚刚点击的按钮运行的功能\n")

    # 勾选框模板
    def checkbox_model(self, x, y, text, set_checked):
        normal_font = QFont()
        normal_font.setPointSize(12)
        checkbox = QCheckBox(text, self.setting_frame)
        checkbox.setFont(normal_font)
        checkbox.setGeometry(x, y, 150, 40)
        checkbox.setChecked(set_checked)
        return checkbox

    # ui初始化
    def setup_ui(self):
        self.setFixedSize(1200, 950)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('picture/icon.jpg'))
        Level.Get()
        CompleteSetting.Get()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.create_header()
        self.create_left_area()
        self.create_main_frame()
        self.create_setting_frame()
        self.create_help_frame()

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

    def type_combobox_changed(self):
        Level.level_type = self.type_combobox.currentText()
        Level.Save()

    def rank_combobox_changed(self):
        Level.level_rank = self.rank_combobox.currentText()
        Level.Save()

    def times_combobox_changed(self):
        Level.level_times = int(self.times_combobox.currentText())
        Level.Save()

    def company_checkbox_changed(self):
        if self.company_checkbox.isChecked():
            CompleteSetting.company = True
        else:
            CompleteSetting.company = False
        CompleteSetting.Save()

    def yiwusuo_checkbox_changed(self):
        if self.yiwusuo_checkbox.isChecked():
            CompleteSetting.yiwusuo = True
        else:
            CompleteSetting.yiwusuo = False
        CompleteSetting.Save()

    def cleanhp_checkbox_changed(self):
        if self.cleanhp_checkbox.isChecked():
            CompleteSetting.cleanhp = True
        else:
            CompleteSetting.cleanhp = False
        CompleteSetting.Save()

    def task_checkbox_changed(self):
        if self.task_checkbox.isChecked():
            CompleteSetting.task = True
        else:
            CompleteSetting.task = False
        CompleteSetting.Save()

    def shop_checkbox_changed(self):
        if self.task_checkbox.isChecked():
            CompleteSetting.shop = True
        else:
            CompleteSetting.shop = False
        CompleteSetting.Save()

    def youli_checkbox_changed(self):
        if self.task_checkbox.isChecked():
            CompleteSetting.youli = True
        else:
            CompleteSetting.youli = False
        CompleteSetting.Save()

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
            QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
        else:
            print("启动游戏")
            subprocess.Popen(exe_path)
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
            times = 0
            while times < 40 and stop_thread is False:
                if JudgeMainPage():
                    time.sleep(1)
                    print("启动游戏成功！")
                    self.raise_()  # 让窗口置顶
                    self.activateWindow()  # 激活窗口
                    time.sleep(1)
                    QMessageBox.information(self, '', '启动游戏成功！', QMessageBox.Ok)
                    break
                # 2560 1440
                pyautogui.click(ScreenSize.width * 0.81, ScreenSize.height * 0.229)
                time.sleep(5)
                click_check_close()
                times += 1

    # 完整运行
    def complete_execution(self):
        global stop_thread, is_complete_execution
        is_complete_execution = True
        stop_thread = False
        for i in range(3):
            if stop_thread is True:
                QMessageBox.information(self, '', '进程已停止', QMessageBox.Ok)
                return
            time.sleep(1)
        if CompleteSetting.company is True and stop_thread is False:
            self.dispatch_company()
            time.sleep(3)
        if CompleteSetting.cleanhp is True and stop_thread is False:
            self.clean_hp()
            time.sleep(3)
        if CompleteSetting.yiwusuo is True and stop_thread is False:
            self.yiwusuo()
            time.sleep(3)
        if CompleteSetting.task is True and stop_thread is False:
            self.get_task()
            time.sleep(3)
        if CompleteSetting.youli is True and stop_thread is False:
            self.youli()
            time.sleep(3)
        if CompleteSetting.shop is True and stop_thread is False:
            self.shop()
            time.sleep(3)
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
        subprocess.Popen(exe_path)  # 打开游戏界面
        time.sleep(1)
        if ReturnMainPage() is True:
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
        subprocess.Popen(exe_path)  # 打开游戏界面
        time.sleep(1)
        self.yiwusuo()
        time.sleep(1)
        self.get_task()
        if is_complete_execution is False:
            self.raise_()  # 让窗口置顶
            self.activateWindow()  # 激活窗口
            time.sleep(1)
            QMessageBox.information(self, '', '脚本运行结束', QMessageBox.Ok)

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
        process = subprocess.Popen(exe_path)  # 打开游戏界面
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
        time.sleep(1)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec())
