# 开发时间:2025/1/19 18:13
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolButton, QPushButton

from DataPack import Level, CompleteSetting
from DataPack.FilePath import image_checkClose_path, image_update_path
from Utils.Utils import get_xy, auto_click

def get_all_json_data():
    Level.Get()
    CompleteSetting.Get()

def click_check_close():
    avg = get_xy(image_checkClose_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_update():
    avg = get_xy(image_update_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

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

