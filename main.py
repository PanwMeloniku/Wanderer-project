# &&&&&&&&&&&&> Imports <&&&&&&&&&&&
#import discord
import asyncio
from discord.ext import commands
import os
import random
import json
#własne pliki zewnętrzne
import save_and_insert_progress as saip
import combat
import class2_0
#import test
import shop

#używane Emoji
#💖
#🍀
#🗡
#🏃
#✨
#🛡
#👍
#👎
#⛔

r_token = open("token.txt", "r")
TOKEN = r_token.readline()
r_token.close()

client = commands.Bot(command_prefix='!')

#***************************************
#********** Funkcje ogólne *************


assortment_list = shop.items_for_sell

def equal_spacing(list_of_words):
    the_longest = 0
    for words in list_of_words:
        space = len(words)
        if space > the_longest:
            the_longest = space
    new_list = []
    for words in list_of_words:
        spaces = len(words)
        while spaces < (the_longest + 2):
            words = words + ' '
            spaces += 1
        new_list.append(words)
    return new_list

def c_hp(amount, max_amount = None):
    if max_amount == None:
        return f"{amount}"
    else:
        return (f"{amount}/{max_amount}")

def i_points(emote, rightemote, stat, points, who_react, player_id):
  if str(emote) == rightemote:
    for who in who_react:
      if who.id == player_id:
        stat = stat + 1.0
        points -= 1
        break
  return stat, points

def stats(player, new = False):
    newl = '\n'
    end = "```"
    all_stats = ["```"]
    if new:
        all_stats.append(player.kind + 2 * newl + player.description)

    parameter = equal_spacing(["Atak:", "Obrona:", "Życie:", "Kondycja:", "Moc:", "Szczęście:", "Poziom:", "Progres:"])
    all_stats.append(parameter[0] + str(player.attack))
    all_stats.append(parameter[1] + str(player.deffence))
    all_stats.append(parameter[2] + c_hp(player.hp, player.health))
    all_stats.append(parameter[3] + str(player.stamina))
    all_stats.append(parameter[4] + str(player.mana))
    all_stats.append(parameter[5] + str(player.luck))
    all_stats.append(parameter[6] + str(player.lvl))
    all_stats.append(parameter[7] + c_hp(player.exp[0], player.exp[1]))
    all_stats.append(end)
    stat_message = newl.join(all_stats)
    return stat_message

@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

#Sprawia że po napisaniu jakiejkolwiek wiadomości na serwerze pojawia się id tego użytkownika w terminalu
'''@client.event
async def on_message(message):
    print('Pisał '+str(message.author.id))
    #dba o to aby nie nadpisało tego co aktualnie robi domyślnie funkcja on_message
    await client.process_commands(message)
'''

@client.command()
async def manual(ctx):
    with open("players/list_of_players.json") as p_l:
        players_l = json.load(p_l)
    if ctx.author.name in players_l:
        sentence = 'Lista dostępnych komend:\n\n**`!fight`** - wpisanie komendy skutkuje wyszukaniem przeciwnika (sterowanego przez komputer) i rozpoczęcie walki\n\n' \
                   '**`!shop`** - wyświetla dostępne rzeczy na sprzedaż\n\n**`!buy <nazwa_przedmiotu> <liczba_sztuk>`** - kup przedmiot(przy nie podaniu żadnej liczby przyjmuje domyślnie 1). Właściwe nazwy przedmiotu na sprzedaż podane są na prawo od przedmiotu w sklepie\n\n' \
                   '**`!sell <nazwa przemiotu> <liczba_sztuk>`** - sprzedaj przedmiot (przy nie podaniu żadnej liczby przyjmuje domyślnie 1). __Przedmiot w plecaku nie jest właściwą nazwą przedmiotu__ (aby sprawdzić właściwą nazwę przedmiotu wpisz !check <przedmiot>)\n\n' \
                   '**`!check <przedmiot>`** - nazwę wprowadasz tak jak piszę w ekwipunku (ze spacjami). Zwraca informację o przedmiocie (jego nazwę i opis)\n\n' \
                   '**`!use <nazwa_przedmiotu> <*liczba_sztuk>`** - zużywa przedmiot stosując jego efekty. *wartość opcjonalna, przy nie wpisaniu wartości przyjmuje domyślnie 1\n\n' \
                   '**`!sp_distribute`** - włącza aplet do rozdysponowania punktów umiejętności jeżeli się jakieś posiada. Punkty wydaje się klikając na reakcje reprezentującą umiejętność. Aby zużyć więcej niż jeden punkt na daną umiejętność należy poczekać aż wiadomość zniknię i pojawi się odświeżona\n\n' \
                   '**`!profile <*nazwa_gracza/id_gracza>`** - wyświetla profil gracza. *parametr opcjonalny pozwalający sprawdzić profile innych graczy (domyślnie przy nie podaniu nazwy wyświetli twój profil)\n\n' \
                   '**`!bag`** - wyświetla ekwipunek'
    else:
        sentence = 'Witaj w świecie lejącej się juchy, parszywych kreatur i brudnych trolów (na księżniczni zabrakło budżetu)\nJesteś początkującym? Możesz utworzyć Całkiem Nowiutką postać wpisując **`!newcharacter`**. Po utworzeniu postaci ta komenda wyświetli dostępne opcje.'
    await ctx.send(sentence)

