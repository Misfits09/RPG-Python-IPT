# -*- coding: utf-8 -*-
""" Server Code : RPG IPT 2018"""
from serv_ui import *
import time
import socket
import pickle
import random
from classes import *
from threading import Thread,Event,Lock
import sys


class signals(QtCore.QObject):
    fld_updt = QtCore.pyqtSignal()
    spell_end = QtCore.pyqtSignal(list)
class log(QtCore.QObject):
    out = QtCore.pyqtSignal(str)

class MainWindow(Ui_Server):
    def send(self,mss, lp = None):
        time.sleep(.1)
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
            app.processEvents()
            return a
        except:
            return ['error',0]
    def chat(self):
        while True:
            for pl in self.F.player:
                try:
                    mss = pickle.loads(pl.chatsocket.recv(1024))
                    self.log.emit(pl.name+' : '+mss)
                    self.send(['chat',pl.name+' : '+mss])
                except:pass
    
    def __init__(self,frame):
        self.setupUi(frame)
        version = "RPG ALPHA 1.0"
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
        self.signals = signals()
        self.signals.fld_updt.connect(self.printfld)
        self.signals.spell_end.connect(self.validerspells)
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
        self.connectthread = Thread(target=self.search_ip)
        self.connectthread.start()
    def connect_ssip(self):
        self.RightButton.setEnabled(False)
        self.RightButton.hide()
        self.LeftButton.setText("Demarrer")
        self.LeftButton.clicked.disconnect()
        self.LeftButton.clicked.connect(self.start_game)
        self.event = Event()
        self.log.emit('En attente de joueurs')
        self.connectthread = Thread(target=self.search_ssip)
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
                    sock,_unused = s.accept()
                    sock2,_unused = s.accept()
                    sock2.settimeout(.2)
                    t = Thread(target=self.get_infos,args=(i,sock,sock2))
                    t.start()
                    i += 1
                except socket.timeout : pass
        return None
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
                    _unused, address = s2.recvfrom(1024)
                    connections += 1
                    s2.sendto(pickle.dumps("Hi there"),address)
                    sock,_unused = s.accept()
                    sock2,_unused = s.accept()
                    sock2.settimeout(.2)
                    th = Thread(target=self.get_infos,args=(connections,sock,sock2))
                    th.start()
                except socket.timeout: pass
        return None

    def get_infos(self,i,sock,sock2):
        self.log.emit("Joueur "+str(i)+" arrivé et enregistré !!")
        mss = pickle.loads(sock.recv(1024))
        if mss[0] == "get_infos":
            try : 
                name = mss[1]
                self.log.emit('Joueur '+str(i)+' s\'appelle '+mss[1])
            except:
                name = 'SansNom'+str(i)
                self.log.emit("Joueur "+str(i)+" sans nom")
            try:
                for cl in classes:
                    if mss[2] == cl.classname:
                        j = cl(i,sock,sock2)
                        j.name = name
                        self.log.emit('Classe recue : \''+mss[2]+'\' par joueur '+str(i))
                        break
                else:
                    j = guerrier(i,sock,sock2)
                    j.name = name
                    self.log.emit('Joueur '+str(i)+' guerrier par defaut : ERRCLSS1')
            except:
                j = guerrier(i,sock,sock2)
                j.name = name
                self.log.emit('Joueur '+str(i)+' guerrier par defaut : ERRCLSS2')
            self.plock.acquire()
            self.players.append(j)
            self.table.append([str(j.id),j.name,j.classname,str(j.hp),str(j.stamina)])
            self.plock.release()
            self.signals.fld_updt.emit()
            return None
    
    def command(self,j): #gestion des commandes pendant un tour
        sotstamina = j.stamina
        cd = True
        self.send_param()
        spelllist = []
        while cd:
            self.send(['get_c','main'],[j])
            ms = self.get_rsp(j)
            if ms[0] == 'cmd':
                self.log.emit(j.name+' : '+str(ms[1]))
                al = ms[1].strip().split()
                if al[0] == 'fin':
                    self.send(['mess','Attente des autres joueurs...'],[j])
                    cd = False
                elif(al[0] == 'spell'):
                    try:
                        toshow = j.spell(al[1],self.F)
                        if len(toshow) == 3:
                            self.send(['spell',al[1]],[j])
                        elif len(toshow) == 4:
                            self.send(['spell',al[1]+' : '+toshow[3].name],[j])
                        spelllist.append(toshow)
                    except Empty_fld : self.send(['alert','erreur','Aucune cible disponible'],[j])
                    except NoStamina : self.send(['alert','erreur','Pas assez d\'endurance'],[j])
                    except Spellerror : self.send(['alert','erreur','Impossible de lancer ce sort'],[j])
                    except : pass
                elif al[0] == 'cancel':
                    a = spelllist.pop()
                    a = a[1].__name__
                    for h in j.help:
                        if h[0] == a:
                            j.stamina += h[1]
            self.send_param()
        j.stamina = sotstamina
        self.send_param()
        self.signals.spell_end.emit(spelllist)
        return None
        
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
        app.processEvents()
    def send_param(self):    
        self.send(['field',[(p[1],p[2],p[3],p[5]) for p in self.F.getTable()]])
        self.table =self.F.getTable()
        self.signals.fld_updt.emit()
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
            self.signals.spell_end.emit([])
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
        th= Thread(target=self.chat)
        th.start()
        app.processEvents()
        for j in self.F.player:
            self.send(['setSpell',j.help],[j])
            self.send(['setParam',[('id',j.id),('maxhp',j.pvMAX)]],[j])
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
        self.turnnb = 1
        self.start_tour()

    def start_tour(self):
        self.spelllist = []
        for j in self.F.player:
            try:
                if not(j.alive):
                    raise Spellcancel
                j.restore_stamina()
                j.turn_speed()
                spells = []
                for typeR,obj in j.new_turn():
                    if typeR == 'death':
                        other_pl = [y for y in self.F.player if y != j]
                        if(obj == j): #Si le joueur meurt de lui même
                            self.send(['mess','Vous êtes mort au debut de votre tour'],[j])
                            self.send(['mess', j.name+' est mort en commencant son tour'],other_pl)
                            self.log.emit(j.name+' est mort en commencant son tour')
                            j.alive = False #Juste pour être sûre xD
                            break
                        else:
                            other_pl2 = other_pl.copy()
                            other_pl.remove(obj)
                            self.send(['mess',' Vous avez tué '+obj.name],[j])
                            self.send(['mess',j.name+ ' vous a tué '],[obj])
                            self.send(['mess',j.name+' a tué '+obj.name],other_pl2)
                            self.log.emit(j.name+' a tué '+obj.name)
                    elif typeR == 'mess':
                        self.send(['mess',obj])
                        self.log.emit(obj)
                    elif typeR == 'spell':
                        spells.append(obj)
                self.send_param()
                self.spelllist.append(spells)
            except: pass
        self.thinking = self.F.nb
        self.send(['mess','\n \n \n    --Actions du tour-- '])
        for j in self.F.player:
            th = Thread(target=self.command,args=(j,))
            th.start()

    def trispell(self):
        t = []
        t2 = []
        for k in self.spelllist:
            j = 0
            while j < len(k):
                if k[j][0] == 0:
                    t.append(k[j])
                    k.remove(k[j])
                elif k[j][0] == 1:
                    t2.append(k[j])
                    k.remove(k[j])
                else:
                    j += 1
        while [] in self.spelllist:
            self.spelllist.remove([])
        for k in range(1,len(self.spelllist)):
            temp=self.spelllist[k].copy()
            j=k
            while j>0 and self.spelllist[j-1][0][0] > temp[0][0]:
                self.spelllist[j]=self.spelllist[j-1].copy()
                j-=1
            self.spelllist[j] = temp
        for k in self.spelllist:
            t += k
        self.spelllist = t + t2
    def validerspells(self,liste):
        self.thinking -= 1
        self.spelllist.append(liste)
        if self.thinking == 0:
            self.trispell()
            self.processturn()
    
    def processturn(self):
        self.send(['mess','\n \n     --DEBUT DE TOUR '+str(self.turnnb)+'--   \n \n'])
        self.log.emit('\n \n     --DEBUT DE TOUR '+str(self.turnnb)+'--   \n \n')
        self.send(['gametext','Tour '+str(self.turnnb)])
        for s in self.spelllist:
            try:
                if not(s[2].alive):
                    raise Spellcancel
                self.send_param()
                if len(s) == 3:
                    toshow = s[1]()
                elif len(s) == 4:
                    toshow = s[1](s[3])
                for typeR,obj in toshow:
                    if typeR == 'death':
                        other_pl = [p for p in self.F.player if p.id != s[2].id]
                        if(obj == s[2]): #Si le joueur meurt de lui même
                            self.send(['mess','Vous êtes mort en attaquant'],[s[2]])
                            self.send(['mess', s[2].name+' est mort au combat'],other_pl)
                            self.log.emit(s[2].name+' est mort au combat')
                        else:
                            other_pl2 = other_pl.copy()
                            other_pl2.remove(obj)
                            self.send(['mess',' Vous avez tué '+obj.name],[s[2]])
                            self.send(['mess','Vous avez ete tue par '+s[2].name],[obj])
                            self.send(['mess',s[2].name+' a tué '+obj.name],other_pl2)
                            self.log.emit(s[2].name+' a tué '+obj.name)
                    elif typeR == 'mess':
                        self.log.emit(obj)
                        self.send(['mess',obj])
            except: pass
            self.send_param()
        self.send(['mess','\n \n     --FIN DE TOUR '+str(self.turnnb)+'--   \n \n'])
        self.log.emit('\n \n     --FIN DE TOUR '+str(self.turnnb)+'--   \n \n')
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
        self.turnnb += 1
        self.start_tour()


if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    RPG = QtWidgets.QMainWindow()
    ui = MainWindow(RPG)
    RPG.show()
    sys.exit(app.exec_())
