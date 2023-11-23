from PyQt6.QtCore import QThread, pyqtSignal


class GameThread(QThread):
    gameover = pyqtSignal()

    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.game = game

    def run(self):
        self.game.start_game()
        self.gameover.emit()


class WaitingThread(QThread):
    responseReceived = pyqtSignal(str)

    def __init__(self, socket, parent=None):
        super().__init__(parent)
        self.socket = socket
        self.isRunning = True

    def run(self):
        while self.isRunning:
            try:
                response = self.socket.recv(1024).decode('utf-8')
                if response == "Start game!":
                    self.isRunning = False
                    self.responseReceived.emit(response)
                else:
                    print(response)
                    self.responseReceived.emit(response)
            except:
                self.isRunning = False
                self.responseReceived.emit("Server terminate")
                break

    def quit(self):
        self.isRunning = False
        super().quit()