@client.command()
async def newcharacter(ctx):
    poacher = saip.data_unpacking("poacher", "templates_characters/classes/")
    rascal = saip.data_unpacking("rascal", "templates_characters/classes/")
    serf = saip.data_unpacking("serf", "templates_characters/classes/")
    nc_choice = 'Wybierz klasę postaci którą będziesz przemieżał pustkowia i knieje\n'
    nc_choice2 = '\nAby wybrać klasę pisz **`!choose_class poacher/rascal/serf`** (wybierz jedno)'
    await ctx.send(nc_choice+"\n*poacher*\n"+stats(poacher, True)+"\n*rascal*\n"+stats(rascal, True)+"\n*serf*\n"+stats(serf, True)+nc_choice2)

@client.command()
async def sp_distribute(ctx):        #skillpoints distributing
    player = saip.data_unpacking(ctx.author.id)
    while player.available_skillpoints > 0:
        info = await ctx.send(f'Masz {player.available_skillpoints} punktów umiejętności do rozdysponowania. (jeśli nie chcesz już rozdawać punktów, kliknij ⛔')
        await info.add_reaction("⛔")
        msg = await ctx.send(f'Atak: {player.attack}🗡\nObrona: {player.deffence}🛡\nŻycie: {c_hp(player.hp, player.health)}💖\nMoc: {player.mana}✨\nKondycja: {player.stamina}🏃\nSzczęście: {player.luck}🍀')
        await msg.add_reaction("🗡")
        await msg.add_reaction("🛡")
        await msg.add_reaction("💖")
        await msg.add_reaction("✨")
        await msg.add_reaction("🏃")
        await msg.add_reaction("🍀")
        await asyncio.sleep(3)
        the_same_msg = await ctx.channel.fetch_message(msg.id)
        msg_reactions = the_same_msg.reactions
        for emotes in msg_reactions:
            who_react = await emotes.users().flatten()
            player.attack, player.available_skillpoints = i_points(emotes, "🗡", player.attack, player.available_skillpoints, who_react, player.id)

            if not player.available_skillpoints > 0: break
            player.deffence, player.available_skillpoints = i_points(emotes, "🛡", player.deffence, player.available_skillpoints, who_react, player.id)

            if not player.available_skillpoints > 0: break
            player.health, player.available_skillpoints = i_points(emotes, "💖", player.health, player.available_skillpoints, who_react, player.id)

            if not player.available_skillpoints > 0: break
            player.mana, player.available_skillpoints = i_points(emotes, "✨", player.mana, player.available_skillpoints, who_react, player.id)

            if not player.available_skillpoints > 0: break
            player.stamina, player.available_skillpoints = i_points(emotes, "🏃", player.stamina, player.available_skillpoints, who_react, player.id)

            if not player.available_skillpoints > 0: break
            player.luck, player.available_skillpoints = i_points(emotes, "🍀", player.luck, player.available_skillpoints, who_react, player.id)

            if not player.available_skillpoints > 0: break
        emoji_info = await ctx.channel.fetch_message(info.id)
        emoji_info = emoji_info.reactions
        cancel = False
        for e in emoji_info:
            who_react = await e.users().flatten()
            if str(e) == "⛔":
                for who in who_react:
                    if who.id == player.id:
                        cancel = True
                        break
        await info.delete()
        await msg.delete()
        if cancel:
            break
    saip.data_packing(player)

