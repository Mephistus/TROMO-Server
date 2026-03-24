# Copyright (c) 2010 Cassio Maciel.
    
from twisted.internet import reactor

from lacewing.server import ServerProtocol, ServerDatagram, ServerFactory, ServerChannel

from paccount import PlayerAccount
from item import Item
from skill import Skill
from monster import Monster
from monsterParty import MonsterParty
from map import Map
from party import Party
from battle import Battle
from fieldFunctions import FieldFunctions
from levelUp import LevelUp
from changeMap import ChangeMap
from random import randint

from time import strftime
from time import sleep
from threading import Thread
import thread
import copy

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
REQUEST_CHMI = 7
AREA_SERVER_MOVING_COMPLETE = 8
REQUEST_STATUS = 9
UPDATE_EQUIP = 10
INVITE_TO_PARTY = 11
ACCEPT_DECLINE_INVITATION = 12
REQUEST_PARTY_UPDATE = 13
REQUEST_PARTY_SWITCH = 14
REQUEST_PARTY_REMOVE = 15
REQUEST_PARTY_LEAVE = 16
PLAYER_FIGHT = 17
PLAYER_BATTLE_CHAT = 18
PLAYER_BATTLE_SKILL = 19
PLAYER_BATTLE_MAGIC = 20
PLAYER_BATTLE_ITEM = 21
AREA_SERVER_PLAYER_CHANGE_MAP = 22
PLAYER_FIELD_USE_ITEM = 23
LEVEL_UP_ADD_ATTRIBUTES = 24

# server-to-client
LOGIN_RESULT = 0
CHARACTER_LISTING_RESULT = 1
CHARACTER_SHOW_LOGIN_INFO = 2
CHARACTER_VALIDATE_NAME_RESULT = 3
CHARACTER_CREATE_NEW_CHARACTER_RESULT = 4
CHARACTER_DELETE_RESULT = 5
CHARACTER_LOGIN_RESULT = 6
CHARACTER_INICIAL_POSITION_RESULT = 7
CHARACTER_CHMI_HABILITY = 8
CHARACTER_CHMI_MAGIC = 9
CHARACTER_CHMI_ITEM = 10
CHARACTER_STATUS = 11
UPDATE_EQUIP_OK = 12
INVITE_RESPONSE = 13
SEND_INVITE = 14
PARTY_UPDATE_RESPONSE = 15
PARTY_REMOVE_RESPONSE = 16
PARTY_LEAVE_RESPONSE = 17
PARTY_DISSOLVE_RESPONSE = 18
START_BATTLE = 19
BATTLE_LOAD_COMPLETE = 20
TURN_LOAD_TIME = 21
PLAYER_PHASE = 22
FINAL_DAMAGE = 23
BATTLE_CHAT = 24
BATTLE_HP_MP_UPDATE = 25
ITEM_REMOVE = 26
ITEM_ADD = 27
POISON_REGENERATE_DAMAGE = 28
BATTLE_VERIFY_STATUS = 29
END_BATTLE_WON = 30
DEACTIVATE_BATTLE = 31
CHANNEL_CHANGE = 32
PLAYER_UPDATE_ALL_STATUS = 33
END_BATTLE_LOSE = 34

# server-to-area-server
CHARACTER_MOVE_POSITION = 0
CHARACTER_BALOON_DISAPPEAR = 1
CHARACTER_DISCONNECT = 2

# channel messages

SEND_INICIAL_POSITION = 0
SEND_CHARACTER_DIRECTION = 1
SEND_CHARACTER_POSITION = 2
SEND_BALOON_MESSAGE = 3
REQUEST_UPDATE_OUTFITS = 4
REQUEST_CHANGE_OUTFIT = 5
SEND_CHANGE_MAP = 6
USE_FIELD_ITEM = 7
USE_FIELD_SKILL = 8
DISCARD_FIELD_ITEM = 9

# peer messages (private messages)

REQUEST_OUTFIT = '0'

# error codes
SUCCESS = 0
ERROR = 1

# delimiters
DELIMITER = '|'
DELIMITER2 = ','

# attributes
BALOON_TIMER = 7.0 #Time the baloon will stand visible on screen
BALOON_TIMER_REQUEST = 1

NEW_ITEM = 1
LOST_ITEM = 0

