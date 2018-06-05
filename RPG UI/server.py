# -*- coding: utf-8 -*-
""" Server Code : RPG IPT 2018"""
from serv_ui import *
import time
import socket
import pickle
import random
from classes import *
from threading import Event,Lock
import sys

class threads(QtCore.QThread):
    def __init__(self,fct,args = ()):
        super().__init__()
        self.target = fct
        self.args = args
    def run(self):
        self.target(*self.args)
class fldedit(QtCore.QObject):
    event = QtCore.pyqtSignal()
class log(QtCore.QObject):
    out = QtCore.pyqtSignal(str)

class MainWindow(Ui_Server):
    def send(self,mss, lp = None):
        self.log.emit(str(mss))
        time.sleep(.3)
        if lp == None :
            lp = self.F.player
        try:
            for j in lp :
                j.socket.send(pickle.dumps(mss))
                app.processEvents()
            return True
        except:
            return False
    def get_rsp(self,j):
        try:
            a=pickle.loads(j.socket.recv(1024))
            self.log.emit(str(a))
            app.processEvents()
            return a
        except:
            return ['error',0]
    
    def __init__(self,frame):
        self.setupUi(frame)
        version = "RPG PRE-ALPHA 3.0"
        frame.setWindowTitle(version)
        self.centralwidget.setStyleSheet("background:url(./tel.png)")
        self.Titre.setText("<html><head/><body><p align=\"center\">"+version+"</p></body></html>")
        localIP = socket.gethostbyname(socket.gethostname())
        if localIP == '127.0.0.1' :
            localIP = 'Inconnue'
        self.labelIP.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">IP : "+localIP+"</span></p></body></html>")
        self.LeftButton.setText("Avec IP")
        self.RightButton.setText("Sans IP")
        self.RightButton.clicked.connect(self.connect_ssip)
        self.LeftButton.clicked.connect(self.connect_avecip)
        self.logevent = log()
        self.log = self.logevent.out
        self.log.connect(self.gameLog.append)
        self.table = []
        self.tableevent = fldedit()
        self.tableevent.event.connect(self.printfld)
        self.players=[]
        self.plock = Lock()
    
    def connect_avecip(self):
        self.RightButton.setEnabled(False)
        self.RightButton.hide()
        self.LeftButton.setText("Demarrer")
        self.LeftButton.clicked.disconnect()
        self.LeftButton.clicked.connect(self.start_game)
        self.event = Event()
        self.log.emit('En attente de joueurs')
        self.connectthread = threads(self.search_ip)
        self.connectthread.start()
    def connect_ssip(self):
        self.RightButton.setEnabled(False)
        self.RightButton.hide()
        self.LeftButton.setText("Demarrer")
        self.LeftButton.clicked.disconnect()
        self.LeftButton.clicked.connect(self.start_game)
        self.event = Event()
        self.log.emit('En attente de joueurs')
        self.connectthread = threads(self.search_ssip)
        self.connectthread.start()
    
    def search_ip(self):
        i = 1
        with socket.socket() as s:
            port = int(self.comboBox.currentText())
            s.bind(('',port))
            s.listen()
            s.settimeout(1.)
            while not self.event.is_set():
                try : 
                    sock,address = s.accept()
                    t = threads(self.get_infos,(i,sock))
                    t.start()
                    i += 1
                except socket.timeout : pass
    def search_ssip(self):
        connections = 0
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s2, socket.socket() as s:
            s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s2.settimeout(1.)
            port = int(self.comboBox.currentText())
            s2.bind(('', port))
            s.bind(('',4392))
            s.listen()
            while not self.event.is_set() :
                try :
                    message, address = s2.recvfrom(1024)
                    connections += 1
                    s2.sendto(pickle.dumps("Hi there"),address)
                    sock,address = s.accept()
                    th = threads(self.get_infos,(connections,sock))
                    th.start()
                except socket.timeout: pass

    def get_infos(self,i,sock):
        self.log.emit("Joueur "+str(i)+" arrivé et enregistré !!")
        mss = pickle.loads(sock.recv(1024))
        if mss[0] == "get_infos":
            try : 
                name = mss[1]
                self.log.emit('Joueur '+str(i)+' s\'appelle '+mss[1])
            except:
                name = 'SansNom'+str(i)
                self.log.emit("Joueur "+str(i)+" sans nom")
            if True:
                for cl in classes:
                    if mss[2] == cl.classname:
                        j = cl(i,sock)
                        j.name = name
                        self.log.emit('Classe recue : \''+mss[2]+'\' par joueur '+str(i))
                        break
                else:
                    j = guerrier(i,sock)
                    j.name = name
                    self.log.emit('Joueur '+str(i)+' guerrier par defaut : ERRCLSS1')
            else:
                j = guerrier(i,sock)
                j.name = name
                self.log.emit('Joueur '+str(i)+' guerrier par defaut : ERRCLSS2')
            self.plock.acquire()
            self.players.append(j)
            self.table.append([str(j.id),j.name,j.classname,str(j.hp),str(j.stamina)])
            self.plock.release()
            self.tableevent.event.emit()
    
    def command(self,a,j): #gestion des commandes pendant un tour
        other_pl = [y for y in self.F.player if y != j]
        def wrong_c(j):
            self.send(['mess','\n Commande incomprise '+a+' : Vérifiez votre commande'],[j])
            self.send(['mess',j.name+' a voulu faire quelque chose d\' impossible'],other_pl)
            self.log.emit('Mauvaise commande de '+j.name+' : '+a)
            return True
        a = a.strip()
        al = a.split()
        try:
            if(al[0] == 'fin'):
                self.log.emit('\n    -Fin du tour de '+j.name+'-   \n \n')
                self.send(['mess',j.name+' a fini de se battre'])
                return False
            elif(al[0] == 'spell'):
                try: toshow = j.spell(al[1],self.F)
                except: return wrong_c(j)
                for typeR,obj in toshow:
                    if typeR == 'death':
                        if(obj == j): #Si le joueur meurt de lui même
                            self.send(['mess','Vous êtes mort en attaquant'],[j])
                            self.send(['mess', j.name+' est mort au combat'],other_pl)
                            j.alive = False #Juste pour être sûre xD
                        else:
                            other_pl2 = other_pl.copy()
                            other_pl2.remove(obj)
                            self.send(['mess',' Vous avez tué '+obj.name],[j])
                            self.send(['mess','Vous avez ete tue par '+j.name],[obj])
                            self.send(['mess',j.name+' a tué '+obj.name],other_pl2)
                    elif typeR == 'mess':
                        self.send(['mess',obj])
                return j.alive
            else:
                return wrong_c(j)
        except:
            return wrong_c(j)
        
    def printfld(self):
        fieldStr = """<html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><table border="0" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;width:100%" cellspacing="2" cellpadding="0"><tr><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">ID</span><span style=" font-size:8pt;">    </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Nom</span><span style=" font-size:8pt;">    </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Classe</span><span style=" font-size:8pt;">     </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">PV</span><span style=" font-size:8pt;">    </span></p></td> </span></p></td><td><p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt; font-weight:600;">Stamina</span><span style=" font-size:8pt;">    </span></p></td> </tr>"""
        for p in self.table:
            fieldStr += """<tr><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[0]+"""</span></p></td><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[1]+"""</span></p></td><td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[2]+""" </span></p></td>"""
            try : 
                fieldStr += """<td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[3]+"""</span></p></td> <td><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">"""+p[4]+"""</span></p></td>"""
            except : pass
            fieldStr += """</tr>"""
        fieldStr += "</table></body></html>"
        self.fieldBOX.setText(fieldStr)
    def rStartTour(self,name): #Phrases aléatoires de début de tour
        l1 = ["*namej* est prêt à se battre !","Craignez la puissance *namej* :o","Cachez vous ! *namej* est prêt à jouer","*namej* va jouer mais personne n'a peur de lui ;-( ","*namej* commence son tour !","*namej* semble inarretable préparez vous à son tour"] 
        rint = random.randint(0,len(l1)-1)
        return l1[rint].replace('*namej*',name)
    def send_param(self):    
        self.send(['field',[(p[1],p[2],p[3]) for p in self.F.getTable()]])
        self.table =self.F.getTable()
        self.tableevent.event.emit()
        for k in self.F.player:
            self.send(['setParam',[('hp',k.hp),('stamina',k.stamina)]],[k])
    def kick (self):
        item, ok = QtWidgets.QInputDialog.getItem(RPG, "Qui voulez-vous kick ?", "Joueurs", [j.name for j in self.F.player], 0, False)
        if ok and item:
            for j in self.F.player:
                if item == j.name :
                    break
            else :
                return None
            if j.alive :
                self.F.nb -= 1
            j.socket.close()
            self.F.player.remove(j)
        elif not(ok):
            return None
        else:
            return self.kick()
    def exitf(self):
        self.send(['end_game','Arret force de la partie par le serveur'])
        for pl in self.F.player:
            pl.socket.close()
        RPG.close()
        sys.exit(0)

    def start_game(self):
        self.event.set()
        self.F = field(self.players)
        app.processEvents()
        for j in self.F.player:
            self.send(['setSpell',j.help],[j])
            self.send(['setParam',[('id',j.id),('maxhp',j.pvMAX),('spell',j.staminaMAX)]],[j])
        self.LeftButton.setText("Kick")
        self.LeftButton.clicked.disconnect()
        self.LeftButton.clicked.connect(self.kick)
        self.RightButton.show()
        self.RightButton.setEnabled(True)
        self.RightButton.setText("Fin")
        self.RightButton.clicked.disconnect()
        self.RightButton.clicked.connect(self.exitf)
        self.send(['mess','\n \n \n      ---------------- \n      DEBUT DE LA PARTIE \n      ----------------\n'])
        self.log.emit('\n \n \n      ---------------- \n      DEBUT DE LA PARTIE \n      ----------------\n')
        while True:
            i = 1
            for j in self.F.player:
                try:
                    if not(j.alive):
                        raise Spellcancel
                    other_pl = [y for y in self.F.player if y != j]
                    j.restore_stamina()
                    self.send(['mess',"\n \n >> C'est le tour de "+j.name+" << "])
                    self.log.emit('Tour de '+j.name)
                    strt_mss = self.rStartTour(j.name)
                    self.log.emit(strt_mss)
                    self.send(['turnof',j.name],other_pl)
                    self.send(['mess',strt_mss])
                    for typeR,obj in j.new_turn():
                        if typeR == 'death':
                            if(obj == j): #Si le joueur meurt de lui même
                                self.send(['mess','Vous êtes mort au debut de votre tour'],[j])
                                self.send(['mess', j.name+' est mort en commencant son tour'],other_pl)
                                j.alive = False #Juste pour être sûre xD
                                break
                            else:
                                other_pl2 = other_pl.copy()
                                other_pl.remove(obj)
                                self.send(['mess',' Vous avez tué '+obj.name],[j])
                                self.send(['mess',j.name+ ' vous a tué '],[obj])
                                self.send(['mess',j.name+' a tué '+obj.name],other_pl2)
                        elif typeR == 'mess':
                            self.send(['mess',obj])
                    cd = True
                    self.send_param()
                    while cd:
                        self.send(['get_c','main'],[j])
                        ms = self.get_rsp(j)
                        if ms[0] == 'cmd':
                            print(str(ms[1]))
                            cd = self.command(ms[1],j)
                        self.send_param()
                except: pass
            self.send_param()
            self.send(['mess','\n \n     --FIN DE TOUR '+str(i)+'--   \n \n'])
            if( self.F.nb == 1):
                self.send_param()
                a = 'Fin de la partie, le gagnant est : '+[pl for pl in self.F.player if pl.alive == True][0].name
                self.send(['end_game',a])
                self.log.emit('Fin de partie')
                app.processEvents()
                QtWidgets.QMessageBox.about(RPG, "FIN DE PARTIE",a)
                RPG.close()
                sys.exit(0)
            elif( self.F.nb == 0):
                self.send_param()
                a = 'Fin de la partie, le combat a été rude... Personne ne gagne ! '
                self.send(['end_game',a])
                self.log.emit('Fin de partie')
                app.processEvents()
                QtWidgets.QMessageBox.about(RPG, "FIN DE PARTIE",a)
                RPG.close()
                sys.exit(0)
            i += 1


if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    RPG = QtWidgets.QMainWindow()
    ui = MainWindow(RPG)
    RPG.show()
    sys.exit(app.exec_())
