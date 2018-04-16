# -*- coding: utf-8 -*-
""" Server Code : RPG IPT 2018"""
import time
class joueur():
    classes = ['guerrier']
    alive = True
    spike = 0
    armor = 0
    ad = 0
    F = None
    def __init__(self,i,add):
        self.hp = 100
        self.id,self.name = i,str(i)
        self.ad = add
    def set_field(self,fi):
        self.F = fi
    def take_damage(self, amount):
        self.hp -= amount*(1 - self.armor)
        if self.hp <= 0 :
            self.hp = 0
            return False
        return True
    def attack(self,cible):
        commList = []
        commList.append(('allOK',jName+' attaque '+cible.name+' !'))
        if not cible.take_damage(self.ad):  
            commList.append(self.F.isDead(cible))
            if(cible.spike != 0):
                commList.append(('allOK',self.name + ' évite les épines de '+cible.name+' en le tuant'))
        elif (cible.spike != 0 and self.take_damage(cible.spike)): # Argument après le 'and' ne se lance que si spike != 0
            commList.append(('allOK',self.name + ' a attaque '+cible.name+' qui a maintenant '+cible.hp+' PV '+'\n'+' Mais s\'est fait mal en attaquant et a maintenant '+self.hp+' PV '))
        elif (cible.spike != 0): #donc self.take_damage(cible.spike) a renvoyé False
            commList.append(self.F.isDead(self))
        else:
            commList.append(('allOK',self.name + 'a attaque '+cible.name+' qui a maintenant '+str(cible.hp)+' PV (sans se faire mal) '))
        commList.reverse()
        return commList
    def set_spec(self,dm):
        self.ad = dm
    
    def __str__(self):
        return str(self.name) + " à " + str(self.hp) + "PV et fait "+str(self.ad)+" de dégats"
    def __eq__(self,other):
        return self.id == other.id

class field():
    player = []
    nb = 0
    def __init__(self,p):
        self.player = p
        self.nb = len(p)
        for j in self.player:
            j.set_field(self)
    def isDead(self, joueur):
        self.player[joueur.id - 1].alive = False
        self.nb -= 1
        return ('death',joueur)
    def __str__(self):
        a = "Joueurs : "
        for j in self.player:
            a += str(j)+" | "
        return a
import socket
import pickle
from builtins import *
import random

#DÃ©finition des fonctions
def TF(message):
    while 1:
        try:
            a = bool(int(input(message+" 1 / 0 :")))
            return a
        except:
            print("Mauvaise entrée : Veuillez rentrer 1 ou 0 \n ")
def idle(action):
    input("Appuyez sur entrer pour "+action)
def getInt(message):
    while 1:
        try:
            a = int(input(message+" :"))
            if (a < 1) : 
                print("Nombre de joueur au moins égal Ã  2 \n ")
            else :
                return a
        except:
            print("Mauvaise entrée : Veuillez rentrer un entier >= 2 \n ")


#Initialisation de la partie

version = 'BETA 2.0'
port = 4291
localIP = socket.gethostbyname(socket.gethostname())
if localIP == '127.0.0.1' :
    localIP = 'Inconnue'
print('-------SERVER RPG '+version+' ----------'+'\n \n')
print('Vos informations \n     IP = '+localIP+' \n     Port = '+str(port)+' \n \n')
if(TF("Voulez vous lancer une partie ?")):
    
    nbj = getInt("Nombre de joueurs")
    idle("rechercher des joueurs : ")
    s = socket.socket()
    s.bind((socket.gethostname(),port))
    s.listen()
    p = []
    sockp = []
    for i in range(nbj):
        print("     Attente joueur "+str(i+1))
        (sock,address) = s.accept()
        p.append(joueur(i+1,random.randint(30,50)))
        sockp.append(sock)
        sock.send(pickle.dumps(["player_id",i+1]))
        print("     Joueur "+str(i+1)+" arrivé et enregistré !! \n")
    F = field(p)
else:
    print("Ah bah... Au revoir ?")
    input('?')

