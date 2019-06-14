'''
游戏机制
'''
import os, sys

print(os.getcwd())

import pygame
from pygame.locals import *
import sprites
import controllers
from gameobjects import Vec2d
import random
from constants import *
from asserts import PIPE_LIST, BACKGROUND_LIST, STARTMESSAGE, GAMEOVERMESSAGE
from asserts import SOUND_HIT, SOUND_DIE
# from itertools import cycle


SCREEN = None       # 窗口
FPSclock = None     # 总时钟
# 函数使用的全局变量
swing_passed_time = 0

def run():
    
    # 初始设置
    pygame.init()
    pygame.event.set_blocked(MOUSEMOTION)
    pygame.display.set_caption('Flappy Bird')
    global FPSclock, SCREEN
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
    FPSclock = pygame.time.Clock()
    
    # 游戏循环
    while True:
        sprites_start = startMenu()
        message_over = maingame(sprites_start)
        gameover(message_over)

def startMenu():
    '''
    创建背景、小鸟、地面，再传递到maingame中
    '''
    def birdswing(bird, passed_time, swingderection):
        '''小鸟在游戏开始前上下摆动'''
        global swing_passed_time
        swing_passed_time += passed_time
        movementy = swing_passed_time//20
        swing_passed_time -= movementy*20
        if swingderection:
            bird.rect.y -= movementy
            if bird.rect.y < BIRDY - SWINGSCOPE:
                bird.rect.y = 2*(BIRDY - SWINGSCOPE) - bird.rect.y
                return not swingderection
            return swingderection
        else:
            bird.rect.y += movementy
            if bird.rect.y > BIRDY + SWINGSCOPE:
                bird.rect.y = 2*(BIRDY + SWINGSCOPE) - bird.rect.y
                return not swingderection
            return swingderection
    
    # 小鸟
    bird = sprites.Bird(Vec2d([BIRDX, BIRDY]), random.randint(0, 2))
    birdswingdirection = True  # 开始界面中小鸟上下摆动的方向，True表示上
    # 地面
    base = sprites.Base()
    # 背景和开始信息
    background = pygame.image.load(random.choice(BACKGROUND_LIST)).convert()
    startmessage = pygame.image.load(STARTMESSAGE).convert_alpha()
    message_position = Vec2d(
        (SCREENWIDTH-startmessage.get_width())//2,
        (SCREENHEIGHT-startmessage.get_height()-base.height)//2
    )
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif (event.type == KEYDOWN and event.key in (K_SPACE, K_UP, )) \
                or event.type == MOUSEBUTTONDOWN:
                    return {
                        'bird': bird,
                        'background': background,
                        'base': base,
                    }
        
        passed_time = FPSclock.tick(FPS)
        bird.update(passed_time)
        birdswingdirection = birdswing(bird, passed_time, birdswingdirection)
        base.update(passed_time)
        
        SCREEN.blit(background, (0, 0))
        SCREEN.blit(startmessage, message_position)
        SCREEN.blit(bird.image, bird.rect)
        SCREEN.blit(base.image, base.position)
        
        pygame.display.update()

