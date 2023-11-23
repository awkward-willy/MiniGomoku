import pygame
import numpy as np
from pygame.locals import QUIT, KEYDOWN
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "True"
# 呼叫常用關鍵字常量
# 初始化pygame
pygame.init()
# 獲取對顯示系統的訪問，并創建一個視窗screen
# 視窗大小為670x670
screen = pygame.display.set_mode((670, 670))
screen_color = [238, 154, 73]  # 設定畫布顏色,[238,154,73]對應為棕黃色
line_color = [0, 0, 0]  # 設定線條顏色，[0,0,0]對應黑色


def check_win(over_pos):  # 判斷五子連心
    mp = np.zeros([15, 15], dtype=int)
    for val in over_pos:
        x = int((val[0][0]-27)/44)
        y = int((val[0][1]-27)/44)
        if val[1] == white_color:
            mp[x][y] = 2  # 表示白子
        else:
            mp[x][y] = 1  # 表示黑子

    for i in range(15):
        pos1 = []
        pos2 = []
        for j in range(15):
            if mp[i][j] == 1:
                pos1.append([i, j])
            else:
                pos1 = []
            if mp[i][j] == 2:
                pos2.append([i, j])
            else:
                pos2 = []
            if len(pos1) >= 5:  # 五子連心
                return [1, pos1]
            if len(pos2) >= 5:
                return [2, pos2]

    for j in range(15):
        pos1 = []
        pos2 = []
        for i in range(15):
            if mp[i][j] == 1:
                pos1.append([i, j])
            else:
                pos1 = []
            if mp[i][j] == 2:
                pos2.append([i, j])
            else:
                pos2 = []
            if len(pos1) >= 5:
                return [1, pos1]
            if len(pos2) >= 5:
                return [2, pos2]
    for i in range(15):
        for j in range(15):
            pos1 = []
            pos2 = []
            for k in range(15):
                if i+k >= 15 or j+k >= 15:
                    break
                if mp[i+k][j+k] == 1:
                    pos1.append([i+k, j+k])
                else:
                    pos1 = []
                if mp[i+k][j+k] == 2:
                    pos2.append([i+k, j+k])
                else:
                    pos2 = []
                if len(pos1) >= 5:
                    return [1, pos1]
                if len(pos2) >= 5:
                    return [2, pos2]
    for i in range(15):
        for j in range(15):
            pos1 = []
            pos2 = []
            for k in range(15):
                if i+k >= 15 or j-k < 0:
                    break
                if mp[i+k][j-k] == 1:
                    pos1.append([i+k, j-k])
                else:
                    pos1 = []
                if mp[i+k][j-k] == 2:
                    pos2.append([i+k, j-k])
                else:
                    pos2 = []
                if len(pos1) >= 5:
                    return [1, pos1]
                if len(pos2) >= 5:
                    return [2, pos2]
    return [0, []]


def find_pos(x, y):  # 找到顯示的可以落子的位置
    if (x < 27):
        x = 27
    if (x > 670-27):
        x = 670-27
    if (y < 27):
        y = 27
    if (y > 670-27):
        y = 670-27
    for i in range(27, 670, 44):
        for j in range(27, 670, 44):
            L1 = i-22
            L2 = i+22
            R1 = j-22
            R2 = j+22
            if x >= L1 and x <= L2 and y >= R1 and y <= R2:
                return i, j
    return x, y


def check_over_pos(x, y, over_pos):  # 檢查當前的位置是否已經落子
    for val in over_pos:
        if val[0][0] == x and val[0][1] == y:
            return False
    return True  # 表示沒有落子


flag = False
tim = 0

over_pos = []  # 表示已經落子的位置
white_color = [255, 255, 255]  # 白棋顏色
black_color = [0, 0, 0]  # 黑棋顏色

while True:  # 不斷訓練重繪畫布

    for event in pygame.event.get():  # 獲取事件，如果滑鼠點擊右上角關閉按鈕，關閉
        if event.type in (QUIT, KEYDOWN):
            sys.exit()

    screen.fill(screen_color)  # 清屏
    for i in range(27, 670, 44):
        # 先畫豎線
        if i == 27 or i == 670-27:  # 邊緣線稍微粗一些
            pygame.draw.line(screen, line_color, [i, 27], [i, 670-27], 4)
        else:
            pygame.draw.line(screen, line_color, [i, 27], [i, 670-27], 2)
        # 再畫橫線
        if i == 27 or i == 670-27:  # 邊緣線稍微粗一些
            pygame.draw.line(screen, line_color, [27, i], [670-27, i], 4)
        else:
            pygame.draw.line(screen, line_color, [27, i], [670-27, i], 2)

    # 在棋盤中心畫個小圓表示正中心位置
    pygame.draw.circle(screen, line_color, [27+44*7, 27+44*7], 8, 0)

    for val in over_pos:  # 顯示所有落下的棋子
        pygame.draw.circle(screen, val[1], val[0], 20, 0)

    # 判斷是否存在五子連心
    res = check_win(over_pos)
    if res[0] != 0:
        for pos in res[1]:
            pygame.draw.rect(screen, [238, 48, 167], [
                             pos[0]*44+27-22, pos[1]*44+27-22, 44, 44], 2, 1)
        pygame.display.update()  # 重繪顯示
        continue  # 游戲結束，停止下面的操作
    # 獲取滑鼠坐標資訊
    x, y = pygame.mouse.get_pos()

    x, y = find_pos(x, y)
    if check_over_pos(x, y, over_pos):  # 判斷是否可以落子，再顯示
        pygame.draw.rect(screen, [0, 229, 238], [x-22, y-22, 44, 44], 2, 1)

    keys_pressed = pygame.mouse.get_pressed()  # 獲取滑鼠按鍵資訊
    # 滑鼠左鍵表示落子,tim用來延時的，因為每次回圈時間間隔很斷，容易導致明明只按了一次左鍵，卻被多次獲取，認為我按了多次
    if keys_pressed[0] and tim == 0:
        flag = True
        if check_over_pos(x, y, over_pos):  # 判斷是否可以落子，再落子
            if len(over_pos) % 2 == 0:  # 黑子
                over_pos.append([[x, y], black_color])
            else:
                over_pos.append([[x, y], white_color])

    # 滑鼠左鍵延時作用
    if flag:
        tim += 1
    if tim % 50 == 0:  # 延時200ms
        flag = False
        tim = 0

    pygame.display.update()  # 重繪顯示
