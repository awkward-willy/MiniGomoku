from UI import Ui_MainWidget
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtWidgets import QWidget
import sys
import socket
from Game import Game
import Thread

ADDR = '127.0.0.1'
PORT = 8000


class Page(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)
        self.set_Control()
        self.show()

    def closeEvent(self, event):
        if hasattr(self, 'game') and self.game.game_running:
            self.showPopup("Error", "遊戲進行中，請先結束遊戲再離開！")
            event.ignore()
        else:
            event.accept()

    def set_Control(self):
        self.ui.JoinRoom_Button.clicked.connect(self.JoinGame)
        self.ui.lineEdit.textChanged.connect(self.inputRoomNumber)

    def inputRoomNumber(self):
        # must be number
        if not self.getRoomNumber().isnumeric():
            # remove last char
            self.ui.lineEdit.setText(self.getRoomNumber()[:-1])
        # max length: 5
        if len(self.getRoomNumber()) > 5:
            # remove last char
            self.ui.lineEdit.setText(self.getRoomNumber()[:-1])

    def getRoomNumber(self):
        return self.ui.lineEdit.text()

    def checkRoomNumber(self):
        # check room number
        if self.getRoomNumber() == '':
            self.showPopup('Error', 'Please enter room number.')
            return 0
        # check room number
        if not self.getRoomNumber().isnumeric():
            self.showPopup('Error', 'Room number must be number.')
            return 0
        # check room number
        if len(self.getRoomNumber()) > 5:
            self.showPopup('Error', 'Room number must be 5 digits.')
            return 0
        # check room number
        if len(self.getRoomNumber()) < 5:
            self.showPopup('Error', 'Room number must be 5 digits.')
            return 0
        return 1

    def JoinGame(self):
        check = self.checkRoomNumber()
        if check == 0:
            return
        else:
            try:
                self.client_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((ADDR, PORT))
                self.client_socket.send(self.getRoomNumber().encode('utf-8'))
                response = self.client_socket.recv(1024).decode('utf-8')
                self.handleResponse(response)
            except:
                self.showPopup(
                    "Error", "Cannot connect to server, please try again later")
                return

    def handleResponse(self, response):
        if response == "Room is full. Try again later.":
            self.showPopup("Error", response)
            self.ui.JoinRoom_Button.setEnabled(True)
        elif response == "Server is busy. Try again later.":
            self.showPopup("Error", response)
            self.ui.JoinRoom_Button.setEnabled(True)
        elif response == "Success! Waiting for other player...":
            self.showPopup("Success", response)
            self.waitingThread = Thread.WaitingThread(self.client_socket)
            self.waitingThread.responseReceived.connect(self.doneWaiting)
            self.ui.JoinRoom_Button.setEnabled(False)
            self.waitingThread.start()
        elif response == "Start game!":
            self.showPopup("Success", response)
            self.game = Game(self.client_socket,
                             self.getRoomNumber(), 2)
            self.game_thread = Thread.GameThread(self.game)
            self.ui.JoinRoom_Button.setEnabled(False)
            self.game_thread.gameover.connect(self.game_over)
            self.game_thread.start()
        elif response == "Server terminate":
            self.showPopup("Error", "Server terminate")
        else:
            self.showPopup("Error", "Invalid message received.")

    def doneWaiting(self, response):
        if response == "Server terminate":
            self.showPopup("Error", "Server terminate")
            self.ui.JoinRoom_Button.setEnabled(True)
            return
        self.waitingThread.quit()
        self.game = Game(self.client_socket, self.getRoomNumber(), 1)
        self.game_thread = Thread.GameThread(self.game)
        self.ui.JoinRoom_Button.setEnabled(False)
        self.game_thread.gameover.connect(self.game_over)
        self.game_thread.start()

    def game_over(self):
        try:
            if (self.game.quitFlag == True):
                self.showPopup("Game Over", "您已離開遊戲！")
            elif (self.game.winner == 1 and self.game.turn == 1):
                self.showPopup("Game Over", "您已勝出！")
            elif (self.game.winner == 2 and self.game.turn == 2):
                self.showPopup("Game Over", "您已勝出！")
            elif (self.game.winner == 1 and self.game.turn == 2):
                self.showPopup("Game Over", "您已敗北！")
            elif (self.game.winner == 2 and self.game.turn == 1):
                self.showPopup("Game Over", "您已敗北！")
        except:
            self.showPopup("Game Over", "對方已經離開遊戲，您已勝出！")
        self.ui.JoinRoom_Button.setEnabled(True)
        self.game.game_over()
        pass

    def showPopup(self, title, content):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(content)
        dlg.setIcon(QMessageBox.Icon.Warning)
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        # use default styling
        dlg.setStyleSheet("background: none;")
        # 顯示彈出視窗
        dlg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app background
    login_window = Page()
    login_window.setWindowTitle('110403548_Socket Programming HW')
    sys.exit(app.exec())
