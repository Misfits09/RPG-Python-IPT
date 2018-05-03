# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 15:56:35 2018

@author: nperriolat
"""

import socket
import random
import pickle
from classes import *
import time

""" Règles :
-> Chaque joueur a une caractéristique d'attaque et d'épine
-> Si un joueur attaque un autre il prend des dégats d'épine
-> Si un joueur tue un autre il ne prend pas les dégats d'épine
""" 
#Définition des fonctions pour recevoir des updates du serveur et en envoyer
def get_updt():
    up_r = pickle.loads(s.recv(1024))
    return up_r
def send_updt(u):
    s.send(pickle.dumps(u))
    time.sleep(.5)
def send_error(ider):
    send_updt(["error",ider])

def rStartTour(name): #Phrases aléatoires de début de tour
    l1 = ["*namej* est prêt à se battre !","Craignez la puissance *namej* :o","Cachez vous ! *namej* est prêt à jouer","*namej* va jouer mais personne n'a peur de lui ;-( ","*namej* commence son tour !","*namej* semble inarretable préparez vous à son tour"] 
    rint = random.randint(0,len(l1)-1)
    return l1[rint].replace('*namej*',name)

def command(a): #gestion des commandes pendant un tour
    global F, u_alive
    def wrong_c():
        print('\n Commande incomprise '+a+' : Vérifiez votre commande (un seul espace entre chaque argument)')
        send_updt(['mess',jName+' a voulu faire quelque chose d\' impossible'])
        return True
    a = a.strip().casefold()
    al = a.split()
    try:
        if(al[0] == 'help'): #Commande d'aide
            print('\n       Voici la liste des commandes :')
            
            cmdlist = [('help','Obtenir la description des commandes'),
                       ('fin','Termine votre tour'),
                       ('stats','Vous donne toutes les informations sur votre personnage'),
                       ('field','Affiche l\'état du terrain'),
                       ('helpspell','Affiche vos sorts'),
                       ('spell nomdusort','Lance le sort')]
            for (a,b) in cmdlist:
                print('       -> '+a+' : '+b)
            send_updt(['mess',jName+' a demandé de l\'aide']) 
            return True 
        elif(al[0] == 'helpspell'):
            print('Voici vos sorts : \n')
            for a,b in F.player[jID - 1].classe.help:
                print('       -> '+a+' : '+b)
            send_updt(['mess',jName+' consulte son livre de sorts']) 
            return True
        elif(al[0] == 'fin'):
            print('\n    -Fin de votre tour-   \n \n')
            send_updt(['mess',jName+' a fini de se battre'])
            return False
        elif(al[0] == 'spell'):
            try:
                toshow = F.player[jID - 1].classe.spell(al[1],F)
                for typeR,obj in toshow:
                    if typeR == 'death':
                        if(obj == F.player[jID-1]): #Si le joueur meurt de lui même
                            print('Vous êtes mort en attaquant')
                            send_updt(['mess', jName+' est mort au combat'])
                            u_alive = False
                            return False
                        else:
                            print(' Vous avez tué '+obj.name)
                            send_updt(['death',obj,jName+' a tué '+obj.name])
                    elif typeR == 'mess':
                        print(obj)
                        send_updt(['mess',obj])
                return True
            except:
                return wrong_c()

        elif(al[0] == 'stats'): # A REVOIR #
            you = F.player[jID - 1].classe
            print('     -> Voici vos informations :')
            print('         - PV : '+str(you.hp))
            print('         - Stamina : '+str(you.stamina))
            print('         - Dégâts : '+str(you.ad)+' et une attaque coûte '+str(you.att_cost)+' d\'endurance')
            print('         - Armure : '+str(you.armor*100)+'% des dégâts physiques absorbés')
            print('         - Résistance : '+str(you.resistance*100)+'% des dégâts magiques absorbés')
            return True
        elif(al[0] == 'forceend'):
            print('\n    -Fin de partie-   \n \n')
            send_updt(['mess','\n    -Fin de partie-   \n \n'])
            send_updt(['forceEND',True])
            return False
        elif(al[0] == 'field'):
            print('Voici l\'état du terrain : ')
            print(str(F))
            send_updt(['mess',F.player[jID - 1].name + ' observe le terrain'])
            return True
        else:
            return wrong_c()

    except:
        return wrong_c()
        

def mon_tour(): #Gestion locale du tour avec le terrain donné
    global F,u_alive
    strt_mss = rStartTour(jName)
    print(strt_mss)
    send_updt(['mess',strt_mss])
    for typeR,obj in F.player[jID - 1].classe.new_turn():
        if typeR == 'death':
             if(obj == F.player[jID-1]): #Si le joueur meurt de lui même
                    print('Vous êtes mort en commencant votre tour')
                    send_updt(['mess', jName+' est mort en commençant son tour'])
                    u_alive = False
                    return False
             else:
                print(' Vous avez tué '+obj.name)
                send_updt(['death',obj,jName+' a tué '+obj.name])
        elif typeR == 'mess':
            print(obj)
            send_updt(['mess',obj])
    cd = True
    while cd:
        cmd = input('Que voulez vous faire ? (détails : help) : \n')
        cd = command(cmd)
        print('\n')


version = "BETA 3.0"
print("Bienvenue sur RPG "+version+"\n \n \n")
print("Connection à un serveur :")
r = 0
while r == 0 :
    try :
        ip = str(input('IP de connection au serveur LOCAL : '))
        port = int(input('Port de connection : '))
        print("     Connection en cours...")
        s = socket.socket()
        s.connect((ip,port))
        r = pickle.loads(s.recv(1024))
        print("     Connection effectuée")
        break
    except:
        print('Erreur dans l\' écriture de l \' IP et port OU erreur de connection')
        pass

# Récupération du numéro de joueur
if(r[0]=='player_id'):
    print("\n \n Vous êtes le --> JOUEUR "+str(r[1])+" <--")
    jID = r[1]
    send_updt(["get_pl_id",True])
else:
    send_error(0)

#Envoi pseudo 
print('En attente des autres joueurs ...')
if(get_updt() == ["get_name", True]):
    while 1:
        try :
            usrnm = str(input('\n Choissisez un pseudo : '))
            jName = usrnm
            send_updt(["name",usrnm])
            break
        except:
            send_error(2)

#Récupération classe
print('En attente des autres joueurs ...')
if(get_updt() == ["get_classe", True]):
    print('Choissisez parmis les classes suivantes : ')
    for k in [j.name for j in classes]:
        print(' -> '+k)
    while 1:
        try :
            maclasse = str(input('Votre classe : '))
            if maclasse in [j.name for j in classes]:
                send_updt(["classe",maclasse])
                break
            else:
                print('Ce nom de classe n\'est pas valide, réessayez.')
        except:
            send_error(2)
#Création du terrain depuis le serveur
print('Attente des autres joueurs...')
up = get_updt()
print('--> Démarrage de la partie <--')
if(up[0] == 'fld_update'):
    F = up[1]
    print('Le terrain contient '+str(len(F.player))+' joueurs :')
    for i in range(len(F.player)):
        print(str(F.player[i]))
    send_updt(["get_fld",True])
    u_alive = F.player[jID-1].alive
else:
    send_error(1)

#Partie ...

while 1:
    [t,c] = get_updt()
    if t == "mess":
        print(c)
    elif t == "fld_update":
        F = c
        u_alive = F.player[jID-1].alive
        send_updt(['get_fld',True])
        print("\n \n> Voici l'état du terrain : ")
        for ply in F.player:
            print("     - "+str(ply))
    elif t == "deb_tour":
        if(u_alive):
            send_updt(['deb_tour',True])
            F.player[jID - 1].restore_stamina()
            mon_tour()
            send_updt(['end_tour',F])
        else:
            send_updt(['deb_tour',True])
            send_updt(['end_tour',F])
    elif t == "death" :
        print('  -> VOUS ETES MORT <-  ')
        u_alive = False
        print('Vous passez en mode spectateur')
    elif t == "end_game":
        print(c)
        break
    else:
        break

input('Fin')


