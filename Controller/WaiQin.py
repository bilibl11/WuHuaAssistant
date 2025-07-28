# 开发时间:2025/7/21 17:13
# 进入外勤界面
from DataPack.FilePath import image_waiqin_path, image_startWaiqin_path, image_waiqin_ok_path, image_zhengzai_path
from Utils.Utils import get_xy, auto_click


def enter_waiqin():
    print("进入外勤界面：")
    avg = get_xy(image_waiqin_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def start_waiqin():
    print("开始外勤：")
    avg = get_xy(image_startWaiqin_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_ok():
    print("点击确定：")
    avg = get_xy(image_waiqin_ok_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def zhengzaiwaiqin():
    print("正在外勤：")
    avg = get_xy(image_zhengzai_path)
    if avg is not None:
        return True
    else:
        return False