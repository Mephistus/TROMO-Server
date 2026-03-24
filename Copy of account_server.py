# Copyright (c) 2010 Cassio Maciel.
    
from twisted.internet import reactor

from lacewing.server import ServerProtocol, ServerDatagram, ServerFactory, ServerChannel

from paccount import PlayerAccount
from item import Item
from skill import Skill
from monster import Monster
from monsterParty import MonsterParty
from map import Map

from time import strftime
import kinterbasdb
import sys
import traceback

# client-to-server
LOGIN_SUBCHANNEL = 0
REQUEST_PLAYER_ACCOUNT = 1
CHARACTER_VALIDATE_NAME = 2
CREATE_NEW_CHARACTER = 3
DELETE_CHARACTER = 4
LOGIN_CHARACTER = 5
REQUEST_LOGIN_TO_CHANNEL = 6

# server-to-client
LOGIN_RESULT = 0
CHARACTER_LISTING_RESULT = 1
CHARACTER_SHOW_LOGIN_INFO = 2
CHARACTER_VALIDATE_NAME_RESULT = 3
CHARACTER_CREATE_NEW_CHARACTER_RESULT = 4
CHARACTER_DELETE_RESULT = 5
CHARACTER_LOGIN_RESULT = 6
CHARACTER_INICIAL_POSITION_RESULT = 7

# channel messages

SEND_INICIAL_POSITION = '0'
REQUEST_CHANGE_OUTFIT = '5'

# error codes
SUCCESS = 0
ERROR = 1

DELIMITER = '|'
DELIMITER2 = ','

con = None
items = []
skills = []
monsters = []
monsterParties = []
maps = []

def formatExceptionInfo(maxTBlevel=5):
         cla, exc, trbk = sys.exc_info()
         excName = cla.__name__
         try:
             excArgs = exc.__dict__["args"]
         except KeyError:
             excArgs = "<no args>"
         excTb = traceback.format_tb(trbk, maxTBlevel)
         return (excName, excArgs, excTb)

def loadItems(con):
    print "----------------------------------------"
    print '> Loading Items...'
    try:    
        cur = con.cursor()
        cur.execute("SELECT * FROM item")
        for row in cur:
            items.append(Item(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],
                             row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],
                             row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],
                             row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],
                             row[36],row[37],row[38],row[39],row[40],row[41],row[42],row[43],row[44],
                             row[45],row[46],row[47],row[48],row[49],row[50],row[51],row[52],row[53]))
    except:
        print 'Exception caught on AccountServer() in loadItems()'
        print formatExceptionInfo()
        con.rollback()
    print "> Items loaded successfully\n----------------------------------------"
            

def loadSkills(con):
    print '> Loading Skills...'
    try:    
        cur = con.cursor()
        cur.execute("SELECT * FROM skill")
        for row in cur:
            skills.append(Skill(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],
                             row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],
                             row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],
                             row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],
                             row[36],row[37],row[38],row[39],row[40],row[41],row[42],row[43],row[44],
                             row[45],row[46],row[47],row[48]))
    except:
        print 'Exception caught on AccountServer() in loadSkills()'
        print formatExceptionInfo()
        con.rollback()
    print "> Skills loaded successfully\n----------------------------------------"

def loadMonsters(con):
    print '> Loading Monsters...'
    try:    
        cur = con.cursor()
        cur.execute("SELECT * FROM monster")
        for row in cur:
            monsters.append(Monster(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],
                             row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],
                             row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],
                             row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],
                             row[36],row[37],row[38],row[39],row[40],row[41],row[42],row[43],row[44]))
    except:
        print 'Exception caught on AccountServer() in loadMonsters()'
        print formatExceptionInfo()
        con.rollback()
    print "> Monsters loaded successfully\n----------------------------------------"

def loadMonsterParties(con):
    print '> Loading Monster Parties...'
    try:    
        cur = con.cursor()
        cur.execute("SELECT * FROM monster_party")
        for row in cur:
            monsterParties.append(MonsterParty(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],
                             row[9],row[10],row[11],row[12],row[13],row[14]))
    except:
        print 'Exception caught on AccountServer() in loadMonsterParties()'
        print formatExceptionInfo()
        con.rollback()
    print "> Monster Parties loaded successfully\n----------------------------------------"