con = None
items = []
skills = []
monsters = []
monsterParties = []
maps = []
parties = []
battles = []
fieldFunctions = FieldFunctions()
levelUp = LevelUp()
changeMap = ChangeMap()

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
        cur.execute("SELECT * FROM item ORDER BY id")
        for row in cur:
            items.append(Item(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],
                             row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],
                             row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],
                             row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],
                             row[36],row[37],row[38],row[39],row[40],row[41],row[42],row[43],row[44],
                             row[45],row[46],row[47],row[48],row[49],row[50],row[51],row[52],row[53],
                             row[54]))
            
    except:
        print '!!!!!!!!!!!!Exception caught on AccountServer() in loadItems()!!!!!!!!!!!!'
        print formatExceptionInfo()
        con.rollback()
    print "> Items loaded successfully\n----------------------------------------"
            

def loadSkills(con):
    print '> Loading Skills...'
    try:    
        cur = con.cursor()
        cur.execute("SELECT * FROM skill ORDER BY id")
        for row in cur:
            skills.append(Skill(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],
                             row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],
                             row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],
                             row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],
                             row[36],row[37],row[38],row[39],row[40],row[41],row[42],row[43],row[44],
                             row[45],row[46],row[47],row[48],row[49]))
    except:
        print '!!!!!!!!!!!!Exception caught on AccountServer() in loadSkills()!!!!!!!!!!!!'
        print formatExceptionInfo()
        con.rollback()
    print "> Skills loaded successfully\n----------------------------------------"

def loadMonsters(con):
    
    skills_list = []
    
    print '> Loading Monsters...'
    try:    
        cur = con.cursor()
         
        cur.execute("SELECT * FROM monster ORDER BY id")
        
        cont = 0
        for row in cur:
            monsters.append(Monster(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],
                             row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],
                             row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],
                             row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],
                             row[36],row[37],row[38],row[39],row[40],row[41],row[42],row[43],row[44]))
            monsters[cont].loadSkills(con)
            cont=cont+1
    except:
        print '!!!!!!!!!!!!Exception caught on AccountServer() in loadMonsters()!!!!!!!!!!!!'
        print formatExceptionInfo()
        con.rollback()
    print "> Monsters loaded successfully\n----------------------------------------"

def loadMonsterParties(con):
    print '> Loading Monster Parties...'
    try:    
        cur = con.cursor()
        cur.execute("SELECT * FROM monster_party ORDER BY id")
        for row in cur:
            monsterParties.append(MonsterParty(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],
                             row[9],row[10],row[11],row[12],row[13],row[14]))
    except:
        print '!!!!!!!!!!!!Exception caught on AccountServer() in loadMonsterParties()!!!!!!!!!!!!'
        print formatExceptionInfo()
        con.rollback()
    print "> Monster Parties loaded successfully\n----------------------------------------"

