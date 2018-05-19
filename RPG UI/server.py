# -*- coding: utf-8 -*-
""" Server Code : RPG IPT 2018"""
import time
import socket
import pickle
from builtins import *
import random
from classes import *
from threading import Thread,Barrier,Lock
import sys
#DÃ©finition des fonctions
def TF(message):
    while True:
        try:
            a = bool(int(input(message+" 1 / 0 :")))
            return a
        except:
            print("Mauvaise entrée : Veuillez rentrer 1 ou 0 \n ")
def idle(action):
    input("Appuyez sur entrer pour "+action)
def getInt(message):
    while True:
        try:
            a = int(input(message+" :"))
            if (a < 1) : 
                print("Nombre de joueur au moins égal Ã  2 \n ")
            else :
                return a
        except:
            print("Mauvaise entrée : Veuillez rentrer un entier >= 2 \n ")

#Initialisation de la partie
def connect_ssip(adress,i):
    s2.sendto(pickle.dumps("Hi there"), address)
    get_infos(i)
def get_infos(i):
    (sock,address) = s.accept()
    print("     Joueur "+str(i)+" arrivé et enregistré !! \n")
    mss = pickle.loads(sock.recv(1024))
    try :
        if mss[0] == "name":
            name = mss[1]
            print('Joueur '+str(i)+' s\'appelle '+mss[1]+'\n')
    except:
        name = 'SansNom'+str(i)
    sock.send(pickle.dumps(["get_classe",True]))
    mss = pickle.loads(sock.recv(1024)) # de type ['classe', nomdelaclasse]
    try :
        if (mss[0] == "classe"):
            print('Classe recue : \'',mss[1],'\' par joueur '+str(i))
            for cl in classes:
                if mss[1] == cl.classname:
                    j = cl(i,sock)
                    j.name = name
                    break
        else:
            j = guerrier(i,sock)
            j.name = name
            print('Joueur '+str(i)+' guerrier par defaut')
    except:
        j = guerrier(i,sock)
        j.name = name
        print('Joueur '+str(i)+' guerrier par defaut')
    l.acquire()
    p.append(j)
    l.release()
    b.wait()

version = 'BETA 3.0'
port = 4291
localIP = socket.gethostbyname(socket.gethostname())
if localIP == '127.0.0.1' :
    localIP = 'Inconnue'
print('-------SERVER RPG '+version+' ----------'+'\n \n')
print('Vos informations \n     IP = '+localIP+' \n     Port = '+str(port)+' \n \n')
if(TF("Voulez vous lancer une partie ?")):
    
    nbj = getInt("Nombre de joueurs")
    l = Lock()
    b = Barrier(nbj+1)
    p = []
    s = socket.socket()
    connections = 0
    if TF('sans ip?'):
        s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s2.bind(('', port))
        s.bind(('',4392))
        s.listen()
        while connections < nbj :
            message, address = s2.recvfrom(1024)
            connections += 1
            th = Thread(target=connect_ssip,args=(address,connections))
            th.start()
    else:
        s.bind(('',port))
        s.listen()
        th = [Thread(target=get_infos,args=(i)) for i in range(nbj)]
        for t in th:
            t.start()
    b.wait()
    s2.close()
    s.close()
    print('usernames et classes recuperes')
    F = field(p)
else:
    print("Ah bah... Au revoir ?")
    input('?')
    sys.exit(0)

#Définition de la fonction récupérant la vérification qu'une update est généralisée
def isOk(cd):
    for j in p:
        sp = j.socket
        t_ms = pickle.loads(sp.recv(1024))
        if(t_ms[0] != cd or t_ms[1] == False):
            return False
        elif(t_ms[0] == "error"):
            errorlist = ['Wrong request from server : expected player_id','Wrong request from server : expected fld_update','Wrong request from server : expected get_name'] # Liste de l'ensemble des erreurs renvoyées par ID
            print('A player got the following error : '+errorlist[t_ms[1]])
    return True


# Définition des fonctions de communication
def send(mss, lp = p):
    print(str(mss))
    time.sleep(.3)
    try:
        for j in lp :
            j.socket.send(pickle.dumps(mss))
        return True
    except:
        return False
def get_rsp(j):
    try:
        a=pickle.loads(j.socket.recv(1024))
        print(str(a))
        return a
    except:
        return ['error',0]

time.sleep(.5)
#Envoi des paramètres à tous
send(['field',F.getTable()])

time.sleep(.5)

for j in p:
    send(['you', j.pvMAX, j.help],[j])
for j in p:
    send(['setParam',[('id',j.id)]],[j])

###### PARTIE #######

