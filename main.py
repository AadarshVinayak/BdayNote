import discord
from datetime import datetime
import asyncio

intents = discord.Intents.default()
intents.message_content = True

dictionaryOfBirthdays = {}
fileName = ''

client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
        
    for guild in client.guilds:
        getFileName(guild.name)
        print(fileName)
        
    await asyncio.sleep(1)
    processFile()

    print(dictionaryOfBirthdays)

    

@client.event
async def on_message(message):

    if message.author == client.user:
        return


    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$create'):
        getFileName(message.guild.name)
        await asyncio.sleep(1)
        processFile()
        params= message.content.split()
        if len(params) == 3:
            if await hasLog(params[1]) == False:
                if await isDateTime(params[2]):
                    date_object = datetime.strptime(params[2], '%m-%d-%Y').date()
                    addToFile(params[1], date_object)
                    await message.channel.send(f'{params[1]}\'s Birthday is {date_object}!')
                else:
                    await message.channel.send('Please use the date format MM-DD-YYYY')
            else:
                await message.channel.send('Already have a log for there birthday, please either update or lookup the value')
        dictionaryOfBirthdays.clear()

    if message.content.startswith('$lookup'):
        getFileName(message.guild.name)
        await asyncio.sleep(1)
        processFile()
        params = message.content.split()
        if len(params) == 2:
            if await hasLog(params[1]):
                await message.channel.send(f'{params[1]} {getLog(params[1])}')
        dictionaryOfBirthdays.clear()
    
    if message.content.startswith('$update'):
        getFileName(message.guild.name)
        await asyncio.sleep(1)
        processFile()
        getFileName(message.guild.name)
        params = message.content.split()
        if len(params) == 3:
            if await hasLog(params[1]):
                if await isDateTime(params[2]):
                    date_object = datetime.strptime(params[2], '%m-%d-%Y').date()
                    updateFile(params[1], date_object)
                    await message.channel.send(f'{date_object}')
                else:
                    await message.channel.send('Please use the date format MM-DD-YYYY')
            else:
                await message.channel.send('I dont have a birthday for this person')
        dictionaryOfBirthdays.clear()

    if message.content.startswith('$listAll'):
        getFileName(message.guild.name)
        await asyncio.sleep(1)
        processFile()
        getFileName(message.guild.name)
        params = message.content.split()
        if len(params) == 1:
            for i in dictionaryOfBirthdays:
                await message.channel.send(f'{i}\'s Birthday is {dictionaryOfBirthdays.get(i)}')
        dictionaryOfBirthdays.clear()

    if message.content.startswith('$help'):
        await message.channel.send('Here are the functions to get and save your friends birthday\n')
        await message.channel.send('$create - Syntax $create **name** **MM-DD-YYYY** - Add a birthday to the list!\n')
        await message.channel.send('$lookup - Syntax $lookup **name** - Lookup the birthday of a friend via there name!\n')
        await message.channel.send('$update - Syntax $update **name** **MM-DD-YYYY** - Update the birthday of a friend via there name!\n')
        await message.channel.send('$listAll - Syntax $listAll - List all the birthdays configured\n')


def getFileName(s):
    global fileName
    fileName = s + '.txt'
    f = open(fileName, 'a')
    f.close
        
def processFile():
    print(fileName)
    f = open(fileName, 'r')
    listOfBirthdays = f.readlines()
    for i in listOfBirthdays:
        tmpLis = i.split()
        dictionaryOfBirthdays[tmpLis[0]] = tmpLis[1]


def addToFile(key, val):
    updateDictionary(key, val)
    f = open(fileName, "a")
    f.write(f'{key}  {val}\n')
    f.close

def updateFile(key, val):
    updateDictionary(key, val)
    f = open(fileName, "w")
    for x in dictionaryOfBirthdays:
        f.write(f'{x}  {dictionaryOfBirthdays.get(x)}\n')
    f.close

async def isDateTime(s):
    tmp = s.split('-')
    if len(tmp) == 3:
        return True
    return False

async def hasLog(s):
    if dictionaryOfBirthdays.get(s) == None:
        return False
    return True

def getLog(key):
    return dictionaryOfBirthdays.get(key)

def updateDictionary(key, val):
    dictionaryOfBirthdays[key] = val


client.run('token')