def loadMaps(con):
    print '> Loading Maps...'
    try:    
        cur = con.cursor()
        cur.execute("SELECT * FROM map")
        for row in cur:
            maps.append(Map(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    except:
        print 'Exception caught on AccountServer() in loadMaps()'
        print formatExceptionInfo()
        con.rollback()
    print "> Maps loaded successfully\n----------------------------------------"

def loadServerData(con):
    loadItems(con)
    loadSkills(con)
    loadMonsters(con)
    loadMonsterParties(con)
    loadMaps(con)
    print "> Server Started Succesfully."
    print "----------------------------------------"
    print strftime("> %a, %d %b %Y %H:%M:%S")



class AccountProtocol(ServerProtocol):
    myName = ''

    def connectionAccepted(self, welcome):
        self.setName('Client')
        self.log('> connection accepted')
    
    def messageReceived(self, message):
        print self.myName + " EH O NOME"
        playerAccount = None
        accountIter = None
        playerIndex = -1
        
        for accountIter in self.factory.accountList:
            playerIndex = playerIndex + 1
            if accountIter.playerCharacter:
                if self.name == accountIter.playerCharacter.name:
                    playerAccount = accountIter
                    break
            elif self.name == accountIter.account_name:
                playerAccount = accountIter
                break
        
        try:
            # split the message by a delimiter
            value = message.value.split(DELIMITER)
        except:
            # if the message is a integer don't split
            pass
            
        # client wants to register
        if message.subchannel == LOGIN_SUBCHANNEL:
            name, password = value # get the specified name and password
            # validate login and send back response
            newAccount = PlayerAccount()
            playerAccount = newAccount.checkLogin(con, name, password)
            if  not playerAccount:
                self.sendMessage('0', LOGIN_RESULT)
            else:
                newAccount.client_ID = self.id
                self.factory.accountList.append(newAccount)
                for i in range (0,len(self.factory.accountList)):
                    self.factory.accountList[i].needSync = True
                self.setName(playerAccount.account_name)
                print 'registrou?'
                self.myName = playerAccount.account_name
                self.sendMessage('1', LOGIN_RESULT)
                self.log("> "+self.name+' with id '+str(self.id)+' has logged in.')
                self.log("> "+str(len(self.factory.connections)) + ' Players are now connected to the server')
            return
        
        elif message.subchannel == REQUEST_PLAYER_ACCOUNT:
            requestText, characterPos = value
            if requestText == 'RequestCharacterList':
                self.sendMessage(playerAccount.loadCharacterList(), CHARACTER_LISTING_RESULT)
                return
            if requestText == 'RequestCharacter':
                self.sendMessage(playerAccount.loadCharacterInfo(con, characterPos), CHARACTER_SHOW_LOGIN_INFO)
                return
            
        elif message.subchannel == CHARACTER_VALIDATE_NAME:
            self.sendMessage(playerAccount.validateName(con, message.value), CHARACTER_VALIDATE_NAME_RESULT)
            return
        
        elif message.subchannel == CREATE_NEW_CHARACTER:
            name, gender, strenght, physical, mind, agility = value
            self.sendMessage(playerAccount.createNewCharacter(con, name, gender, strenght, physical, mind, agility), CHARACTER_CREATE_NEW_CHARACTER_RESULT)
            return
        
        elif message.subchannel == DELETE_CHARACTER:
            self.sendMessage(playerAccount.deleteCharacter(con, message.value), CHARACTER_DELETE_RESULT)
            return
        
        elif message.subchannel == LOGIN_CHARACTER:
            resp = playerAccount.loginCharacter(con, message.value)
            if resp == 1:
                self.setName(playerAccount.playerCharacter.name)
            self.sendMessage(resp, CHARACTER_LOGIN_RESULT)
            return
        
        elif message.subchannel == REQUEST_LOGIN_TO_CHANNEL:
            if message.value == "RequestChannelLogin":
                self.joinChannel(playerAccount.playerCharacter.starting_Map)
                return
            if message.value == "RequestInicialData":
                response = DELIMITER2.join([str(playerAccount.playerCharacter.starting_PosX*40),
                                 str(playerAccount.playerCharacter.starting_PosY*40),
                                 playerAccount.playerCharacter.starting_Map,
                                 str(playerAccount.playerCharacter.starting_PosX),
                                 str(playerAccount.playerCharacter.starting_PosY),
                                 str(playerAccount.playerCharacter.inicialOutFitHeadID),
                                 str(playerAccount.playerCharacter.inicialOutFitBodyID),
                                 str(playerAccount.playerCharacter.inicialOutfitLegID)])
                self.sendMessage(response, CHARACTER_INICIAL_POSITION_RESULT)
                return
            return
        
        else:
            # for some reason, the client sent us something on
            # an unknown subchannel (that we can't handle)
            self.log('Client sent unexpected data')
            self.disconnect('UnexpectedPacket')
            
    def acceptChannelMessage(self, channel, message):
        ret = False
        
        try:
            value = message.value.split(DELIMITER2)
        except:
            #channel message is in uncorrect format
            return False
        
        #Checking if the message is an inicial position
        if not ret:
            try:
                request, xpos, ypos = value
                ret = True
            except:
                ret = False
        #Checking if the message is an outfit change
        if not ret:
            try:
                request, head, body, legs = value
                ret = True
            except:
                ret = False
        
        if ret:
            if request == SEND_INICIAL_POSITION:
                playerIndex = -1
                for accountIter in self.factory.accountList:
                    playerIndex = playerIndex + 1
                    if accountIter.playerCharacter:
                        if self.name == accountIter.playerCharacter.name:
                            playerAccount = accountIter
                            break
                
                if ((playerAccount.playerCharacter.starting_PosX/40 == xpos) and
                    (playerAccount.playerCharacter.starting_PosY/40 == ypos)):
                    return True
                else:
                    return False
            
            elif request == REQUEST_CHANGE_OUTFIT:
                playerIndex = -1
                for accountIter in self.factory.accountList:
                    playerIndex = playerIndex + 1
                    if accountIter.playerCharacter:
                        if self.name == accountIter.playerCharacter.name:
                            playerAccount = accountIter
                            break
                    
                if not playerAccount.playerCharacter.checkOutfitItem(int(head),items[int(head)]):
                    return False
                elif not playerAccount.playerCharacter.checkOutfitItem(int(body),items[int(body)]):
                    return False
                elif not playerAccount.playerCharacter.checkOutfitItem(int(legs),int(legs)):
                    return False
                else:
                    return True
        
        return False
        
            
            
            
    
    #Client can't join channels on it's own
    def acceptChannelJoin(self, channelName):
        self.log("> WARNING : Client: "+self.name+ "ID: "+self.id+" tried to join a channel illegally")
        return False
    
    #Client can't change it's own name
    def acceptNameChange(self, name):
        self.log("> WARNING :Client: "+self.name+ "ID: "+self.id+" tried to change connection name illegally")
        return False
    
    #Client can't request the channel list
    def acceptChannelListRequest(self):
        self.log("> WARNING :Client: "+self.name+ "ID: "+self.id+" requested server list illegally")
        return False
    
    #Client can't request the channel list
    def acceptChannelLeave(self, channel):
        self.log("> WARNING :Client: "+self.name+ "ID: "+self.id+" tried to leave the channel illegally")
        return False

    def sendResponse(self, code, details = ''):
        message = DELIMITER2.join([str(code), details])
        self.sendMessage(message, ERROR_SUBCHANNEL)
    
    def acceptLogin(self, name):
        # client can't set it's own name
        self.log("> WARNING :Client: "+self.name+ "ID: "+self.id+" Tried to set it's own name illegally")
        self.warn('NameDenied', 'InvalidName')
        return False
    
    def connectionLost(self, reason):
        playerIndex = -1
        self.log("> connection lost")
        for accountIter in self.factory.accountList:
            playerIndex = playerIndex + 1
            if accountIter.playerCharacter:
                if self.name == accountIter.playerCharacter.name:
                    self.factory.accountList.pop(playerIndex)
                    break
            elif self.name == accountIter.account_name:
                self.factory.accountList.pop(playerIndex)
                break
            
            for i in range (0,len(self.factory.accountList)):
                    self.factory.accountList[i].needSync = True
            
        ServerProtocol.connectionLost(self, reason)
        # if we're logged in, unload the account
        #if self.account:
        #    self.account.unload()
            
    def log(self, message):
        """
        Log a message.
        """
        print '%s: %s' % (self.id, message)
        

class AccountFactory(ServerFactory):
    protocol = AccountProtocol
    def __init__(self):
        self.accountList = []
    
    
newFactory = AccountFactory()
# connect the main TCP factory
port = reactor.listenTCP(6121, newFactory)
# just so we know it's working
print '> Opening new server on port %s...' % port.port
con = kinterbasdb.connect(dsn='C:/Program Files/Firebird/Firebird_2_1/romdatabase.fdb',user='SYSDBA',password='masterkey')
loadServerData(con)
reactor.run()