def command(a,j): #gestion des commandes pendant un tour
    other_pl = [y for y in p if y != j]
    def wrong_c(j):
        send(['mess','\n Commande incomprise '+a+' : Vérifiez votre commande'],[j])
        send(['mess',j.name+' a voulu faire quelque chose d\' impossible'],other_pl)
        print('Mauvaise commande de '+j.name+' : '+a)
        return True
    a = a.strip().casefold()
    al = a.split()
    try:
        if(al[0] == 'fin'):
            print('\n    -Fin de votre tour-   \n \n')
            send(['mess',j.name+' a fini de se battre'])
            return False
        elif(al[0] == 'spell'):
            try: toshow = j.spell(al[1],F)
            except: return wrong_c(j)
            for typeR,obj in toshow:
                if typeR == 'death':
                    if(obj == j): #Si le joueur meurt de lui même
                        send(['mess','Vous êtes mort en attaquant'],[j])
                        send(['mess', j.name+' est mort au combat'],other_pl)
                        j.alive = False #Juste pour être sûre xD
                    else:
                        other_pl2 = other_pl.copy()
                        other_pl2.remove(obj)
                        send(['mess',' Vous avez tué '+obj.name],[j])
                        send(['mess','Vous avez ete tue par '+j.name],[obj])
                        send(['mess',j.name+' a tué '+obj.name],other_pl2)
                elif typeR == 'mess':
                    send(['mess',obj])
            return j.alive

        elif(al[0] == 'stats'): # A REVOIR #
            statStr = ''
            statStr +='     -> Voici vos informations : \n'
            statStr +='         - PV : '+str(j.hp) + '\n'
            statStr +='         - Stamina : '+str(j.stamina) + '\n'
            statStr +='         - Dégâts : '+str(j.ad)+' et une attaque coûte '+str(j.att_cost)+' d\'endurance' + '\n'
            statStr +='         - Armure : '+str(j.armor*100)+'% des dégâts physiques absorbés' + '\n'
            statStr +='         - Résistance : '+str(j.resistance*100)+'% des dégâts magiques absorbés' + '\n'
            send(['mess',statStr],[j])
            return True
        elif(al[0] == 'forceend'):
            send(['mess','\n    -Fin de partie-   \n \n'])
            print('\n    -Fin de partie-   \n')
            send(['forceEND',j])
            return False
        elif(al[0] == 'field'):
            strFld = 'Voici l\'état du terrain : ' + str(F)
            send(['mess',strFld])
            send(['mess',j.name + ' observe le terrain'],other_pl)
            return True
        else:
            return wrong_c(j)
    except:
        return wrong_c(j)
    
def rStartTour(name): #Phrases aléatoires de début de tour
    l1 = ["*namej* est prêt à se battre !","Craignez la puissance *namej* :o","Cachez vous ! *namej* est prêt à jouer","*namej* va jouer mais personne n'a peur de lui ;-( ","*namej* commence son tour !","*namej* semble inarretable préparez vous à son tour"] 
    rint = random.randint(0,len(l1)-1)
    return l1[rint].replace('*namej*',name)
send(['mess','\n \n \n      ---------------- \n      DEBUT DE LA PARTIE \n      ----------------\n'])
def send_param():    
    for k in F.player:
        send(['setParam',[('hp',k.hp),('stamina',k.stamina)]],[k])
while True:
    i = 1
    for j in p:
        try:
            if(j.alive):
                other_pl = [y for y in p if y != j]
                j.restore_stamina()
                send(['mess',"\n \n >> C'est le tour de "+j.name+" << "])
                print('Tour de '+j.name)
                strt_mss = rStartTour(j.name)
                print(strt_mss)
                send(['mess',strt_mss])
                for typeR,obj in j.new_turn():
                    if typeR == 'death':
                        if(obj == j): #Si le joueur meurt de lui même
                            send(['mess','Vous êtes mort au debut de votre tour'],[j])
                            send(['mess', j.name+' est mort en commencant son tour'],other_pl)
                            j.alive = False #Juste pour être sûre xD
                            break
                        else:
                            send(['mess',' Vous avez tué '+obj.name],[j])
                            send(['mess',j.name+' a tué '+obj.name],other_pl)
                    elif typeR == 'mess':
                        send(['mess',obj])
                cd = True
                send_param()
                while cd:
                    send(['get_c','main'],[j])
                    ms = get_rsp(j)
                    if ms[0] == 'cmd':
                        print(str(ms[1]))
                        cd = command(ms[1],j)
                    send_param()
                    send(['field',F.getTable()])
                send(['field',F.getTable()])
        except: pass
    send(['mess','\n \n     --FIN DE TOUR '+str(i)+'--   \n \n'])
    if( F.nb == 1):
        send(['mess',str(F)])
        send(['end_game','Fin de la partie, le gagnant est : '+[pl for pl in p if pl.alive == True][0].name])
        input('Fin de partie')
        sys.exit(0)
    elif( F.nb == 0):
        send(['mess',str(F)])
        send(['end_game','Fin de la partie, le combat a été rude... Personne ne gagne ! '])
        input('Fin de partie')
        sys.exit(0)
    i += 1


