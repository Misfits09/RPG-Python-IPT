import random
import pickle
import socket
import time
class Empty_fld(Exception):
    pass
class Spellcancel(Exception):
    pass
class NoStamina(Exception):
    pass
class Spellerror(Exception):
    pass
class field():
    def __init__(self,p):
        self.player = p
        self.nb = len(p)
        for j in self.player:
            j.set_field(self)
    def isDead(self, joueur):
        joueur.alive = False
        self.nb -= 1
        return ('death',joueur)
    def __str__(self):
        a = "\n Joueurs : "
        for j in self.player:
            a +='\n' + str(j)
        return a
    def getTable(self):
        terrain=[]
        for j in self.player:
            terrain.append([str(j.id),j.name,j.classname,str(j.hp),str(j.stamina),j.pvMAX])
        return terrain

class joueur():
    def __init__(self,i,sk,csk): 
        self.id,self.name = i,str(i)
        self.alive = True
        self.F = None
        self.socket = sk
        self.chatsocket = csk
        self.trigger = triggers()
        self.trigger.addDmg(self.spikes)
        self.trigger.addT(self.dodgef)
        self.hp = self.pvMAX
        self.stamina = self.staminaMAX
        self.speed = self.basespeed
    def set_field(self,fi):
        self.F = fi
    def restore_stamina(self):
        self.stamina = self.staminaMAX
    def turn_speed(self):
        self.speed = random.gauss(self.basespeed,self.basespeed/5)
    def __str__(self):
        if self.alive:
            return self.classestr()
        else:
            return str(self.name) + " est mort"
    def __eq__(self,other):
        return self.id == other.id
    
    #appelée à chaque début de tour du joueur
    def new_turn(self): 
        commlist = []
        for nb,fct in self.trigger.turnresolve:
            if nb != 0:
                self.trigger.dec_counter(fct)
            else:
                try :
                    commlist += fct()
                except : pass
        return commlist
    
    #ciblage d'attaque
    def attack_target(self,target,amount,dtype):
        commlist = []
        do_attk = True
        for fct in self.trigger.init:
            try : 
                a,b = fct(self,amount,dtype)
                commlist += b
                if a :
                    do_attk = False
                    break
            except : pass
        if not do_attk:
            return commlist
        for fct in target.trigger.target:
            try : 
                a,b = fct(self,target,amount,dtype)
                commlist += b
                if a :
                    do_attk = False
                    break
            except : pass
        if do_attk:
            return commlist + self.hit_attack(target,amount,dtype)
        else :
            return commlist
    
    #application dégâts
    def hit_attack(self,target,amount,dtype):
        commlist = []
        for fct in self.trigger.hit:
            try : 
                a,dt,b = fct(self,target,amount,dtype)
                amount = a
                dtype = dt
                commlist += b
            except : pass
        return commlist + target.take_damage(self,amount,dtype)
    
    #réception dégâts
    def take_damage(self,source,amount,dtype):
        commlist = []
        for fct in self.trigger.damage:
            try : 
                a,b = fct(source,self,amount,dtype)
                amount = a
                commlist += b
            except : pass
        if dtype == 'physique':
            amount = amount*(1 - self.armor)
        elif dtype == 'magique' :
            amount = amount*(1 - self.resistance)
        self.hp -= amount
        commlist += [('mess',self.name+' subit '+str(amount)+' degats')]
        if self.hp <= 0 :
            self.hp = 0
            commlist += [self.F.isDead(self)]
        return commlist
    
    #dégâts d'épine
    def spikes(self,source,target,amount,dtype):
        if dtype == 'physique' and self.spike != 0:
            return amount,([('mess',source.name+' se blesse en attaquant')] +source.take_damage(self,self.spike,'spike'))
    
    #esquive
    def dodgef(self,source,target,amount,dtype):
        if self.dodge != 0:
            rd = random.randint(1,100)
            if rd <= self.dodge:
                return True,[('mess',self.name+' a esquivé l\'attaque')]

