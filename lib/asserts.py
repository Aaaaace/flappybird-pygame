'''
包含了游戏中的图片、音效资源
'''
import sys

# ------图片资源------
# 小鸟
BIRD_LIST = (
    [
        'assets\\sprites\\bluebird-downflap.png',
        'assets\\sprites\\bluebird-midflap.png',
        'assets\\sprites\\bluebird-upflap.png',
    ],[
        'assets\\sprites\\redbird-downflap.png',
        'assets\\sprites\\redbird-midflap.png',
        'assets\\sprites\\redbird-upflap.png',
    ],[
        'assets\\sprites\\yellowbird-downflap.png',
        'assets\\sprites\\yellowbird-midflap.png',
        'assets\\sprites\\yellowbird-upflap.png',
    ],
)
# 管道
PIPE_LIST = (
    'assets\\sprites\\pipe-green.png',
    'assets\\sprites\\pipe-red.png',
)
# 背景
BACKGROUND_LIST = [
    'assets\\sprites\\background-day.png',
    'assets\\sprites\\background-night.png',
]
# 游戏开始信息
STARTMESSAGE = 'assets\\sprites\\message.png'
# 游戏结束信息
GAMEOVERMESSAGE = 'assets\\sprites\\gameover.png'
# 地面
BASE = 'assets\\sprites\\base.png'
# 计分板数字
NUMBER_LIST = [
    'assets\\sprites\\%s.png' % i for i in range(10)
]

# ------音效文件------
# 振翅音效
SOUND_FLAP = ('assets\\audio\\wing.wav', 'assets\\audio\\wing.ogg')
# 撞击音效
SOUND_HIT = ('assets\\audio\\hit.wav', 'assets\\audio\\hit.ogg')
# 死亡音效
SOUND_DIE = ('assets\\audio\\die.wav', 'assets\\audio\\die.ogg')