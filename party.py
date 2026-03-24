# Copyright (c) 2010 Cassio Maciel.

import os
import yaml
import kinterbasdb
import sys
import traceback
from threading import Timer

DELIMITER = ','
DELIMITER2 = ':'
BATTLE_LOAD_TIMER = 3.0

#Subchannels for Client Messages
INVITE_RESPONSE = 13
SEND_INVITE = 14
PARTY_UPDATE_RESPONSE = 15
PARTY_REMOVE_RESPONSE = 16
PARTY_LEAVE_RESPONSE = 17
PARTY_DISSOLVE_RESPONSE = 18
START_BATTLE = 19
BATTLE_LOAD_COMPLETE = 20

def formatExceptionInfo(maxTBlevel=5):
         cla, exc, trbk = sys.exc_info()
         excName = cla.__name__
         try:
             excArgs = exc.__dict__["args"]
         except KeyError:
             excArgs = "<no args>"
         excTb = traceback.format_tb(trbk, maxTBlevel)
         return (excName, excArgs, excTb)
         
class Party(object):

    def __init__(self,arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8):
         #Party Information
         self.ID = arg1
         self.party_member_1 = arg2
         self.party_member_2 = arg3
         self.party_member_3 = arg4
         self.party_member_4 = arg5
         self.party_member_5 = arg6
         self.party_leader = arg7
         self.party_member_count = arg8
         self.invitationIDList = [] #For controlling real invited members
         
    def validatePartyInvitation(self, sender, receiver):
         try:
             if sender != self.party_leader:
                 return 0 #Not the party leader
             elif (self.party_member_count >= 5):
                 return 1 #Party is full
             elif (self.party_member_1 != None and receiver.id == self.party_member_1.id):
                 return 2 #This player is already in party
             elif (self.party_member_2 != None and receiver.id == self.party_member_2.id):
                 return 2 #This player is already in party
             elif (self.party_member_3 != None and receiver.id == self.party_member_3.id):
                 return 2 #This player is already in party
             elif (self.party_member_4 != None and receiver.id == self.party_member_4.id):
                 return 2 #This player is already in party
             elif (self.party_member_5 != None and receiver.id == self.party_member_5.id):
                 return 2 #This player is already in party
             elif receiver.playerAccount.playerCharacter.inAParty:
                 return 3 #This player is already on a party
             else:
                 self.invitationIDList.append(receiver.id)
                 return -1 #Ok to send invitation
         except:
             print '!!!!!!!!!!!!Exception caught on PlayerCharacter() in validatePartyInvitation()!!!!!!!!!!!!'
             print formatExceptionInfo()
             return 7 #Unknown Error
         
    def sendMessageAll(self, message, subchannel):
         if self.party_member_1:
                  self.party_member_1.sendMessage(message, subchannel)
         if self.party_member_2:
                  self.party_member_2.sendMessage(message, subchannel)
         if self.party_member_3:
                  self.party_member_3.sendMessage(message, subchannel)
         if self.party_member_4:
                  self.party_member_4.sendMessage(message, subchannel)
         if self.party_member_5:
                  self.party_member_5.sendMessage(message, subchannel)
         return

    def addMember(self, member):
         member1Name = ' '
         member1Level = ' '
         member2Name = ' '
         member2Level = ' '
         member3Name = ' '
         member3Level = ' '
         member4Name = ' '
         member4Level = ' '
         member5Name = ' '
         member5Level = ' '
         count = 0
         validatedMember = False
         
         for memberID in self.invitationIDList:
            if memberID == member.id:
                validatedMember = True
                self.invitationIDList.remove(memberID)
                
         if not validatedMember: #If player was not really invited to this party, cancel party join
            return validatedMember
         
         if self.party_member_count < 5:
             if self.party_member_1 == None:
                 self.party_member_1 = member
             elif self.party_member_2 == None:
                 self.party_member_2 = member
             elif self.party_member_3 == None:
                 self.party_member_3 = member
             elif self.party_member_4 == None:
                 self.party_member_4 = member
             elif self.party_member_5 == None:
                 self.party_member_5 = member
                 
             self.party_member_count += 1
             
             if self.party_member_1:
                 member1Name = self.party_member_1.playerAccount.playerCharacter.name
                 member1Level = str(self.party_member_1.playerAccount.playerCharacter.cLevel)
             if self.party_member_2:
                 member2Name = self.party_member_2.playerAccount.playerCharacter.name
                 member2Level = str(self.party_member_2.playerAccount.playerCharacter.cLevel)
             if self.party_member_3:
                 member3Name = self.party_member_3.playerAccount.playerCharacter.name
                 member3Level = str(self.party_member_3.playerAccount.playerCharacter.cLevel)
             if self.party_member_4:
                 member4Name = self.party_member_4.playerAccount.playerCharacter.name
                 member4Level = str(self.party_member_4.playerAccount.playerCharacter.cLevel)
             if self.party_member_5:
                 member5Name = self.party_member_5.playerAccount.playerCharacter.name
                 member5Level = str(self.party_member_5.playerAccount.playerCharacter.cLevel)
             
             response = DELIMITER.join(["5", str(member.id),
                                         member1Name,
                                         member1Level,
                                         member2Name,
                                         member2Level,
                                         member3Name,
                                         member3Level,
                                         member4Name,
                                         member4Level,
                                         member5Name,
                                         member5Level])
             
             self.sendMessageAll(response, INVITE_RESPONSE)
             return True
         else:
             member.sendMessage(4,INVITE_RESPONSE)
    
    def partyUpdate(self):
        response = ""
        partyLeader = ",0"
        member1Name = " "
        member1Level = " "
        member2Name = " "
        member2Level = " "
        member3Name = " "
        member3Level = " "
        member4Name = " "
        member4Level = " "
        member5Name = " "
        member5Level = " "
        
        if self.party_member_1:
            member1Name = self.party_member_1.playerAccount.playerCharacter.name
            member1Level = str(self.party_member_1.playerAccount.playerCharacter.cLevel)
        if self.party_member_2:
            member2Name = self.party_member_2.playerAccount.playerCharacter.name
            member2Level = str(self.party_member_2.playerAccount.playerCharacter.cLevel)
        if self.party_member_3:
            member3Name = self.party_member_3.playerAccount.playerCharacter.name
            member3Level = str(self.party_member_3.playerAccount.playerCharacter.cLevel)
        if self.party_member_4:
            member4Name = self.party_member_4.playerAccount.playerCharacter.name
            member4Level = str(self.party_member_4.playerAccount.playerCharacter.cLevel)
        if self.party_member_5:
            member5Name = self.party_member_5.playerAccount.playerCharacter.name
            member5Level = str(self.party_member_5.playerAccount.playerCharacter.cLevel)
            
            
        response = DELIMITER.join([member1Name,
                                    member1Level,
                                    member2Name,
                                    member2Level,
                                    member3Name,
                                    member3Level,
                                    member4Name,
                                    member4Level,
                                    member5Name,
                                    member5Level])
         
        if self.party_member_1:
            if self.party_leader == self.party_member_1:
                partyLeader = ",1"
            self.party_member_1.sendMessage(response+partyLeader, PARTY_UPDATE_RESPONSE)
            partyLeader = ",0"
        if self.party_member_2:
            if self.party_leader == self.party_member_2:
                partyLeader = ",1"
            self.party_member_2.sendMessage(response+partyLeader, PARTY_UPDATE_RESPONSE)
            partyLeader = ",0"
        if self.party_member_3:
            if self.party_leader == self.party_member_3:
                partyLeader = ",1"
            self.party_member_3.sendMessage(response+partyLeader, PARTY_UPDATE_RESPONSE)
            partyLeader = ",0"
        if self.party_member_4:
            if self.party_leader == self.party_member_4:
                partyLeader = ",1"
            self.party_member_4.sendMessage(response+partyLeader, PARTY_UPDATE_RESPONSE)
            partyLeader = ",0"
        if self.party_member_5:
            if self.party_leader == self.party_member_5:
                partyLeader = ",1"
            self.party_member_5.sendMessage(response+partyLeader, PARTY_UPDATE_RESPONSE)
            partyLeader = ",0"

    def partySwitch(self,sender,pos1,pos2):
        switchAux = None
        switchAux2 = None
        try:
            if (sender == self.party_leader  and (pos1 >= 1 and pos1 <= 5)
                and (pos2 >= 1 and pos2 <= 5)
                and (pos1 != pos2)) :
                if pos1 == 1:
                    switchAux = self.party_member_1
                elif pos1 == 2:
                    switchAux = self.party_member_2
                elif pos1 == 3:
                    switchAux = self.party_member_3
                elif pos1 == 4:
                    switchAux = self.party_member_4
                elif pos1 == 5:
                    switchAux = self.party_member_5
                
                if pos2 == 1:
                    switchAux2 = self.party_member_1
                    self.party_member_1 = switchAux
                elif pos2 == 2:
                    switchAux2 = self.party_member_2
                    self.party_member_2 = switchAux
                elif pos2 == 3:
                    switchAux2 = self.party_member_3
                    self.party_member_3 = switchAux
                elif pos2 == 4:
                    switchAux2 = self.party_member_4
                    self.party_member_4 = switchAux
                elif pos2 == 5:
                    switchAux2 = self.party_member_5
                    self.party_member_5 = switchAux
                    
                if pos1 == 1:
                    self.party_member_1 = switchAux2
                elif pos1 == 2:
                    self.party_member_2 = switchAux2
                elif pos1 == 3:
                    self.party_member_3 = switchAux2
                elif pos1 == 4:
                    self.party_member_4 = switchAux2
                elif pos1 == 5:
                    self.party_member_5 = switchAux2
                return True
            else:
                return False
        except:
            print '!!!!!!!!!!!!Exception caught on PlayerCharacter() in partySwitch()!!!!!!!!!!!!'
            print formatExceptionInfo()
            return
        
    def removePartyMember(self, sender, memberPos):
         try:
            charName = ''
            memberID = 0
            member1 = None
            member2 = None
            member3 = None
            member4 = None
            member5 = None
            if memberPos >=1 and memberPos <=5 and sender == self.party_leader:
                member1 = self.party_member_1
                member2 = self.party_member_2
                member3 = self.party_member_3
                member4 = self.party_member_4
                member5 = self.party_member_5
                    
                if memberPos == 1 and member1 != self.party_leader:
                    charName = member1.name
                    memberID = member1.id
                    self.party_member_1 = None
                if memberPos == 2 and member2 != self.party_leader:
                    charName = member2.name
                    memberID = member2.id
                    self.party_member_2 = None
                if memberPos == 3 and member3 != self.party_leader:
                    charName = member3.name
                    memberID = member3.id
                    self.party_member_3 = None
                if memberPos == 4 and member4 != self.party_leader:
                    charName = member4.name
                    memberID = member4.id
                    self.party_member_4 = None
                if memberPos == 5 and member5 != self.party_leader:
                    charName = member5.name
                    memberID = member5.id
                    self.party_member_5 = None
                    
                self.party_member_count -= 1
                    
                if member1:
                    member1.sendMessage(charName,PARTY_REMOVE_RESPONSE)
                if member2:
                    member2.sendMessage(charName,PARTY_REMOVE_RESPONSE)
                if member3:
                    member3.sendMessage(charName,PARTY_REMOVE_RESPONSE)
                if member4:
                    member4.sendMessage(charName,PARTY_REMOVE_RESPONSE)
                if member5:
                    member5.sendMessage(charName,PARTY_REMOVE_RESPONSE)
                    
                self.partyUpdate()
                    
            return memberID
         
         except:
            print '!!!!!!!!!!!!Exception caught on PlayerCharacter() in removePartyMember()!!!!!!!!!!!!'
            print formatExceptionInfo()
            return 0 
         
    def leaveParty(self, member):
         try:
             charName = member.name
             if member != self.party_leader:
                  if member == self.party_member_1:
                           self.party_member_1 = None
                  if member == self.party_member_2:
                           self.party_member_2 = None
                  if member == self.party_member_3:
                           self.party_member_3 = None
                  if member == self.party_member_4:
                           self.party_member_4 = None
                  if member == self.party_member_5:
                           self.party_member_5 = None
                  
                  self.party_member_count -= 1
                  
                  if self.party_member_1:
                      self.party_member_1.sendMessage(charName,PARTY_LEAVE_RESPONSE)
                  if self.party_member_2:
                      self.party_member_2.sendMessage(charName,PARTY_LEAVE_RESPONSE)
                  if self.party_member_3:
                      self.party_member_3.sendMessage(charName,PARTY_LEAVE_RESPONSE)
                  if self.party_member_4:
                      self.party_member_4.sendMessage(charName,PARTY_LEAVE_RESPONSE)
                  if self.party_member_5:
                      self.party_member_5.sendMessage(charName,PARTY_LEAVE_RESPONSE)
                  
                  self.partyUpdate()
                      
                  return True
             else:
                  return False
         except:
            print '!!!!!!!!!!!!Exception caught on PlayerCharacter() in leaveParty()!!!!!!!!!!!!'
            print formatExceptionInfo()
            return False
    
    def findParty(self, id, parties):
        i = 0
        for party in parties: 
            if party.ID == id:
                return i
                break
            i+=1
         
    def dissolveParty(self, sender, parties):
         try:
            if sender == self.party_leader:
                parties.remove(self)
                if self.party_member_1:
                    parties.append(Party(self.party_member_1.playerAccount.playerCharacter.ID,self.party_member_1,None,None,None,None,self.party_member_1,1)) #Party instantiate
                    self.party_member_1.playerAccount.playerCharacter.partyID = self.party_member_1.playerAccount.playerCharacter.ID #Party initialize
                    self.party_member_1.playerAccount.playerCharacter.inAParty = False
                    parties[self.findParty(self.party_member_1.playerAccount.playerCharacter.partyID,parties)].partyUpdate()
                    self.party_member_1.sendMessage("OK",PARTY_DISSOLVE_RESPONSE)
                if self.party_member_2:
                    parties.append(Party(self.party_member_2.playerAccount.playerCharacter.ID,self.party_member_2,None,None,None,None,self.party_member_2,1)) #Party instantiate
                    self.party_member_2.playerAccount.playerCharacter.partyID = self.party_member_2.playerAccount.playerCharacter.ID #Party initialize
                    self.party_member_2.playerAccount.playerCharacter.inAParty = False
                    parties[self.findParty(self.party_member_2.playerAccount.playerCharacter.partyID,parties)].partyUpdate()
                    self.party_member_2.sendMessage("OK",PARTY_DISSOLVE_RESPONSE)
                if self.party_member_3:
                    parties.append(Party(self.party_member_3.playerAccount.playerCharacter.ID,self.party_member_3,None,None,None,None,self.party_member_3,1)) #Party instantiate
                    self.party_member_3.playerAccount.playerCharacter.partyID = self.party_member_3.playerAccount.playerCharacter.ID #Party initialize
                    self.party_member_3.playerAccount.playerCharacter.inAParty = False
                    parties[self.findParty(self.party_member_3.playerAccount.playerCharacter.partyID,parties)].partyUpdate()
                    self.party_member_3.sendMessage("OK",PARTY_DISSOLVE_RESPONSE)
                if self.party_member_4:
                    parties.append(Party(self.party_member_4.playerAccount.playerCharacter.ID,self.party_member_4,None,None,None,None,self.party_member_4,1)) #Party instantiate
                    self.party_member_4.playerAccount.playerCharacter.partyID = self.party_member_4.playerAccount.playerCharacter.ID #Party initialize
                    self.party_member_4.playerAccount.playerCharacter.inAParty = False
                    parties[self.findParty(self.party_member_4.playerAccount.playerCharacter.partyID,parties)].partyUpdate()
                    self.party_member_4.sendMessage("OK",PARTY_DISSOLVE_RESPONSE)
                if self.party_member_5:
                    parties.append(Party(self.party_member_5.playerAccount.playerCharacter.ID,self.party_member_5,None,None,None,None,self.party_member_5,1)) #Party instantiate
                    self.party_member_5.playerAccount.playerCharacter.partyID = self.party_member_5.playerAccount.playerCharacter.ID #Party initialize
                    self.party_member_5.playerAccount.playerCharacter.inAParty = False
                    parties[self.findParty(self.party_member_5.playerAccount.playerCharacter.partyID,parties)].partyUpdate()
                    self.party_member_5.sendMessage("OK",PARTY_DISSOLVE_RESPONSE)
                return True
            else:
                return False
         except:
                  print '!!!!!!!!!!!!Exception caught on Party() in dissolveParty()!!!!!!!!!!!!'
                  print formatExceptionInfo()
                  return False
         
    def battleOpen(self):
         if self.party_member_1:
                  self.party_member_1.sendMessage(1,BATTLE_LOAD_COMPLETE)
         if self.party_member_2:
                  self.party_member_2.sendMessage(1,BATTLE_LOAD_COMPLETE)
         if self.party_member_3:
                  self.party_member_3.sendMessage(1,BATTLE_LOAD_COMPLETE)
         if self.party_member_4:
                  self.party_member_4.sendMessage(1,BATTLE_LOAD_COMPLETE)
         if self.party_member_5:
                  self.party_member_5.sendMessage(1,BATTLE_LOAD_COMPLETE)
    
    
    def startBattle(self, mapID, battle):
         try:
                  response = ''
                  if self.party_member_1:
                           response = DELIMITER.join([self.party_member_1.name,#1
                                                      str(self.party_member_1.playerAccount.playerCharacter.inicialHP),#2
                                                      str(self.party_member_1.playerAccount.playerCharacter.inicialMP),#3
                                                      str(self.party_member_1.playerAccount.playerCharacter.inicialOutFitHeadID),#4
                                                      str(self.party_member_1.playerAccount.playerCharacter.inicialOutFitBodyID),#5
                                                      str(self.party_member_1.playerAccount.playerCharacter.inicialOutFitLegID)])#6
                  else:
                           response = DELIMITER.join(["0","0","0","0","0","0"])
                  if self.party_member_2:
                           response = DELIMITER.join([response,
                                                      self.party_member_2.name,#7
                                                      str(self.party_member_2.playerAccount.playerCharacter.inicialHP),#8
                                                      str(self.party_member_2.playerAccount.playerCharacter.inicialMP),#9
                                                      str(self.party_member_2.playerAccount.playerCharacter.inicialOutFitHeadID),#10
                                                      str(self.party_member_2.playerAccount.playerCharacter.inicialOutFitBodyID),#11
                                                      str(self.party_member_2.playerAccount.playerCharacter.inicialOutFitLegID)])#12
                  else:
                           response = DELIMITER.join([response,"0","0","0","0","0","0"])
                  if self.party_member_3:
                           response = DELIMITER.join([response,
                                                      self.party_member_3.name,#13
                                                      str(self.party_member_3.playerAccount.playerCharacter.inicialHP),#14
                                                      str(self.party_member_3.playerAccount.playerCharacter.inicialMP),#15
                                                      str(self.party_member_3.playerAccount.playerCharacter.inicialOutFitHeadID),#16
                                                      str(self.party_member_3.playerAccount.playerCharacter.inicialOutFitBodyID),#17
                                                      str(self.party_member_3.playerAccount.playerCharacter.inicialOutFitLegID)])#18
                  else:
                           response = DELIMITER.join([response,"0","0","0","0","0","0"])
                  if self.party_member_4:
                           response = DELIMITER.join([response,
                                                      self.party_member_4.name,#19
                                                      str(self.party_member_4.playerAccount.playerCharacter.inicialHP),#20
                                                      str(self.party_member_4.playerAccount.playerCharacter.inicialMP),#21
                                                      str(self.party_member_4.playerAccount.playerCharacter.inicialOutFitHeadID),#22
                                                      str(self.party_member_4.playerAccount.playerCharacter.inicialOutFitBodyID),#23
                                                      str(self.party_member_4.playerAccount.playerCharacter.inicialOutFitLegID)])#24
                  else:
                           response = DELIMITER.join([response,"0","0","0","0","0","0"])
                  if self.party_member_5:
                           response = DELIMITER.join([response,
                                                      self.party_member_5.name,#25
                                                      str(self.party_member_5.playerAccount.playerCharacter.inicialHP),#26
                                                      str(self.party_member_5.playerAccount.playerCharacter.inicialMP),#27
                                                      str(self.party_member_5.playerAccount.playerCharacter.inicialOutFitHeadID),#28
                                                      str(self.party_member_5.playerAccount.playerCharacter.inicialOutFitBodyID),#29
                                                      str(self.party_member_5.playerAccount.playerCharacter.inicialOutFitLegID)])#30
                  else:
                           response = DELIMITER.join([response,"0","0","0","0","0","0"])
                  
                  response = DELIMITER.join([response,
                                             battle.monster_1.name,#31
                                             str(battle.monster_1.grapphic),#32
                                             battle.monster_2.name,#33
                                             str(battle.monster_2.grapphic),#34
                                             battle.monster_3.name,#35
                                             str(battle.monster_3.grapphic),#36
                                             battle.monster_4.name,#37
                                             str(battle.monster_4.grapphic),#38
                                             battle.monster_5.name,#39
                                             str(battle.monster_5.grapphic),#40
                                             battle.monster_6.name,#41
                                             str(battle.monster_6.grapphic),#42
                                             battle.monster_7.name,#43
                                             str(battle.monster_7.grapphic),#44
                                             battle.monster_8.name,#45
                                             str(battle.monster_8.grapphic),#46
                                             battle.monster_9.name,#47
                                             str(battle.monster_9.grapphic),#48
                                             battle.monster_10.name,#49
                                             str(battle.monster_10.grapphic),#50
                                             battle.monster_11.name,#51
                                             str(battle.monster_11.grapphic),#52
                                             battle.monster_12.name,#53
                                             str(battle.monster_12.grapphic),#54
                                             battle.monster_13.name,#55
                                             str(battle.monster_13.grapphic),#56
                                             str(mapID)])#57
                  
                  
                  if self.party_member_1:
                           self.party_member_1.playerAccount.playerCharacter.inBattle = True
                           self.party_member_1.playerAccount.playerCharacter.battleID = battle.ID
                           self.party_member_1.sendMessage(response,START_BATTLE)
                  if self.party_member_2:
                           self.party_member_2.playerAccount.playerCharacter.inBattle = True
                           self.party_member_2.playerAccount.playerCharacter.battleID = battle.ID
                           self.party_member_2.sendMessage(response,START_BATTLE)
                  if self.party_member_3:
                           self.party_member_3.playerAccount.playerCharacter.inBattle = True
                           self.party_member_3.playerAccount.playerCharacter.battleID = battle.ID
                           self.party_member_3.sendMessage(response,START_BATTLE)
                  if self.party_member_4:
                           self.party_member_4.playerAccount.playerCharacter.inBattle = True
                           self.party_member_4.playerAccount.playerCharacter.battleID = battle.ID
                           self.party_member_4.sendMessage(response,START_BATTLE)
                  if self.party_member_5:
                           self.party_member_5.playerAccount.playerCharacter.inBattle = True
                           self.party_member_5.playerAccount.playerCharacter.battleID = battle.ID
                           self.party_member_5.sendMessage(response,START_BATTLE)
                           
                           
         except:
                  print '!!!!!!!!!!!!Exception caught on PlayerCharacter() in startBattle()!!!!!!!!!!!!'
                  print formatExceptionInfo()
                  return
         