import json
#import Class
import class2_0
import os


#Konwersja danych gracza na ciąg znaków dla JSONA i wyeksportowanie go do zewnętrznego pliku
def data_packing(player):
    #nazwa pliku
    file_name = str(player.id)+'.json'
    #tworzy w folderze players plik o powyższej nazwie. Jeśli już istnieje taki plik, nadpisuje go
    with open('players/'+file_name, 'w') as character_save:
        json.dump(player.__dict__, character_save)
    del player

#znajduje statystyki gracza o danym id, tworzy obiekt wypełniając jego danymi po czym go zwraca
def data_unpacking(person, file_path = 'players/'):
    file_name = str(person)+'.json'
    #sprawdza czy w folderze players znajduje się plik o nazwie file_name
    if file_name in os.listdir(file_path):
        with open(file_path + file_name) as f:
            #konwersja obiektu JSONowego na słownik Pythonowski
            data = json.load(f)
        #tworzenie obiektu przekazując do konstruktora pobrane dane
        if str(person).isdigit():
            player_obj = class2_0.Hero(data['attack'], data['deffence'], data['health'], data['hp'], data['mana'], data['stamina'], data['luck'], data['kind'], data['description'])
            player_obj.id = data['id']
            player_obj.lvl = data['lvl']
            player_obj.exp = data['exp']
            player_obj.available_skillpoints = data['available_skillpoints']
            player_obj.bag = data['bag']
        else:
            player_obj = class2_0.Creature(data['exp'], data['attack'] ,data['deffence'] ,data['health'] ,data['hp'] ,data['mana'] ,data['stamina'] ,data['luck'] ,data['kind'] ,data['description'])
            player_obj.possible_loot = data['loot']
        return player_obj
    else:
        print("nie znaleziono zapisu postępu osoby o numerze id: ", person)
        return -1

def player_list(player_name, player_id):
    #p_dict = {}
    with open('players/list_of_players.json') as file:
        p_dict = json.load(file)
    p_dict[player_name] = player_id
    with open("players/list_of_players.json", "w") as file:
        json.dump(p_dict, file)