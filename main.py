#ścieżka do odpalenia bota:
#cd Desktop/UWR/SEMESTR 2/Bot_discord
#potem odpalasz nazwą pliku głównego
#python main.py


#linki fajne
#https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list
#https://stackoverflow.com/questions/59570301/how-can-i-make-my-discord-bot-respond-to-the-correct-answer
#https://stackoverflow.com/questions/3253966/python-string-to-attribute
#https://pythonexamples.org/convert-python-class-object-to-json/
#https://www.writebots.com/discord-text-formatting/
#do Znajdywania Emoji
#https://unicode.org/emoji/charts/full-emoji-list.html#1f496



# Imports
#import discord
import asyncio
from discord.ext import commands
import os
import random
import json
#własne pliki zewnętrzne
import save_and_insert_progress as saip
from museum import Class
import combat
import class2_0
#import test

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
    parameter = equal_spacing(["Atak:", "Obrona:", "Życie:", "Kondycja:", "Moc:", "Szczęście:", "Poziom:", "Progres:"])
    all_stats.append(parameter[0] + str(player.attack))
    all_stats.append(parameter[1] + str(player.deffence))
    all_stats.append(parameter[2] + c_hp(player.hp, player.health))
    all_stats.append(parameter[3] + str(player.stamina))
    all_stats.append(parameter[4] + str(player.mana))
    all_stats.append(parameter[5] + str(player.luck))
    all_stats.append(parameter[6] + str(player.lvl))
    all_stats.append(parameter[7] + c_hp(player.exp[0], player.exp[1]))
    if new:
        all_stats.append(player.kind + 2 * newl + player.description)
    else:
        all_stats.append("\nPlecak:")
        for elem in player.bag:
            all_stats.append(f'\t{elem}: {player.bag[elem]}')
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
async def helloworld(ctx, lang = ""):
    if lang == "":
        await ctx.send('Hello World!')
    else:
        if lang == "pl":
            await ctx.send('Witaj świecie!')
        elif lang == "de":
            await ctx.send('Hallo Welt!')



@client.command()
async def manual(ctx):
    powitanie = 'Witaj w świecie lejącej się juchy, parszywych kreatur i brudnych trolów (na księżniczni zabrakło budżetu)\n'
    m_new = 'Jesteś początkującym? Możesz utworzyć Całkiem Nowiutką postać wpisując **`!newcharacter`**'
    await ctx.send(powitanie + m_new)

@client.command()
async def newcharacter(ctx):
    poacher = Class.Poacher()
    rascal = Class.Rascal()
    serf = Class.Serf()
    nc_choice = 'Wybierz klasę postaci którą będziesz przemieżał pustkowia i knieje\n'
    nc_choice2 = '\nAby wybrać klasę pisz **`!choose_ch poacher/rascal/serf`** (wybierz jedno)'
    await ctx.send(nc_choice+stats(poacher, True)+stats(rascal, True)+stats(serf, True)+nc_choice2)

@client.command()
async def sp_distribut(ctx):        #skillpoints distributing
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
                    if who.id == 448140125394829312:
                        cancel = True
                        break
        await info.delete()
        await msg.delete()
        if cancel:
            break
    saip.data_packing(player)

@client.command()
async def choose_ch(ctx, character_class):
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
    hero = saip.data_unpacking(player_id)
    await ctx.send(str(hero.attack))


@client.command()
async def statystyki(ctx, player_id):
    if not player_id.isdigit():
        with open("players/list_of_players.json") as file:
            player_dict = json.load(file)
        if player_id in player_dict:
            player_id = player_dict[player_id]
        else:
            await ctx.send("Nie ma w bazie użytkownika o takim Nicku")
    player = saip.data_unpacking(player_id)
    await ctx.send(stats(player))

#-------!!>>Tu skończyłeś, miałeś rozkmine co do walki jak ma przebiegać [bot działa]<<!!----------
@client.command()
async def fight(ctx):
    players = [saip.data_unpacking(ctx.author.id), saip.data_unpacking('spider', 'templates_characters/enemies/')]
    players[1].add_to_loot(players[1].possible_loot, players[0].luck)
    await ctx.send(f"Podczas podróży drogę zagrodził ci {players[1].kind}")
    await ctx.send(f"{players[0].kind}\t\t\t\t\t\t{players[1].kind}\n{c_hp(players[0].hp, players[0].health)}\t\t\t\t\t\t{c_hp(players[1].hp, players[1].health)}")

    text_turn = ["Twoja tura", "Tura przeciwnika"]
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
        await ctx.send(f"Wygrałeś\nZostało ci {c_hp(players[0].hp, players[0].health)}")
        players[0].add_to_bag(players[1].loot)
        players[0].lvlup(players[1].exp)
        await ctx.send(stats(players[0]))
    else:
        await ctx.send("Wąchasz kwiatki od spodu")
    saip.data_packing(players[0])

client.run(TOKEN)