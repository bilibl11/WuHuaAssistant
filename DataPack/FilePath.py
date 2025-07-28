# 开发时间:2024/10/4 23:44
import sys

# model
image_company_path = '.\picture\model\company.png'
image_game_exe_path = ".\picture\model\WuHua.png"
image_home_path = ".\picture\model\home.png"
image_close_path = ".\picture\model\close.png"
image_simulator_path = ".\picture\model\simulator.png"
image_checkClose_path = ".\picture\model\checkclose.png"
image_JudgeMainPage_path = ".\picture\model\JudgeMainPage.png"
image_back_path = ".\picture\model\\back.png"
image_update_path = ".\picture\model\\update.png"

# CleanHP
image_YanXun_path = ".\picture\model\cleanHP\YanXun.png"
image_StartTrain_path = ".\picture\model\cleanHP\StartTrain.png"
image_SuTong_path = ".\picture\model\cleanHP\SuTong.png"
image_Add_path = ".\picture\model\cleanHP\Add.png"
image_ok_path = ".\picture\model\cleanHP\ok.png"
image_finish_path = ".\picture\model\cleanHP\\finish.png"

# 培养本
image_Money_path = ".\picture\model\cleanHP\PeiYang\Money.png"
image_JiaoCai_path = ".\picture\model\cleanHP\PeiYang\JiaoCai.png"
image_ZhuangBei_path = ".\picture\model\cleanHP\PeiYang\ZhuangBei.png"
image_PeiYang_Zi_path = ".\picture\model\cleanHP\PeiYang\Zi.png"
image_PeiYang_Chou_path = ".\picture\model\cleanHP\PeiYang\Chou.png"
image_PeiYang_Yin_path = ".\picture\model\cleanHP\PeiYang\Yin.png"
image_PeiYang_Mao_path = ".\picture\model\cleanHP\PeiYang\Mao.png"
image_PeiYang_Chen_path = ".\picture\model\cleanHP\PeiYang\Chen.png"

# 考核本
image_KaoHe_path = ".\picture\model\cleanHP\KaoHe\KaoHe.png"
image_SuWei_path = ".\picture\model\cleanHP\KaoHe\SuWei.png"
image_GouShu_path = ".\picture\model\cleanHP\KaoHe\GouShu.png"
image_YuanJi_path = ".\picture\model\cleanHP\KaoHe\YuanJi.png"
image_QingRui_path = ".\picture\model\cleanHP\KaoHe\QingRui.png"
image_ZhanLue_path = ".\picture\model\cleanHP\KaoHe\ZhanLue.png"
image_KaoHe_Zi_path = ".\picture\model\cleanHP\KaoHe\Zi.png"
image_KaoHe_Chou_path = ".\picture\model\cleanHP\KaoHe\Chou.png"
image_KaoHe_Yin_path = ".\picture\model\cleanHP\KaoHe\Yin.png"
image_KaoHe_Mao_path = ".\picture\model\cleanHP\KaoHe\Mao.png"
image_KaoHe_Chen_path = ".\picture\model\cleanHP\KaoHe\Chen.png"

# 派遣公司
image_collect_path = ".\picture\model\company\collect.png"
image_DunShe_path = ".\picture\model\company\DunShe.png"
image_office_path = ".\picture\model\company\office.png"
image_gift_path = ".\picture\model\company\gift.png"
image_coin_path = ".\picture\model\company\coin.png"
image_getGanYing_path = ".\picture\model\company\getGanYing.png"
image_enterDunShe_path = ".\picture\model\company\enterDunShe.png"
image_getHP_path = ".\picture\model\company\getHP.png"
image_return_path = ".\picture\model\company\\return.png"

# 任务
image_entryTask_path = ".\picture\model\\task\entryTask.png"
image_weekTask_path = ".\picture\model\\task\weekTask.png"
image_getTask_path = ".\picture\model\\task\getTask.png"

# 易物所
image_yiwusuo_path = ".\picture\model\yiwusuo\yiwusuo.png"
image_money_path = ".\picture\model\yiwusuo\money.png"
image_moneyGreen_path = ".\picture\model\yiwusuo\moneyGreen.png"

# 商亭
image_shop_path = ".\picture\model\shop\shop.png"
image_shop_gift_path = ".\picture\model\shop\gift.png"
image_xunshi_path = ".\picture\model\shop\\xunshi.png"
image_goBuy_path = ".\picture\model\shop\goBuy.png"
image_shop_buy_path = ".\picture\model\shop\\buy.png"

# 游历
image_youli_path = ".\picture\model\youli\youli.png"
image_getAll_path = ".\picture\model\youli\getAll.png"
image_task_path = ".\picture\model\youli\\task.png"
image_reward_path = ".\picture\model\youli\\reward.png"

# 博物研学
image_bowu_path = ".\picture\model\\bowu\\bowu.png"
image_zhuti_path = ".\picture\model\\bowu\\zhuti.png"
image_qicheng_path = ".\picture\model\\bowu\\qicheng.png"
image_continue_path = ".\picture\model\\bowu\\continue.png"
image_jinyinjixing_path = ".\picture\model\\bowu\\jinyinjixing.png"
image_chooseBoss_path = ".\picture\model\\bowu\\chooseBoss.png"
image_chooseDiffculty_path = ".\picture\model\\bowu\\chooseDiffculty.png"
image_addRole_path = ".\picture\model\\bowu\\addRole.png"
image_addRole2_path = ".\picture\model\\bowu\\addRole2.png"
image_bowu_ok_path = ".\picture\model\\bowu\\ok.png"
image_bowu_ok2_path = ".\picture\model\\bowu\\ok2.png"
image_bowu_ok3_path = ".\picture\model\\bowu\\ok3.png"
image_bowu_ok4_path = ".\picture\model\\bowu\\ok4.png"
image_bowu_ok5_path = ".\picture\model\\bowu\\ok5.png"
image_choosefuzhu_path = ".\picture\model\\bowu\\choosefuzhu.png"
image_enteryanxue_path = ".\picture\model\\bowu\\enteryanxue.png"
image_rest_path = ".\picture\model\\bowu\\rest.png"
image_role_path = ".\picture\model\\bowu\\role.png"
image_battle_path = ".\picture\model\\bowu\\battle.png"
image_hardBattle_path = ".\picture\model\\bowu\\hardBattle.png"
image_revive_path = ".\picture\model\\bowu\\revive.png"
image_start_path = ".\picture\model\\bowu\\start.png"
image_startBattle_path = ".\picture\model\\bowu\\startBattle.png"
image_own_path = ".\picture\model\\bowu\\own.png"
image_boss_path = ".\picture\model\\bowu\\boss.png"
image_bowu_finish_path = ".\picture\model\\bowu\\finish.png"
image_bowu_reward_path = ".\picture\model\\bowu\\reward.png"
image_click_reward_path = ".\picture\model\\bowu\\clickReward.png"

# 外勤
image_waiqin_path = ".\picture\model\\waiqin\\waiqin.png"
image_startWaiqin_path = ".\picture\model\\waiqin\\startWaiqin.png"
image_waiqin_ok_path = ".\picture\model\\waiqin\\ok.png"
image_zhengzai_path = ".\picture\model\\waiqin\\zhengzaiwaiqin.png"