def sendc(mss, p):
    time.sleep(.3)
    try:
        p.socket.send(pickle.dumps(mss))
        return True
    except:
        return False
def get_rspc(j):
    try:
        a=pickle.loads(j.socket.recv(1024))
        return a
    except:
        return ['error',0]

# DEFINITION DES CLASSES #
def findtarget(j,alive = True):
    global F
    namelist = [x.name for x in F.player if x.alive == alive]
    if namelist == []:
        raise Empty_fld
    while True:
        sendc(['get_c','target',namelist ],j)
        _unused,name = get_rspc(j)
        if name == 'cancel':
            raise Spellcancel
        plFound = False
        for pl in F.player:
            if(pl.name.casefold().strip() == name.casefold().strip() and (pl.alive == alive)):
                plFound = True
                return pl
        if (not plFound):
            raise Empty_fld

class triggers():
    def __init__(self):
        self.target = []
        self.init = []
        self.damage = []
        self.turnresolve = []
        self.hit = []
    def addT(self,f):
        self.target.append(f)
    def remT(self,f):
        self.target.remove(f)
    def addI(self,f):
        self.init.append(f)
    def remI(self,f):
        self.init.remove(f)
    def addDmg(self,f):
        self.damage.append(f)
    def remDmg(self,f):
        self.damage.remove(f)
    def addTrRes(self,nb,f):
        self.turnresolve.append((nb,f))
    def remTrRes(self,f):
        for nb,fct in self.turnresolve:
            if fct == f:
                self.turnresolve.remove((nb,f))
                break
    def dec_counter(self,f):
        L = self.turnresolve
        for i in range(len(L)):
            if L[i][1] == f:
                L[i] = (L[i][0]-1,f)
                break
    def addHit(self,f):
        self.hit.append(f)
    def remHit(self,f):
        self.hit.remove(f)
    def __str__(self):
        return str((self.init,self.target,self.damage,self.turnresolve,self.hit))

class guerrier(joueur):
    classname = 'guerrier'
    spike = 10
    dodge = 0
    armor = .25
    resistance = .10
    ad = 17.5
    att_cost = 30
    staminaMAX = 100
    pvMAX = 150
    basespeed = 50
    help = [('block',40,'réduit les dégâts physiques pendant un tour'),
            ('protect',30,'encaisse les attaques à la place de la cible (un tour)'),
            ('attack',att_cost,'attaque de base')]
    def classestr(self):
        return 'Guerrier '+self.name+' a '+str(self.hp)+' PV, une armure moyenne et un bon bouclier !'
    def __init__(self, *args):
        super().__init__(*args)
        self.protecting = None

    #bloquer la prochaine attaque (dmgtrigger sur soi)
    def block(self):
        if self.stamina < 40 :
            return [('mess', self.name+' n\'a pas la force de bloquer : Endurance à '+str(self.stamina))]
        self.stamina -= 40
        self.trigger.addDmg(self.blocking)
        self.trigger.addTrRes(0,self.removeblocking)
        return [('mess', self.name+' se prépare à bloquer')]
    def blocking(self,source,target,amount,dtype):
        if dtype == 'physique':
            return amount/2,[('mess',self.name+' bloque l\'attaque')]
    def removeblocking(self):
        self.trigger.remDmg(self.blocking)
        self.trigger.remTrRes(self.removeblocking)
        return [('mess',self.name + ' ne bloque plus les coups')]
    
    #prendre une attaque à la place de la cible (targettrigger sur cible)
    def protect (self,target):
        if self.stamina < 30 :
            return [('mess', self.name+' n\'a pas la force de protéger : Endurance à '+str(self.stamina))]
        if not target.alive:
            return[('mess',target.name+' est morte et ne peut pas être protégée')]
        self.stamina -= 30
        target.trigger.addT(self.protection)
        self.trigger.addTrRes(0,self.remprotect)
        self.protecting = target
        return [('mess',self.name+' protège '+target.name)]
    def protection(self,source,target,amount,dtype):
        if dtype == 'physique':
            return True,([('mess',self.name+' encaisse l\'attaque à sa place')] + source.hit_attack(self,amount,dtype))
    def remprotect(self):
        self.protecting.trigger.remT(self.protection)
        self.trigger.remTrRes(self.removeblocking)

    #lancer un sort
    def spell (self,nomduspell,fld):
        global F
        F = fld
        if nomduspell == 'block':
            if self.stamina < 40 :
                raise NoStamina
            self.stamina -= 40
            return (0,self.block,self)
        elif nomduspell == 'protect':
            if self.stamina < 30 :
                raise NoStamina
            pl = findtarget(self)
            self.stamina -= 30
            return (0,self.protect,self,pl)
        elif nomduspell == 'attack':
            if(self.stamina < self.att_cost):
                raise NoStamina
            pl = findtarget(self)
            self.stamina -= self.att_cost
            return (1/self.speed,self.attack,self,pl)
        else:
            raise Spellerror
        
    #attaque de base
    def attack(self,target):
        if not target.alive:
            return [('mess',self.name+' essaie de frapper '+target.name+' mais il est déjà mort')]
        if(self.stamina >= self.att_cost):
            self.stamina -= self.att_cost
        else:
            return [('mess', self.name+' n\' a pas la force d\'attaquer : Endurance à '+str(self.stamina))]
        return [('mess', self.name + ' attaque '+ target.name )] + self.attack_target(target,self.ad,'physique')
    
