# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RPG(object):
    def setupUi(self, RPG):
        RPG.setObjectName("RPG")
        RPG.setFixedSize(603, 466)
        font = QtGui.QFont()
        font.setFamily("OpenSymbol")
        RPG.setFont(font)
        RPG.setAutoFillBackground(False)
        RPG.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(RPG)
        self.centralwidget.setStyleSheet("background:url(./tel.png)")
        self.centralwidget.setObjectName("centralwidget")
        self.Titre = QtWidgets.QLabel(self.centralwidget)
        self.Titre.setGeometry(QtCore.QRect(0, 0, 601, 51))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Titre.setFont(font)
        self.Titre.setStyleSheet("background:rgba(1,1,1,.8);color:white; margin: 5")
        self.Titre.setObjectName("Titre")
        self.playeGui = QtWidgets.QFrame(self.centralwidget)
        self.playeGui.setEnabled(True)
        self.playeGui.setGeometry(QtCore.QRect(0, 350, 601, 121))
        self.playeGui.setStyleSheet("background: rgba(1,1,1,.5)")
        self.playeGui.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.playeGui.setFrameShadow(QtWidgets.QFrame.Raised)
        self.playeGui.setObjectName("playeGui")
        self.HP = QtWidgets.QProgressBar(self.playeGui)
        self.HP.setGeometry(QtCore.QRect(10, 20, 123, 23))
        self.HP.setStyleSheet("background: rgba(1,1,1,.7); color:white;")
        self.HP.setMaximum(200)
        self.HP.setProperty("value", 122)
        self.HP.setInvertedAppearance(False)
        self.HP.setFormat("%v HP")
        self.HP.setObjectName("HP")
        self.stamina = QtWidgets.QProgressBar(self.playeGui)
        self.stamina.setGeometry(QtCore.QRect(10, 50, 161, 23))
        self.stamina.setStyleSheet("background: rgba(1,1,1,.7); color:white;")
        self.stamina.setProperty("value", 100)
        self.stamina.setInvertedAppearance(False)
        self.stamina.setFormat("%p Endurance")
        self.stamina.setObjectName("stamina")
        self.pseudo = QtWidgets.QLabel(self.playeGui)
        self.pseudo.setGeometry(QtCore.QRect(490, 10, 101, 41))
        self.pseudo.setStyleSheet("background:none")
        self.pseudo.setObjectName("pseudo")
        self.labelJoueur = QtWidgets.QLabel(self.playeGui)
        self.labelJoueur.setGeometry(QtCore.QRect(490, 40, 61, 41))
        self.labelJoueur.setStyleSheet("background:none")
        self.labelJoueur.setObjectName("labelJoueur")
        self.pID = QtWidgets.QLabel(self.playeGui)
        self.pID.setGeometry(QtCore.QRect(550, 40, 61, 41))
        self.pID.setStyleSheet("background:none")
        self.pID.setObjectName("pID")
        self.gameLog = QtWidgets.QTextBrowser(self.playeGui)
        self.gameLog.setGeometry(QtCore.QRect(190, 10, 256, 81))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(10)
        self.gameLog.setFont(font)
        self.gameLog.setStyleSheet("color:white")
        self.gameLog.setObjectName("gameLog")
        self.endTour = QtWidgets.QPushButton(self.playeGui)
        self.endTour.setGeometry(QtCore.QRect(520, 90, 75, 23))
        self.endTour.setStyleSheet("background: red; color:white;")
        self.endTour.setObjectName("endTour")
        self.setupFrame = QtWidgets.QFrame(self.centralwidget)
        self.setupFrame.setEnabled(True)
        self.setupFrame.setGeometry(QtCore.QRect(10, 60, 571, 261))
        self.setupFrame.setStyleSheet("background: none;")
        self.setupFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setupFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setupFrame.setObjectName("setupFrame")
        self.entete = QtWidgets.QLabel(self.setupFrame)
        self.entete.setGeometry(QtCore.QRect(150, 0, 261, 51))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.entete.setFont(font)
        self.entete.setStyleSheet("background:rgba(1,1,1,.8);color:white; margin: 5")
        self.entete.setObjectName("entete")
        self.labelIP = QtWidgets.QLabel(self.setupFrame)
        self.labelIP.setGeometry(QtCore.QRect(270, 80, 21, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.labelIP.setFont(font)
        self.labelIP.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.labelIP.setAutoFillBackground(False)
        self.labelIP.setStyleSheet("background: rgba(1,1,1,.7); color:white;")
        self.labelIP.setObjectName("labelIP")
        self.ipBOX = QtWidgets.QLineEdit(self.setupFrame)
        self.ipBOX.setGeometry(QtCore.QRect(190, 120, 181, 20))
        self.ipBOX.setStyleSheet("background:white")
        self.ipBOX.setObjectName("ipBOX")
        self.labelPort = QtWidgets.QLabel(self.setupFrame)
        self.labelPort.setGeometry(QtCore.QRect(260, 150, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.labelPort.setFont(font)
        self.labelPort.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.labelPort.setAutoFillBackground(False)
        self.labelPort.setStyleSheet("background: rgba(1,1,1,.7); color:white;")
        self.labelPort.setObjectName("labelPort")
        self.connectButton = QtWidgets.QPushButton(self.setupFrame)
        self.connectButton.setGeometry(QtCore.QRect(224, 230, 101, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.connectButton.setFont(font)
        self.connectButton.setStyleSheet("background:white; color:green")
        self.connectButton.setObjectName("connectButton")
        self.comboBox = QtWidgets.QComboBox(self.setupFrame)
        self.comboBox.setGeometry(QtCore.QRect(240, 190, 81, 22))
        self.comboBox.setEditable(False)
        self.comboBox.setIconSize(QtCore.QSize(5, 5))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.BoxClass = QtWidgets.QComboBox(self.setupFrame)
        self.BoxClass.setGeometry(QtCore.QRect(170, 120, 231, 22))
        self.BoxClass.setStyleSheet("background: purple; color: yellow;")
        self.BoxClass.setDuplicatesEnabled(False)
        self.BoxClass.setObjectName("BoxClass")
        self.gameFrame = QtWidgets.QFrame(self.centralwidget)
        self.gameFrame.setEnabled(True)
        self.gameFrame.setGeometry(QtCore.QRect(0, 60, 601, 281))
        self.gameFrame.setAutoFillBackground(False)
        self.gameFrame.setStyleSheet("background: rgba(0,0,0,.5);color: white")
        self.gameFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.gameFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gameFrame.setObjectName("gameFrame")
        self.spells = QtWidgets.QFrame(self.gameFrame)
        self.spells.setGeometry(QtCore.QRect(429, 10, 151, 261))
        self.spells.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.spells.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spells.setObjectName("spells")
        self.helpSpell = QtWidgets.QPushButton(self.gameFrame)
        self.helpSpell.setGeometry(QtCore.QRect(410, 250, 21, 21))
        self.helpSpell.setStyleSheet("background: green; color:white")
        self.helpSpell.setObjectName("helpSpell")
        self.gameText = QtWidgets.QLabel(self.gameFrame)
        self.gameText.setGeometry(QtCore.QRect(10, 0, 411, 31))
        self.gameText.setStyleSheet("background: none")
        self.gameText.setObjectName("gameText")
        self.GamePicture = QtWidgets.QFrame(self.gameFrame)
        self.GamePicture.setGeometry(QtCore.QRect(10, 30, 221, 241))
        self.GamePicture.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.GamePicture.setFrameShadow(QtWidgets.QFrame.Raised)
        self.GamePicture.setObjectName("GamePicture")
        self.fieldBOX = QtWidgets.QTextBrowser(self.gameFrame)
        self.fieldBOX.setGeometry(QtCore.QRect(250, 50, 141, 201))
        self.fieldBOX.setObjectName("fieldBOX")
        self.label = QtWidgets.QLabel(self.gameFrame)
        self.label.setGeometry(QtCore.QRect(286, 23, 61, 20))
        self.label.setStyleSheet("background:none")
        self.label.setObjectName("label")
        RPG.setCentralWidget(self.centralwidget)

        self.retranslateUi(RPG)
        QtCore.QMetaObject.connectSlotsByName(RPG)

    def retranslateUi(self, RPG):
        _translate = QtCore.QCoreApplication.translate
        RPG.setWindowTitle(_translate("RPG", "RPG 1.0"))
        self.Titre.setText(_translate("RPG", "<html><head/><body><p align=\"center\">RPG - BETA 1.0</p></body></html>"))
        self.pseudo.setText(_translate("RPG", "<html><head/><body><p><span style=\" font-size:14pt; font-style:italic;\">TonPseudo</span></p></body></html>"))
        self.labelJoueur.setText(_translate("RPG", "<html><head/><body><p><span style=\" font-size:14pt;\">Joueur</span></p></body></html>"))
        self.pID.setText(_translate("RPG", "<html><head/><body><p><span style=\" font-size:14pt;\">1</span></p></body></html>"))
        self.gameLog.setHtml(_translate("RPG", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MV Boli\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\">Logs de la partie</span></p></body></html>"))
        self.endTour.setText(_translate("RPG", "Fin de Tour"))
        self.entete.setText(_translate("RPG", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#a50002;\">Connection au serveur :</span></p></body></html>"))
        self.labelIP.setText(_translate("RPG", "IP"))
        self.labelPort.setText(_translate("RPG", "Port"))
        self.connectButton.setText(_translate("RPG", "Se connecter"))
        self.comboBox.setCurrentText(_translate("RPG", "4291"))
        self.comboBox.setItemText(0, _translate("RPG", "4291"))
        self.comboBox.setItemText(1, _translate("RPG", "5536"))
        self.comboBox.setItemText(2, _translate("RPG", "7289"))
        self.helpSpell.setText(_translate("RPG", "?"))
        self.gameText.setText(_translate("RPG", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Démarrage de la partie...</span></p></body></html>"))
        self.fieldBOX.setHtml(_translate("RPG", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Nom</span><span style=\" font-size:8pt;\">    </span></p></td>\n"
"<td>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Classe</span><span style=\" font-size:8pt;\">     </span></p></td>\n"
"<td>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">PV</span><span style=\" font-size:8pt;\">    </span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Jill    </span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Smith     </span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">50    </span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Eve    </span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Jackson     </span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">94  </span></p></td></tr></table></body></html>"))
        self.label.setText(_translate("RPG", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Terrain</span></p></body></html>"))

