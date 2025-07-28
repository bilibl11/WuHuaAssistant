# 开发时间:2025/5/30 19:48
# 使用指南界面(帮助界面)
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QLabel


def create_help_frame(main_ui):
    help_frame = QFrame(main_ui.central_widget)
    help_frame.raise_()
    help_frame.hide()
    help_frame.setGeometry(85, 45, 1100, 900)
    # 中间分隔线
    line = QFrame(help_frame)
    line.setFrameShape(QFrame.VLine)  # 竖线
    line.setFrameShadow(QFrame.Plain)  # 样式
    line.setGeometry(520, 20, 5, 860)
    big_font = QFont()
    big_font.setPointSize(14)
    normal_font = QFont()
    normal_font.setPointSize(12)
    # 硬件要求
    require_title = QLabel("硬件要求:", help_frame)
    require_title.setGeometry(15, 10, 100, 40)
    require_title.setFont(big_font)
    require_text = QLabel("", help_frame)
    require_text.setGeometry(20, 55, 500, 120)
    require_text.setFont(normal_font)
    require_text.setWordWrap(True)  # 让 QLabel 自动换行
    require_text.setText("1.电脑显示屏分辨率16:9\n"
                              "2.游戏需要使用雷电模拟器运行\n"
                              "3.游戏图标需要放在桌面上\n"
                              "4.模拟器窗口为启动大小(不是全屏)")
    # 注意事项
    note_title = QLabel("注意事项:", help_frame)
    note_title.setGeometry(15, 220, 100, 40)
    note_title.setFont(big_font)
    note_text = QLabel("", help_frame)
    note_text.setGeometry(20, 245, 500, 120)
    note_text.setFont(normal_font)
    note_text.setWordWrap(True)  # 让 QLabel 自动换行
    note_text.setText("1.脚本运行过程中请不要使用电脑\n"
                           "2.脚本运行完成会弹出通知窗口\n")
    # 功能说明
    description_title = QLabel("功能说明:", help_frame)
    description_title.setGeometry(535, 10, 100, 40)
    description_title.setFont(big_font)
    description_text = QLabel("", help_frame)
    description_text.setGeometry(540, 55, 500, 120)
    description_text.setFont(normal_font)
    description_text.setWordWrap(True)  # 让 QLabel 自动换行
    description_text.setText("1.不小心点错按钮：\n"
                             "三秒内点击鼠标右键可以取消刚刚点击的按钮运行的功能\n"
                             "2.模拟器路径设置：\n"
                             "一般是选择dnplayer.exe文件\n")
    # 博物研学功能说明
    bowu_description_title = QLabel("博物研学功能说明:", help_frame)
    bowu_description_title.setGeometry(535, 200, 200, 40)
    bowu_description_title.setFont(big_font)
    bowu_description_text = QLabel("", help_frame)
    bowu_description_text.setGeometry(540, 245, 500, 180)
    bowu_description_text.setFont(normal_font)
    bowu_description_text.setWordWrap(True)  # 让 QLabel 自动换行
    bowu_description_text.setText("1.功能运行时间说明：\n"
                                  "本功能运行时间较长，大概10-15分钟，中途无法使用电脑，目前没有中途暂停功能，请看情况使用该功能\n"
                                  "2.挂机器者选择：\n"
                                  "通过设置关心器者可以选择脚本上阵的器者，一般六个满级器者是能成功完成挂机的\n")
    return help_frame