def loadMaps(con):
    print '> Loading Maps...'
    try:    
        cur = con.cursor()
        cur.execute("SELECT * FROM map ORDER BY id")
        cont = 0
        for row in cur:
            maps.append(Map(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],
                            row[12],row[13],row[14],row[15],row[16],row[17],row[18]))
            maps[cont].loadParties(con)
            cont=cont+1
    except:
        print '!!!!!!!!!!!!Exception caught on AccountServer() in loadMaps()!!!!!!!!!!!!'
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
    #playerAccount = None
    identifier = 'HUMAN'
    
    def findParty(self, id):
        i = 0
        for party in parties: 
            if party.ID == id:
                return i
                break
            i+=1
            
    def findBattle(self, id):
        i = 0
        for battle in battles: 
            if battle.ID == id:
                return i
                break
            i+=1
    
    def findMap(self, name):
        i = 0
        for map in maps: 
            if map.name == name:
                return i
                break
            i+=1

    def connectionAccepted(self, welcome):
        self.setName('Client')
        self.log('> connection accepted')
        
        if self.id == 0:
            self.factory.areaServer = self
            for channel in maps:
                self.joinChannel(channel.name)
    
    def messageReceived(self, message):
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
            self.playerAccount = newAccount.checkLogin(con, name, password)
            if  not self.playerAccount:
                self.sendMessage('0', LOGIN_RESULT)
            else:
                newAccount.client_ID = self.id
                self.setName(self.playerAccount.account_name)
                self.sendMessage('1', LOGIN_RESULT)
                self.log("> "+self.name+' with id '+str(self.id)+' has logged in.')
                self.log("> "+str(len(self.factory.connections)) + ' Players are now connected to the server')
            return
        
        elif message.subchannel == REQUEST_PLAYER_ACCOUNT:
            requestText, characterPos = value
            if requestText == 'RequestCharacterList':
                self.sendMessage(self.playerAccount.loadCharacterList(), CHARACTER_LISTING_RESULT)
                return
            if requestText == 'RequestCharacter':
                self.sendMessage(self.playerAccount.loadCharacterInfo(con, characterPos), CHARACTER_SHOW_LOGIN_INFO)
                return
            
        elif message.subchannel == CHARACTER_VALIDATE_NAME:
            self.sendMessage(self.playerAccount.validateName(con, message.value), CHARACTER_VALIDATE_NAME_RESULT)
            return
        
        elif message.subchannel == CREATE_NEW_CHARACTER:
            name, gender, strenght, physical, mind, agility = value
            self.sendMessage(self.playerAccount.createNewCharacter(con, name, gender, strenght, physical, mind, agility), CHARACTER_CREATE_NEW_CHARACTER_RESULT)
            return
        
        elif message.subchannel == DELETE_CHARACTER:
            self.sendMessage(self.playerAccount.deleteCharacter(con, message.value), CHARACTER_DELETE_RESULT)
            return
        
        elif message.subchannel == LOGIN_CHARACTER:
            partyID = 0
            resp = self.playerAccount.loginCharacter(con, message.value)
            if resp == 1:
                self.setName(self.playerAccount.playerCharacter.name)
                parties.append(Party(self.playerAccount.playerCharacter.ID,self,None,None,None,None,self,1)) #Party instantiate
                self.playerAccount.playerCharacter.partyID = self.playerAccount.playerCharacter.ID #Party initialize
                if maps[self.findMap(self.playerAccount.playerCharacter.starting_Map)].hostile_place:
                    self.playerAccount.playerCharacter.hostileArea = True
            self.sendMessage(resp, CHARACTER_LOGIN_RESULT)
            return
        
        elif message.subchannel == REQUEST_LOGIN_TO_CHANNEL:
            if message.value == "RequestChannelLogin":
                self.joinChannel(self.playerAccount.playerCharacter.starting_Map)
                return
            if message.value == "RequestInicialData":
                response = DELIMITER2.join([str(self.playerAccount.playerCharacter.starting_PosX*40),
                                 str(self.playerAccount.playerCharacter.starting_PosY*40),
                                 self.playerAccount.playerCharacter.starting_Map,
                                 str(self.playerAccount.playerCharacter.starting_PosX),
                                 str(self.playerAccount.playerCharacter.starting_PosY),
                                 str(self.playerAccount.playerCharacter.inicialOutFitHeadID),
                                 str(self.playerAccount.playerCharacter.inicialOutFitBodyID),
                                 str(self.playerAccount.playerCharacter.inicialOutFitLegID),
                                 str(self.playerAccount.playerCharacter.equipped_RightHand),
                                 str(self.playerAccount.playerCharacter.equipped_LeftHand),
                                 str(self.playerAccount.playerCharacter.equipped_Body),
                                 str(self.playerAccount.playerCharacter.equipped_Head),
                                 str(self.playerAccount.playerCharacter.equipped_Accessory)])
                self.sendMessage(response, CHARACTER_INICIAL_POSITION_RESULT)
                return
            return
        
        elif message.subchannel == REQUEST_CHMI:
            if message.value == "RequestCHMIHability":
                self.sendMessage(self.playerAccount.playerCharacter.requestCHMIHability(),CHARACTER_CHMI_HABILITY)
            elif message.value == "RequestCHMIMagic":
                self.sendMessage(self.playerAccount.playerCharacter.requestCHMIMagic(),CHARACTER_CHMI_MAGIC)
            elif message.value == "RequestCHMIItem":
                self.sendMessage(self.playerAccount.playerCharacter.requestCHMIItem(),CHARACTER_CHMI_ITEM)
                return
            return
        
        elif message.subchannel == AREA_SERVER_MOVING_COMPLETE:
            if self.id == 0:
                self.factory.sendMoveComplete(int(message.value))
            return
        
        elif message.subchannel == REQUEST_STATUS:
            ret = ''
            strBonus = ''
            phyBonus = ''
            minBonus = ''
            agiBonus = ''
            if self.playerAccount.playerCharacter.updateStatus(items[self.playerAccount.playerCharacter.equipped_RightHand],
                                                               items[self.playerAccount.playerCharacter.equipped_LeftHand],
                                                               items[self.playerAccount.playerCharacter.equipped_Body],
                                                               items[self.playerAccount.playerCharacter.equipped_Head],
                                                               items[self.playerAccount.playerCharacter.equipped_Accessory]):
                
                if (self.playerAccount.playerCharacter.strenghtBonus < 0):
                    strBonus = str(self.playerAccount.playerCharacter.strenghtBonus)
                elif (self.playerAccount.playerCharacter.strenghtBonus > 0):
                    strBonus = '+'+str(self.playerAccount.playerCharacter.strenghtBonus)
                else:
                    strBonus = ' '
                if (self.playerAccount.playerCharacter.physicalBonus < 0):
                    phyBonus = str(self.playerAccount.playerCharacter.physicalBonus)
                elif (self.playerAccount.playerCharacter.physicalBonus > 0):
                    phyBonus = '+'+str(self.playerAccount.playerCharacter.physicalBonus)
                else:
                    phyBonus = ' '
                if (self.playerAccount.playerCharacter.mindBonus < 0):
                    minBonus = str(self.playerAccount.playerCharacter.mindBonus)
                elif (self.playerAccount.playerCharacter.mindBonus > 0):
                    minBonus = '+'+str(self.playerAccount.playerCharacter.mindBonus)
                else:
                    minBonus = ' '
                if (self.playerAccount.playerCharacter.agilityBonus < 0):
                    agiBonus = str(self.playerAccount.playerCharacter.agilityBonus)
                elif (self.playerAccount.playerCharacter.agilityBonus > 0):
                    agiBonus = '+'+str(self.playerAccount.playerCharacter.agilityBonus)
                else:
                    agiBonus = ' '
                
                ret = DELIMITER2.join([str(self.playerAccount.playerCharacter.cLevel), #1
                                       str(self.playerAccount.playerCharacter.cClass),#2
                                       str(self.playerAccount.playerCharacter.hp),#3
                                       str(self.playerAccount.playerCharacter.mp),#4
                                       str(self.playerAccount.playerCharacter.inicialHP),#5
                                       str(self.playerAccount.playerCharacter.inicialMP),#6
                                       str(self.playerAccount.playerCharacter.gold),#7
                                       str(self.playerAccount.playerCharacter.xGold),#8
                                       str(self.playerAccount.playerCharacter.strenght),#9
                                       str(self.playerAccount.playerCharacter.physical),#10
                                       str(self.playerAccount.playerCharacter.mind),#11
                                       str(self.playerAccount.playerCharacter.agility),#12
                                       strBonus,#13
                                       phyBonus,#14
                                       minBonus,#15
                                       agiBonus,#16
                                       str(self.playerAccount.playerCharacter.attack),#17
                                       str(self.playerAccount.playerCharacter.defense),#18
                                       str(self.playerAccount.playerCharacter.magic_defense),#19
                                       str(self.playerAccount.playerCharacter.magic),#20
                                       str(self.playerAccount.playerCharacter.speed),#21
                                       str(self.playerAccount.playerCharacter.elemental_resist_electricity),#22
                                       str(self.playerAccount.playerCharacter.elemental_resist_fire),#23
                                       str(self.playerAccount.playerCharacter.elemental_resist_water),#24
                                       str(self.playerAccount.playerCharacter.elemental_resist_earth),#25
                                       str(self.playerAccount.playerCharacter.elemental_resist_wind),#26
                                       str(self.playerAccount.playerCharacter.elemental_resist_ice),#27
                                       str(self.playerAccount.playerCharacter.elemental_resist_dark),#28
                                       str(self.playerAccount.playerCharacter.elemental_resist_light),#29
                                       str(self.playerAccount.playerCharacter.status_resist_poison),#30
                                       str(self.playerAccount.playerCharacter.status_resist_paralyze),#31
                                       str(self.playerAccount.playerCharacter.status_resist_tired),#32
                                       str(self.playerAccount.playerCharacter.status_resist_slow),#33
                                       str(self.playerAccount.playerCharacter.status_resist_mentalblock),#34
                                       str(self.playerAccount.playerCharacter.status_resist_alergic),#35
                                       str(self.playerAccount.playerCharacter.exp),#36
                                       str(self.playerAccount.playerCharacter.nextExp),#37
                                       str(self.playerAccount.playerCharacter.gender),#38
                                       str(self.playerAccount.playerCharacter.remaining_attributes)])#39
                self.sendMessage(ret,CHARACTER_STATUS)
                return
            else:
                return
            
        elif message.subchannel == UPDATE_EQUIP:
                rHand, lHand, body, head, acc = value # get new equipment
                result = -1
                
                #validate equipment and equip it
                result = self.playerAccount.playerCharacter.updateEquip(items[int(rHand)],
                                                                  items[int(lHand)],
                                                                  items[int(body)],
                                                                  items[int(head)],
                                                                  items[int(acc)])
                if result == 1:
                    self.sendMessage("EQUIP_OK",UPDATE_EQUIP_OK)
                elif result == 0:
                    self.sendMessage("UNEQUIP_OK",UPDATE_EQUIP_OK)
                else:
                    return
        
        elif message.subchannel == INVITE_TO_PARTY:
            response = 0
            peer = self.factory.findPeer(int(message.value))
            response = parties[self.findParty(self.playerAccount.playerCharacter.partyID)].validatePartyInvitation(self, peer)
            if response == -1:
                peer.sendMessage(self.id,SEND_INVITE)
            else:
                self.sendMessage(response,INVITE_RESPONSE)
            return
                
        elif message.subchannel == ACCEPT_DECLINE_INVITATION:
            peerID, option = value
            response = ''
            peer = self.factory.findPeer(int(peerID))
            if peer:
                if option == '1':
                    if (parties[self.findParty(peer.playerAccount.playerCharacter.partyID)].addMember(self)):
                        parties.pop(self.findParty(self.playerAccount.playerCharacter.partyID))
                        self.playerAccount.playerCharacter.partyID = peer.playerAccount.playerCharacter.partyID
                        self.playerAccount.playerCharacter.inAParty = True
                        peer.playerAccount.playerCharacter.inAParty = True
                
                else:
                    response = DELIMITER2.join(["6",str(self.id)])
                    peer.sendMessage(response,INVITE_RESPONSE)
            
            return
        
        elif message.subchannel == REQUEST_PARTY_UPDATE:
            if message.value == "Request_Party_Update":
                parties[self.findParty(self.playerAccount.playerCharacter.partyID)].partyUpdate()      
            return
        
        elif message.subchannel == REQUEST_PARTY_SWITCH:
            pos1, pos2 = value
            response = ''
            if parties[self.findParty(self.playerAccount.playerCharacter.partyID)].partySwitch(self, int(pos1),int(pos2)):
                parties[self.findParty(self.playerAccount.playerCharacter.partyID)].partyUpdate() 
            return
        
        elif message.subchannel == REQUEST_PARTY_REMOVE:
            memberID = 0
            memberID = parties[self.findParty(self.playerAccount.playerCharacter.partyID)].removePartyMember(self,message.value)
            if memberID > 0:
                peer = self.factory.findPeer(memberID)
                parties.append(Party(peer.playerAccount.playerCharacter.ID,peer,None,None,None,None,peer,1)) #Party instantiate
                peer.playerAccount.playerCharacter.partyID = peer.playerAccount.playerCharacter.ID #Party initialize
                parties[peer.findParty(peer.playerAccount.playerCharacter.partyID)].partyUpdate()
                peer.playerAccount.playerCharacter.inAParty = False
                peer.sendMessage("you",PARTY_REMOVE_RESPONSE)
                
                if parties[self.findParty(self.playerAccount.playerCharacter.partyID)].party_member_count == 1:
                    self.playerAccount.playerCharacter.inAParty = False
                    
            return
        
        elif message.subchannel == REQUEST_PARTY_LEAVE:
            if message.value == "Request_Leave_Party":
                if parties[self.findParty(self.playerAccount.playerCharacter.partyID)].leaveParty(self):
                    if parties[self.findParty(self.playerAccount.playerCharacter.partyID)].party_member_count == 1:
                        peer = self.factory.findPeer(parties[self.findParty(self.playerAccount.playerCharacter.partyID)].party_leader.id)
                        peer.playerAccount.playerCharacter.inAParty = False
                        
                    parties.append(Party(self.playerAccount.playerCharacter.ID,self,None,None,None,None,self,1)) #Party instantiate
                    self.playerAccount.playerCharacter.partyID = self.playerAccount.playerCharacter.ID #Party initialize
                    self.playerAccount.playerCharacter.inAParty = False
                    parties[self.findParty(self.playerAccount.playerCharacter.partyID)].partyUpdate()
                    self.sendMessage("you",PARTY_LEAVE_RESPONSE)
                    
            elif message.value == "Request_Dissolve_Party":
                party = parties[self.findParty(self.playerAccount.playerCharacter.partyID)]
                if party.dissolveParty(self, parties):
                    pass
            return
        
        elif message.subchannel == PLAYER_FIGHT:
            targetPos = message.value
            if self.playerAccount.playerCharacter.inBattle:
                if targetPos <= 0 or targetPos >13:
                    targetPos = 1
                battles[self.findBattle(self.playerAccount.playerCharacter.battleID)].playerFight(self, targetPos)
        
        elif message.subchannel == PLAYER_BATTLE_CHAT:
            if self.playerAccount.playerCharacter.inBattle:
                battles[self.findBattle(self.playerAccount.playerCharacter.battleID)].playerChat(self, message.value)
        
        elif message.subchannel == PLAYER_BATTLE_SKILL:
            target, skillID = value
            myBattle = None
            if self.playerAccount.playerCharacter.inBattle:
                myBattle = battles[self.findBattle(self.playerAccount.playerCharacter.battleID)]
                if self.playerAccount.playerCharacter.validateBattleSkill(int(skillID),skills[int(skillID)]):
                    myBattle.playerSkill(self, int(target), int(skillID))
                    return
                myBattle.calculateTurnWait(myBattle.findPlayerPosition(self))
            return
        
        elif message.subchannel == PLAYER_BATTLE_MAGIC:
            target, magicID = value
            myBattle = None
            if self.playerAccount.playerCharacter.inBattle:
                myBattle = battles[self.findBattle(self.playerAccount.playerCharacter.battleID)]
                if self.playerAccount.playerCharacter.validateBattleMagic(int(magicID),skills[int(magicID)]):
                    myBattle.playerSkill(self, int(target), int(magicID))
                    return
                myBattle.calculateTurnWait(myBattle.findPlayerPosition(self))
            return
        
        elif message.subchannel == PLAYER_BATTLE_ITEM:
            target, itemID = value
            myBattle = None
            if self.playerAccount.playerCharacter.inBattle:
                myBattle = battles[self.findBattle(self.playerAccount.playerCharacter.battleID)]
                if self.playerAccount.playerCharacter.validateBattleItem(int(itemID),items[int(itemID)]):
                    myBattle.playerItem(self, int(target), int(itemID))
                    return
                myBattle.calculateTurnWait(myBattle.findPlayerPosition(self))
            return
        
        elif message.subchannel == AREA_SERVER_PLAYER_CHANGE_MAP:
            exit, playerID, mapName = value
            player = None
            channelName = ''
            posX = 0
            posY = 0
            message = ''
            player = self.factory.findPeer(int(playerID))
            map = maps[self.findMap(mapName)]
            channelName,posX,posY = map.changeMap(int(exit))
            destinationMap = maps[self.findMap(channelName)]
            changeMap.mapChange(player,destinationMap,posX,posY,self.factory)
            return
            #if channelName!= '':
            #    player.playerAccount.playerCharacter.battleStepCounter = 15
            #    player.leaveChannel(self.factory.findChannel(player.playerAccount.playerCharacter.starting_Map))
            #    message = DELIMITER.join([player.playerAccount.playerCharacter.starting_Map,
            #                            str(player.playerAccount.playerCharacter.starting_PosX),
            #                            str(player.playerAccount.playerCharacter.starting_PosY)])
            #    self.factory.playerDisconnect(message)
            #    player.playerAccount.playerCharacter.starting_Map = channelName
            #    player.playerAccount.playerCharacter.starting_PosX = posX
            #    player.playerAccount.playerCharacter.starting_PosY = posY
            #    player.playerAccount.playerCharacter.tempX = posX
            #    player.playerAccount.playerCharacter.tempY = posY
            #    player.playerAccount.playerCharacter.lastX = posX
            #    player.playerAccount.playerCharacter.lastY = posY
            #    if destinationMap.hostile_place:
            #        player.playerAccount.playerCharacter.hostileArea = True
            #    else:
            #        player.playerAccount.playerCharacter.hostileArea = False
            #    player.sendMessage(1,CHANNEL_CHANGE)
            #return
        
        elif message.subchannel == LEVEL_UP_ADD_ATTRIBUTES:
            mode = message.value
            if mode == 1:
                if levelUp.levelUpAddStrenght(self):
                    self.sendMessage(0,PLAYER_UPDATE_ALL_STATUS)
            elif mode == 2:
                if levelUp.levelUpAddPhysical(self):
                    self.sendMessage(0,PLAYER_UPDATE_ALL_STATUS)
            elif mode == 3:
                if levelUp.levelUpAddMind(self):
                    self.sendMessage(0,PLAYER_UPDATE_ALL_STATUS)
            elif mode == 4:
                if levelUp.levelUpAddAgility(self):
                    self.sendMessage(0,PLAYER_UPDATE_ALL_STATUS)
            return
            
        else:
            # for some reason, the client sent us something on
            # an unknown subchannel (that we can't handle)
            self.log('Client sent unexpected data')
            self.disconnect('UnexpectedPacket')
            
            
    def splitValue(self, message):
        try:
        # split the message by a delimiter
            value = message.value.split(DELIMITER2)
        except:
        # if the message is a integer don't split
            pass
        
        return value
            
    def acceptChannelMessage(self, channel, message):
        #If it's the area server let it accept automatically
        if self.id == 0:
            return True
        
        if message.subchannel == SEND_INICIAL_POSITION:
            xpos,ypos,dir = self.splitValue(message)
                
            if ((self.playerAccount.playerCharacter.starting_PosX == int(xpos)/40) and
               (self.playerAccount.playerCharacter.starting_PosY == int(ypos)/40)):
                return True
            else:
                return False
            
        elif message.subchannel == REQUEST_CHANGE_OUTFIT:
            head,body,legs = self.splitValue(message)
                
            if not self.playerAccount.playerCharacter.checkOutfitItem(int(head),items[int(head)]):
                return False
            elif not self.playerAccount.playerCharacter.checkOutfitItem(int(body),items[int(body)]):
                return False
            elif not self.playerAccount.playerCharacter.checkOutfitItem(int(legs),items[int(legs)]):
                return False
            else:
                return True
                
        elif message.subchannel == SEND_CHARACTER_POSITION:
            if self.playerAccount.playerCharacter.checkLegitMove(message.value):
                    
                response = DELIMITER.join([
                                            str(self.playerAccount.playerCharacter.tempX),
                                            str(self.playerAccount.playerCharacter.tempY),
                                            str(self.id),
                                            self.playerAccount.playerCharacter.starting_Map,
                                            str(message.value),
                                            str(self.playerAccount.playerCharacter.starting_PosX),
                                            str(self.playerAccount.playerCharacter.starting_PosY)])
                self.factory.sendToAreaServer(response)
                
            return False

        elif message.subchannel == SEND_BALOON_MESSAGE:
            if (len(message.value) < 100 and message.value != ""):
                return True
            else:
                return False
                
        elif message.subchannel == REQUEST_UPDATE_OUTFITS:
            if message.value == 'Update_Another_Outfits':    
                return True
            
        elif message.subchannel == USE_FIELD_ITEM:
            if self.id == 0:
                return True
            itemID = message.value
            channel = None
            party = None
            try:
                item = items[itemID]
            except:
                return False
            if self.playerAccount.playerCharacter.validateFieldItem(itemID, item):
                channel = self.factory.findChannel(self.playerAccount.playerCharacter.starting_Map)
                party = parties[self.findParty(self.playerAccount.playerCharacter.partyID)]
                fieldFunctions.calculateItemDamage(item,party,channel,self,self.factory.areaServer)
            return False    
        
        elif message.subchannel == USE_FIELD_SKILL:
            if self.id == 0:
                return True
            skillID = message.value
            channel = None
            party = None
            try:
                skill = skills[skillID]
            except:
                return False
            if self.playerAccount.playerCharacter.validateFieldSkill(skillID, skill):
                channel = self.factory.findChannel(self.playerAccount.playerCharacter.starting_Map)
                party = parties[self.findParty(self.playerAccount.playerCharacter.partyID)]
                fieldFunctions.calculateSkillDamage(skill,party,channel,self,self.factory.areaServer)
            return False
        
        elif message.subchannel == DISCARD_FIELD_ITEM:
            itemID = message.value
            try:
                item = items[itemID]
            except:
                return False
            if item.sell_value > 0:
                fieldFunctions.updatePlayerItem(self,itemID, LOST_ITEM)
            return False   
        
        else:
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
    
    #Client can't request leave the channel on it's on
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
    
    def channelLeft(self,channel):
        message = DELIMITER.join([self.playerAccount.playerCharacter.starting_Map,
                                    str(self.playerAccount.playerCharacter.starting_PosX),
                                    str(self.playerAccount.playerCharacter.starting_PosY)])
        self.factory.playerDisconnect(message)
    
    def connectionLost(self, reason):
        message = ''
        resOk = False
        party = None
        message = DELIMITER.join([self.playerAccount.playerCharacter.starting_Map,
                                  str(self.playerAccount.playerCharacter.starting_PosX),
                                  str(self.playerAccount.playerCharacter.starting_PosY)])
        party = parties[self.findParty(self.playerAccount.playerCharacter.partyID)]
        if not party.leaveParty(self):
            resOk = party.dissolveParty(self,parties)
        if resOk:
            parties.pop(self.findParty(self.playerAccount.playerCharacter.partyID))
        self.factory.playerDisconnect(message)
        playerIndex = -1
        self.log("> connection lost")
        
            
        ServerProtocol.connectionLost(self, reason)
        # if we're logged in, unload the account
        #if self.account:
        #    self.account.unload()
            
    def log(self, message):
        """
        Log a message.
        """
        print '%s: %s' % (self.id, message)
        
        
