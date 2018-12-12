'''
包含了游戏中的设置常量
'''

# 界面设置
SCREENWIDTH  = 288
SCREENHEIGHT = 512
FPS = 60
DURATION = 1000//FPS

# 游戏设置
SPEED = 125     # 前进速度(px/s)

PIPESLOT = 180  # 管道间隔(px)
PIPESLOT = max(PIPESLOT, (SCREENWIDTH+60)//2)
SLOT = 100      # 上下管道间隙
PP_MIN = -250
PP_MAX = -120   # 管道随机位置(pipe position)