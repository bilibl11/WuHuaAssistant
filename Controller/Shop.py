# 开发时间:2025/3/10 11:18
# 点击商亭
from DataPack.FilePath import image_shop_path, image_shop_gift_path, image_xunshi_path, image_goBuy_path, \
    image_shop_buy_path
from Utils.Utils import get_xy, auto_click


def GoShop():
    print("点击商亭")
    avg = get_xy(image_shop_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def ClickGift():
    print("点击礼包")
    avg = get_xy(image_shop_gift_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def ClickXunShi():
    print("点击循时补给")
    avg = get_xy(image_xunshi_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def Gobuy():
    print("前往购买")
    avg = get_xy(image_goBuy_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False

def BuyGift():
    print("点击购买")
    avg = get_xy(image_shop_buy_path)
    if avg is not None:
        auto_click(avg)
        return True
    else:
        return False