class ninja(joueur):
    classname = 'ninja'
    spike = 0
    dodge = 30
    armor = 0
    resistance = 0
    base_ad = 17.5
    att_cost = 25
    staminaMAX = 100
    pvMAX = 85
    basespeed = 150
    help = [('hide',50, 'Se cache pendant un tour et ne peut plus attaquer'),
            ('attack',att_cost,'Attaque physique de base'),
            ('esquive',35,'Esquive la prochaine attaque'),
            ('affutage',30,'Augmente légèrement les dégâtes infligés'),]

    def __init__(self, *args):
        super().__init__(*args)
        self.lastTurnHide = False
        self.ad = self.base_ad

    #Se cacher pendant un tour (si dtype != zone)
    def hide(self): #Se retire au bout d'un tour
        if self.stamina < 50 :
            return [('mess', self.name+' n\'a pas la force de se cacher : Endurance à '+str(self.stamina))]
        elif self.lastTurnHide :
            return [('mess', self.name+' a encore voulu se cacher mais n\'a pas pu')]
        self.stamina -= 50
        self.lastTurnHide = True
        self.trigger.addT(self.hiding)
        self.trigger.addTrRes(0,self.endHiding)
        self.trigger.addTrRes(1,self.canHide)
        return [('mess', self.name+' est caché ! Mon dieu... où est-il passé ?!')]
    def hiding(self,source,target,amount,dtype):
        return True,[('mess',self.name + ' est trop bien caché et l\'attaque part dans le vent...')]
    def canHide(self):
        self.lastTurnHide = False
        self.trigger.remTrRes(self.canHide)
        return []
    def endHiding(self):
        self.trigger.remTrRes(self.endHiding)
        self.trigger.remT(self.hiding)
        return [('mess', self.name + ' est sorti de sa cachette')]
    
    def affutage(self):
        if self.stamina < 30 :
            return [('mess', self.name+' n\'a pas la force de renforcer son attaque : Endurance à '+str(self.stamina))]
        self.stamina -= 30
        self.ad += 6
        return [('mess',self.name + ' a renforcé sa force d\'attaque')]
    
    def attack(self,target):
        if not target.alive:
            return [('mess',self.name+' essaie de frapper '+target.name+' mais il est déjà mort')]
        if(self.stamina >= self.att_cost):
            self.stamina -= self.att_cost
        else:
            return [('mess', self.name+' n\' a pas la force d\'attaquer : Endurance à '+str(self.stamina))]
        return [('mess', self.name + ' attaque '+ target.name )] + self.attack_target(target,self.ad,'physique')
    
    def esquive(self):
        if self.stamina < 35:
            return [('mess', self.name+' n\' a pas la force de se préparer à esquiver : Endurance à '+str(self.stamina))]
        else:
            self.stamina -= 35
        self.trigger.addT(self.esquiving)
        return [('mess',self.name+' est prêt à esquiver l\'attaque')]
    def esquiving(self,source,target,amount,dtype):
        self.trigger.remT(self.esquiving)
        return True,[('mess',self.name + ' esquive l\'attaque avec classe ! ')]

    def spell (self,nomduspell, fld):
        global F
        F = fld
        if nomduspell == 'hide':
            if self.lastTurnHide:
                raise Spellerror
            if self.stamina < 50:
                raise NoStamina
            self.stamina -= 50
            return (0,self.hide,self)
        elif nomduspell == 'attack':
            if self.stamina < self.att_cost:
                raise NoStamina
            target = findtarget(self)
            self.stamina -= self.att_cost
            return (1/self.speed,self.attack,self,target)
        elif nomduspell == 'esquive':
            if self.stamina < 35:
                raise NoStamina
            self.stamina -= 35
            return (1/self.speed,self.esquive,self)
        elif nomduspell == 'affutage':
            if self.stamina < 30:
                raise NoStamina
            self.stamina -= 30
            return (1/self.speed,self.affutage,self)
        else:
            raise Spellerror
    def classestr(self):
        return 'Maître Ninja '+self.name+' a '+str(self.hp)+' PV, et un entrainement aux arts martiaux !'

