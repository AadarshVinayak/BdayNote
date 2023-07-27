import discord
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
dictionaryOfBirthdays = {}

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    processFile()
    print(dictionaryOfBirthdays)
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$create'):
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

    if message.content.startswith('$lookup'):
        params = message.content.split()
        if len(params) == 2:
            if await hasLog(params[1]):
                await message.channel.send(f'{params[1]} {getLog(params[1])}')
    
    if message.content.startswith('$update'):
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

    if message.content.startswith('$help'):
        await message.channel.send('Here are the functions to get and save your friends birthday\n')
        await message.channel.send('$create - Syntax $create **name** **MM-DD-YYYY** - Add a birthday to the list!\n')
        await message.channel.send('$lookup - Syntax $lookup **name** - Lookup the birthday of a friend via there name!\n')
        await message.channel.send('$update - Syntax $update **name** **MM-DD-YYYY** - Update the birthday of a friend via there name!\n')


        
def processFile():
    f = open('myfile.txt', 'r')
    listOfBirthdays = f.readlines()
    for i in listOfBirthdays:
        tmpLis = i.split()
        dictionaryOfBirthdays[tmpLis[0]] = tmpLis[1]

def addToFile(key, val):
    updateDictionary(key, val)
    f = open("myfile.txt", "a")
    f.write(f'{key}  {val}\n')
    f.close

def updateFile(key, val):
    updateDictionary(key, val)
    f = open("myfile.txt", "w")
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

client.run('MTEzMzkxOTg3Mzk2MjA4NjQ1MQ.GkK7EF.TnY6rekxVdiKyjAPe3jsXrSPhh4Svmm4KHAeCg')