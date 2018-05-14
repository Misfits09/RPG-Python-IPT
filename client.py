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
import sys

""" Règles :
-> Chaque joueur a une caractéristique d'attaque et d'épine
-> Si un joueur attaque un autre il prend des dégats d'épine
-> Si un joueur tue un autre il ne prend pas les dégats d'épine
""" 
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

#Définition des fonctions pour recevoir des updates du serveur et en envoyer
def get_updt():
    up_r = pickle.loads(s.recv(1024))
    return up_r
def send_updt(u):
    s.send(pickle.dumps(u))
    time.sleep(.5)
def send_error(ider):
    send_updt(["error",ider])

# Récupération du numéro de joueur
if(r[0]=='player_id'):
    print("\n \n Vous êtes le --> JOUEUR "+str(r[1])+" <--")
    send_updt(["get_pl_id",True])
else:
    send_error(0)

#Envoi pseudo 
print('En attente des autres joueurs ...')
if(get_updt() == ["get_name", True]):
    while True:
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
    while True:
        try :
            maclasse = str(input('Votre classe : '))
            if maclasse in [j.name for j in classes]:
                send_updt(["classe",maclasse])
                break
            else:
                print('Ce nom de classe n\'est pas valide, réessayez.')
        except:
            send_error(2)
print('En attente des autres joueurs ...')

while True:
    up = get_updt()
    t = up[0]
    if t == "mess":
        print(up[1])
    elif t == "get_c":
        print('\n')
        c = str(input(up[1]))
        send_updt(['cmd',c])
    elif t == "death" :
        print('  -> VOUS ETES MORT <-  ')
        print('Vous passez en mode spectateur')
    elif t == "end_game":
        print(up[1])
        break
    elif t == "forceEND":
        print('arret force de la partie par '+up[1].name)
        break
    else:
        print(str(up))

input('Fin')