class mage_noir(joueur):
    classname = 'mage noir'
    spike = 0
    dodge = 0
    armor = 0
    resistance = .20
    ad = 60
    att_cost = 50
    staminaMAX = 100
    pvMAX = 100
    basespeed = 95

class mage_blanc(joueur):
    classname = 'mage blanc'
    spike = 0
    dodge = 0
    armor = .25
    resistance = .30
    ad = 10
    att_cost = 20
    staminaMAX = 100
    pvMAX = 100
    basespeed = 115
    help = [('soin',30,'Soigne la cible de 25 PV'),
            ('reborn',100,'Fait renaitre un joueur mort avec la moitié de sa vie'),
            ('godshield',100,'Bouclier invulnérable d\'un tour sur une cible (Un tour de delai)'),
            ('attack',att_cost,'Lance une faible attaque magique sur la cible')]
    def __init__(self, *args):
        super().__init__(*args)
        self.hasDoneGS = False

    def soin(self,tg):
        if not tg.alive:
            return [('mess',self.name+' essaye de soigner '+tg.name+' mais il est mort')]
        if self.stamina < 30:
            return [('mess',self.name + ' n\' a pas l\'énergie suffisante pour soigner : '+str(self.stamina))]
        self.stamina -= 30
        tg.hp += 25
        if tg.hp > tg.pvMAX:
            tg.hp = tg.pvMAX
        return [('mess',tg.name + ' a été soigné de 25 PV par '+self.name)]

    def attack(self,target):
        if not target.alive:
            return [('mess',self.name+' essaie de frapper '+target.name+' mais il est déjà mort')]
        if(self.stamina >= self.att_cost):
            self.stamina -= self.att_cost
        else:
            return [('mess', self.name+' n\' a pas la force d\'attaquer : Endurance à '+str(self.stamina))]
        return [('mess', self.name + ' attaque '+ target.name )] + self.attack_target(target,self.ad,'magique')
    
    def godshield(self,tg):
        if not tg.alive:
            return [('mess',self.name+' ne peut protéger '+tg.name+' car il est mort')]
        if self.stamina <  100:
            return [('mess',self.name + ' n\' a pas l\'énergie suffisante pour canaliser un bouclier divin : '+str(self.stamina))]
        elif self.hasDoneGS:
            return [('mess',self.name + ' ne peut pas canaliser un nouveau bouclier divin ')]
        self.stamina -= 100
        tg.trigger.addDmg(self.isGodShielded)
        self.trigger.addTrRes(0,self.remGodShield)
        self.trigger.addTrRes(1,self.canGodShield)
        self.godshielding = tg
        self.hasDoneGS = True
        return [('mess',tg.name + ' a reçu une protection divine par '+self.name)]
    def isGodShielded(self,src,tg,amount,dtyp):
        return 0,[('mess',tg.name +' est protégé par les dieux')]
    def remGodShield(self):
        self.godshielding.trigger.remT(self.isGodShielded)
        self.trigger.remTrRes(self.remGodShield)
        return [('mess','Le bouclier divin de '+self.godshielding.name+' est tombé')]
    def canGodShield(self):
        self.trigger.remTrRes(self.canGodShield)
        self.hasDoneGS = False
        return []

    def reborn(self,pl):
        if pl.alive:
            return [('mess',self.name+' essaye de ressuciter '+pl.name+' mais il n\'est pas mort')]
        if self.stamina <  100:
            return [('mess',self.name + ' n\' a pas l\'énergie suffisante pour réanimer : '+str(self.stamina))]
        self.stamina -= 100
        pl.alive = True
        pl.hp = int(pl.pvMAX/2)
        F.nb += 1
        return [('mess',pl.name+' est réanimé par '+self.name)]

    def spell (self,nomduspell, fld):
        global F
        F = fld
        if nomduspell == 'soin':
            if self.stamina < 30:
                raise NoStamina
            target = findtarget(self)
            self.stamina -= 30
            return (1/self.speed,self.soin,self,target)
        elif nomduspell == 'reborn':
            if self.stamina < 100:
                raise NoStamina
            target = findtarget(self,False)
            self.stamina -= 100
            return (1/self.speed,self.reborn,self,target)
        elif nomduspell == 'godshield':
            if self.hasDoneGS:
                raise Spellerror
            if self.stamina < 100:
                raise NoStamina
            target = findtarget(self)
            self.stamina -= 100
            return (1/self.speed,self.godshield,self,target)
        elif nomduspell == 'attack':
            if self.stamina < self.att_cost:
                raise NoStamina
            target = findtarget(self)
            self.stamina -= self.att_cost
            return (1/self.speed,self.attack,self,target)
        else:
            raise Spellerror
        
    def classestr(self):
        return 'Mage Blanc '+self.name+' a '+str(self.hp)+' PV, et fait le bien autour de lui !'        
    