@client.command()
async def choose_class(ctx, character_class):
    player_id = ctx.author.id
    class_dict = {}
    for template in os.listdir('templates_characters/classes/'):
        class_dict[template[0:-5]] = template

    yes_emote = False

    exist = str(player_id)+'.json' in os.listdir('players/')
    if exist:
        msg = await ctx.send(
            'Posiadasz już postać, jesteś pewien, że chcesz stworzyć nową? (!!Usunie to poprzednią postać wraz z jej postępem!!)\nZdecyduj wybierając reakcje pod tą wiadomością')
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await asyncio.sleep(10)
        the_same_msg = await ctx.channel.fetch_message(msg.id)
        msg_reactions = the_same_msg.reactions
        for emotes in msg_reactions:
            who_react = await emotes.users().flatten()
            if str(emotes) == "👍":
                for who in who_react:
                    if who.id == player_id:
                        yes_emote = True
                        break
                break
    if not(exist) or exist and yes_emote:
        with open("templates_characters/classes/" + class_dict[character_class]) as d:
            s = json.load(d)
        new_hero = class2_0.Hero(s['attack'], s['deffence'], s['health'], s['hp'], s['mana'], s['stamina'], s['luck'], s['kind'], s['description'])
        new_hero.id = player_id
        new_hero.aviable_skillpoints = 0
        saip.data_packing(new_hero)
        saip.player_list(ctx.author.name, ctx.author.id)
        msg2 = "Pomyślnie utworzono nową postać. Jej statystyki to:\n\n"
        msg2 += stats(new_hero, True)
    else:
        msg2 = "Nie dokonano zmian"
    await ctx.send(msg2)


@client.command()
async def profile(ctx, player_id = ""):
    if player_id == "":
        player_id = ctx.author.id
    if not str(player_id).isdigit():
        with open("players/list_of_players.json") as file:
            player_dict = json.load(file)
        if player_id in player_dict:
            player_id = player_dict[player_id]
        else:
            await ctx.send("Nie ma w bazie użytkownika o takim Nicku")
    player = saip.data_unpacking(player_id)
    await ctx.send(stats(player))

@client.command()
async def bag(ctx):
    player = saip.data_unpacking(ctx.author.id)
    backpack = ["```Plecak:"]
    newline = "\n"
    items = []
    amounts = []
    for elem in player.bag:
        with open("items/" + elem + ".json") as d:
            data = json.load(d)
        items.append("\t" + data["name"] + ":")
        amounts.append(player.bag[elem])
    items = equal_spacing(items)
    for i in range(len(items)):
        backpack.append(items[i] + str(amounts[i]))
    backpack.append("```")
    backpack = newline.join(backpack)
    await ctx.send(backpack)

@client.command()
async def check(ctx, item, i2 = "", i3 = ""):
    if i2 != "":
        item = item + " " + i2
        if i3 != "":
            item = item + " " + i3
    msg = "Nie ma takiego przedmiotu"
    for items in os.listdir('items/'):
        with open('items/' + items) as d:
            data = json.load(d)
        if data['name'] == item:
            msg = f"```{data['name']}\n\nNazwa przedmiotu: {items[:-5]}\nOpis:\n{data['description']}```"
            break
    await ctx.send(msg)

@client.command()
async def fight(ctx):
    enemies = []
    for enemy in os.listdir("templates_characters/enemies/"):
        enemies.append(enemy[:-5])
    random_enemy = random.randint(0, len(enemies) - 1)
    players = [saip.data_unpacking(ctx.author.id), saip.data_unpacking(enemies[random_enemy], 'templates_characters/enemies/')]
    players[1].add_to_loot(players[1].possible_loot, players[0].luck)
    await ctx.send(f"Podczas podróży drogę zagrodził ci {players[1].kind}")
    await ctx.send(f"{players[0].kind}\t\t\t\t\t\t{players[1].kind}\n{c_hp(players[0].hp, players[0].health)}\t\t\t\t\t\t{c_hp(players[1].hp, players[1].health)}")

    text_turn = ["\n**Twoja tura**", "\n**Tura przeciwnika**"]
    whoose_turn = random.randint(0, 1)
    other_one = (whoose_turn + 1) % 2
    while not(combat.is_dead(players[other_one])):
        other_one = whoose_turn
        whoose_turn = (whoose_turn + 1) % 2

        await ctx.send(text_turn[whoose_turn])
        players[other_one], reaction_message = combat.attack_action(players[whoose_turn], players[other_one])
        await ctx.send(reaction_message)
        await asyncio.sleep(2)
    if combat.is_dead(players[other_one]) and players[other_one].id != players[0].id:
        await ctx.send(f"'\n\nWygrałeś\nZostało ci {c_hp(players[0].hp, players[0].health)}\nZdobyłeś {players[1].exp} punktów doświadczenia")
        if len(players[1].loot) > 0:
            rewards_msg = ["oraz:"]
            for item in players[1].loot:
                with open("items/" + item + ".json") as d:
                    data = json.load(d)
                rewards_msg.append(f"{data['name']} {players[1].loot[item]}")
            nl = "\n"

            await ctx.send(nl.join(rewards_msg))
        players[0].add_to_bag(players[1].loot)
        players[0].lvlup(players[1].exp)
    else:
        await ctx.send("Wąchasz kwiatki od spodu. Udaj się do sklepu po miksture życia aby przywrócić siły witalne")
    players[0].hp = round(players[0].hp, 2)
    saip.data_packing(players[0])