#class Timer(Thread):
#        def __init__(self, seconds, request, factory, arg1=None, arg2=None):
#            self.runTime = seconds
#            self.request = request
#            self.factory = factory
#            self.arg1 = arg1
#            self.arg2 = arg2
#            self.message = ''
#            Thread.__init__(self)
#        def run(self):
#            if self.request == BALOON_TIMER_REQUEST:
#                #sleep(self.runTime)
#                #self.message = DELIMITER.join([str(self.arg1),self.arg2])
#                #self.factory.sendToAreaServerBaloonDisappear(self.arg1, self.message) 

class AccountFactory(ServerFactory):
    protocol = AccountProtocol
    areaServer = None
    def __init__(self):
        pass
    
    def findPeer(self, peerID):
        for peer in self.connections.values():
            if peer.id == peerID:
                return peer
                break
            
    def findChannel(self, channelName):
        for channel in self.channels.values():
            if channel.name == channelName:
                return channel
                break
    
    def sendToAreaServer(self, message):
        self.areaServer.sendMessage(message,CHARACTER_MOVE_POSITION)
        return
    
    def startBattle(self, peer):
        battleID = 0
        party = parties[peer.findParty(peer.playerAccount.playerCharacter.partyID)]
        map = maps[peer.findMap(peer.playerAccount.playerCharacter.starting_Map)]
        monster_party = monsterParties[map.monster_party_list[randint(0,len(map.monster_party_list)-1)].ID-1]
        battleID = len(battles)
        battles.append(Battle(battleID,
                              copy.copy(monsters[monster_party.monster_pos1_id]),
                              copy.copy(monsters[monster_party.monster_pos2_id]),
                              copy.copy(monsters[monster_party.monster_pos3_id]),
                              copy.copy(monsters[monster_party.monster_pos4_id]),
                              copy.copy(monsters[monster_party.monster_pos5_id]),
                              copy.copy(monsters[monster_party.monster_pos6_id]),
                              copy.copy(monsters[monster_party.monster_pos7_id]),
                              copy.copy(monsters[monster_party.monster_pos8_id]),
                              copy.copy(monsters[monster_party.monster_pos9_id]),
                              copy.copy(monsters[monster_party.monster_pos10_id]),
                              copy.copy(monsters[monster_party.monster_pos11_id]),
                              copy.copy(monsters[monster_party.monster_pos12_id]),
                              copy.copy(monsters[monster_party.monster_pos13_id]),
                              party.party_member_1,
                              party.party_member_2,
                              party.party_member_3,
                              party.party_member_4,
                              party.party_member_5,
                              items,
                              skills,
                              battles,
                              maps,
                              self))
        party.startBattle(map.ID, battles[peer.findBattle(battleID)])
        battles[peer.findBattle(battleID)].battleInit()
        return
        
    
    def sendMoveComplete(self, peerID):
        peer = self.findPeer(peerID)
        peer.playerAccount.playerCharacter.completeMove()
        if peer.playerAccount.playerCharacter.checkBattle():
            self.startBattle(peer)
        return
    
    def playerDisconnect(self,message):
        self.areaServer.sendMessage(message, CHARACTER_DISCONNECT)
        return
        
    
    
newFactory = AccountFactory()
# connect the main TCP factory
port = reactor.listenTCP(6121, newFactory)
# just so we know it's working
print '> Opening new server on port %s...' % port.port
con = kinterbasdb.connect(dsn='C:/Program Files/Firebird/Firebird_2_1/romdatabase.fdb',user='SYSDBA',password='masterkey')
loadServerData(con)
reactor.run()