#Définition de la fonction récupérant la vérification qu'une update est généralisée
def isOk(cd):
    for sp in sockp:
        t_ms = pickle.loads(sp.recv(1024))
        if(t_ms[0] != cd or t_ms[1] == False):
            return False
        elif(t_ms[0] == "error"):
            errorlist = ['Wrong request from server : expected player_id','Wrong request from server : expected fld_update','Wrong request from server : expected get_name'] # Liste de l'ensemble des erreurs renvoyées par ID
            print('A player got the following error : '+errorlist[t_ms[1]])
    return True

#   Vérification que tous ont initialisé leurs ID
if(isOk('get_pl_id')):
    print("     Tous connectés !")
else:
    print(" !!!! FATAL ERROR !!!! ")

# Récupération des usernames
for i in range(nbj):
    sockp[i].send(pickle.dumps(["get_name",True]))
    print("     Récupération nom du joueur "+str(i+1)+"\n")
    mss = pickle.loads(sockp[i].recv(1024))
    try :
        if mss[0] == "name":
            F.player[i].name = mss[1]
    except:
        F.player[i].name = 'SansNom'+str(i+1)

#Récupération des classes
for i in range(nbj):
    sockp[i].send(pickle.dumps(["get_classe",True]))
    print("     Récupération des classes du joueur "+str(i+1)+"\n")
    mss = pickle.loads(sockp[i].recv(1024)) # de type ['classe', nomdelaclasse]
    try :
        if (mss[0] == "classe"):
            F.player[i].set_classe(mss[1])
        else:
            F.player[i].set_classe('freelance')
    except:
        F.player[i].set_classe('freelance')

# Téléchargement du Field chez les clients
print('\n \n Tour 0 : Mise a jour du terrain pour les '+str(nbj)+' joueurs')

# Définition de la fonction Mise à Jour du terrain
def updt_fld():
    for i in range(nbj):
        sockp[i].send(pickle.dumps(["fld_update",F]))
        print("     Joueur "+str(i+1)+" mis à jour \n")

    if(isOk('get_fld')):
        print("     Tous à jour !")
    else:
        print(" !!!! FATAL ERROR !!!! ")

updt_fld()

# Définition des fonctions de communication
def send(lp, mss):
    try:
        for i in lp:
            sockp[i-1].send(pickle.dumps(mss))
        return True
    except:
        return False
def get_rsp(i):
    try:
        return pickle.loads(sockp[i-1].recv(1024))
    except:
        return ['error',0]

###### PARTIE #######
while 1:
    i = 1
    for tour in range(nbj):
        if(F.player[tour].alive):
            send(list(range(1,nbj+1)),['mess',"\n \n >> C'est le tour de "+F.player[tour].name+" << "])
            print('Tour de '+F.player[tour].name)
            time.sleep(.5)
            send([tour+1],['deb_tour',True])
            if(get_rsp(tour+1) == ['deb_tour',True]):
                while 1:
                    ms = get_rsp(tour+1)
                    if(ms[0] == 'death'):
                        print("\n"+ms[1].name+' est mort')
                        a = list(range(1,nbj+1))
                        a.remove(tour+1)
                        send(a,['mess',ms[2]])
                        send([ms[1].id],['death', True])
                    elif(ms[0] == 'mess'):
                        print("\n     "+ms[1])
                        a = list(range(1,nbj+1))
                        a.remove(tour+1)
                        send(a,['mess',"    "+ms[1]])

                    elif(ms[0] == 'end_tour'):
                        F = ms[1]
                        updt_fld()
                        print('Fin du tour')
                        break
                    elif(ms[0] == 'forceEND'):
                        send(list(range(1,nbj+1)),['end_game','Arrêt forcé de la partie par '+F.player[tour].name])
                    else:
                        break
            else:
                pass
    send(list(range(1,nbj+1)),['mess','\n \n     --FIN DE TOUR '+str(i)+'--   \n \n'])
    if( F.nb == 1):
        send(list(range(1,nbj+1)),['end_game','Fin de la partie, le gagnant est : '+F.player[0].name])
    elif( F.nb == 0):
        send(list(range(1,nbj+1)),['end_game','Fin de la partie, le combat a été rude... Personne ne gagne ! '])
    i += 1


input('Fin de partie')