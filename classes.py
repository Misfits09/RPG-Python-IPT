class joueur():
    alive = True
    F = None
    def __init__(self,i): #stat = [ad,att_cost,heal_points,heal_cost,pvMAX,staminaMAX]
        self.id,self.name = i,str(i)
    def set_field(self,fi):
        self.F = fi
    def set_classe(self,nomclasse):
        for i in self.classes:
            if i.name == nomclasse:
                self.classe = i(self)
    def restore_stamina(self):
        self.classe.stamina = self.classe.staminaMAX
    def __str__(self):
        if self.alive:
            return str(self.name) + " à " + str(self.hp) + "PV et fait "+str(self.ad)+" de dégats"
        else:
            return str(self.name) + " est mort"
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

# DEFINITION DES CLASSES #
def findtarget():
    global F
    while 1:
        name = str(input('nom de la cible'))
        plFound = False
        for pl in F.player:
            if(pl.name.casefold().strip() == name and pl.alive):
                plFound = True
                print('\n  Vous ciblez '+pl.name)
                return pl.class
        if (not plFound):
            print('\n  Aucun joueur avec ce nom n\' a ete trouvé ou alors il est déjà mort')

class classe():
    def ___init__(self,joueur):
        self.player = joueur
        self.adddmgtrigger(self.spikes)
        self.addtargettrigger(self.dodge)
        
    targettrigger = []
    def addtargettrigger(self,function):
        self.targettrigger.append(function)
    def removetargettrigger(self,function):
        self.targettrigger.remove(function)
    
    dmgtrigger = []
    def adddmgtrigger(self,function):
        self.dmgtrigger.append(function)
    def removedmgtrigger(self,function):
        self.dmgtrigger.remove(function)
    
    inittrigger = []
    def addinittrigger(self,function):
        self.inittrigger.append(function)
    def removeinittrigger(self,function):
        self.inittrigger.remove(function)
    
    hittrigger = []
    def addhittrigger(self,function):
        self.hittrigger.append(function)
    def removehittrigger(self,function):
        self.hittrigger.remove(function)
    
    onturnresolve = []
    def addonturnresolve(self,function):
        self.onturnresolve.append(function)
    def removeonturnresolve(self,function):
        self.onturnresolve.remove(function)
    
    #appelée à chaque début de tour du joueur
    def new_turn(self): 
        commlist = []
        for fct in onturnresolve:
            commlist += fct(self)
        return commlist
    
    #ciblage d'attaque
    def attack_target(self,target,amount,dtype):
        commlist = []
        do_attk = True
        for fct in self.inittrigger:
            try : 
                a,b = fct(self,amount,dtype)
                if a :
                    do_attk = False
                commlist += b
            except : pass
        if not do_attk:
            return commlist
        for fct in target.targettrigger:
            try : 
                a,b = fct(self,target,amount,dtype)
                if a :
                    do_attk = False
                commlist += b
            except : pass
        if do_attk:
            return commlist + self.hit_attack(target,amount,dtype)
        else :
            return commlist
    
    #application dégâts
    def hit_attack(self,target,amount,dtype):
        commlist = []
        for fct in self.hittrigger:
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
        for fct in self.dmgtrigger:
            try : 
                a,b = fct(source,self,amount,dtype)
                amount = a
                commlist += b
            except : pass
        if dtype == 'physique':    
            self.hp -= amount*(1 - self.armor)
        elif dtype == 'magique' :
            self.hp -= amount*(1 - self.resistance)
        else :
            self.hp -= amount
        if self.hp <= 0 :
            self.hp = 0
            return [self.player.F.isDead(self.player)]
        return commlist + [('mess',self.player.name+' a maintenant '+str(self.hp)+' PV')]
    
    #dégâts d'épine
    def spikes(self,source,target,amount,dtype):
        if dtype == 'physique':
            return [('mess',source.player.name+' se blesse en attaquant')] +source.take_damage(self,self.spike,'physique')
    
    #esquive
    def dodge(self,source,target,amount,dtype):
        rd = random.randint(1,100)
        if rd <= self.dodge:
            return True,[('mess',self.player.name+' a esquivé l\'attaque')]

class guerrier(classe):
    name = 'guerrier'
    spike = 10
    dodge = 0
    armor = .25
    resistance = .10
    ad = 25
    heal_points = 40
    att_cost = 30
    heal_cost = 70
    staminaMAX = 100
    pvMAX = 150
    speed = 50
    hp = pvMAX
    stamina = staminaMAX
    help = [('block','réduit les dégâts physiques pendant un tour (40 Endurance)'),
            ('protect','encaisse la prochaine attaque à la place de la cible (40 Endurance)'),
            ('attack','attaque de base ('+str(att_cost)+' Endurance)')]
    
    #bloquer la prochaine attaque
    def block(self):
        if self.stamina < 40 :
            return [('mess', self.player.name+' n\'a pas la force de bloquer : Endurance à '+str(self.stamina))]
        self.stamina = 0
        self.adddmgtrigger(self.blocking)
        self.addonturnresolve(self.removeblocking)
        return [('mess', self.player.name+' se prépare à bloquer')]
    def blocking(self,source,target,amount,dtype):
        if dtype == 'physique':
            return amount/2,[('mess',self.player.name+' bloque l\'attaque')]
    def removeblocking(self):
        self.removedmgtrigger(self.blocking)
        self.removeonturnresolve(self.removeblocking)
    
    #prendre une attaque à la place de la cible
    def protect (self):
        if self.stamina < 40 :
            return [('mess', self.player.name+' n\'a pas la force de protéger : Endurance à '+str(self.stamina))]
        self.stamina -= 40
        pl = findtarget()
        pl.addtargettrigger(self.protection)
        return [('mess',self.player.name+' protège '+pl.name)]
    def protection(self,source,target,amount,dtype):
        if dtype == 'physique':
            target.removetargettrigger(self.protection)
            return True,([('mess',self.player.name+' bloque le coup')] + source.hit_attack(self,amount,dtype))
    
    #lancer un sort
    def spell (self,nomduspell):
        return {'block':self.block , 'protect':self.protect , 'attaque':self.attack}[nomduspell]()
    
    #attaque de base
    def attack(self):
        if(self.stamina >= self.att_cost):
            self.stamina -= self.att_cost
        else:
            return [('mess', self.player.name+' n\' a pas la force d\'attaquer : Endurance à '+str(self.stamina))]
        target = findtarget()
        return self.attack_target(target,self.ad,'physique')
    
