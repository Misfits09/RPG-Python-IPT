class joueur():
    alive = True
    spike = 0
    armor = 0
    ad = 0
    heal_points = 10
    att_cost = 30
    heal_cost = 70
    stamina = 100
    staminaMAX = 100
    pvMAX = 100

    F = None
    def __init__(self,i,stat): #stat = [ad,att_cost,heal_points,heal_cost,pvMAX,staminaMAX]
        self.hp = 100
        self.id,self.name = i,str(i)
        self.ad = add
    def set_field(self,fi):
        self.F = fi
    def restore_stamina(self):
        self.stamina = 100
    def take_damage(self, amount):
        self.hp -= amount*(1 - self.armor)
        if self.hp <= 0 :
            self.hp = 0
            return False
        return True
    def attack(self,cible):
        commList = []
        if(self.stamina >= self.att_cost):
            self.stamina -= self.att_cost
        else:
            return [('allOK', jName+' n\' a pas la force d\'attaquer : Endurance à '+str(self.stamina))]
        commList.append(('allOK',jName+' attaque '+cible.name+' !'))
        if not cible.take_damage(self.ad):  
            commList.append(self.F.isDead(cible))
            if(cible.spike != 0):
                commList.append(('allOK',self.name + ' évite les épines de '+cible.name+' en le tuant'))
        elif (cible.spike != 0 and self.take_damage(cible.spike)): # Argument après le 'and' ne se lance que si spike != 0
            commList.append(('allOK',self.name + ' a attaqué '+cible.name+' qui a maintenant '+cible.hp+' PV '+'\n'+' Mais s\'est fait mal en attaquant et a maintenant '+self.hp+' PV '))
        elif (cible.spike != 0): #donc self.take_damage(cible.spike) a renvoyé False
            commList.append(self.F.isDead(self))
        else:
            commList.append(('allOK',self.name + ' a attaqué '+cible.name+' qui a maintenant '+str(cible.hp)+' PV (sans se faire mal) '))
        commList.reverse()
        return commList
    def heal(self):
        if(self.stamina >= self.heal_cost):
            self.stamina -= self.heal_cost
        else:
            print('Vous n\'avez pas la force de vous soigner')
            return ['mess', jName+' n\a pas la force de se soigner : Endurance à '+str(self.stamina)]
        self.hp += self.heal_points
        if (self.hp > 100): 
            self.hp = 100
        print( 'Vous vous êtes soigné , vous avez '+str(self.hp)+' PV')
        return ['mess', jName+' s\'est soigné et a maintenant '+str(self.hp)+' PV']
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