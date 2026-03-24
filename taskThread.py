import os
import yaml
import kinterbasdb
import sys
import traceback
import threading

import time

DELIMITER = ','

BATTLE_HP_MP_UPDATE = 25
POISON_REGENERATE_DAMAGE = 28
BATTLE_VERIFY_STATUS = 29
END_BATTLE_WON = 30

class TaskThread(threading.Thread):
    """Thread that executes a task every N seconds"""
    
    def __init__(self, statusList, party_member_1, party_member_2, party_member_3, party_member_4, party_member_5,
                 monster_1,monster_2,monster_3,monster_4,monster_5,monster_6,monster_7,monster_8,monster_9,
                 monster_10,monster_11,monster_12,monster_13,battle):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = 4.0
        self.statusList = statusList
        self.party_member_1 = party_member_1
        self.party_member_2 = party_member_2
        self.party_member_3 = party_member_3
        self.party_member_4 = party_member_4
        self.party_member_5 = party_member_5
        self.monster_1 = monster_1
        self.monster_2 = monster_2
        self.monster_3 = monster_3
        self.monster_4 = monster_4
        self.monster_5 = monster_5
        self.monster_6 = monster_6
        self.monster_7 = monster_7
        self.monster_8 = monster_8
        self.monster_9 = monster_9
        self.monster_10 = monster_10
        self.monster_11 = monster_11
        self.monster_12 = monster_12
        self.monster_13 = monster_13
        self.battle = battle
    
    def sendMessageAll(self,message,subchannel):
        if self.party_member_1:
            self.party_member_1.sendMessage(message,subchannel)
        if self.party_member_2:
            self.party_member_2.sendMessage(message,subchannel)
        if self.party_member_3:
            self.party_member_3.sendMessage(message,subchannel)
        if self.party_member_4:
            self.party_member_4.sendMessage(message,subchannel)
        if self.party_member_5:
            self.party_member_5.sendMessage(message,subchannel)
    
    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval
        
    def setStatusList(self, statusList):
        self.statusList = statusList
    
    def shutdown(self):
        """Stop this thread"""
        self._finished.set()
    
    def run(self):
        while 1:
            if self._finished.isSet(): return
            self.task()
            
            # sleep for interval or until shutdown
            self._finished.wait(self._interval)
    
    def findPlayerPosition(self, playerObj):
        if playerObj == self.monster_1:
                return 1
        elif playerObj == self.monster_2:
                return 2
        elif playerObj == self.monster_3:
                return 3
        elif playerObj == self.monster_4:
                return 4
        elif playerObj == self.monster_5:
                return 5
        elif playerObj == self.monster_6:
                return 6
        elif playerObj == self.monster_7:
                return 7
        elif playerObj == self.monster_8:
                return 8
        elif playerObj == self.monster_9:
                return 9
        elif playerObj == self.monster_10:
                return 10
        elif playerObj == self.monster_11:
                return 11
        elif playerObj == self.monster_12:
                return 12
        elif playerObj == self.monster_13:
                return 13
        elif playerObj == self.party_member_1.playerAccount.playerCharacter:
                return 14
        elif playerObj == self.party_member_2.playerAccount.playerCharacter:
                return 15
        elif playerObj == self.party_member_3.playerAccount.playerCharacter:
                return 16
        elif playerObj == self.party_member_4.playerAccount.playerCharacter:
                return 17
        elif playerObj == self.party_member_5.playerAccount.playerCharacter:
                return 18
        else:
            return 0
    
    def task(self):
        """The task done by this thread - override in subclasses"""
        for iter in self.statusList:
            hpMpStatus = ''
            hasStatus = False
            regenerateOrDamage = 0
            action = ''
            animation = 0
            targetPos = 0
            poisonTurn = False
            regenerateTurn = False
            
            if iter.poison_status_counter % 2 != 0:
                poisonTurn = True
            if iter.regenerate_status_counter % 2 != 0:
                regenerateTurn = True
            
            targetPos = self.findPlayerPosition(iter)
            
            if iter.poison_status_counter > 0:
                if iter.poison_status_counter > 1:
                    hasStatus = True
                iter.poison_status_counter -= 1
                if poisonTurn:
                    regenerateOrDamage = int((iter.inicialHP*15)/100)
                    iter.inicialHP -= regenerateOrDamage
                    
            if iter.slow_status_counter > 0:
                if iter.slow_status_counter > 1:
                    hasStatus = True
                iter.slow_status_counter-=1
                iter.relative_speed = int((iter.speed*50)/100)
            elif iter.slow_status_counter <= 0:
                iter.relative_speed = iter.speed
            
            if iter.haste_status_counter > 0:
                print iter.haste_status_counter
                if iter.haste_status_counter > 1:
                    hasStatus = True
                iter.haste_status_counter-=1
                iter.relative_speed += int(iter.speed)
            elif iter.haste_status_counter <= 0:
                iter.relative_speed = iter.speed
                
            if iter.paralyze_status_counter > 0:
                if iter.paralyze_status_counter > 1:
                    hasStatus = True
                if iter.paralyze_status_counter == 1:
                    self.battle.calculateTurnWait(targetPos)
                elif iter.paralyze_status_counter > 1:
                    iter.relative_speed = 0
                iter.paralyze_status_counter-=1
            elif iter.haste_status_counter <= 0 and iter.slow_status_counter <= 0 and iter.paralyze_status_counter <= 0:
                iter.relative_speed = iter.speed
                
            if iter.tired_status_counter > 0:
                if iter.tired_status_counter > 1:
                    hasStatus = True
                iter.tired_status_counter-=1
                iter.relative_attack = int((iter.attack*50)/100)
                iter.relative_defense = int((iter.defense*50)/100)
            else:
                iter.relative_attack = iter.attack
                iter.relative_defense = iter.defense
                
            if iter.enchant_status_counter > 0:
                if iter.enchant_status_counter > 1:
                    hasStatus = True
                iter.enchant_status_counter-=1
                iter.relative_attack += int((iter.attack*50)/100)
                iter.relative_defense += int((iter.defense*50)/100)
            elif iter.tired_status_counter <= 0 and iter.enchant_status_counter <= 0:
                iter.relative_attack = iter.attack
                iter.relative_defense = iter.defense
                
            if iter.regenerate_status_counter > 0:
                if iter.regenerate_status_counter > 1:
                    hasStatus = True
                iter.regenerate_status_counter-=1
                if regenerateTurn:
                    regenerateOrDamage = int((iter.hp*15)/100)
                    iter.inicialHP += regenerateOrDamage
                    if iter.inicialHP >= iter.hp:
                        iter.inicialHP = iter.hp
                        
            if iter.mentalBlock_status_counter > 0:
                if iter.mentalBlock_status_counter > 1:
                    hasStatus = True
                iter.mentalBlock_status_counter-=1
            
            if iter.alergic_status_counter > 0:
                if iter.alergic_status_counter > 1:
                    hasStatus = True
                iter.alergic_status_counter-=1
                
            if iter.revive_status_counter > 0:
                if iter.revive_status_counter > 1:
                    hasStatus = True
                if iter.revive_status_counter == 1:    
                    self.battle.calculateTurnWait(targetPos)
                iter.revive_status_counter-=1
                
            hpMpStatus = DELIMITER.join([str(targetPos),                    #1
                                     str(iter.inicialHP),                   #2
                                     str(iter.inicialMP),                   #3
                                     str(iter.poison_status_counter),       #4
                                     str(iter.paralyze_status_counter),     #5
                                     str(iter.tired_status_counter),        #6
                                     str(iter.slow_status_counter),         #7
                                     str(iter.mentalBlock_status_counter),  #8
                                     str(iter.alergic_status_counter),      #9
                                     str(iter.haste_status_counter),        #10
                                     str(iter.enchant_status_counter),      #11
                                     str(iter.regenerate_status_counter)])  #12
            
            if targetPos >=14:
                self.sendMessageAll(hpMpStatus,BATTLE_HP_MP_UPDATE)
            if not iter.cured:
                self.sendMessageAll(targetPos,BATTLE_VERIFY_STATUS)
            
            action =          DELIMITER.join([str(targetPos),          #(1) Target
                                              str(regenerateOrDamage)  #(2) hpDamage
                                            ])

            self.battle.calculateLoadTime(targetPos)
            self.sendMessageAll(action, POISON_REGENERATE_DAMAGE)
            
            iter.cured = False
            if not hasStatus:
                self.statusList.remove(iter)
                
                
                
                
                
                
                
                
                
                