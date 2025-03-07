# 开发时间:2024/10/5 0:16
import subprocess
import sys
import time

from DataPack import Level
from DataPack.FilePath import image_game_exe_path, image_company_path, image_YanXun_path, image_StartTrain_path, \
    image_JiaoCai_path, image_SuTong_path, image_Add_path, image_ok_path, image_finish_path, \
    image_home_path, image_Money_path, image_ZhuangBei_path, image_SuWei_path, image_ZhanLue_path, image_QingRui_path, \
    image_YuanJi_path, image_GouShu_path, image_PeiYang_Zi_path, image_PeiYang_Chou_path, image_PeiYang_Yin_path, \
    image_PeiYang_Mao_path, image_PeiYang_Chen_path, image_KaoHe_Zi_path, image_KaoHe_Chou_path, image_KaoHe_Mao_path, \
    image_KaoHe_Chen_path, image_KaoHe_Yin_path, image_KaoHe_path
from Utils import get_xy, auto_click, CompareImageAndClick

PeiYang_dict = {
    "冬谷币": image_Money_path,
    "教材": image_JiaoCai_path,
    "装备": image_ZhuangBei_path,
}
KaoHe_dict = {
    "宿卫本": image_SuWei_path,
    "构术本": image_GouShu_path,
    "远击本": image_YuanJi_path,
    "轻锐本": image_QingRui_path,
    "战略本": image_ZhanLue_path
}
PeiYang_Rank_dict = {
    "子": image_PeiYang_Zi_path,
    "丑": image_PeiYang_Chou_path,
    "寅": image_PeiYang_Yin_path,
    "卯": image_PeiYang_Mao_path,
    "辰": image_PeiYang_Chen_path
}
KaoHe_Rank_dict = {
    "子": image_KaoHe_Zi_path,
    "丑": image_KaoHe_Chou_path,
    "寅": image_KaoHe_Yin_path,
    "卯": image_KaoHe_Mao_path,
    "辰": image_KaoHe_Chen_path
}


def ChangeLevelPath():
    for key, value in PeiYang_dict.items():
        if Level.level_type == key:
            return value
    return image_KaoHe_path


def ChangeKaoHeLevelPath():
    for key, value in KaoHe_dict.items():
        if Level.level_type == key:
            return value


def ChangeRankPath(level_path):
    # 培养本
    if level_path != image_KaoHe_path:
        print("选择培养本关卡")
        for key, value in PeiYang_Rank_dict.items():
            if Level.level_rank == key:
                return value
    else:
        print("选择考核本关卡")
        for key, value in KaoHe_Rank_dict.items():
            if Level.level_rank == key:
                return value
    return image_KaoHe_path


def ClickYanXun():
    print("点击演训")
    avg = get_xy(image_YanXun_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def ClickStartTrain():
    print("点击开始训练")
    avg = get_xy(image_StartTrain_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def ChooseLevel(levelPath):
    print("选择关卡类型")
    avg = get_xy(levelPath)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def ChooseRank(rankPath):
    print("选择关卡")
    avg = get_xy(rankPath)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def ClickSuTong():
    print("点击速通")
    avg = get_xy(image_SuTong_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def AddTimes(times):
    print("选择次数")
    avg = get_xy(image_Add_path)
    if avg is not None:
        for num in range(1, times):
            auto_click(avg)
            time.sleep(0.1)
        return True
    else:
        return False


def ClickOK():
    print("点击确认")
    avg = get_xy(image_ok_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False


def ClickFinish():
    print("点击完成")
    avg = get_xy(image_finish_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False
