import discord
from datetime import datetime
import asyncio
from BDayIns import BDayIns

intents = discord.Intents.default()
intents.message_content = True

dictionaryOfBirthdays = {}
listOfBDays = []
fileName = ''

client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    for guild in client.guilds:
        tmp = BDayIns(guild.name)
        listOfBDays.append(tmp)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$create'):
        tmp = getBDayIns(message.guild.name)
        if tmp != None:
            params= message.content.split()
            if len(params) == 3:
                if await tmp.hasLog(params[1]) == False:
                    if await BDayIns.isDateTime(params[2]):
                        date_object = datetime.strptime(params[2], '%m-%d-%Y').date()
                        tmp.addToFile(params[1], date_object)
                        await message.channel.send(f'{params[1]}\'s Birthday is {date_object}!')
                    else:
                        await message.channel.send('Please use the date format MM-DD-YYYY')
                else:
                    await message.channel.send('Already have a log for there birthday, please either update or lookup the value')

    if message.content.startswith('$lookup'):
        tmp = getBDayIns(message.guild.name)
        if tmp != None:
            params = message.content.split()
            if len(params) == 2:
                if await tmp.hasLog(params[1]):
                    await message.channel.send(f'{params[1]} {tmp.getLog(params[1])}')
    
    if message.content.startswith('$update'):
        tmp = getBDayIns(message.guild.name)
        if tmp != None:
            params = message.content.split()
            if len(params) == 3:
                if await tmp.hasLog(params[1]):
                    if await BDayIns.isDateTime(params[2]):
                        date_object = datetime.strptime(params[2], '%m-%d-%Y').date()
                        tmp.updateFile(params[1], date_object)
                        await message.channel.send(f'{date_object}')
                    else:
                        await message.channel.send('Please use the date format MM-DD-YYYY')
                else:
                    await message.channel.send('I dont have a birthday for this person')

    if message.content.startswith('$listAll'):
        tmp = getBDayIns(message.guild.name)
        if tmp != None:
            params = message.content.split()
            if len(params) == 1:
                for i in tmp.dictionaryOfBirthdays:
                    await message.channel.send(f'{i}\'s Birthday is {tmp.dictionaryOfBirthdays.get(i)}')

    if message.content.startswith('$help'):
        await message.channel.send('Here are the functions to get and save your friends birthday\n')
        await message.channel.send('$create - Syntax $create **name** **MM-DD-YYYY** - Add a birthday to the list!\n')
        await message.channel.send('$lookup - Syntax $lookup **name** - Lookup the birthday of a friend via there name!\n')
        await message.channel.send('$update - Syntax $update **name** **MM-DD-YYYY** - Update the birthday of a friend via there name!\n')
        await message.channel.send('$listAll - Syntax $listAll - List all the birthdays configured\n')

def getBDayIns(guildName):
    for bDay in listOfBDays:
        if bDay.guildName == guildName:
            return bDay
    return None

client.run('MTEzMzkxOTg3Mzk2MjA4NjQ1MQ.GDnXSE.k0lfkylCwM3YWaloWu5jCwx6-4QP8nD7cZtFQc')