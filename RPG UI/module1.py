from untitled import *
import time
import socket
import pickle
import sys

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
        self.setupUi(frame)
        self.gameFrame.hide()
        self.playeGui.hide()
        RPG.setWindowTitle("RPG PRE-ALPHA 3.0")
        self.Titre.setText("<html><head/><body><p align=\"center\">RPG - PRE-ALPHA 3.0</p></body></html>")

        self.BoxClass.hide()
        for cl in self.valideClasses:
            self.BoxClass.addItem(cl)
        self.connectButton.clicked.connect(self.getPseudo)
        self.Spellbuttons = []
        self.ipBOX.returnPressed.connect(self.connectButton.click)
        self.helpSpell.clicked.connect(self.showHelp)
        self.endTour.hide()
        self.endTour.clicked.connect(self.endTourFct)
    def failwith(self,string):
        QtWidgets.QMessageBox.about(RPG, "Erreur", string)
        return False
    def success(self,string):
        QtWidgets.QMessageBox.about(RPG, "Super !", string)
        return False

    def endTourFct(self):
        self.endTour.hide()
        self.spells.setEnabled(False)
        self.gameText.setText('Tour des autres joueurs...')
        self.send_updt(['cmd','fin'])
    def LaunchSpell(self):
        spellname = RPG.sender().text()
        for i in range(len(self.mySpell)):
            if self.mySpell[i][0] == spellname:
                break
        if self.stamina.value() < self.mySpell[i][1]:
            return self.failwith('Pas assez d\'endurance')
        self.spells.setEnabled(False)
        self.gameText.setText('Lancement de : '+spellname)
        self.send_updt(['cmd','spell '+spellname])
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
                self.endTour.show()
                self.gameText.setText('A vous de jouer')
            elif a[1] == 'target':
                self.send_updt(['name',self.pick(a[2])])
        elif a[0] == 'turnof':
            self.gameText.setText('Tour de '+a[1])
        elif a[0] == 'mess': #['alert','log']
            self.gameLog.append(a[1])
        elif a[0] == 'field': #['alert','log']
            fieldStr = """<html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><table border="0" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;width:100%" cellspacing="2" cellpadding="0"><tr><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Nom</span><span style=" font-size:8pt;">    </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Classe</span><span style=" font-size:8pt;">     </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">PV</span><span style=" font-size:8pt;">    </span></p></td></tr>"""
            for p in a[1]:
                fieldStr += """<tr><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[0]+"""</span></p></td><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[1]+""" </span></p></td><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+str(int(float(p[2])))+"""</span></p></td></tr>"""
            fieldStr += "</table></body></html>"
            self.fieldBOX.setText(fieldStr)
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
            confirm = a
            if(confirm[0] != "setSpell"):
                self.connectButton.setText("Valider")
                self.connectButton.setEnabled(True)
                return self.failwith('Erreur communication')
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
                recv_data, addr = s.recvfrom(1024)
                ip = addr[0]
                port = 4392
                time.sleep(.3)
            else:
                ip = self.ipBOX.text()
                port = int(self.comboBox.currentText())
            s = socket.socket()
            s.connect((ip,port))
            self.socket = s
            self.macom = com(self.get_updt)
        except:
            self.connectButton.setStyleSheet('background: white')
            self.connectButton.setEnabled(True)
            return self.failwith('Erreur dans l\' écriture de l \' IP et port OU erreur de connection')
        self.ipBOX.clear()
        self.entete.setText('Recuperation Pseudo')
        self.connectButton.setText("Valider Pseudo")
        self.labelIP.hide()
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
        time.sleep(.5)
    def send_error(self,ider):
        self.send_updt(["error",ider])

    #Changement des valeurs
    def setParam(self,k):
        for a,b in k:
            if a == 'hp':
                self.HP.setProperty('value',b)
            elif a == 'stamina' :
                self.stamina.setProperty('value',b)
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