class barbare(joueur):
    classname = 'barbare'
    spike = 15
    dodge = 0
    basearmor = .2
    baseresistance = .15
    basead = 20
    att_cost = 30
    staminaMAX = 100
    pvMAX = 125
    basespeed = 75
    help = [('passif',0,'le barbare augmente passivement sa force s\'il est frappé'),
            ('attack',att_cost,'attaque de base('+str(att_cost)+' Endurance)'),
            ('all_in',40,'augmente l\'attaque au prix de la défense ')]
    def __init__(self, *args):
        super().__init__(*args)
        self.ad = self.basead
        self.armor = self.basearmor
        self.resistance = self.baseresistance
        self.crit = 0
        self.berzdmg = 0
        self.trigger.addDmg(self.berzerk)
    
    def classestr(self):
        return 'Barbare '+self.name+ ' a '+str(self.hp)+' PV, une hache et s\'énerve facilement'

    #augmenter son attaque pour 2 tours mais devient vulnérable
    def double_tranchant(self):
        if self.stamina < 40:
            return [('mess',self.name+' n\' a pas la force de se booster')]
        self.stamina -= 40
        self.ad += 10
        self.armor = -.25
        self.resistance = -.25
        self.trigger.remDmg(self.spikes)
        self.trigger.addTrRes(1,self.remboost)
        return [('mess',self.name+' prend une posture offensive mais risquée')]
    def remboost(self):
        self.ad = self.basead
        self.armor = self.basearmor
        self.resistance = self.baseresistance
        self.trigger.addDmg(self.spikes)
        return [('mess',self.name+' est de nouveau sur la défensive')]

    #passif: augmenter l'ad et le crit si frappé
    def berzerk(self,source,target,amount,dtype):
        if dtype != 'spike':
            self.berzdmg += 2.5
            self.crit += 7
            return amount,[('mess','la rage de '+self.name+' monte')]
    
    #attaque de base
    def attack(self,target):
        if not target.alive:
            return [('mess',self.name+' essaie de frapper '+target.name+' mais il est déjà mort')]
        if(self.stamina >= self.att_cost):
            self.stamina -= self.att_cost
        else:
            return [('mess', self.name+' n\' a pas la force d\'attaquer : Endurance à '+str(self.stamina))]
        rd = random.randint(1,100)
        if rd <= self.crit:
            return ([('mess', self.name + ' attaque '+ target.name + ' et effectue un critique !')] + 
                    self.attack_target(target,(self.ad+self.berzdmg)*2,'physique'))
        else :
            return [('mess', self.name + ' attaque '+ target.name )] + self.attack_target(target,self.ad+self.berzdmg,'physique')
    #lancer un sort
    def spell(self,nomduspell,fld):
        global F
        F = fld
        if nomduspell == 'attack':
            if self.stamina < self.att_cost :
                raise NoStamina
            target = findtarget(self)
            self.stamina -= self.att_cost
            return (1/self.speed,self.attack,self,target)
        elif nomduspell == 'all_in':
            if self.stamina <= 40:
                raise NoStamina
            self.stamina -= 40
            return (0,self.double_tranchant,self)
        else:
            raise Spellerror
        
