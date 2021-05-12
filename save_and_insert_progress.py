import json
import Class
import os

def data_packing(player):
    json_str = json.dumps(player.__dict__)
    #print(json_str)
    file_name = str(player.id)+'.json'
    with open('players/'+file_name, 'w') as character_save:
        json.dump(player.__dict__, character_save)
    del player

def get_stats(player):
    file_name = str(player)+'.json'
    if file_name in os.listdir('players/'):
        with open('players/'+file_name) as f:
            data = json.load(f)
        player_obj = Class.Character(data['attack'] ,data['deffence'] ,data['health'] ,data['mana'] ,data['stamina'] ,data['luck'] ,data['kind'] ,data['description'])
        player_obj.id = data['id']
        return player_obj
    else:
        print("nie znaleziono zapisu postępu osoby o numerze id: ", player)
        #return -1