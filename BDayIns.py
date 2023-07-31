class BDayIns:

    def __init__(self, guildName):
        self.guildName = guildName
        self.fileName = BDayIns.getFileName(guildName)
        self.dictionaryOfBirthdays = BDayIns.processFile(self.fileName)
    


    #instance methods
    def addToFile(self, key, val):
        self.updateDictionary(key, val)
        f = open(self.fileName, "a")
        f.write(f'{key}  {val}\n')
        f.close

    def updateFile(self, key, val):
        self.updateDictionary(key, val)
        f = open(self.fileName, "w")
        for x in self.dictionaryOfBirthdays:
            f.write(f'{x}  {self.dictionaryOfBirthdays.get(x)}\n')
        f.close

    async def hasLog(self, s):
        if self.dictionaryOfBirthdays.get(s) == None:
            return False
        return True

    def getLog(self, key):
        return self.dictionaryOfBirthdays.get(key)

    def updateDictionary(self, key, val):
        self.dictionaryOfBirthdays[key] = val


    @staticmethod
    def processFile(fileName):
        f = open(fileName, 'r')
        listOfBirthdays = f.readlines()
        tmpDict = {}
        for i in listOfBirthdays:
            tmpLis = i.split()
            tmpDict[tmpLis[0]] = tmpLis[1]
        return tmpDict

    def getFileName(s):
        fileName = s + '.txt'
        f = open(fileName, 'a')
        f.close
        return fileName
    
    async def isDateTime(s):
        tmp = s.split('-')
        if len(tmp) == 3:
            return True
        return False