class ninja(classe):
    name = 'ninja'
    spike = 0
    dodge = 20
    armor = 0
    resistance = 0
    ad = 40
    heal_points = 15
    att_cost = 25
    heal_cost = 50
    staminaMAX = 100
    pvMAX = 85
    speed = 150
    hp = pvMAX
    stamina = staminaMAX
    help = [('hide', 'Se cache pendant un tour et ne peut plus attaquer (40 Endurance)'),('attack','Attaque physique de base ('+str(att_cost))+' Endurance)']
    lastTurnHide = False

    #Se cacher pendant un tour (si dtype != zone)
    def hide(self): #Se retire au bout d'un tour
        if self.stamina < 40 :
            return [('mess', self.player.name+' n\'a pas la force de se cacher : Endurance à '+str(self.stamina))]
        elif self.lastTurnHide :
            return [('mess', self.player.name+' a encore voulu se cacher mais n\'a pas pu')]
        self.stamina = 0
        self.addtargettrigger(self.hiding)
        self.addonturnresolve(self.endHiding)
        return [('mess', self.player.name+' est caché ! Mon dieu... où est-il passé ?!')]
    def hiding(self,target,amount,dtype):
        return True,['mess',self.player.name + ' est trop bien caché et l\'attaque part dans le vent...']
    def canHide(self):
        self.lastTurnHide = False
        return []
    def endHiding(self):
        self.lastTurnHide = True
        self.removeonturnresolve(self.endHiding)
        self.removetargettrigger(self.hiding)
        self.addonturnresolve(self.canHide)
        return ['mess', self.player.name + ' est sorti de sa cachette']


    def attack(self):
        if(self.stamina >= self.att_cost):
            self.stamina -= self.att_cost
        else:
            return [('mess', self.player.name+' n\' a pas la force d\'attaquer : Endurance à '+str(self.stamina))]
        target = findtarget()
        return [('mess', self.player.name + ' attaque '+ target.player.name )] + self.attack_target(target,self.ad,'physique')
    def spell (self,nomduspell):
        return {'hide':self.hide , 'attack':self.attack}[nomduspell]()
    
class mage_noir(classe):
    name = 'mage noir'
    spike = 0
    dodge = 0
    armor = 0
    resistance = .20
    ad = 60
    heal_points = 10
    att_cost = 50
    heal_cost = 50
    staminaMAX = 100
    pvMAX = 100
    speed = 95
    hp = pvMAX
    stamina = staminaMAX

class mage_blanc(classe):
    name = 'mage blanc'
    spike = 0
    dodge = 0
    armor = .25
    resistance = .30
    ad = 30
    heal_points = 40
    att_cost = 30
    heal_cost = 30
    staminaMAX = 100
    pvMAX = 100
    speed = 115
    hp = pvMAX
    stamina = staminaMAX
    
class barbare(classe):
    name = 'barbare'
    spike = 15
    dodge = 0
    armor = .15
    resistance = 0
    ad = 35
    heal_points = 10
    att_cost = 30
    heal_cost = 70
    staminaMAX = 100
    pvMAX = 125
    speed = 75
    hp = pvMAX
    stamina = staminaMAX

class freelance(classe):
    name = 'freelance'
    spike = 0
    dodge = 10
    armor = .1
    resistance = .1
    ad = 30
    heal_points = 30
    att_cost = 30
    heal_cost = 50
    staminaMAX = 100
    pvMAX = 100
    speed = 100
    hp = pvMAX
    stamina = staminaMAX

class barde(classe):
    name = 'barde'
    spike = 0
    dodge = 10
    armor = .10
    resistance = .15
    ad = 25
    heal_points = 20
    att_cost = 30
    heal_cost = 40
    staminaMAX = 100
    pvMAX = 110
    speed = 125
    hp = pvMAX
    stamina = staminaMAX

class mage_rouge(classe):
    name = 'mage rouge'
    spike = 0
    dodge = 0
    armor = 0
    resistance = .10
    ad = 50
    heal_points = 30
    att_cost = 50
    heal_cost = 30
    staminaMAX = 100
    pvMAX = 100
    speed = 100
    hp = pvMAX
    stamina = staminaMAX
    
class lancier(classe):
    name = 'lancier'
    spike = 0
    dodge = 0
    armor = .20
    resistance = .10
    ad = 40
    heal_points = 10
    att_cost = 30
    heal_cost = 70
    staminaMAX = 100
    pvMAX = 125
    speed = 60
    hp = pvMAX
    stamina = staminaMAX
    
