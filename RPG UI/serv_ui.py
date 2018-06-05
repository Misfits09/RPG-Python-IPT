# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serv_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Server(object):
    def setupUi(self, Server):
        Server.setObjectName("Server")
        Server.resize(640, 480)
        Server.setMinimumSize(QtCore.QSize(640, 480))
        Server.setMaximumSize(QtCore.QSize(640, 480))
        Server.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtWidgets.QWidget(Server)
        self.centralwidget.setObjectName("centralwidget")
        self.mainFrame = QtWidgets.QFrame(self.centralwidget)
        self.mainFrame.setEnabled(True)
        self.mainFrame.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.mainFrame.setAutoFillBackground(False)
        self.mainFrame.setStyleSheet("background: rgba(0,0,0,.5);color: white")
        self.mainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.LeftButton = QtWidgets.QPushButton(self.mainFrame)
        self.LeftButton.setGeometry(QtCore.QRect(50, 430, 93, 28))
        self.LeftButton.setObjectName("LeftButton")
        self.Titre = QtWidgets.QLabel(self.mainFrame)
        self.Titre.setGeometry(QtCore.QRect(0, 0, 641, 51))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Titre.setFont(font)
        self.Titre.setStyleSheet("background:rgba(1,1,1,.8);color:white; margin: 5")
        self.Titre.setObjectName("Titre")
        self.fieldBOX = QtWidgets.QTextBrowser(self.mainFrame)
        self.fieldBOX.setGeometry(QtCore.QRect(10, 100, 321, 311))
        self.fieldBOX.setObjectName("fieldBOX")
        self.gameLog = QtWidgets.QTextBrowser(self.mainFrame)
        self.gameLog.setGeometry(QtCore.QRect(350, 60, 271, 391))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(10)
        self.gameLog.setFont(font)
        self.gameLog.setMouseTracking(True)
        self.gameLog.setStyleSheet("color:white")
        self.gameLog.setObjectName("gameLog")
        self.RightButton = QtWidgets.QPushButton(self.mainFrame)
        self.RightButton.setGeometry(QtCore.QRect(190, 430, 93, 28))
        self.RightButton.setObjectName("RightButton")
        self.labelIP = QtWidgets.QLabel(self.mainFrame)
        self.labelIP.setGeometry(QtCore.QRect(20, 60, 231, 31))
        self.labelIP.setObjectName("labelIP")
        self.comboBox = QtWidgets.QComboBox(self.mainFrame)
        self.comboBox.setGeometry(QtCore.QRect(260, 60, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setEditable(False)
        self.comboBox.setIconSize(QtCore.QSize(5, 5))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        Server.setCentralWidget(self.centralwidget)

        self.retranslateUi(Server)
        QtCore.QMetaObject.connectSlotsByName(Server)

    def retranslateUi(self, Server):
        _translate = QtCore.QCoreApplication.translate
        Server.setWindowTitle(_translate("Server", "RPG IPT server"))
        self.LeftButton.setText(_translate("Server", "PushButton"))
        self.Titre.setText(_translate("Server", "<html><head/><body><p align=\"center\">RPG - BETA 1.0</p></body></html>"))
        self.fieldBOX.setHtml(_translate("Server", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.gameLog.setHtml(_translate("Server", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MV Boli\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\">Logs de la partie</span></p></body></html>"))
        self.RightButton.setText(_translate("Server", "PushButton"))
        self.labelIP.setText(_translate("Server", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">IP : 127.0.0.1</span></p></body></html>"))
        self.comboBox.setCurrentText(_translate("Server", "4291"))
        self.comboBox.setItemText(0, _translate("Server", "4291"))
        self.comboBox.setItemText(1, _translate("Server", "5536"))
        self.comboBox.setItemText(2, _translate("Server", "7289"))

