#class of hole creatures


#***************************************
#*************** Klasy *****************
#***************************************

#postać szablon
class Character:
    def __init__(self, attack = 0.0, deffence = 0.0, health = 0.0, mana = 0.0, stamina = 0.0, luck = 0.0, kind = "uknown", description = "..."):
        self.id = 0
        self.attack = attack
        self.deffence = deffence
        self.health = health
        self.mana = mana
        self.stamina = stamina
        self.luck = luck
        self.kind = kind
        self.description = description
        self.hp = health


#Klasy postaci:
#Kłusownik
class Poacher(Character):
    def __init__(self):
        Character.__init__(self, 4.0, 3.0, 12.0, 0.0, 12.5, 3.0, "kłusownik", "Outsider przymuszony nędzą i głodem przemieżać pańszczyźniane bory uszczuplając gromady zajęcy i cietrzewii co nie umyka uwadze władzy...\n")

#Kmieć osiłek
class Serf(Character):
    def __init__(self):
        Character.__init__(self, 5.0, 6.0, 15.0, 0.0, 15.0, 1.0, "kmieć")

#Łotr
class Rascal(Character):
    def __init__(self):
        Character.__init__(self, 3.0, 1.0, 10.0, 0.0, 10.0, 7.5, "Łotr", "Rzezimieszek jakich mało, szabrując domy mieszkańców miasta i zagarniająć ich ostatnie srebrniki w końcu zajżałeś w nie te progi i zostałeś przyłapany przez herszta bandy który dokonując samosądu obcina ci prawą dłoń i zabrania przekraczać bram miasta skazując cię na wygnanie...\n")



#%%%%%%%%%%%%%%% Przeciwnicy %%%%%%%%%%%%%%%%%

#Pająk
class Spider(Character):
    def __init__(self):
        Character.__init__(self, 2.5, 1.0, 7.5, 0.0, 8.0, 1.0, "pająk")