class yolosaruken(joueur):
    classname = 'yolosaruken'
    spike = 0
    dodge = 10
    armor = .1
    resistance = .1
    ad = 5
    att_cost = 15
    staminaMAX = 100
    pvMAX = 100
    basespeed = 100
    help = [('attack',att_cost,'attaque de base('+str(att_cost)+' Endurance)'),
            ('healmate',100,'Soin de 100PV de soi et d\'un allié aléatoire'),
            ('exodia',100,'1 chance sur 1000 de one-shot un ennemi non insensible aux dégats'),
            ('DisciplesExodia',85,'Multiplie par 10 les chances du sort "Exodia"'),
            ('SurpriseMthrFcker',35,'Choisi une cible aléatoire et soit la soigne de 50 PV (50%) soit l\'attaque de 50 (50%)')]
    def __init__(self, *args):
        super().__init__(*args)
        self.exodia_multiplier = 0

    def classestr(self):
        return 'Le prêtre japonais '+self.name+ ' a '+str(self.hp)+' PV, et maîtrise le hasard à la perfection'

    def healmate(self):
        if(self.stamina >= 100):
            self.stamina -= 100
        else:
            return [('mess', self.name+' n\' a pas la force de soigner : Endurance à '+str(self.stamina))]

        self.hp += 100
        if self.hp > self.pvMAX :
            self.hp = self.pvMAX
        targetlist = [p for p in self.F.player if p.id != self.id and p.alive]
        if targetlist != []:
            targ = targetlist[random.randint(0,len(targetlist) - 1)]
            targ.hp += 100
            if targ.hp > targ.pvMAX:
                targ.hp = targ.pvMAX
            return [('mess', self.name+' s\'est soigné et a soigné '+targ.name+" au passage de 100 PV")]
        else:
            return [('mess', self.name+' s\'est soigné de 100 PV et n\'a pas trouvé d\'énemis à soigner ')]
    def suprisemothfcker(self):
        if(self.stamina >= 35):
            self.stamina -= 35
        else:
            return [('mess', self.name+' n\' a pas la force de surprendre : Endurance à '+str(self.stamina))]
        if random.randint(0,1) == 0:
            targetlist = [p for p in self.F.player if p.alive]
            targ = targetlist[random.randint(0,len(targetlist) - 1)]
            return [('mess','Le hasard pointe '+targ.name+' et il se fait attaquer par '+self.name)] + self.attack_target(targ,50,'magique')
        else:
            targetlist = [p for p in self.F.player if p.alive]
            targ = targetlist[random.randint(0,len(targetlist) - 1)]
            targ.hp += 50
            if targ.hp > targ.pvMAX:
                targ.hp = targ.pvMAX
            return [('mess','Le hasard pointe '+targ.name+' et il se fait soigner par '+self.name)]
    def exodia(self):
        if(self.stamina >= 100):
            self.stamina -= 100
        else:
            return [('mess', self.name+' n\' a pas la force d\'utiliser Exodia : Endurance à '+str(self.stamina))]
        if self.exodia_multiplier >= 3 :
            r = True
        else:
            r = (random.randint(0,(10**(3-self.exodia_multiplier))) == 0)
        if r:
            targetlist = [p for p in self.F.player if p.id != self.id and p.alive]
            if targetlist == []:
                return [('mess','Aucun ennemi n\'a pu être frappé')]
            targ = targetlist[random.randint(0,len(targetlist) - 1)]
            return [('mess',self.name+" déchaine la puissance du hasard et inflige des dégats inifinis à "+targ.name)] + self.attack_target(targ,9999999,'brut')
        else :
            return [("mess","La tentative de meurtre de "+self.name+" échoue lamentablement")]
    def membresExo(self):
        if(self.stamina >= 85):
            self.stamina -= 85
        else:
            return [('mess', self.name+' n\' a pas la force d\'appeler les membres d\'exodia : Endurance à '+str(self.stamina))]
        
        self.exodia_multiplier += 1
        if self.exodia_multiplier >= 3 :
            return [('mess',self.name+' peut maintenant executer des gens de façon certaine avec EXODIA')]
        else:
            return [('mess',self.name+' a maintenant une chance sur '+str( 10**(3-self.exodia_multiplier) )+' d\' executer des gens avec EXODIA')]

    def attack(self,target):
        if not target.alive:
            return [('mess',self.name+' essaie de frapper '+target.name+' mais il est déjà mort')]
        if(self.stamina >= self.att_cost):
            self.stamina -= self.att_cost
        else:
            return [('mess', self.name+' n\' a pas la force d\'attaquer : Endurance à '+str(self.stamina))]
        return [('mess', self.name + ' attaque '+ target.name )] + self.attack_target(target,self.ad,'physique')

    def spell(self,nomduspell,fld):
        global F
        F = fld
        if nomduspell == 'attack':
            if self.stamina < self.att_cost:
                raise NoStamina
            target = findtarget(self)
            self.stamina -= self.att_cost
            return (1/self.speed,self.attack,self,target)
        elif nomduspell == 'healmate':
            if self.stamina < 100:
                raise NoStamina
            self.stamina -= 100
            return (1/self.speed,self.healmate,self)
        elif nomduspell == 'exodia':
            if self.stamina < 100:
                raise NoStamina
            self.stamina -= 100
            return (1/self.speed,self.exodia,self)
        elif nomduspell == 'DisciplesExodia':
            if self.stamina < 85:
                raise NoStamina
            self.stamina -= 85
            return (1/self.speed,self.membresExo,self)
        elif nomduspell == 'SurpriseMthrFcker':
            if self.stamina < 35:
                raise NoStamina
            self.stamina -= 35
            return (1/self.speed,self.suprisemothfcker,self)
        else:
            raise Spellerror