def maingame(sprites_start):
    '''
    游戏开始后的内容
    '''
    score = 0
    maygetscore = False
    scorefigure = sprites.ScoreFigure()
    # 管道
    pipes = {}
    pipecolor = random.randint(0, 1)
    pipepositionys = [random.randint(PP_MIN, PP_MAX) for _ in range(2)]
    
    pipeexample = pygame.image.load(PIPE_LIST[pipecolor]).convert_alpha()
    pipeexample_inv = pygame.transform.flip(pipeexample, 0, 1)
    pipe_width, pipe_height = pipeexample.get_size()
    
    pipes['top'] = (
        sprites.Pipe(Vec2d(2*SCREENWIDTH, pipepositionys[0]), pipeexample_inv.copy()),
        sprites.Pipe(Vec2d(2*SCREENWIDTH+PIPESLOT, pipepositionys[1]), pipeexample_inv.copy()),
    )
    pipes['bottom'] = (
        sprites.Pipe(Vec2d(2*SCREENWIDTH, pipepositionys[0]+pipe_height+SLOT), pipeexample.copy()),
        sprites.Pipe(Vec2d(2*SCREENWIDTH+PIPESLOT, pipepositionys[1]+pipe_height+SLOT), pipeexample.copy()),
    )
    for idx in range(2):
        pipes['top'][idx].mask = controllers.gethitmask(pipes['top'][idx].image)
        pipes['bottom'][idx].mask = controllers.gethitmask(pipes['bottom'][idx].image)
    
    # 从startMenu获取的sprites
    bird = sprites_start['bird']
    background = sprites_start['background']
    base = sprites_start['base']
    # 小鸟控制器
    birdcontroller = controllers.BirdController(bird)
    birdcontroller.flap()   # 振翅
    
    # 主循环
    while True:
        # 事件监听
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_r:
                return None
            elif (event.type == KEYDOWN and event.key in (K_SPACE, K_UP, )) \
                or event.type == MOUSEBUTTONDOWN:
                birdcontroller.flap()  # 振翅
        
        passed_time = FPSclock.tick(FPS)
        # 更新小鸟、地面、管道
        birdcontroller.update(passed_time)
        base.update(passed_time)
        up_y1 = pipes['top'][0].update(passed_time)
        up_y2 = pipes['top'][1].update(passed_time)
        pipes['bottom'][0].update(passed_time, up_y1)
        pipes['bottom'][1].update(passed_time, up_y2)
        scorefigure.update(score)
        
        if maygetscore and \
            (bird.rect.x > pipes['top'][0].rect.x \
            or bird.rect.x > pipes['top'][1].rect.x):
            score += 1
            maygetscore = False
            
        if bird.rect.x < pipes['top'][0].rect.x \
            and bird.rect.x < pipes['top'][1].rect.x:
            maygetscore = True
        
        # 碰撞检测
        if bird.rect[1] + bird.image.get_width()/1.5 > base.position[1] or \
            crashdetect(bird,(
                    pipes['top'][0], pipes['top'][1],
                    pipes['bottom'][0], pipes['bottom'][1],)):
            pygame.mixer.Sound(SOUND_HIT[0]).play()
            return{
                'birdcontroller': birdcontroller,
                'pipes': pipes,
                'base': base,
                'background': background,
                'scorefigure': scorefigure, 
            }
        # 绘制
        SCREEN.blit(background, (0, 0))
        SCREEN.blits((
                (pipes['top'][0].image, pipes['top'][0].rect),
                (pipes['bottom'][0].image, pipes['bottom'][0].rect),
                (pipes['top'][1].image, pipes['top'][1].rect),
                (pipes['bottom'][1].image, pipes['bottom'][1].rect),
        ))
        SCREEN.blit(base.image, base.position)
        SCREEN.blit(scorefigure.image, scorefigure.rect)
        SCREEN.blit(bird.image, bird.rect)
        pygame.display.update()

def gameover(sprites_end):
    '''
    结束动画和结束信息
    '''
    if sprites_end is None:
        return None
    pygame.mixer.Sound(SOUND_DIE[0]).play()
    base = sprites_end['base']
    background = sprites_end['background']
    pipes = sprites_end['pipes']
    birdcontroller = sprites_end['birdcontroller']
    scorefigure = sprites_end['scorefigure']
    
    birdcontroller.bird_angle = 30
    birdcontroller.bird_speedy = 100
    birdcontroller._gravityspeedyacc *= 1.5
    birdcontroller._gravityangleacc *= 4
    bird = birdcontroller.bird
    gameovermessage = pygame.image.load(GAMEOVERMESSAGE).convert_alpha()
    gameoverwidth, gameoverheight = gameovermessage.get_size()
    SCREEN.blit(gameovermessage,
        ((SCREENWIDTH-gameoverwidth)//2, int(0.33*SCREENHEIGHT)))
    pygame.display.update()
    
    FPSclock.tick()
    
    # 游戏结束动画
    while True:
        passed_time = FPSclock.tick(FPS)
        birdcontroller.update(passed_time)
        if bird.rect[1] + bird.image.get_width()/1.5 > base.position[1]:
            break
        
        SCREEN.blit(background, (0, 0))
        SCREEN.blits((
                (pipes['top'][0].image, pipes['top'][0].rect),
                (pipes['bottom'][0].image, pipes['bottom'][0].rect),
                (pipes['top'][1].image, pipes['top'][1].rect),
                (pipes['bottom'][1].image, pipes['bottom'][1].rect),
                (base.image, base.position),
                (scorefigure.image, scorefigure.rect),
        ))
        # SCREEN.blit(base.image, base.position)
        SCREEN.blit(bird.image, bird.rect)
        SCREEN.blit(gameovermessage,
            ((SCREENWIDTH-gameoverwidth)//2, int(0.35*SCREENHEIGHT)))
        pygame.display.update()
        
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type in (KEYDOWN, MOUSEBUTTONDOWN):
                return None
    
def crashdetect(bird, pipelist):
    '''游戏中对小鸟与管道的碰撞检测'''
    for pipe in pipelist:
        if controllers.crashdetect_mask(
            bird.rect, bird.mask, pipe.rect, pipe.mask
        ):
            return True
    return False

    
if __name__ == '__main__':
    MAIN_DIR = os.path.split(os.path.abspath(sys.argv[0]))[0]
    os.chdir(MAIN_DIR)
    os.chdir('..')  # 调用assets内数据需要到该文件夹
    run()
