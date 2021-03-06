import random

class Character:
    def __init__(self, attack = 0.0, deffence = 0.0, health = 0.0, hp = 0.0, mana = 0.0, stamina = 0.0, luck = 0.0, kind = "uknown", description = "..."):
        self.id = 0
        self.attack = attack
        self.deffence = deffence
        self.health = health
        self.hp = hp
        self.mana = mana
        self.stamina = stamina
        self.luck = luck
        self.kind = kind
        self.description = description


class Hero(Character):
    def __init__(self, attack, deffence, health, hp, mana, stamina, luck, kind, description = "..."):
        super().__init__(attack, deffence, health, hp, mana, stamina, luck, kind, description)

        self.lvl = 1
        self.exp = [0, 512]
        self.bag = {'money': 0}
        self.available_skillpoints = 0

    def lvlup(self, exp_points):
        self.exp[0] += exp_points
        if self.exp[0] >= self.exp[1]:
            self.lvl += 1
            self.available_skillpoints += 2
            self.exp[0] = self.exp[0] - self.exp[1]
            self.exp[1] = int(self.exp[1] * 1.5)
            return True
        else:
            return False

    def add_to_bag(self, loot, amount = None):
        if type(loot) == str and not amount == None:
            if loot in self.bag:
                self.bag[loot] = self.bag[loot] + amount
            else:
                self.bag[loot] = amount
        else:
            for item in loot:
                if item in self.bag:
                    self.bag[item] = self.bag[item] + loot[item]
                else:
                    self.bag[item] = loot[item]
        self.sort_bag()

    def remove_from_bag(self, item, amount = 1):
        self.bag.update({item: self.bag[item] - amount})
        self.sort_bag()

    def sort_bag(self):
        new_bag = {'money': self.bag['money']}
        sorted_bag = sorted(self.bag)
        for i in sorted_bag:
            if self.bag[i] != 0 and i != 'money':
                new_bag[i] = self.bag[i]
        self.bag = new_bag

class Creature(Character):
    def __init__(self, exp, attack, deffence, health, hp, mana, stamina, luck, kind, description = "..."):
        super().__init__(attack, deffence, health, hp, mana, stamina, luck, kind, description)

        self.possible_loot = []
        self.loot = {}
        self.exp = int((exp * 0.5) + (random.random() * exp))

    def add_to_loot(self, base_loot, luck):
        for loot in base_loot:
            item = loot['name']
            amount = loot['amount']
            rarity = loot['rarity']
            if (random.randint(1, 100) + luck) >= (rarity * 10 + 10):
                final_a = int((amount * 0.5) + (random.random() * amount))
                if final_a > 0:
                    self.loot[item] = final_a
