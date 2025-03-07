import sys
import time
import subprocess

import pyautogui
from PyQt5.QtCore import Qt, QSize, QEvent, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QToolButton, QFrame, QWidget, QComboBox

from DataPack import Level
from DataPack.FilePath import exe_path, image_game_exe_path, image_PeiYang_Chen_path, image_KaoHe_path
from Scripts.CleanHP import (
    ClickYanXun, ChooseLevel, ClickSuTong,
    AddTimes, ClickOK, ClickFinish, ClickStartTrain, ChooseRank, ChangeLevelPath, ChangeRankPath, ChangeKaoHeLevelPath
)
from Scripts.DispatchCompany import (
    EntryCompany, CollectDunShe, CollectMaterial,
    ClickGift, ClickCoin, GetGanYing, GoToDunShe, GetHP, ReturnCompany
)
from Scripts.GameStateServlet import ReturnMainPage, JudgeMainPage
from Scripts.MainWindowServlet import click_check_close
from Scripts.Task import EntryTask, ClickWeekTask, GetTaskReward
from Scripts.YIWUSUO import EntryYiWuSuo, ConfirmBuy, Buy
from Utils import CompareImageAndClick

ScreenSize = pyautogui.size()


class MainPage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.dragging = False  # 是否正在拖动
        self.offset = QPoint()  # 鼠标按下时的偏移量

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
        self.title_label = QLabel("WuHua Assistant", self.central_widget)
        self.title_label.setGeometry(55, 5, 200, 30)
        self.title_label.setFont(QFont('Arial', 10, QFont.Bold))

        # Minimize button
        self.minimize_button = QPushButton(self.central_widget)
        self.minimize_button.setGeometry(1080, 0, 60, 40)
        self.minimize_button.setIcon(QIcon("picture/minimize.png"))
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;  /* 圆角 */
                border: none;  /* 去掉边框 */
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: white;  /* 悬停时背景透明 */
            }
        """)

        # Close button
        self.close_button = QPushButton(self.central_widget)
        self.close_button.setGeometry(1140, 0, 60, 40)
        self.close_button.setIcon(QIcon("picture/close.png"))
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;  /* 圆角 */
                border: none;  /* 去掉边框 */
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: white;  /* 悬停时背景透明 */
            }
        """)

    # 左侧区域
    def create_left_area(self):
        self.main_page_button = self.create_left_button(
            0, 40, "picture/MainPage.png", "主页", lambda: self.show_main_frame()
        )
        self.start_button = self.create_left_button(
            0, 760, "picture/launch.png", "启动游戏", lambda: self.launch_game()
        )
        self.setting_button = self.create_left_button(
            0, 840, "picture/install.png", "设置", lambda: self.show_setting_frame()
        )

    # 左侧区域按钮模板
    def create_left_button(self, x, y, icon_path, text, callback=None):
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
        self.all_process_button = self.create_right_button(
            70, 630, "picture/AllProcess.jpg", "完整运行",
            lambda: self.complete_execution()
        )
        self.clean_hp_button = self.create_right_button(
            320, 630, "picture/CleanHP.jpg", "清理体力",
            lambda: self.clean_hp()
        )
        self.company_button = self.create_right_button(
            570, 630, "picture/Company.jpg", "派遣公司",
            lambda: self.dispatch_company()
        )
        self.bowu_button = self.create_right_button(
            820, 630, "picture/BoWU.jpg", "易物所和任务领取",
            lambda: self.bowu()
        )

    # 右侧区域按钮模板
    def create_right_button(self, x, y, icon_path, text, callback=None):
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
        Level.Get()
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
        times_option = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.times_combobox.addItems(times_option)
        self.times_combobox.setCurrentText(str(Level.level_times))
        self.times_combobox.currentIndexChanged.connect(self.times_combobox_changed)

    def setup_ui(self):
        self.setWindowTitle("WuHua Assistant")
        self.setFixedSize(1200, 950)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('picture/icon.jpg'))
        Level.Get()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.create_header()
        self.create_left_area()
        self.create_main_frame()
        self.create_setting_frame()

        self.show_main_frame()

    def show_main_frame(self):
        if self.setting_frame.isVisible() or self.main_frame.isVisible() is False:
            self.setting_frame.hide()
            self.main_frame.show()
            self.main_page_button.setStyleSheet("""
                QToolButton {
                    border-left: 5px solid rgba(255, 105, 180, 255);  /* 粉色左边边框 */
                    border-radius: 0px;
                    background-color: rgba(255, 255, 255, 255);  /* 背景颜色 */
                }
                QToolButton:hover { 
                }
                QToolButton:pressed {
                    background-color: rgba(255, 105, 180, 100);  /* 按下时背景颜色 */
                }
            """)
            self.setting_button.setStyleSheet("""
                QToolButton {
                    border-left: 0px solid rgba(255, 105, 180, 255);  /* 粉色左边边框 */
                    border-radius: 0px;
                    background-color: rgba(255, 255, 255, 255);  /* 背景颜色 */
                }
                QToolButton:hover { 
                }
                QToolButton:pressed {
                    background-color: rgba(255, 105, 180, 100);  /* 按下时背景颜色 */
                }
            """)

    def show_setting_frame(self):
        if self.main_frame.isVisible():
            # 切换界面
            self.main_frame.hide()
            self.setting_frame.show()
            self.setting_button.setStyleSheet("""
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
            self.main_page_button.setStyleSheet("""
                QToolButton {
                    border-left: 0px solid rgba(255, 105, 180, 255);  /* 粉色左边边框 */
                    border-radius: 0px;  /* 圆角 */
                    background-color: rgba(255, 255, 255, 255);  /* 背景颜色 */
                }
                QToolButton:hover { 
                }
                QToolButton:pressed {
                    background-color: rgba(255, 105, 180, 100);  /* 按下时背景颜色 */
                }
            """)
            # 读取当前选择的数据
            Level.Get()

    def type_combobox_changed(self):
        Level.level_type = self.type_combobox.currentText()
        Level.Save()

    def rank_combobox_changed(self):
        Level.level_rank = self.rank_combobox.currentText()
        Level.Save()

    def times_combobox_changed(self):
        Level.level_times = int(self.times_combobox.currentText())
        Level.Save()

    # 启动并进入游戏
    def launch_game(self):
        print("启动游戏")
        subprocess.Popen(exe_path)
        self.start_button.setEnabled(False)
        time.sleep(1)
        # 如果游戏已经启动
        if JudgeMainPage():
            print("启动游戏成功！")
            return
        times = 0
        while times < 20:
            if CompareImageAndClick(image_game_exe_path, "启动游戏") is False:
                print("未成功加载模拟器")
                time.sleep(5)
                times += 1
        times = 0
        while times < 40:
            if JudgeMainPage():
                time.sleep(1)
                print("启动游戏成功！")
                break
            # 2560 1440
            pyautogui.click(ScreenSize.width * 0.81, ScreenSize.height * 0.229)
            time.sleep(5)
            click_check_close()
            times += 1

    # 完整运行
    def complete_execution(self):
        self.dispatch_company()
        time.sleep(1)
        self.yiwusuo()
        time.sleep(1)
        self.clean_hp()
        time.sleep(1)
        self.get_task()

    # 派遣公司
    def dispatch_company(self):
        print("派遣公司")
        subprocess.Popen(exe_path)  # 打开游戏界面
        time.sleep(1)
        if ReturnMainPage() is True:
            time.sleep(2.5)
        EntryCompany()
        time.sleep(5)
        GetGanYing()
        time.sleep(2)
        pyautogui.click(1200, 400)
        time.sleep(1)
        CollectMaterial()
        time.sleep(2)
        pyautogui.click(1200, 400)
        CollectDunShe()
        time.sleep(2)
        pyautogui.click(1200, 400)
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
        ClickGift()
        time.sleep(1)
        ClickCoin()
        time.sleep(3)
        pyautogui.click(1200, 600)
        time.sleep(3)
        pyautogui.click(1200, 600)
        ReturnMainPage()

    # 博物研学
    def bowu(self):
        subprocess.Popen(exe_path)  # 打开游戏界面
        time.sleep(1)
        self.yiwusuo()
        time.sleep(1)
        self.get_task()

    # 易物所
    def yiwusuo(self):
        EntryYiWuSuo()
        time.sleep(0.5)
        for i in range(2):
            Buy()
            time.sleep(0.5)
            ConfirmBuy()
            time.sleep(0.5)
            pyautogui.click(1200, 600)
            time.sleep(0.5)
        ReturnMainPage()

    # 领取任务奖励
    def get_task(self):
        print("领取任务")
        EntryTask()
        time.sleep(0.5)
        GetTaskReward()
        time.sleep(0.5)
        pyautogui.click(1320, 420)
        time.sleep(0.5)
        pyautogui.click(1320, 420)
        time.sleep(0.5)
        ClickWeekTask()
        time.sleep(0.5)
        GetTaskReward()
        time.sleep(0.5)
        pyautogui.click(1320, 420)
        time.sleep(0.5)
        pyautogui.click(1320, 420)
        time.sleep(0.5)
        ReturnMainPage()

    # 清理体力
    def clean_hp(self):
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
        ChooseRank(rank_path)
        time.sleep(1)
        ClickSuTong()
        time.sleep(2)
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
        ReturnMainPage()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec())
