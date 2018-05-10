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
        while 1 :
            a = self.com()
            print('J\'ai essayé d\'émettre : '+str(a))
            self.commTrigger.emit(a)
class MainWindow(Ui_RPG):
    valideClasses = ['guerrier','ninja','mage blanc','barbare','lancier']
    def __init__(self, frame,getM,sendM):
        self.setupUi(frame)
        self.gameFrame.hide()
        self.playeGui.hide()
        self.BoxClass.hide()
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
        isIN = False
        for i in range(len(self.mySpell)):
            if self.mySpell[i][0] == spellname:
                isIN = True
                break
        if self.stamina.value() < self.mySpell[i][1]:
            return self.failwith('Pas assez d\'endurance')
        self.spells.setEnabled(False)
        self.gameText.setText('Lancement de : '+spellname)
        print(str(['cmd','spell '+spellname]))
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
            print(x[0])
        i = -1
        for x in self.Spellbuttons:
            i += 1
            x.setGeometry(QtCore.QRect(0,i*(261/nbSpells),151,(261/nbSpells)))
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
        else:
            return self.pick(liste)
    def infiniteloop(self,a):
        print('IL')
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
        elif a[0] == 'mess': #['alert','log']
            self.gameLog.append(a[1])
        elif a[0] == 'field': #['alert','log']
                fieldStr = """<html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><table border="0" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;" cellspacing="2" cellpadding="0"><tr><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Nom</span><span style=" font-size:8pt;">    </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Classe</span><span style=" font-size:8pt;">     </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">PV</span><span style=" font-size:8pt;">    </span></p></td></tr><tr><td>"""
                for p in a[1]:
                    fieldStr += """<tr><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[0]+"""</span></p></td><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[1]+""" </span></p></td><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[2]+"""</span></p></td></tr>"""
                self.fieldBOX.setText(fieldStr)
        elif a[0] == 'endT':
            fieldStr = """<html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><table border="0" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;" cellspacing="2" cellpadding="0"><tr><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Nom</span><span style=" font-size:8pt;">    </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Classe</span><span style=" font-size:8pt;">     </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">PV</span><span style=" font-size:8pt;">    </span></p></td></tr><tr><td>"""
            for p in a[1]:
                fieldStr += """<tr><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[0]+"""</span></p></td><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[1]+""" </span></p></td><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[2]+"""</span></p></td></tr>"""
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
        self.send_updt(['classe', a])

        def onGetConfirm2(a):
            self.macom.commTrigger.disconnect()
            self.macom.commTrigger.connect(self.infiniteloop)
            print('OKKKKKKKK2')
            confirm = a
            if(confirm[0] != "you"):
                self.connectButton.setText("Valider")
                self.connectButton.setEnabled(True)
                return self.failwith('Erreur communication')
            self.HP.setProperty('maximum',int(confirm[1]))
            self.setSpell(confirm[2])
            self.setupFrame.hide()
            self.BoxClass.hide()
            self.gameFrame.show()
            self.playeGui.show()
            app.processEvents()

        def onGetConfirm(a):
            self.macom.commTrigger.disconnect()
            self.macom.commTrigger.connect(onGetConfirm2)
            print('OKKKKKKKK')
            confirm = a
            if(confirm[0] != "field"):
                self.connectButton.setText("Valider")
                self.connectButton.setEnabled(True)
                return self.failwith('Erreur communication')
            fieldStr = """<html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><table border="0" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;" cellspacing="2" cellpadding="0"><tr><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Nom</span><span style=" font-size:8pt;">    </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Classe</span><span style=" font-size:8pt;">     </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">PV</span><span style=" font-size:8pt;">    </span></p></td></tr><tr><td>"""
            for p in confirm[1]:
                fieldStr += """<tr><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[0]+"""</span></p></td><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[1]+""" </span></p></td><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[2]+"""</span></p></td></tr>"""
            self.fieldBOX.setText(fieldStr)
        self.macom.commTrigger.connect(onGetConfirm)
        
        

    #Envoi pseudo et Récupération Classe
    def getClasse(self):
        if self.ipBOX.text() == '':
            return self.failwith('Nom Invalide, nom : '+self.ipBOX.text())
        self.setParam([('name',self.ipBOX.text())])
        self.send_updt( [ 'name',str(self.ipBOX.text())] )
        self.connectButton.setText("En attente...")
        self.connectButton.setEnabled(False)
        app.processEvents()
        def onGetClasse(a):
            if(a != ["get_classe",True]):
                self.connectButton.setText("Valider")
                self.connectButton.setEnabled(True)
                return self.failwith('Erreur communication')
            self.ipBOX.hide()
            self.BoxClass.show()
            self.entete.setText('Recuperation Classe')
            self.connectButton.setText("Valider Classe")
            self.connectButton.setEnabled(False)
            self.connectButton.setEnabled(True)
            self.macom.commTrigger.disconnect()
            self.connectButton.clicked.disconnect()
            self.connectButton.clicked.connect(self.startGame)
        self.macom.commTrigger.connect(onGetClasse)
        self.macom.start()

    #Connection Et Recup pseudo
    def getPseudo(self):
        if self.ipBOX.text() == '':
            return self.failwith('IP Invalide')
        if True:
            self.connectButton.setEnabled(False)
            self.connectButton.setStyleSheet('background: grey')
            app.processEvents()
            s = socket.socket()
            s.connect((self.ipBOX.text(),int(self.comboBox.currentText())))
            self.socket = s
            self.macom = com(self.get_updt)
        else:
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
        send_updt(["error",ider])

    #Changement des valeurs
    def setParam(self,k):
        for a,b in k:
            if a == 'hp':
                self.HP.setProperty('value',b)
            elif a == 'stamina' :
                self.stamina.setProperty('value',b)
            elif a == 'name' :
                self.pseudo.setText("<html><head/><body><p><span style=\" font-size:14pt; font-style:italic;\">"+str(b)+"</span></p></body></html>")
            elif a == 'id' :
                self.pID.setText(str(b))



def boot():
    import sys
    global app,RPG,ui
    app = QtWidgets.QApplication(sys.argv)
    RPG = QtWidgets.QMainWindow()
    ui = MainWindow(RPG,lambda: 'a', lambda x : print(x))
    RPG.show()
    sys.exit(app.exec_())

boot()