class barde(joueur):
    classname = 'barde'
    spike = 0
    dodge = 10
    armor = .10
    resistance = .15
    ad = 25
    att_cost = 30
    staminaMAX = 100
    pvMAX = 110
    basespeed = 125

class mage_rouge(joueur):
    classname = 'mage rouge'
    spike = 0
    dodge = 0
    armor = 0
    resistance = .10
    ad = 50
    att_cost = 50
    staminaMAX = 100
    pvMAX = 100
    basespeed = 100
    
class lancier(joueur):
    classname = 'lancier'
    spike = 0
    dodge = 0
    armor = .20
    resistance = .10
    ad = 20
    att_cost = 30
    staminaMAX = 100
    pvMAX = 125
    basespeed = 60
    help = [('attack',att_cost,'attaque de base'),
            ('jump',40,'saute en l\'air et retombe au tour suivant sur la cible '),
            ('ProPecTorat',40,'Donne un bouclier qui protege d\'une attaque'),
            ('Passif',0,'Ensemble c\'est plus mieux : pv max + 50 si deux lanciers dans la partie')]
    def __init__(self, *args):
        super().__init__(*args)
        self.lastTurnJump = False
    def classestr(self):
        return 'Lancier '+self.name+' a '+str(self.hp)+' PV, une lance et saute très haut'
    
    #Attaque de base
    def attack(self,target):
        if not target.alive:
            return [('mess',self.name+' essaie de frapper '+target.name+' mais il est déjà mort')]
        if(self.stamina >= self.att_cost):
            self.stamina -= self.att_cost
        else:
            return [('mess', self.name+' n\' a pas la force d\'attaquer : Endurance à '+str(self.stamina))]
        return [('mess', self.name + ' attaque '+ target.name )] + self.attack_target(target,self.ad,'physique')

    #saut
    def jump(self,target):
        if self.lastTurnJump:
            return [('mess',self.name+' a encore essayé de sauter mais il n\'a pas pu')]
        if self.stamina < 40:
            return [('mess', self.name+' n\' a pas la force de sauter : Endurance à '+str(self.stamina))]
        self.jumptarget = target
        self.stamina -= 40
        self.lastTurnJump = True
        self.trigger.addT(self.jumping)
        self.trigger.addTrRes(0,self.turnland)
        self.trigger.addTrRes(1,self.canjump)
        return [('mess',self.name+' saute très haut')]
    def jumping(self,source,target,amount,dtype):
        return True,[('mess',self.name + ' est en l\'air et évite l\'attaque')]
    def turnland(self):
        self.trigger.remTrRes(self.turnland)
        return [('spell',(1/self.speed,self.land,self))]
    def land(self):
        self.trigger.remT(self.jumping)
        if not self.jumptarget.alive:
            return [('mess',self.name+' atterit sur '+self.jumptarget.name+' mais il est déjà mort')]
        return [('mess',self.name+' atterrit sur '+self.jumptarget.name)]+self.attack_target(self.jumptarget,self.ad*2,'physique')
    def canjump(self):
        self.lastTurnJump = False
        self.trigger.remTrRes(self.canjump)
        return []
    
    def ProPecTorat(self):
        if self.stamina < 40:
            return [('mess', self.name+' n\' a pas la force de se protéger : Endurance à '+str(self.stamina))]
        else:
            self.stamina -= 40
        self.trigger.addT(self.shielding)
        return [('mess',self.name+' bombe le torse et une barriere apparait autour de lui')]
    def shielding(self,source,target,amount,dtype):
        self.trigger.remT(self.shielding)
        return True,[('mess','La barriere de '+self.name + ' le protege de l\'attaque ! ')]
    
    def passif(self):
        return [('mess','Le passif n\'est pas activable')]
    
    #Override set_field pour le passif
    def set_field(self,fi):
        self.F = fi
        for pl in fi.player:
            if pl.id != self.id and pl.classname == 'lancier':
                self.pvMAX = 175
                self.hp = 175
                break
    
    def spell(self,nomduspell,fld):
        global F
        F = fld
        if nomduspell == 'attack':
            if self.stamina < self.att_cost :
                raise NoStamina
            target = findtarget(self)
            self.stamina -= self.att_cost
            return (1/self.speed,self.attack,self,target)
        elif nomduspell == 'ProPecTorat':
            if self.stamina < 40:
                raise NoStamina
            self.stamina -= 40
            return (0,self.ProPecTorat,self)
        elif nomduspell == 'jump':
            if self.lastTurnJump:
                raise Spellerror
            if self.stamina < 40 :
                raise NoStamina
            target = findtarget(self)
            self.stamina -= 40
            return (1/self.speed,self.jump,self,target)
        else:
            raise Spellerror

classes = [guerrier,ninja,mage_blanc,barbare,lancier,yolosaruken]
