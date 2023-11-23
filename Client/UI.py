# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'UILtSaRT.ui'
##
# Created by: Qt User Interface Compiler version 6.4.3
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PyQt6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PyQt6.QtCore import *
from PyQt6.QtGui import (QFont, QPixmap)
from PyQt6.QtWidgets import (
    QGridLayout, QLabel, QLineEdit, QPushButton)
import background_rc


class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.resize(765, 368)
        MainWidget.setMaximumSize(QSize(1000, 550))
        MainWidget.setStyleSheet(
            u"background-image: url(:/Resources/Background.png);")
        background_label = QLabel(MainWidget)
        background_label.setPixmap(QPixmap(":/Resources/Background.png"))
        background_label.setGeometry(0, 0, 1000, 550)
        self.gridLayout = QGridLayout(MainWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.MainGrid = QGridLayout()
        self.MainGrid.setObjectName(u"MainGrid")
        self.Title = QLabel(MainWidget)
        self.Title.setObjectName(u"Title")
        self.Title.setMinimumSize(QSize(530, 111))
        font = QFont()
        font.setFamilies([u"\u6a19\u6977\u9ad4"])
        font.setPointSize(25)
        self.Title.setFont(font)
        self.Title.setStyleSheet(
            u"background: no-repeat center center transparent;")
        self.Title.setPixmap(QPixmap(u":/Resources/Title.png"))
        self.Title.setScaledContents(False)
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.MainGrid.addWidget(self.Title, 1, 0, 1, 1)

        self.lineEdit = QLineEdit(MainWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(745, 93))
        font1 = QFont()
        font1.setFamilies([u"\u6a19\u6977\u9ad4"])
        font1.setPointSize(45)
        self.lineEdit.setFont(font1)
        self.lineEdit.setStyleSheet(u"background: no-repeat center center transparent; \n"
                                    "background-image: url(:/Resources/RoomNumber.png);\n"
                                    "border-radius: 35px;")
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.MainGrid.addWidget(self.lineEdit, 2, 0, 1, 1)

        self.JoinRoom_Button = QPushButton(MainWidget)
        self.JoinRoom_Button.setObjectName(u"JoinRoom_Button")
        self.JoinRoom_Button.setMinimumSize(QSize(377, 76))
        font2 = QFont()
        font2.setFamilies([u"\u6a19\u6977\u9ad4"])
        font2.setPointSize(12)
        self.JoinRoom_Button.setFont(font2)
        self.JoinRoom_Button.setStyleSheet('''
        QPushButton{
            background: no-repeat center center transparent;\n
            background-image: url(:/Resources/JoinRoom.png);\n
            border-radius: 20px;\n
        }
        QPushButton:disabled{
            background: no-repeat center center transparent;\n
            background-image: url(:/Resources/JoinRoom_Disabled.png);\n
            border-radius: 20px;\n
        }
        ''')
        self.JoinRoom_Button.setAutoRepeat(False)

        self.MainGrid.addWidget(self.JoinRoom_Button, 3, 0, 1, 1)

        self.Info_label = QLabel(MainWidget)
        self.Info_label.setObjectName(u"Info_label")
        self.Info_label.setMinimumSize(QSize(588, 50))
        self.Info_label.setStyleSheet(
            u"background: no-repeat bottom left transparent;")
        self.Info_label.setPixmap(QPixmap(u":/Resources/Info.png"))
        self.Info_label.setScaledContents(False)
        # alignment bottom left
        self.Info_label.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignBottom)

        self.MainGrid.addWidget(self.Info_label, 4, 0, 1, 1)

        self.gridLayout.addLayout(self.MainGrid, 0, 0, 1, 1)

        self.retranslateUi(MainWidget)

        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(
            QCoreApplication.translate("MainWidget", u"Form", None))
        self.Title.setText("")
        self.lineEdit.setText("")
        self.JoinRoom_Button.setText("")
        self.Info_label.setText("")
    # retranslateUi
