'''
包含了游戏中的所有Sprite
'''

import pygame
from pygame.locals import *
import constants
from itertools import cycle
from gameobjects import Vec2d
import random

from asserts import BIRD_LIST, PIPE_LIST, BASE, NUMBER_LIST     # 图片资源


class Bird(pygame.sprite.Sprite):
    '''
    <summary>玩家控制的小鸟，只用于更新小鸟的动画(结构通用)</summary>
    '''
    _FPS = 5                            # sprite动画FPS
    _duration = 1000//_FPS              # 每一帧持续的时间(ms)
    _number = 4                         # 帧数量
    _loop = cycle([0, 1, 2, 1])         # 帧循环顺序
    
    def __init__(self, position, color=0):
        super().__init__()
        self.passed_frame = 0                       # 经过的帧
        self.imageidx = next(self._loop)            # 当前帧下标
        self.images = [
            pygame.image.load(file).convert_alpha() for file in BIRD_LIST[color]
        ]
        self.image = self.images[self.imageidx]     # 显示的surface
        self.width, self.height = self.image.get_size()
        self.rect = Rect(position, (self.width, self.height))
        self.passed_time = 0                        # 过去的时间(ms)
    
    def update(self, passed_time):
        '''
        更新小鸟动画帧
        '''
        self.passed_time += passed_time
        self.passed_frame = self.passed_time // self._duration
        for _ in range(self.passed_frame):
            self.imageidx = next(self._loop)
        self.image = self.images[self.imageidx]
        self.passed_time -= self._duration * self.passed_frame

class Pipe(pygame.sprite.Sprite):
    '''
    <summary>管道</summary>
    '''
    _sloty = constants.SLOT
    _slotx = constants.PIPESLOT
    def __init__(self, position, image):
        '''
        <param name="position">管道的初始坐标</param>
        '''
        super().__init__()
        self.speed = constants.SPEED
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = Rect(position, (self.width, self.height))
        self.passed_time = 0
        
    def update(self, passed_time, up_y=None):
        '''
        <summary>更新管道位置</summary>
        '''
        self.passed_time += passed_time
        move_distance = self.passed_time*self.speed//1000
        self.passed_time -= move_distance*1000/self.speed
        self.rect[0] -= move_distance
        if self.rect[0] < -self.width:
            y = up_y or random.randint(constants.PP_MIN, constants.PP_MAX)
            if up_y:
                y += self.height + constants.SLOT   # 下管道y坐标
            self.rect[0:2] = Vec2d(2 * self._slotx - self.width, y)
            return self.rect[1]
        return None

class Base(pygame.sprite.Sprite):
    '''
    地面
    '''
    def __init__(self):
        super().__init__()
        self.speed = constants.SPEED
        self.image = pygame.image.load(BASE).convert()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.position = Vec2d(0, constants.SCREENHEIGHT - self.height)
        self.baseshift = self.width - constants.SCREENWIDTH  # 用于重置地面位置
        self.passed_time = 0
        
    def update(self, passed_time):
        self.passed_time += passed_time
        basexmovement = self.passed_time*self.speed//1000
        self.passed_time -= basexmovement*1000/self.speed
        self.position[0] = -((-self.position[0] + basexmovement) % self.baseshift)
        
class ScoreFigure(pygame.sprite.Sprite):
    '''<summary>分数板</summary>'''
    def __init__(self):
        super().__init__()
        self.score = 0
        self.figures = [
            pygame.image.load(NUMBER_LIST[i]).convert_alpha() \
                for i in range(10)
        ]
        self.image = self.figures[0]
        self.width, self.height = self.image.get_size()
        self.rect = Rect(
            (constants.SCREENWIDTH-self.width)//2,
            int(0.15*constants.SCREENHEIGHT), self.width, self.height
        )
    
    def update(self, score):
        if score <= self.score:
            return
        self.score = score
        figures = []
        while score > 0:
            figures.append(score%10)
            score = score//10
        self.image = pygame.surface.Surface(
            (self.width*len(figures),self.height), 0, 32
        )
        self.image.fill((0,0,255))
        self.image.set_colorkey((0,0,255))
        
        width, height = self.image.get_size()
        self.rect.x = (constants.SCREENWIDTH - width)//2
        
        for idx, figure in enumerate(figures):
            figurex = width - (idx+1)*self.width
            figurex += (self.width - self.figures[figure].get_width())//2
            self.image.blit(self.figures[figure], (figurex,0))