from untitled import *
import time
import socket
import pickle
import sys
from math import log10

class com(QtCore.QThread):
    commTrigger = QtCore.pyqtSignal(list,name="servercomm")
    def __init__(self,get_up):
        QtCore.QThread.__init__(self)
        self.com = get_up
        
    
        
    def __del__(self):
            self.wait()

    def run(self):
        while True :
            a = self.com()
            self.commTrigger.emit(a)
class MainWindow(Ui_RPG):
    valideClasses = ['guerrier','ninja','mage blanc','barbare','lancier',"yolosaruken"]
    def __init__(self, frame):
        self.isDoneField = False
        self.setupUi(frame)
        self.gameFrame.hide()
        self.playeGui.hide()
        self.ipBOX.setPlaceholderText("Laissez vide pour connection sans IP")
        RPG.setWindowTitle("RPG PRE-ALPHA")
        self.Titre.setText("<html><head/><body><p align=\"center\">RPG - PRE-ALPHA 4.0</p></body></html>")

        self.BoxClass.hide()
        for cl in self.valideClasses:
            self.BoxClass.addItem(cl)
        self.connectButton.clicked.connect(self.getPseudo)
        self.Spellbuttons = []
        self.chatBox.returnPressed.connect(self.chatButton.click)
        self.chatButton.clicked.connect(self.sendchat)
        self.chatButton.setEnabled(False)
        self.ipBOX.returnPressed.connect(self.connectButton.click)
        self.helpSpell.clicked.connect(self.showHelp)
        self.cancelSpell.hide()
        self.cancelSpell.clicked.connect(self.cancelSpellFct)
        self.endTour.hide()
        self.endTour.clicked.connect(self.endTourFct)
        self.spellnb = 0
        self.chatBox.setText("En attente de connection...")
        self.chatBox.setEnabled(False)
    def failwith(self,string):
        QtWidgets.QMessageBox.about(RPG, "Erreur", string)
        return False
    def success(self,string):
        QtWidgets.QMessageBox.about(RPG, "Super !", string)
        return False

    def cancelSpellFct(self):
        if self.spellnb >= 1:
            #supprimer la dernière ligne
            self.gameLog.setFocus()
            self.gameLog.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            self.gameLog.moveCursor(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.MoveAnchor)
            self.gameLog.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
            self.gameLog.textCursor().removeSelectedText()
            self.gameLog.textCursor().deletePreviousChar()
            self.send_updt(['cmd','cancel'])
            self.spellnb -= 1
            self.cancelSpell.setEnabled(False)
            self.endTour.setEnabled(False)
            self.spells.setEnabled(False)
    def endTourFct(self):
        self.endTour.hide()
        self.cancelSpell.hide()
        self.spells.setEnabled(False)
        self.spellnb = 0
        self.gameText.setText('Attente des autres joueurs...')
        self.send_updt(['cmd','fin'])
    def LaunchSpell(self):
        spellname = RPG.sender().text()
        for i in range(len(self.mySpell)):
            if self.mySpell[i][0] == spellname:
                if self.stamina.value() < self.mySpell[i][1]:
                    return self.failwith('Pas assez d\'endurance')
                self.spells.setEnabled(False)
                self.endTour.setEnabled(False)
                self.cancelSpell.setEnabled(False)
                self.send_updt(['cmd','spell '+spellname])
                break
        app.processEvents()

    def showHelp(self):
        superstr = ""
        for a,b,c in self.mySpell:
            superstr += a + " (" + str(b) + ") -> "+c + "<br/>"
        QtWidgets.QMessageBox.about(RPG, "Aide Spells", superstr)


    def setSpell(self,l):
        for x in self.Spellbuttons:
            x.deleteLater()
        self.Spellbuttons = []
        app.processEvents()
        self.mySpell = l
        nbSpells = len(l)
        for x in l:
            self.Spellbuttons.append(QtWidgets.QPushButton(self.spells))
        i = -1
        for x in self.Spellbuttons:
            i += 1
            x.setGeometry(QtCore.QRect(0,i*(261/nbSpells),171,(261/nbSpells)))
            x.setStyleSheet("background: blue; color: orange")
            x.setObjectName(l[i][0])
            x.raise_()
            name = l[i][0]
            x.setText(QtCore.QCoreApplication.translate("RPG", name))
            x.clicked.connect(self.LaunchSpell) 
            x.show()
            
        self.spells.setEnabled(False)

    def pick(self,liste):
        item, ok = QtWidgets.QInputDialog.getItem(RPG, "Choisissez un Cible", "Joueurs", liste, 0, False)
        if ok and item:
            return item
        elif not(ok):
            return 'cancel'
        else:
            return self.pick(liste)
    def infiniteloop(self,a):
        if a[0] == 'setParam': #['setParam',[('hp',15),('stamina',80)]]
            self.setParam(a[1])
        elif a[0] == 'setSpell': #['setParam',[('attack',15,'desc'),('heal',80,'desc')]]
            self.setSpell(a[1])
        elif a[0] == 'alert': #['alert','titreAlerte','ContenuAlerte']
            QtWidgets.QMessageBox.about(RPG, a[1], a[2])
        elif a[0] == 'get_c':
            if a[1] == 'main':
                self.spells.setEnabled(True)
                self.endTour.setEnabled(True)
                self.cancelSpell.setEnabled(True)
                self.endTour.show()
                if self.spellnb >= 1:
                    self.cancelSpell.show()
                self.gameText.setText('A vous de jouer')
            elif a[1] == 'target':
                self.send_updt(['name',self.pick(a[2])])
        elif a[0] == 'mess': #['alert','log']
            self.gameLog.append(a[1])
        elif a[0] == 'spell':
            self.gameLog.append(a[1])
            self.spellnb += 1
        elif a[0] == 'chat':
            self.chatLog.append(a[1])
        elif a[0] == 'gametext':
            self.gameText.setText(a[1])
        elif a[0] == 'field': #['alert','log']
            
            if not self.isDoneField:
                #Setup Field
                self.isDoneField = True
                pl = a[1]
                self.playList = []
                l  = len(pl)
                p1,p2 = pl[:(l//2)],pl[(l//2):]
                lp1,lp2 = len(p1),len(p2)
                import os
                for k in range(lp1):
                    a1=QtWidgets.QFrame(self.gameBOX)
                    a1.setObjectName(p1[k][1])
                    a1.setGeometry(QtCore.QRect((400/lp1)*k,0,(400/lp1)*(k+1),145))
                    pic = QtWidgets.QLabel(a1)
                    pic.setGeometry(QtCore.QRect((200/lp1)-62.5, 20, 400/lp1, 145))
                    #use full ABSOLUTE path to the image, not relative
                    pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/image/"+str(p1[k][1])+".png"))
                    lifebar = QtWidgets.QProgressBar(a1)
                    lifebar.setGeometry(QtCore.QRect(0,22,(400/lp1) - 10,22))
                    lifebar.setMaximum(p1[k][3])
                    lifebar.setFormat("%v/%m")
                    lifebar.setProperty("value",p1[k][2])
                    name = QtWidgets.QLabel(a1)
                    name.setGeometry(QtCore.QRect(0,0,400/lp1,20))
                    name.setText(p1[k][0])
                    name.setStyleSheet('text-align:center; vertical-align: top; color:white;text-decoration:bold;border: 2px white;')
                    name.setAlignment(QtCore.Qt.AlignCenter)
                    pic.show()
                    name.show()
                    a1.show()
                    self.playList.append([p1[k][0],a1,lifebar])
                for k in range(lp2):
                    b1=QtWidgets.QFrame(self.gameBOX)
                    b1.setObjectName(p2[k][1])
                    b1.setGeometry(QtCore.QRect((400/lp2)*k,145,(400/lp2)*(k+1),290))
                    pic = QtWidgets.QLabel(b1)
                    pic.setGeometry(QtCore.QRect((200/lp2)-62.5, 20, 400/lp2, 145))
                    #use full ABSOLUTE path to the image, not relative
                    pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/image/"+str(p2[k][1])+".png"))
                    lifebar = QtWidgets.QProgressBar(b1)
                    lifebar.setGeometry(QtCore.QRect(0,22,(400/lp2)-10,22))
                    lifebar.setMaximum(p2[k][3])
                    lifebar.setFormat("%v/%m")
                    lifebar.setProperty("value",p2[k][2])
                    name = QtWidgets.QLabel(b1)
                    name.setGeometry(QtCore.QRect(0,0,400/lp2,20))
                    name.setText(p2[k][0])
                    name.setStyleSheet('text-align:center; vertical-align: top; color:white; text-decoration:bold;border: 2px white;')
                    name.setAlignment(QtCore.Qt.AlignCenter)
                    pic.show()
                    name.show()
                    b1.show()
                    self.playList.append([p2[k][0],b1,lifebar])
            else:
                if self.playList:
                    up = a[1]
                    for k in range(len(up)):
                        #show field updates
                        if self.playList[k][0] == up[k][0]:
                            self.playList[k][2].setProperty("value",int(float(up[k][2])))
        elif a[0] == 'end_game': #['alert','log']
            QtWidgets.QMessageBox.about(RPG, "FIN DE PARTIE", a[1])
            RPG.close()
            sys.exit(0)
        else:
            self.gameLog.append(str(a))
        app.processEvents()

    #Récupération Classe et Lancement partie
    def startGame(self):
        a = self.BoxClass.currentText().strip().casefold() 
        if not (a in self.valideClasses):
            return self.failwith('Nom de classe invalide')
        self.connectButton.setText("En Attente")
        self.connectButton.setEnabled(False)
        app.processEvents()
        self.send_updt(['get_infos',self.name,a])

        def onGetConfirm(a):
            self.macom.commTrigger.disconnect()
            self.macom.commTrigger.connect(self.infiniteloop)
            self.chatcom.start()
            confirm = a
            if(confirm[0] != "setSpell"):
                self.connectButton.setText("Valider")
                self.connectButton.setEnabled(True)
                return self.failwith('Erreur communication')
            self.chatButton.setEnabled(True)
            self.chatBox.setText("")
            self.chatBox.setPlaceholderText("Tapez ici...")
            self.chatBox.setEnabled(True)
            self.setSpell(confirm[1])
            self.setupFrame.hide()
            self.BoxClass.hide()
            self.gameFrame.show()
            self.playeGui.show()
            app.processEvents()
        self.macom.commTrigger.connect(onGetConfirm)
        self.macom.start()

    #Récupération Classe
    def getClasse(self):
        if self.ipBOX.text() == '':
            return self.failwith('Veuillez entrer un nom')
        self.setParam([('name',self.ipBOX.text())])
        self.name = self.ipBOX.text()
        app.processEvents()
        self.ipBOX.hide()
        self.BoxClass.show()
        self.entete.setText('Recuperation Classe')
        self.connectButton.setText("Valider Classe")
        self.connectButton.clicked.disconnect()
        self.connectButton.clicked.connect(self.startGame)
        
    #Connection Et Recup pseudo
    def getPseudo(self):
        try:
            self.connectButton.setEnabled(False)
            self.connectButton.setStyleSheet('background: grey')
            app.processEvents()
            if self.ipBOX.text() == '':
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)                
                s.sendto(pickle.dumps("Anyone?"), ('<broadcast>', int(self.comboBox.currentText())))
                _unused, addr = s.recvfrom(1024)
                ip = addr[0]
                port = 4392
                time.sleep(.1)
            else:
                ip = self.ipBOX.text()
                port = int(self.comboBox.currentText())
            s = socket.socket()
            s.connect((ip,port))
            self.socket = s
            self.chatsocket = socket.socket()
            self.chatsocket.connect((ip,port))
            self.macom = com(self.get_updt)
            self.chatcom = com(self.get_chat)
        except:
            self.connectButton.setStyleSheet('background: white')
            self.connectButton.setEnabled(True)
            return self.failwith('Erreur dans l\' écriture de l \' IP et port OU erreur de connection')
        self.ipBOX.clear()
        self.entete.setText('Recuperation Pseudo')
        self.connectButton.setText("Valider Pseudo")
        self.labelIP.hide()
        self.ipBOX.setPlaceholderText("")
        self.labelPort.hide()
        self.comboBox.hide()
        self.connectButton.clicked.disconnect()
        self.connectButton.clicked.connect(self.getClasse)
        self.connectButton.setStyleSheet('background: white')
        self.connectButton.setEnabled(True)
    
    #Fonctions Comm    
    def get_updt(self):
        up_r = pickle.loads(self.socket.recv(1024))
        return up_r
    def send_updt(self,u):
        self.socket.send(pickle.dumps(u))
        time.sleep(.1)
    def send_error(self,ider):
        self.send_updt(["error",ider])

    #Fonctions chat
    def sendchat(self):
        self.chatsocket.send(pickle.dumps(self.chatBox.text()))
        self.chatBox.clear()
    def get_chat(self):
        up_r = pickle.loads(self.chatsocket.recv(1024))
        return up_r
    #Changement des valeurs
    def setParam(self,k):
        for a,b in k:
            if a == 'hp':
                self.HP.setProperty('value',b)
                self.HP.setGeometry(QtCore.QRect(10, 20, 95 + 7*(int(log10(b+b==0))+1), 23))
            elif a == 'stamina' :
                self.stamina.setProperty('value',b)
                self.stamina.setGeometry(QtCore.QRect(10, 50, 139 + 7*(int(log10(b+b==0))+1), 23))
            elif a == 'name' :
                self.pseudo.setText("<html><head/><body><p><span style=\" font-size:14pt; font-style:bold;\">"+str(b)+"</span></p></body></html>")
            elif a == 'id' :
                self.pID.setText("<html><head/><body><p><span style=\" font-size:14pt;\">"+str(b)+"</span></p></body></html>")
            elif a == 'maxhp' :
                self.HP.setProperty('maximum',int(b))


def boot():
    import sys
    global app,RPG,ui
    app = QtWidgets.QApplication(sys.argv)
    RPG = QtWidgets.QMainWindow()
    ui = MainWindow(RPG)
    RPG.show()
    sys.exit(app.exec_())

boot()
