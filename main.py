#ścieżka do odpalenia bota:
#cd Desktop/UWR/SEMESTR 2/Bot_discord
#potem odpalasz nazwą pliku głównego
#python main.py


#linki fajne
#https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list
#https://stackoverflow.com/questions/59570301/how-can-i-make-my-discord-bot-respond-to-the-correct-answer
#https://pythonexamples.org/convert-python-class-object-to-json/



# Imports
import discord
import asyncio
import Class
from discord.ext import commands
import save_and_insert_progress as saip
import os

r_token = open("token.txt", "r")
TOKEN = r_token.readline()
r_token.close()

client = commands.Bot(command_prefix='!')
gracze = []



#***************************************
#********** Funkcje ogólne *************
#***************************************

def stats(name, new = False):
    newl = "\n"
    end = "```"
    stat_message = "```"
    stat_attack = "Atak: " + str(name.attack)
    stat_deffence = "Obrona: " + str(name.deffence)
    stat_health = "Życie: " + str(name.health)
    stat_stamina = "Kondycja: " + str(name.stamina)
    stat_mana = "Moc: " + str(name.mana)
    stat_luck = "Szczęście: " + str(name.luck)

    if new:
        stat_message += name.kind + 2 * newl + name.description
    stat_message = stat_message + newl + 'Statystyki:' + newl + stat_attack + newl + stat_deffence + newl + stat_health + newl + stat_stamina + newl + stat_mana + newl + stat_luck + newl + end
    return stat_message


def fight_round(player1, player2, whoose_turn):
    players = [player1, player2]
   #""" if players[whoose_turn].id == 0:
        #Funkcja Bot
   #     pass
    #else:
    #    """



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
        await ctx.send('Hello World!');
    else:
        if lang == "pl":
            await ctx.send('Witaj świecie!');
        elif lang == "de":
            await ctx.send('Hallo Welt!');



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
        'serf': Class.Serf()
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
    hero = saip.get_stats(player_id)
    await ctx.send(str(hero.attack))

#-------!!>>Tu skończyłeś, miałeś rozkmine co do walki jak ma przebiegać (Wrzuć to do innych plików) [bot działa]<<!!----------
@client.command()
async def fight(ctx):
    pl_index = 0
    for gracz in gracze:
        if gracz.id == ctx.author.id:
            pl_index = gracze.index(gracz)
            break
    gracz = gracze[pl_index]
    spider = Class.Spider()
    gracz_hp = gracz.health
    enemy_hp = spider.health
    await ctx.send(f"w przygodzie na przeciwko stanął {spider.kind}")
    await ctx.send(f"{gracz.kind}\t\t\t\t\t\t{spider.kind}\n{gracz_hp}/{gracz.health}\t\t\t\t\t\t{enemy_hp}/{spider.health}")




client.run(TOKEN)