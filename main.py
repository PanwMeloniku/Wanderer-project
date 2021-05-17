#ścieżka do odpalenia bota:
#cd Desktop/UWR/SEMESTR 2/Bot_discord
#potem odpalasz nazwą pliku głównego
#python main.py


#linki fajne
#https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list
#https://stackoverflow.com/questions/59570301/how-can-i-make-my-discord-bot-respond-to-the-correct-answer
#https://pythonexamples.org/convert-python-class-object-to-json/
#https://www.writebots.com/discord-text-formatting/



# Imports
#import discord
import asyncio
from discord.ext import commands
import os
import random
import json
#własne pliki zewnętrzne
import save_and_insert_progress as saip
import Class
import combat
#import test

r_token = open("token.txt", "r")
TOKEN = r_token.readline()
r_token.close()

client = commands.Bot(command_prefix='!')



#***************************************
#********** Funkcje ogólne *************
#***************************************

def c_hp(player):
    return (f"{player.hp}/{player.health}")

def stats(player, new = False):
    newl = "\n"
    end = "```"
    stat_message = "```"
    stat_attack = "Atak: " + str(player.attack)
    stat_deffence = "Obrona: " + str(player.deffence)
    stat_health = "Życie: " + c_hp(player)
    stat_stamina = "Kondycja: " + str(player.stamina)
    stat_mana = "Moc: " + str(player.mana)
    stat_luck = "Szczęście: " + str(player.luck)

    if new:
        stat_message += player.kind + 2 * newl + player.description
    stat_message = stat_message + newl + 'Statystyki:' + newl + stat_attack + newl + stat_deffence + newl + stat_health + newl + stat_stamina + newl + stat_mana + newl + stat_luck + newl + end
    return stat_message

@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

#Sprawia że po napisaniu jakiejkolwiek wiadomości na serwerze pojawia się id tego użytkownika w terminalu
@client.event
async def on_message(message):
    print('Pisał '+str(message.author.id))
    #dba o to aby nie nadpisało tego co aktualnie robi domyślnie funkcja on_message
    await client.process_commands(message)

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
async def choose_ch(ctx, character_class):
    player_id = ctx.author.id
    class_dict = {
        'poacher': Class.Poacher(),
        'rascal': Class.Rascal(),
        'serf': Class.Serf(),
        'spider': Class.Spider()
    }
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
        new_hero = class_dict[character_class]
        new_hero.id = player_id
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
    players = [saip.data_unpacking(ctx.author.id), Class.Spider()]
    await ctx.send(f"Podczas podróży drogę zagrodził ci {players[1].kind}")
    await ctx.send(f"{players[0].kind}\t\t\t\t\t\t{players[1].kind}\n{c_hp(players[0])}\t\t\t\t\t\t{c_hp(players[1])}")

    text_turn = ["Twoja tura", "Tura przeciwnika"]
    whoose_turn = random.randint(0, 1)
    other_one = (whoose_turn + 1) % 2
    print("______")
    while not(combat.is_dead(players[other_one])):
        other_one = whoose_turn
        whoose_turn = (whoose_turn + 1) % 2

        await ctx.send(text_turn[whoose_turn])
        players[other_one], reaction_message = combat.attack_action(players[whoose_turn], players[other_one])
        await ctx.send(reaction_message)
        await asyncio.sleep(2)
        print("______")

    if combat.is_dead(players[other_one]) and players[other_one].id != players[0].id:
        await ctx.send(f"Wygrałeś\nZostało ci {c_hp(players[0])}")
    else:
        await ctx.send("Wąchasz kwiatki od spodu")
    saip.data_packing(players[0])

client.run(TOKEN)