# -*- coding: utf-8 -*-

import wda
import logging
import os
import random
from time import sleep
import time

# 日志输出
logging.basicConfig(format='[%(asctime)s][%(name)s:%(levelname)s(%(lineno)d)][%(module)s:%(funcName)s]:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

# 屏幕分辨率 该分辨率是通过wda的inspector得到的。
# device_x, device_y = 1920, 1080
device_x, device_y = 667, 375
# 截图的分辨率
base_x, base_y = 667, 375

# 小号 60左右 da 30
FIGHT_TIME = 30

# 刷金币次数
repeat_times = 175

c = wda.Client('http://127.0.0.1:8100')
s = c.session()

# ===============================
# 所有坐标轴都以 左上角为原点
# home键在左方
# 按钮:再次挑战
# (650,130) (710,310)
rb_x1, rb_y1 = 520, 330
rb_x2, rb_y2 = 610, 360

# 返回按钮
return_x1, return_y1 = 410, 330
return_x2, return_y2 = 505, 365


def rechallenge_btn():
    x = random.uniform(rb_x1, rb_x2)
    y = random.uniform(rb_y1, rb_y2)
    logging.info("点击再次挑战按钮 [{},{}]".format(x, y))
    return (x, y)


# 按钮:闯关
# (600,220)  (670,400)
sb_x1, sb_y1 = 455, 290
sb_x2, sb_y2 = 540, 315


def start_btn():
    x = random.uniform(sb_x1, sb_x2)
    y = random.uniform(sb_y1, sb_y2)
    logging.info("点击闯关按钮 [{},{}]".format(tranX(x), tranY(y)))
    return (x, y)


# 按钮: 平A 640,115 r=50
def attack_btn():
    return circle_btn(607, 323, 20)


# 按钮: 技能1 660,345 r=35
def skill_one_btn():
    return circle_btn(495, 330, 10)


# 按钮: 技能2 515,255 r=35
def skill_two_btn():
    return circle_btn(537, 260, 10)


# 按钮: 技能3 435,120 r=35
def skill_three_btn():
    return circle_btn(605, 220, 10)


def circle_btn(rx, ry, r):
    x = 6666
    y = 2333
    while x * x + y * y > 5000 and not hit_start_or_recha(x, y):
        x = random.uniform(-r, r)
        y = random.uniform(-r, r)

    return (rx + x, ry + y)


def hit_start_or_recha(x, y):
    if sb_x2 < sb_x1 or sb_y2 < sb_y1 or rb_x2 < rb_x1 or rb_y2 < rb_y1:
        print("坐标2不能小于坐标1")
    if (x >= sb_x1 and x <= sb_x2 and y >= rb_x1 and y <= rb_x2) or \
            (x >= sb_x1 and x <= sb_x2 and y >= sb_y1 and y <= sb_y2) or (
            x >= return_x1 and x <= return_x2 and y >= return_y1 and y <= return_y2):
        return True
    return False


skill_cool_down_time = {
    "skill_one_btn": time.time() - 100,
    "skill_two_btn": time.time() - 100,
    "skill_three_btn": time.time() - 100,
}

skill_cool_down = {
    "skill_one_btn": 4,
    "skill_two_btn": 4,
    "skill_three_btn": 4,
}

skills = {
    "skill_one_btn": skill_one_btn(),
    "skill_two_btn": skill_two_btn(),
    "skill_three_btn": skill_three_btn(),
}


def do_attack_random():
    choice = random.randint(0, 3)
    if choice == 0:
        return attack_btn()
    elif choice == 1:
        return skill_one_btn()
    elif choice == 2:
        return skill_two_btn()
    elif choice == 3:
        return skill_three_btn()


def do_attack():
    now = time.time()
    for i in skill_cool_down:
        if now - skill_cool_down[i] > skill_cool_down_time[i]:
            skill_cool_down_time[i] = now
            logging.debug("click {}".format(i))
            return skills[i]
    logging.debug("click {}".format("attack_btn"))
    return attack_btn()


def tap_screen(func):
    """calculate real x, y according to device resolution."""
    pair = func()
    x = pair[0]
    y = pair[1]
    real_x = tranX(x)
    real_y = tranY(y)
    # os.system('adb shell input tap {} {}'.format(real_x, real_y))
    logging.debug("tap ({},{})".format(real_x, real_y))
    s.tap_hold(real_x, real_y, 200 / 1000)


def do_money_work():
    # 开始闯关
    tap_screen(start_btn)
    # 载入画面
    sleep(4)

    # 战斗场景
    start = time.time()
    while time.time() - start < FIGHT_TIME:
        try:
            tap_screen(do_attack)
            sleep(random.uniform(0.2, 0.4))
        except Exception as e:
            print(e)

    tap_screen(rechallenge_btn)
    sleep(2)


def tranX(x):
    return int(x / base_x * device_x)


def tranY(y):
    return int(y / base_y * device_y)


if __name__ == '__main__':
    mstart = time.time()
    mround = 0
    try:
        for i in range(repeat_times):
            mround = i + 1
            logging.info('round #{}'.format(i + 1))
            try:
                do_money_work()
                logging.info("本次共进行{}轮游戏,总用时{}s,预计刷金币{}g".format(mround, (time.time() - mstart) / 60, 19 * mround))
            except Exception as e:
                print(e)
        # for i in range(100):
        #     tap_screen(start_btn)
    except KeyboardInterrupt as k:
        pass
    finally:
        logging.info("本次共进行{}轮游戏,总用时{}s,预计刷金币{}g".format(mround, (time.time() - mstart) / 60, 19 * mround))
        logging.debug("关闭session")
        s.close()
