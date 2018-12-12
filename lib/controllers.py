'''
包含了游戏中的所有sprite的控制器
用于控制sprite的状态、动作、方向、速度、碰撞等属性
'''

import pygame
from pygame.locals import *
import sprites



def gethitmask(surface):
    '''
    <summary>根据alpha获取surface的碰撞体积</summary>
    <param name="surfaces">surface列表</param>
    <return name="hitmasks">hitmask列表(list)</param>
    '''
    width, height = surface.get_size()
    hitmask = []
    for x in range(width):
        hitmask.append([])
        for y in range(height):
            hitmask[x].append(bool(surface.get_at((x, y))[3]))
    return hitmask

def crashdetect_mask(rect1, hitmask1, rect2, hitmask2):
    '''
    碰撞检测，碰撞返回True
    '''
    overlap_area = rect1.clip(rect2)
    if overlap_area.width == 0 or overlap_area.height == 0:
        return False
    
    x1_start, y1_start = overlap_area.x - rect1.x, overlap_area.y - rect1.y
    x2_start, y2_start = overlap_area.x - rect2.x, overlap_area.y - rect2.y
    
    for x in range(overlap_area.width):
        for y in range(overlap_area.height):
            if hitmask1[x1_start+x][y1_start+y] and hitmask2[x2_start+x][y2_start+y]:
                return True
    return False
    
class BirdController(object):
    '''
    小鸟控制器
    控制小鸟的速度、角度、加速度、振翅动作
    '''
    _flapspeedyacc = -300       # y方向振翅后速度(px/s)
    _initspeedy = -100          # y方向速度(px/s)
    _gravityspeedyacc = 900     # y方向重力加速度(px/s2)
    _flapangleacc = 30          # 振翅后角度
    _initangle = 0              # 角度
    _gravityangleacc = -80      # 角度加速度
    
    def __init__(self, bird):
        super().__init__()
        self.passed_time = 0    # 过去的时间(ms)
        self.bird = bird
        self.bird_angle = self._initangle
        self.bird_speedy = self._initspeedy
        self.bird.masks = [
            gethitmask(pygame.transform.rotate(self.bird.image, angle*5)) \
                for angle in range(-18, 7)
        ]
        self.bird.mask = self.bird.masks[int(self.bird_angle/5 + 18.5)]
        self.bird.mask_sizes = [
            pygame.transform.rotate(self.bird.image, angle*5).get_size() \
                for angle in range(-18, 7)
        ]
        
    def flap(self):
        self.bird_angle = self._flapangleacc
        self.bird_speedy = self._flapspeedyacc
    
    def update(self, passed_time):
        '''更新速度、方向，并更新当前帧、位置'''
        self.bird.update(passed_time)
        # 方向
        self.bird_angle += passed_time/1000 * self._gravityangleacc
        if self.bird_angle <= -90:
            self.bird_angle = -90
        # 速度和位置
        self.bird_speedy += passed_time/1000 * self._gravityspeedyacc
        self.bird.rect[1] += int(passed_time/1000 * self.bird_speedy)
        if self.bird.rect[1] < 0:
            self.bird.rect[1] = 0
        self.bird.image = \
            pygame.transform.rotate(self.bird.image, self.bird_angle)
        # 碰撞蒙版
        idx = int(self.bird_angle/5 + 18.5)
        self.bird.mask = self.bird.masks[idx]
        self.bird.rect[2:4] = self.bird.mask_sizes[idx]