@client.command()
async def shop(ctx):
    items = ["nazwa"]
    pl_name = ["przedmiot"]
    cost = ["cena"]
    for i in assortment_list:
        items.append(i)
        pl_name.append(assortment_list[i]["name"])
        cost.append(str(int(assortment_list[i]["worth"] * 1.25)))
    name_items = equal_spacing(items)
    equal_pl_name = equal_spacing(pl_name)
    text = "```Dostępne przedmioty na sprzedaż:\n"
    for i in range(0, len(name_items)):
        text = text + equal_pl_name[i] + name_items[i] + cost[i] + "\n"
    text += "```"
    await ctx.send(text)

@client.command()
async def buy(ctx, item, amount = 1):
    player = saip.data_unpacking(ctx.author.id)
    if item in assortment_list:
        cost = int(assortment_list[item]["worth"] * 1.25 * amount)
        if cost <= player.bag["money"]:
            msg = await ctx.send(f'Czy na pewno chcesz kupić {amount} {assortment_list[item]["name"]} o koszcie {cost}? Twój budżet wynosi {player.bag["money"]}')
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
            await asyncio.sleep(6)
            emoji_info = await ctx.channel.fetch_message(msg.id)
            emoji_info = emoji_info.reactions
            cancel = True
            for e in emoji_info:
                who_react = await e.users().flatten()
                if str(e) == "👍":
                    for who in who_react:
                        if who.id == player.id:
                            player.remove_from_bag("money", cost)
                            player.add_to_bag(item, amount)
                            await ctx.send(f'Pomyślnie zakupiono {amount} {assortment_list[item]["name"]}')
                            cancel = False
                            break
            if cancel:
                await ctx.send("Anulowano zakup")
        else:
            await ctx.send("Nie posiadasz wystarczającej liczby pieniędzy")
    else:
        await ctx.send("Nie można kupić takiego przedmiotu")
    saip.data_packing(player)

@client.command()
async def sell(ctx, item, amount = 1):
    player = saip.data_unpacking(ctx.author.id)
    if item in player.bag:
        if amount <= player.bag[item]:
            with open("items/"+item+".json") as d:
                data = json.load(d)
            cost = int(data["worth"] * 0.75 * amount)
            msg = await ctx.send(f'Czy na pewno chcesz sprzedać {amount} {data["name"]} o koszcie {cost}?')
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
            await asyncio.sleep(6)
            emoji_info = await ctx.channel.fetch_message(msg.id)
            emoji_info = emoji_info.reactions
            cancel = True
            for e in emoji_info:
                who_react = await e.users().flatten()
                if str(e) == "👍":
                    for who in who_react:
                        if who.id == player.id:
                            player.remove_from_bag(item, amount)
                            player.add_to_bag("money", cost)
                            await ctx.send(f'Pomyślnie sprzedano {amount} {data["name"]}')
                            cancel = False
                            break
                    break
            if cancel:
                await ctx.send("Anulowano sprzedaż")
        else:
            await ctx.send(f'Posiadasz tylko {player.bag[item]} sztuk')
    else:
        await ctx.send("Nie masz takiego przedmiotu")
    saip.data_packing(player)

@client.command()
async def use(ctx, item, amount = 1):
    player = saip.data_unpacking(ctx.author.id)
    if item in player.bag:
        if amount <= player.bag[item]:
            with open("items/"+item+".json") as d:
                data = json.load(d)
            for i in data["effects"]:
                setattr(player, i, getattr(player, i) + amount * data["effects"][i])
                if i == "hp":
                    if player.hp > player.health:
                        player.hp = player.health
                    else:
                        player.hp = round(player.hp, 2)
            player.remove_from_bag(item, amount)
            await ctx.send(f'Zużyto {amount} razy {data["name"]}')
        else:
            await ctx.send(f'Posiadasz tylko {player.bag[item]} sztuk')
    else:
        await ctx.send("Nie masz takiego przedmiotu")
    saip.data_packing(player)

client.run(TOKEN)