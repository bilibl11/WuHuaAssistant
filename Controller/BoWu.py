# 开发时间:2025/7/10 20:52
from DataPack.FilePath import image_bowu_path, image_zhuti_path, image_qicheng_path, image_jinyinjixing_path, \
    image_chooseDiffculty_path, image_chooseBoss_path, image_addRole_path, image_bowu_ok_path, image_choosefuzhu_path, \
    image_enteryanxue_path, image_role_path, image_rest_path, image_bowu_ok2_path, image_bowu_ok3_path, \
    image_addRole2_path, image_battle_path, image_start_path, image_startBattle_path, image_bowu_ok4_path, \
    image_bowu_ok5_path, image_hardBattle_path, image_own_path, image_boss_path, image_bowu_finish_path, \
    image_bowu_reward_path, image_click_reward_path, image_continue_path
from Utils.Utils import get_xy, auto_click, get_xy1

roles = 4

def click_bowu():
    print("点击博物研学：")
    avg = get_xy(image_bowu_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_jinyinjixing():
    print("点击金银纪行：")
    avg = get_xy(image_jinyinjixing_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_zhuti():
    print("点击进入主题：")
    avg = get_xy(image_zhuti_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_qicheng():
    print("点击研学启程：")
    avg = get_xy(image_qicheng_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def choose_boss():
    print("选择boss：")
    avg = get_xy(image_chooseBoss_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def choose_diffculty():
    print("选择难度：")
    avg = get_xy(image_chooseDiffculty_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def add_role():
    print("添加角色：")
    avg = get_xy(image_addRole_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def add_role2():
    print("添加角色：")
    avg = get_xy(image_addRole2_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_ok():
    print("点击确认1：")
    avg = get_xy(image_bowu_ok_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_ok2():
    print("点击确认2：")
    avg = get_xy(image_bowu_ok2_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_ok3():
    print("点击确认3：")
    avg = get_xy(image_bowu_ok3_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_ok4():
    print("点击确认4：")
    avg = get_xy(image_bowu_ok4_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_ok5():
    print("点击确认5：")
    avg = get_xy(image_bowu_ok5_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def choose_fuzhu():
    print("选择辅助效果：")
    avg = get_xy(image_choosefuzhu_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def entry_yanxue():
    print("进入研学：")
    avg = get_xy(image_enteryanxue_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def get_own_position():
    print("获取本人位置：")
    avg = get_xy(image_own_path)
    if avg is not None:
        return avg
    else:
        return None

def click_role():
    own_position = get_own_position()
    avg = get_xy1(image_role_path, own_position[0], own_position[1] - 50, precision = 0.05)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_rest():
    own_position = get_own_position()
    avg = get_xy1(image_rest_path, own_position[0], own_position[1] - 50, precision = 0.05)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_battle():
    own_position = get_own_position()
    avg = get_xy1(image_battle_path, own_position[0], own_position[1] - 50, precision = 0.05)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_hardBattle():
    own_position = get_own_position()
    avg = get_xy1(image_hardBattle_path, own_position[0], own_position[1] - 50, precision = 0.05)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_boss():
    print("点击boss战")
    avg = get_xy(image_boss_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def enter_battleUI():
    print("进入战斗界面：")
    avg = get_xy(image_start_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_start_battle():
    print("开始战斗：")
    avg = get_xy(image_startBattle_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def finish_yanxue():
    print("结束研学：")
    avg = get_xy(image_bowu_finish_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def click_reward():
    print("点击奖励：")
    avg = get_xy(image_bowu_reward_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def get_reward():
    print("领取奖励：")
    avg = get_xy(image_click_reward_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def continue_yanxue():
    print("继续研学：")
    avg = get_xy(image_continue_path, 0.04)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False