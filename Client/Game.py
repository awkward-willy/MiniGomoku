import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "True"
import threading
from pygame.locals import QUIT, KEYDOWN
import numpy as np
import pygame


class Game:
    def __init__(self, client_socket, room_number, turn):
        pygame.init()
        pygame.display.set_caption("五子棋遊戲")
        self.client_socket = client_socket
        self.room_number = room_number

        self.turn = turn  # 0表還未分配，1表黑子，2表白子
        self.current_player = 1
        # Game setup
        self.screen = pygame.display.set_mode((670, 670))
        self.screen_color = [238, 154, 73]
        self.line_color = [0, 0, 0]
        self.game_running = True
        self.flag = False
        self.quitFlag = False
        self.tim = 0
        self.over_pos = []
        self.white_color = [255, 255, 255]
        self.black_color = [0, 0, 0]

    def start_game(self):
        # Start a thread to receive game updates
        threading.Thread(target=self.receive_game_updates).start()
        self.run_game_loop()

    def stop_game(self):
        self.game_running = False

    def check_win(self, over_pos):
        mp = np.zeros([15, 15], dtype=int)
        for val in over_pos:
            x = int((val[0][0]-27)/44)
            y = int((val[0][1]-27)/44)
            if val[1] == self.white_color:
                mp[x][y] = 2
            else:
                mp[x][y] = 1

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
                if len(pos1) >= 5:
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

    def find_pos(self, x, y):  # 找到顯示的可以落子的位置
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

    def check_over_pos(self, x, y, over_pos):  # 檢查當前的位置是否已經落子
        for val in over_pos:
            if val[0][0] == x and val[0][1] == y:
                return False
        return True  # 表示沒有落子

    def run_game_loop(self):
        while self.game_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.client_socket.send(f"GameOver.".encode('utf-8'))
                    self.game_running = False
                    self.game_over()
                    self.quitFlag = True
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.client_socket.send(
                            f"GameOver.".encode('utf-8'))
                        self.game_running = False
                        self.game_over()
                        self.quitFlag = True
            if self.quitFlag:
                break
            self.screen.fill(self.screen_color)

            # ... (draw the game board, pieces, etc.)
            for i in range(27, 670, 44):
                # 先畫豎線
                if i == 27 or i == 670-27:  # 邊緣線稍微粗一些
                    pygame.draw.line(self.screen, self.line_color, [
                                     i, 27], [i, 670-27], 4)
                else:
                    pygame.draw.line(self.screen, self.line_color, [
                                     i, 27], [i, 670-27], 2)
                # 再畫橫線
                if i == 27 or i == 670-27:  # 邊緣線稍微粗一些
                    pygame.draw.line(self.screen, self.line_color, [
                                     27, i], [670-27, i], 4)
                else:
                    pygame.draw.line(self.screen, self.line_color, [
                                     27, i], [670-27, i], 2)

            # 在棋盤中心畫個小圓表示正中心位置
            pygame.draw.circle(self.screen, self.line_color,
                               [27+44*7, 27+44*7], 8, 0)

            for val in self.over_pos:  # 顯示所有落下的棋子
                pygame.draw.circle(self.screen, val[1], val[0], 20, 0)

            # 判斷是否存在五子連心
            res = self.check_win(self.over_pos)
            if res[0] != 0:
                for pos in res[1]:
                    pygame.draw.rect(self.screen, [238, 48, 167], [
                        pos[0]*44+27-22, pos[1]*44+27-22, 44, 44], 2, 1)
                pygame.display.update()  # 重繪顯示
                self.winner = res[0]
                font = pygame.font.Font("./Resources/標楷體.ttf", 74)
                if self.winner == self.turn:
                    text = font.render('勝利!', True, (0, 255, 0))
                else:
                    text = font.render('失敗!', True, (255, 0, 0))

                text_rect = text.get_rect(center=(670 // 2, 670 // 2))
                self.screen.blit(text, text_rect)
                pygame.display.flip()
                break

            # 獲取滑鼠坐標資訊
            x, y = pygame.mouse.get_pos()

            x, y = self.find_pos(x, y)
            # 判斷是否可以落子，再顯示
            if self.check_over_pos(x, y, self.over_pos) and self.current_player == self.turn:
                pygame.draw.rect(self.screen, [0, 229, 238], [
                                 x-22, y-22, 44, 44], 2, 1)
            elif self.check_over_pos(x, y, self.over_pos) and self.current_player != self.turn:
                pygame.draw.rect(self.screen, [255, 0, 0], [
                                 x-22, y-22, 44, 44], 2, 1)

            keys_pressed = pygame.mouse.get_pressed()  # 獲取滑鼠按鍵資訊
            # 滑鼠左鍵表示落子,tim用來延時的，因為每次回圈時間間隔很斷，容易導致明明只按了一次左鍵，卻被多次獲取，認為我按了多次
            if keys_pressed[0] and self.tim == 0:
                self.flag = True
                # 判斷是否可以落子，再落子
                if self.check_over_pos(x, y, self.over_pos) and self.current_player == self.turn:
                    if len(self.over_pos) % 2 == 0:  # 黑子
                        self.over_pos.append([[x, y], self.black_color])
                        self.client_socket.send(
                            f"Move:{x},{y}".encode('utf-8'))
                        self.current_player = 2
                    else:
                        self.over_pos.append([[x, y], self.white_color])
                        self.client_socket.send(
                            f"Move:{x},{y}".encode('utf-8'))
                        self.current_player = 1

            # 滑鼠左鍵延時作用
            if self.flag:
                self.tim += 1
            if self.tim % 50 == 0:  # 延時200ms
                self.flag = False
                self.tim = 0
            pygame.display.update()

    def game_over(self):
        self.game_running = False
        self.client_socket.close()
        pygame.quit()

    # Receive game updates from the server

    def receive_game_updates(self):
        while self.game_running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                print(message)
            except ConnectionAbortedError:
                # Handle the case where the connection is aborted
                print("Error: Connection aborted.")
                self.client_socket.close()
                self.game_running = False
                break
            except ConnectionResetError:
                print("Error: Server disconnected.")
                self.client_socket.close()
                self.game_running = False
                break
            except:
                # Handle the case where the connection is closed
                print("Error: Connection closed.")
                self.client_socket.close()
                self.game_running = False
                break

            # Handle game updates received from the server
            if message.startswith("Move:"):
                move_info = message[5:]
                x, y = map(int, move_info.split(','))
                print(f"Received move: {x}, {y}")
                # Update the game state with the received move
                if self.tim == 0:
                    self.flag = True
                    if self.check_over_pos(x, y, self.over_pos):
                        if len(self.over_pos) % 2 == 0:
                            self.over_pos.append([[x, y], self.black_color])
                            self.current_player = 2
                        else:
                            self.over_pos.append([[x, y], self.white_color])
                            self.current_player = 1
                if self.flag:
                    self.tim += 1
                if self.tim % 50 == 0:
                    self.flag = False
                    self.tim = 0
                pygame.display.update()
            elif message.startswith("GameOver."):
                self.game_running = False
                self.game_over()
                break
            else:
                print(f"Error: Invalid message received: {message}")
                self.game_running = False
                self.game_over()
                break
        self.client_socket.close()
