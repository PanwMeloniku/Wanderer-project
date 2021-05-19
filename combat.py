import random

def attack_action(attacker, deffender):
    chance_for_damage = deffender.deffence * 100.0 / (attacker.attack + deffender.deffence) #%
    if random.randint(1, 100) >= chance_for_damage:
        RNG = random.randint(1, 100) + attacker.luck - deffender.luck
        if RNG <= 5.0:                                                                    #słaby cios
            if random.randint(0, 1) == 1:
                damage = attacker.attack / 2
                text = "Ledwo draśnięty\n"
            else:
                damage = 0.0
                text = "I tak tej części ciała nigdy nie używał\n"
        elif RNG >= 95.0:                                                                 #obrażenia krytyczne
            damage = 2 * attacker.attack
            text = "Krytyczne uderzenie\n"
        else:
            damage = attacker.attack * 3 / 4 + (attacker.attack * RNG / 200)              #zwykłe obrażenia
            text = ""
        damage = round(damage, 2)
        text += "zadane obrażenia: " + str(damage)
    else:
        damage = 0.0
        text = "Nie udało się przebić pancerza"
    deffender.hp -= damage
    deffender.hp = round(deffender.hp, 2)
    return deffender, text

def is_dead(player):
    if player.hp <= 0.0:
        return True
    else:
        return False