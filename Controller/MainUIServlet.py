# 开发时间:2025/1/19 18:13
from DataPack import Level, CompleteSetting
from DataPack.FilePath import image_checkClose_path
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

