# 开发时间:2025/5/29 16:34
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QLabel, QComboBox, QCheckBox, QLineEdit, QFileDialog, QPushButton
from poetry.console.commands import self

from Controller.MainUIServlet import get_all_json_data
from DataPack import Level, CompleteSetting, FilePath, Path
from DataPack.CompleteSetting import state_dict, print_dict

complete_checkbox_texts = ["派遣公司", "易物所", "清理体力", "领取任务", "商亭", "游历", "外勤"]
complete_text_dict = {
    "派遣公司" : "company",
    "易物所": "yiwusuo",
    "清理体力": "cleanhp",
    "领取任务": "task",
    "商亭": "shop",
    "游历": "youli",
    "外勤": "waiqin"
}

def type_combobox_changed(text):
    Level.level_type = text
    Level.Save()

def rank_combobox_changed(text):
    Level.level_rank = text
    Level.Save()

def times_combobox_changed(text):
    Level.level_times = int(text)
    Level.Save()

# 勾选框模板
def checkbox_model(setting_frame, x, y, text, set_checked):
        normal_font = QFont()
        normal_font.setPointSize(12)
        checkbox = QCheckBox(text, setting_frame)
        checkbox.setFont(normal_font)
        checkbox.setGeometry(x, y, 150, 40)
        checkbox.setChecked(set_checked)
        return checkbox

def company_checkboxes_change(state, checkbox_text):
    key = complete_text_dict.get(checkbox_text)
    print(f"State: {state}, Checkbox Text: {checkbox_text}, key: {key}")
    if state == 2:
        CompleteSetting.Revise(key, True)
    else:
        CompleteSetting.Revise(key, False)


def create_setting_frame(main_ui):
    Path.Get()
    setting_frame = QFrame(main_ui.central_widget)
    setting_frame.raise_()
    setting_frame.setGeometry(85, 45, 1100, 900)
    left_setting_frame = QFrame(setting_frame)
    left_setting_frame.setGeometry(5, 5, 540, 865)
    left_setting_frame.setStyleSheet("border: 1px solid black; border-radius: 5px;")
    right_setting_frame = QFrame(setting_frame)
    right_setting_frame.setGeometry(560, 5, 530, 865)
    right_setting_frame.setStyleSheet("border: 1px solid black; border-radius: 5px;")
    big_font = QFont()
    big_font.setPointSize(14)
    normal_font = QFont()
    normal_font.setPointSize(12)
    # 左边设置界面
    level_label = QLabel("关卡设置:", setting_frame)
    level_label.setGeometry(15, 10, 100, 40)
    level_label.setFont(big_font)
    # 类型选择
    Level_type_label = QLabel("关卡类型选择:", setting_frame)
    Level_type_label.setGeometry(10, 60, 150, 40)
    Level_type_label.setFont(normal_font)
    type_combobox = QComboBox(setting_frame)
    type_combobox.setGeometry(420, 60, 100, 40)
    type_combobox.setFont(normal_font)
    type_option = ["冬谷币", "教材", "装备", "宿卫本", "构术本", "远击本", "轻锐本", "战略本"]
    type_combobox.addItems(type_option)
    type_combobox.setCurrentText(Level.level_type)
    type_combobox.currentTextChanged.connect(type_combobox_changed) #combobox修改时回默认传递参数text（当前combobox的文本内容）到槽函数
    # 关卡(rank)选择
    Level_rank_label = QLabel("关卡选择:", setting_frame)
    Level_rank_label.setGeometry(10, 110, 150, 40)
    Level_rank_label.setFont(normal_font)
    rank_combobox = QComboBox(setting_frame)
    rank_combobox.setGeometry(420, 110, 100, 40)
    rank_combobox.setFont(normal_font)
    rank_option = ["子", "丑", "寅", "卯", "辰"]
    rank_combobox.addItems(rank_option)
    rank_combobox.setCurrentText(Level.level_rank)
    rank_combobox.currentTextChanged.connect(rank_combobox_changed)
    # 次数选择
    Level_times_label = QLabel("速通次数选择:", setting_frame)
    Level_times_label.setGeometry(10, 160, 150, 40)
    Level_times_label.setFont(normal_font)
    times_combobox = QComboBox(setting_frame)
    times_combobox.setGeometry(420, 160, 100, 40)
    times_combobox.setFont(normal_font)
    times_option = [str(i) for i in range(1, 21)]  # 列表推导式
    times_combobox.addItems(times_option)
    times_combobox.setCurrentText(str(Level.level_times))
    times_combobox.currentTextChanged.connect(times_combobox_changed)
    # 完整运行设置
    complete_label = QLabel("完整运行设置:", setting_frame)
    complete_label.setGeometry(15, 220, 150, 40)
    complete_label.setFont(big_font)
    index_x = 0
    index_y = 0
    complete_checkboxes = []
    for key, value in CompleteSetting.state_dict.items():
        if index_x >= 4:
            index_x = 0
        checkbox = checkbox_model(setting_frame, 15 + 140*index_x ,270 + (int(index_y/4))*50 , complete_checkbox_texts[index_y], value)
        checkbox.stateChanged.connect(lambda state, checkbox_text = complete_checkbox_texts[index_y]: company_checkboxes_change(state, checkbox_text))
        complete_checkboxes.append(checkbox)
        index_x += 1
        index_y += 1

    # 右边设置界面
    # 雷电模拟器路径设置
    simulator_path_label = QLabel("雷电模拟器路径:", setting_frame)
    simulator_path_label.setGeometry(570, 15, 150, 40)
    simulator_path_label.setFont(normal_font)
    simulator_path_text = QLineEdit(setting_frame)
    simulator_path_text.setGeometry(730, 15, 250, 40)
    simulator_path_text.setPlaceholderText("" + Path.exe_path)
    simulator_path_text.setReadOnly(True)
    simulator_path_button = QPushButton("更改路径", setting_frame)
    simulator_path_button.setGeometry(990, 15, 90, 40)
    simulator_path_button.clicked.connect(lambda: revise_simulator_path(simulator_path_text))  # 绑定点击事件

    return setting_frame

def revise_simulator_path(simulator_path_text):
    print(f"更改模拟器路径")
    try:
        # 打开文件选择对话框,
        file_path, _ = QFileDialog.getOpenFileName(None,
            "选择EXE文件",  # 对话框标题
            Path.exe_path,  # 初始目录
            "可执行文件 (*.exe);;所有文件 (*)"  # 文件筛选器
        )
        # 调试输出
        if file_path:
            print(f"已选择文件: {file_path}")
            # 更新配置
            Path.exe_path = file_path
            Path.Save()
            simulator_path_text.setText(Path.exe_path)
        else:
            print("用户取消了文件选择")
    except Exception as e:
        print(f"发生异常: {e}")
        # 可选：记录详细的堆栈信息
        import traceback
        print(traceback.format_exc())

