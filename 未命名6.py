# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 21:35:57 2024

@author: 86132
"""

import pygame
import random
import time
import json
import os
# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (220, 220, 220)
BUTTON_HIGHLIGHT_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = (0, 0, 0)
# 按钮位置和大小
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
BUTTON_SPACING = 50
BUTTON_START_X = WIDTH // 2 - (3 * BUTTON_WIDTH // 2 + BUTTON_SPACING)
EASY_BUTTON_RECT = pygame.Rect(BUTTON_START_X, HEIGHT // 2 - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
MEDIUM_BUTTON_RECT = pygame.Rect(BUTTON_START_X + BUTTON_WIDTH + BUTTON_SPACING, HEIGHT // 2 - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
HARD_BUTTON_RECT = pygame.Rect(BUTTON_START_X + 2 * (BUTTON_WIDTH + BUTTON_SPACING), HEIGHT // 2 - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
REPLAY_BUTTON_RECT = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 100, BUTTON_WIDTH, BUTTON_HEIGHT)
EXIT_BUTTON_RECT = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 180, BUTTON_WIDTH, BUTTON_HEIGHT)

MENU_BG_COLOR = (245, 245, 245)
TIME_LIMIT = {"easy": 120, "medium": 100, "hard": 80}
SCORE_PER_MATCH = 10

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("开心消消乐小游戏")
clock = pygame.time.Clock()

# 加载字体
font = pygame.font.Font(None, 36)
def load_high_score():
    path = "high_score.json"
    if not os.path.exists(path):
        # 文件不存在，创建文件并写入默认分数
        save_high_score(0)
    try:
        with open(path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # 如果文件存在但无法读取，创建文件并写入默认分数
        save_high_score(0)
        return 0
def draw_timer(elapsed_time, time_limit):
    timer_text = font.render(f"{int(time_limit - elapsed_time)}s", True, TEXT_COLOR)
    timer_rect = timer_text.get_rect(topright=(WIDTH - 10, 10))  # 调整位置到右上角
    screen.blit(timer_text, timer_rect)
def save_high_score(score):
    path = "high_score.json"
    try:
        with open(path, "w") as file:
            json.dump(score, file)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
# 加载图案图片
patterns = [pygame.image.load(f"stable-diffusion-ai ({i}).webp") for i in range(1, 7)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 游戏状态
game_state = "menu"  # "menu", "playing", "game_over"
score = 0
high_score = 0
difficulty = "medium"

def create_board():
    num_pairs = ROWS * COLS*2
    # 生成每个图案两次的列表
    board_flat = [pattern for pattern in patterns for _ in range(2)]
   
    # 如果列表中的元素不足 ROWS * COLS 个，则重复使用图案直到足够
    while len(board_flat) < num_pairs:
       board_flat += [pattern for pattern in patterns for _ in range(2)] 
       random.shuffle(board_flat)
    # 创建配对
    pairs = []
    for i in range(0, len(board_flat), 2):
        pairs.append((board_flat[i], board_flat[i+1]))
    
    # 打乱配对
    
    random.shuffle(pairs)
    board = []
    for pair in pairs:
        board.append([pair[0], pair[1]])
    return board + [None] * (ROWS * COLS - len(pairs))


board = create_board()
selected = []
def draw_menu():
    screen.blit(background_image, (0, 0))
    menu_text = font.render("Click to Start", True, TEXT_COLOR)
    menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
    screen.blit(menu_text, menu_rect)
    
    # 绘制难度选择按钮
    easy_text = font.render("Easy", True, BUTTON_TEXT_COLOR)
    medium_text = font.render("Medium", True, BUTTON_TEXT_COLOR)
    hard_text = font.render("Hard", True, BUTTON_TEXT_COLOR)
    
    # 绘制按钮
    pygame.draw.rect(screen, BUTTON_COLOR, EASY_BUTTON_RECT)
    pygame.draw.rect(screen, BUTTON_COLOR, MEDIUM_BUTTON_RECT)
    pygame.draw.rect(screen, BUTTON_COLOR, HARD_BUTTON_RECT)
    
    # 计算文本位置
    easy_text_rect = easy_text.get_rect(center=EASY_BUTTON_RECT.center)
    medium_text_rect = medium_text.get_rect(center=MEDIUM_BUTTON_RECT.center)
    hard_text_rect = hard_text.get_rect(center=HARD_BUTTON_RECT.center)
    
    # 绘制文本
    screen.blit(easy_text, easy_text_rect)
    screen.blit(medium_text, medium_text_rect)
    screen.blit(hard_text, hard_text_rect)
    
    # 获取时间限制并渲染文本
    easy_time_text = font.render(f"{TIME_LIMIT['easy']}s", True, BUTTON_TEXT_COLOR)
    medium_time_text = font.render(f"{TIME_LIMIT['medium']}s", True, BUTTON_TEXT_COLOR)
    hard_time_text = font.render(f"{TIME_LIMIT['hard']}s", True, BUTTON_TEXT_COLOR)
    
    # 计算时间文本位置
    easy_time_rect = easy_time_text.get_rect(center=(EASY_BUTTON_RECT.centerx, EASY_BUTTON_RECT.bottom+20))
    medium_time_rect = medium_time_text.get_rect(center=(MEDIUM_BUTTON_RECT.centerx, MEDIUM_BUTTON_RECT.bottom+20))
    hard_time_rect = hard_time_text.get_rect(center=(HARD_BUTTON_RECT.centerx, HARD_BUTTON_RECT.bottom+20))
    
    # 绘制时间文本
    screen.blit(easy_time_text, easy_time_rect)
    screen.blit(medium_time_text, medium_time_rect)
    screen.blit(hard_time_text, hard_time_rect)
# 游戏结束，显示分数和最高分
def draw_game_over():
    screen.blit(background_image, (0, 0))
    game_over_text = font.render("Game Over", True, TEXT_COLOR)
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    high_score_text = font.render(f"High Score: {high_score}", True, TEXT_COLOR)
    
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(high_score_text, high_score_rect)
    
    # 绘制“再来一局”和“退出”按钮
    pygame.draw.rect(screen, BUTTON_COLOR, REPLAY_BUTTON_RECT)
    pygame.draw.rect(screen, BUTTON_COLOR, EXIT_BUTTON_RECT)
    
    replay_text = font.render("Replay", True, BUTTON_TEXT_COLOR)
    exit_text = font.render("Exit", True, BUTTON_TEXT_COLOR)
    
    replay_text_rect = replay_text.get_rect(center=REPLAY_BUTTON_RECT.center)
    exit_text_rect = exit_text.get_rect(center=EXIT_BUTTON_RECT.center)
    
    screen.blit(replay_text, replay_text_rect)
    screen.blit(exit_text, exit_text_rect)
    
    
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            index = row * COLS + col
            tiles = board[index]
            if tiles:  # 如果还有图案
                screen.blit(tiles[-1], (col * TILE_SIZE, row * TILE_SIZE))  # 只绘制最上面的图案

def check_match():
    global score
    if len(selected) == 2:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        index1 = r1 * COLS + c1
        index2 = r2 * COLS + c2
        if index1 != index2 and board[index1][-1] == board[index2][-1]:  # 检查最下面的图案是否匹配
            board[index1].pop()  # 移除匹配的图案
            board[index2].pop()
            score += SCORE_PER_MATCH  # 增加分数
            if not board[index1]:  # 如果该位置没有更多图案
                board[index1] = None
            if not board[index2]:
                board[index2] = None
            selected.clear()
            return True
    selected.clear()
    return False
background_image = pygame.image.load("background.png")  # 确保路径正确
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # 缩放到屏幕尺寸
# 主游戏循环
running = True
clock = pygame.time.Clock()
start_time = time.time()  # 记录游戏开始时间
high_score = load_high_score()
while running:
    clock.tick(FPS)
    # 绘制背景图案
    screen.blit(background_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if game_state == "menu":
                # 检测点击位置是否在开始按钮区域内        
                if EASY_BUTTON_RECT.collidepoint(x, y):
                    difficulty = "easy"
                    game_state = "playing"
                    board = create_board()
                    score = 0
                    start_time = time.time()
                elif MEDIUM_BUTTON_RECT.collidepoint(x, y):
                    difficulty = "medium"
                    game_state = "playing"
                    board = create_board()
                    score = 0
                    start_time = time.time()
                elif HARD_BUTTON_RECT.collidepoint(x, y):
                    difficulty = "hard"
                    game_state = "playing"
                    board = create_board()
                    score = 0
                    start_time = time.time()
            elif game_state == "playing":
                col, row = x // TILE_SIZE, y // TILE_SIZE
                index = row * COLS + col
                if 0 <= index < len(board) and board[index] is not None:  # 检查是否有图案
                    if len(selected) < 2:
                        selected.append((row, col))
                    if len(selected) == 2:
                        if check_match():  # 检查是否匹配并消除
                            print("Match found and collapsed.")
                            
                        else:
                            selected.clear()
            elif game_state == "game_over":
                if REPLAY_BUTTON_RECT.collidepoint(x, y):
                    game_state = "menu"  # 重置游戏状态为菜单
                    board = create_board()  # 重新创建游戏板
                    score = 0  # 重置分数
                    selected = []  # 清空已选图案
                    start_time = time.time()  # 重置开始时间
                    difficulty = "medium"  # 可以让用户选择难度
                elif EXIT_BUTTON_RECT.collidepoint(x, y):
                    running = False  # 退出游戏
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_board()
        draw_timer(time.time() - start_time, TIME_LIMIT[difficulty])  # 绘制倒计时
        # 检查游戏是否结束
        if all(board[row * COLS + col] is None for row in range(ROWS) for col in range(COLS)):
            game_state = "game_over"
    elif game_state == "game_over":
        high_score = max(high_score, score)
        save_high_score(high_score)
        draw_game_over()
           
    pygame.display.flip()

    if game_state == "playing":
        elapsed_time = time.time() - start_time
        if elapsed_time > TIME_LIMIT[difficulty]:
            game_state = "game_over"

# 保存最高分
pygame.quit()