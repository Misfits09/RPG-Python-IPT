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
                return pl
        if (not plFound):
            print('\n  Aucun joueur avec ce nom n\' a ete trouvé ou alors il est déjà mort')

class classe():
    def ___init__(self,joueur):
        self.player = joueur
        
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
    onturnresolve = []
    def addonturnresolve(self,function):
        self.onturnresolve.append(function)
    def removeonturnresolve(self,function):
        self.onturnresolve.remove(function)
    def new_turn(self): #appelée à chaque début de tour du joueur
        for fct in onturnresolve:
            fct(self)

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
        for fct in target.onturnremove:
            try : 
                a,b = fct(self,target,amount,dtype)
                if a :
                    do_attk = False
                commlist += b
            except : pass
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
                a,b = fct(self,target,amount,dtype)
                amount = a
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
        elif dtype == 'magique :
            self.hp -= amount*(1 - self.resistance)
        else :
            self.hp -= amount
        if self.hp <= 0 :
            self.hp = 0
            return [self.player.F.isDead(self.player)]
        return commlist + [('mess',self.player.name+' a maintenant '+str(self.hp)+' PV')]

class guerrier(classe):
    name = 'guerrier'
    spike = 10
    armor = .25
    ad = 25
    heal_points = 40
    att_cost = 30
    heal_cost = 70
    staminaMAX = 100
    pvMAX = 150
    speed = 50
    hp = pvMAX
    stamina = staminaMAX
    
    #bloquer la prochaine attaque

    def block(self): #dmgtrigger sur soit même
        if self.stamina < 40 :
            return [('mess', self.player.name+' n\'a pas la force de bloquer : Endurance à '+str(self.stamina))]
        self.stamina = 0
        self.adddmgtrigger(self.blocking)
        return [('mess', self.player.name+' se prépare à bloquer')]
    def blocking(self,source,target,amount,dtype):
        if dtype == 'physique':
            self.removedmgtrigger(self.blocking)
            return amount/2,[('mess',self.player.name+' bloque l\'attaque')]
    
    #prendre une attaque à la place de la cible
    
    def protect (self): #targettrigger sur une cible
        pl = findtarget()
        pl.classe.addtargettrigger(self.protection)
        return [('mess',self.player.name+' protège '+pl.name)]
    def protection(self,source,target,amount,dtype):
        if dtype == 'physique':
            target.removetargettrigger(self.protection)
            return True,([('mess',self.player.name+' bloque le coup')] + source.hit_attack(self,amount,dtype))
    def spell (self,nomduspell):
        return {'block':self.block , 'protect':self.protect}[nomduspell]()
    
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
    armor = 0
    ad = 40
    heal_points = 15
    att_cost = 25
    heal_cost = 50
    staminaMAX = 100
    pvMAX = 85
    speed = 150
    hp = pvMAX
    stamina = staminaMAX

    #Se cacher pendant un tour (si dtype != zone)
    def hide(self): #Se retire au bout d'un tour
        if self.stamina < 40 :
            return [('mess', self.player.name+' n\'a pas la force de se cacher : Endurance à '+str(self.stamina))]
        elif self.lastTurnHide :
            return [('mess', self.player.name+' a encore voulu se cacher '+str(self.stamina))]
        self.stamina = 0
        self.addonturnremove(self.hiding)
        self.lastTurnHide = True
        return [('mess', self.player.name+' est caché ! Mon dieu... où est-il passé ?!')]
    def hiding(self,target,amount,dtype):
        if(dtype != 'zone'):
            return True,['mess',self.player.name + ' est trop bien caché et l\'attaque part dans le vent...']
    

    
class mage_noir(classe):
    name = 'mage noir'
    spike = 0
    armor = 0
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
    armor = .25
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
    armor = .15
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
    armor = 0
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
    armor = .10
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
    armor = 0
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
    armor = .20
    ad = 40
    heal_points = 10
    att_cost = 30
    heal_cost = 70
    staminaMAX = 100
    pvMAX = 125
    speed = 60
    hp = pvMAX
    stamina = staminaMAX
    
