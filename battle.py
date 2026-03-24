#!/usr/bin/env python
# Copyright (c) 2010 Cassio Maciel.

import os
import yaml
import kinterbasdb
import sys
import traceback

from threading import Timer
from threading import Thread
from random import randint
from customTimer import CustomTimer
from taskThread import TaskThread
from levelUp import LevelUp
from changeMap import ChangeMap

import time


DELIMITER = ','
DELIMITER2 = '}'
BATTLE_START_COUNTDOWN = 4.0
NEW_ITEM = 1
LOST_ITEM = 0
DISAPPEAR_BATTLE_TIMER = 7.0
TURN_AVERAGE_TIMER = 5.0

DEAD = 1
ALIVE = 0
WON = 1
LOSE = 0

#Subchannels for Client Requests
PLAYER_FIGHT = 17

#Subchannels for Client Messages
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
END_BATTLE_LOSE = 34

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
    
class Battle(object):
    
    def __init__(self,arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,
                 arg9,arg10,arg11,arg12,arg13,arg14,arg15,arg16,arg17,arg18,arg19,arg20,arg21,arg22,arg23,arg24):
         #Party Information
         self.ID = arg1
         self.monster_1 = arg2
         self.monster_2 = arg3
         self.monster_3 = arg4
         self.monster_4 = arg5
         self.monster_5 = arg6
         self.monster_6 = arg7
         self.monster_7 = arg8
         self.monster_8 = arg9
         self.monster_9 = arg10
         self.monster_10 = arg11
         self.monster_11 = arg12
         self.monster_12 = arg13
         self.monster_13 = arg14
         self.party_member_1 = arg15
         self.party_member_2 = arg16
         self.party_member_3 = arg17
         self.party_member_4 = arg18
         self.party_member_5 = arg19
         self.items = arg20
         self.skills = arg21
         self.battles = arg22
         self.maps = arg23
         self.fact = arg24
         
         self.averageTurnTime = 0
         self.playersMonstersCount = 0
         self.actionQuery = [] #1(0:FIGHT OR 1:SKILL),2(ORIGIN),3(TARGET),4(SKILL ID)
         self.nextAction = ''
         self.lastOrigin = 0
         self.playerSortList = []
         self.monsterSortList = []
         self.statusList = []
         self.statusThread = None
         self.itemsObtained = []
         self.expObtained = 0
         self.goldObtained = 0
         
    
    def findMap(self, name):
        i = 0
        for map in self.maps: 
            if map.name == name:
                return i
                break
            i+=1
    
    def findOriginSprite(self, position):  
        if position <= 13:
            if position == 1 and self.monster_1.inicialHP > 0:
                return self.monster_1
            elif position == 2 and self.monster_2.inicialHP > 0:
                return self.monster_2
            elif position == 3 and self.monster_3.inicialHP > 0:
                return self.monster_3
            elif position == 4 and self.monster_4.inicialHP > 0:
                return self.monster_4
            elif position == 5 and self.monster_5.inicialHP > 0:
                return self.monster_5
            elif position == 6 and self.monster_6.inicialHP > 0:
                return self.monster_6
            elif position == 7 and self.monster_7.inicialHP > 0:
                return self.monster_7
            elif position == 8 and self.monster_8.inicialHP > 0:
                return self.monster_8
            elif position == 9 and self.monster_9.inicialHP > 0:
                return self.monster_9
            elif position == 10 and self.monster_10.inicialHP > 0:
                return self.monster_10
            elif position == 11 and self.monster_11.inicialHP > 0:
                return self.monster_11
            elif position == 12 and self.monster_12.inicialHP > 0:
                return self.monster_12
            elif position == 13 and self.monster_13.inicialHP > 0:
                return self.monster_13
            else:
                return DEAD
        else:
            if position == 14 and self.party_member_1:
                if self.party_member_1.playerAccount.playerCharacter.inicialHP > 0:
                    return self.party_member_1
                else:
                    return DEAD
            elif position == 15 and self.party_member_2:
                if self.party_member_2.playerAccount.playerCharacter.inicialHP > 0:
                    return self.party_member_2
                else:
                    return DEAD
            elif position == 16 and self.party_member_3:
                if self.party_member_3.playerAccount.playerCharacter.inicialHP > 0:
                    return self.party_member_3
                else:
                    return DEAD
            elif position == 17 and self.party_member_4:
                if self.party_member_4.playerAccount.playerCharacter.inicialHP > 0:
                    return self.party_member_4
                else:
                    return DEAD
            elif position == 18 and self.party_member_5:
                if self.party_member_5.playerAccount.playerCharacter.inicialHP > 0:
                    return self.party_member_5
                else:
                    return DEAD
            else:
                return DEAD
                
    def findTargetSprite(self, position):
        if position <= 13:
            if position == 1 and self.monster_1.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_1
            elif position == 2 and self.monster_2.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_2
            elif position == 3 and self.monster_3.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_3
            elif position == 4 and self.monster_4.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_4
            elif position == 5 and self.monster_5.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_5
            elif position == 6 and self.monster_6.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_6
            elif position == 7 and self.monster_7.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_7
            elif position == 8 and self.monster_8.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_8
            elif position == 9 and self.monster_9.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_9
            elif position == 10 and self.monster_10.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_10
            elif position == 11 and self.monster_11.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_11
            elif position == 12 and self.monster_12.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_12
            elif position == 13 and self.monster_13.inicialHP > 0:
                self.actionQuery[0].target = position
                return self.monster_13
            else:
                if position == 13:
                 position = 1
                else:
                    position += 1
                return self.findTargetSprite(position)
        else:
            if position == 14 and self.party_member_1:
                if self.party_member_1.playerAccount.playerCharacter.inicialHP > 0:
                    self.actionQuery[0].target = position
                    return self.party_member_1
            if position == 15 and self.party_member_2:
                if self.party_member_2.playerAccount.playerCharacter.inicialHP > 0:
                    self.actionQuery[0].target = position
                    return self.party_member_2
            if position == 16 and self.party_member_3:
                if self.party_member_3.playerAccount.playerCharacter.inicialHP > 0:
                    self.actionQuery[0].target = position
                    return self.party_member_3
            if position == 17 and self.party_member_4:
                if self.party_member_4.playerAccount.playerCharacter.inicialHP > 0:
                    self.actionQuery[0].target = position
                    return self.party_member_4
            if position == 18 and self.party_member_5:
                if self.party_member_5.playerAccount.playerCharacter.inicialHP > 0:
                    self.actionQuery[0].target = position
                    return self.party_member_5
            
            position +=1
            if position == 19:
                position = 14
            return self.findTargetSprite(position)
             
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
    
    def updateStatus(self, targetSprite):
        if targetSprite.poison_status_counter > 28:
            targetSprite.poison_status_counter = 28
        elif targetSprite.poison_status_counter < 0:
            targetSprite.poison_status_counter = 0
        if targetSprite.paralyze_status_counter > 28:
            targetSprite.paralyze_status_counter = 28
        elif targetSprite.paralyze_status_counter < 0:
            targetSprite.paralyze_status_counter = 0
        if targetSprite.tired_status_counter > 28:
            targetSprite.tired_status_counter = 28
        elif targetSprite.tired_status_counter < 0:
            targetSprite.tired_status_counter = 0
        if targetSprite.slow_status_counter > 28:
            targetSprite.slow_status_counter = 28
        elif targetSprite.slow_status_counter < 0:
            targetSprite.slow_status_counter = 0
        if targetSprite.mentalBlock_status_counter > 28:
            targetSprite.mentalBlock_status_counter = 28
        elif targetSprite.mentalBlock_status_counter <0:
            targetSprite.mentalBlock_status_counter = 0
        if targetSprite.alergic_status_counter > 28:
            targetSprite.alergic_status_counter = 28
        elif targetSprite.alergic_status_counter <0:
            targetSprite.alergic_status_counter = 0
        if targetSprite.haste_status_counter > 28:
            targetSprite.haste_status_counter = 28
        elif targetSprite.haste_status_counter <0:
            targetSprite.haste_status_counter = 0
        if targetSprite.enchant_status_counter > 28:
            targetSprite.enchant_status_counter = 28
        elif targetSprite.enchant_status_counter <0:
            targetSprite.enchant_status_counter = 0
        if targetSprite.regenerate_status_counter > 28:
            targetSprite.regenerate_status_counter = 28
        elif targetSprite.regenerate_status_counter <0:
            targetSprite.regenerate_status_counter = 0
        
        
        i = False
        if (targetSprite.poison_status_counter > 0 or targetSprite.paralyze_status_counter > 0 or
            targetSprite.tired_status_counter  > 0 or targetSprite.slow_status_counter > 0 or
            targetSprite.mentalBlock_status_counter > 0 or targetSprite.alergic_status_counter > 0 or
            targetSprite.haste_status_counter > 0 or targetSprite.enchant_status_counter > 0 or
            targetSprite.regenerate_status_counter >0):
            for iter in self.statusList:
                if iter == targetSprite:
                    i = True
            if not i:
                self.statusList.append(targetSprite)
            self.statusThread.setStatusList(self.statusList)
    
    def monsterItemSort(self, itemID, itemChance):
        if itemChance >= 1:
            if (randint(0,100)) <= (itemChance):
                self.itemsObtained.append(itemID)
        if itemChance >= 0.1 and itemChance < 1:
            if (randint(0,1000)) <= (itemChance*10):
                self.itemsObtained.append(itemID)
        if itemChance >= 0.01 and itemChance < 0.1:
            if (randint(0,10000)) <= (itemChance*100):
                self.itemsObtained.append(itemID)
        if itemChance >= 0.001 and itemChance < 0.01:
            if (randint(0,100000)) <= (itemChance*1000):
                self.itemsObtained.append(itemID)
    
    def monsterItemExpObtain(self,monster):
        if monster.treasure_1_id > 0:
            self.monsterItemSort(monster.treasure_1_id, monster.treasure_1_chance)
        if monster.treasure_2_id > 0:
            self.monsterItemSort(monster.treasure_2_id, monster.treasure_2_chance)
        if monster.treasure_3_id > 0:
            self.monsterItemSort(monster.treasure_3_id, monster.treasure_3_chance)
        if monster.treasure_4_id > 0:
            self.monsterItemSort(monster.treasure_4_id, monster.treasure_4_chance)
        if monster.treasure_5_id > 0:
            self.monsterItemSort(monster.treasure_5_id, monster.treasure_5_chance)
            
        self.expObtained += monster.experience
        self.goldObtained += monster.gold
            

    def updateDamage(self,originPos,targetPos,originSprite,targetSprite,hpDamage,mpDamage,poison,paralyze,tired,slow,mentalBlock,alergic,
                     haste,enchant,regenerate,revive):
        self.lastOrigin = originPos
        hpMpStatus = ''
        
        targetSprite.inicialMP -= mpDamage
        if targetSprite.inicialMP <= 0:
            targetSprite.inicialMP = 0
        if targetSprite.inicialMP > targetSprite.mp:
            targetSprite.inicialMP = targetSprite.mp
        targetSprite.poison_status_counter += poison
        targetSprite.paralyze_status_counter += paralyze
        targetSprite.tired_status_counter += tired
        targetSprite.slow_status_counter += slow
        targetSprite.mentalBlock_status_counter += mentalBlock
        targetSprite.alergic_status_counter += alergic
        targetSprite.haste_status_counter += haste
        targetSprite.enchant_status_counter += enchant
        targetSprite.regenerate_status_counter += regenerate
        targetSprite.revive_status_counter += revive
        self.updateStatus(targetSprite)
        
        targetSprite.inicialHP -= hpDamage
        if targetSprite.inicialHP > targetSprite.hp:
            targetSprite.inicialHP = targetSprite.hp
        if targetSprite.inicialHP <= 0:
            targetSprite.inicialHP = 0
            if targetSprite.identifier == 'NPC':
                self.monsterItemExpObtain(targetSprite)
            self.nextAction = DELIMITER.join([self.nextAction,
                                              str(DEAD)])           
        else:
            self.nextAction = DELIMITER.join([self.nextAction,
                                              str(ALIVE)])
            
        hpMpStatus = DELIMITER.join([str(targetPos),                                #1
                                     str(targetSprite.inicialHP),                   #2
                                     str(targetSprite.inicialMP),                   #3
                                     str(targetSprite.poison_status_counter),       #4
                                     str(targetSprite.paralyze_status_counter),     #5
                                     str(targetSprite.tired_status_counter),        #6
                                     str(targetSprite.slow_status_counter),         #7
                                     str(targetSprite.mentalBlock_status_counter),  #8
                                     str(targetSprite.alergic_status_counter),      #9
                                     str(targetSprite.haste_status_counter),        #10
                                     str(targetSprite.enchant_status_counter),      #11
                                     str(targetSprite.regenerate_status_counter)])  #12
        if targetPos >=14:
            self.sendMessageAll(hpMpStatus,BATTLE_HP_MP_UPDATE)
    
    def calculateMPDamage(self,receiver,habilityObject):
        #Calculate Soul Attack        
        mpDamage =  (habilityObject.mana_attack*-1) - receiver.magic_defense
        if mpDamage < 0:
            mpDamage = 0
        #Calculate Soul Burn        
        if habilityObject.mana_burn < 0 or habilityObject.mana_burn > 0:
            mpDamage += int((receiver.inicialMP*(habilityObject.mana_burn*-1))/100)
            
        return mpDamage
        
    def calculateHPDamage(self,attacker,receiver,hpDamage,habilityObject):
        auxDamage = 0
        #Calculate Skill Life Burn
        if habilityObject.life_burn < 0 or habilityObject.life_burn > 0:
            hpDamage += int((receiver.inicialHP*(habilityObject.life_burn*-1))/100)
        #Calculate Skill Elemental Damage
        if habilityObject.elemental_damage_electricity < 0:
            auxDamage = int((habilityObject.elemental_damage_electricity*-1)*(habilityObject.attack*-1)/100)
            hpDamage += int(auxDamage - ((receiver.elemental_resist_electricity*auxDamage)/100))
        if habilityObject.elemental_damage_fire < 0:
            auxDamage = int((habilityObject.elemental_damage_fire*-1)*(habilityObject.attack*-1)/100)
            hpDamage += int(auxDamage - ((receiver.elemental_resist_fire*auxDamage)/100))
        if habilityObject.elemental_damage_water < 0:
            auxDamage = int((habilityObject.elemental_damage_water*-1)*(habilityObject.attack*-1)/100)
            hpDamage += int(auxDamage - ((receiver.elemental_resist_water*auxDamage)/100))
        if habilityObject.elemental_damage_earth < 0:
            auxDamage = int((habilityObject.elemental_damage_earth*-1)*(habilityObject.attack*-1)/100)
            hpDamage += int(auxDamage - ((receiver.elemental_resist_earth*auxDamage)/100))
        if habilityObject.elemental_damage_wind < 0:
            auxDamage = int((habilityObject.elemental_damage_wind*-1)*(habilityObject.attack*-1)/100)
            hpDamage += int(auxDamage - ((receiver.elemental_resist_wind*auxDamage)/100))
        if habilityObject.elemental_damage_ice < 0:
            auxDamage = int((habilityObject.elemental_damage_ice*-1)*(habilityObject.attack*-1)/100)
            hpDamage += int(auxDamage - ((receiver.elemental_resist_ice*auxDamage)/100))
        if habilityObject.elemental_damage_dark < 0:
            auxDamage = int((habilityObject.elemental_damage_dark*-1)*(habilityObject.attack*-1)/100)
            hpDamage += int(auxDamage - ((receiver.elemental_resist_dark*auxDamage)/100))
        if habilityObject.elemental_damage_light < 0:
            auxDamage = int((habilityObject.elemental_damage_light*-1)*(habilityObject.attack*-1)/100)
            hpDamage += int(auxDamage - ((receiver.elemental_resist_light*auxDamage)/100))
        
        return hpDamage
    
    def checkBadGoodStatus(self, object, receiver):
        poison = 0
        paralyze = 0
        tired = 0
        slow = 0
        mentalBlock = 0
        alergic = 0
        haste = 0
        enchant = 0
        regenerate = 0
        revive = 0
        gotStatus = False
        
        #Checking Bad Status from Object
        if object.status_inflict_poison > 0:
            if (randint(0,100)) <= (object.status_inflict_poison-receiver.status_resist_poison):
                poison = 14
                gotStatus = True
        if object.status_inflict_paralyze > 0:
            if (randint(0,100)) <= (object.status_inflict_paralyze-receiver.status_resist_paralyze):
                paralyze = 14
                gotStatus = True
        if object.status_inflict_tired > 0:
            if (randint(0,100)) <= (object.status_inflict_tired-receiver.status_resist_tired):
                tired = 14
                gotStatus = True
        if object.status_inflict_slow > 0:
            if (randint(0,100)) <= (object.status_inflict_slow-receiver.status_resist_slow):
                slow = 14
                gotStatus = True
        if object.status_inflict_mentalblock > 0:
            if (randint(0,100)) <= (object.status_inflict_mentalblock-receiver.status_resist_mentalblock):
                mentalBlock = 14
                gotStatus = True
        if object.status_inflict_alergic > 0:
            if (randint(0,100)) <= (object.status_inflict_alergic-receiver.status_resist_alergic):
                alergic = 14
                gotStatus = True
                
        #Checking Good Status from Object
        if object.status_inflict_haste > 0:
            if (randint(0,100)) <= (object.status_inflict_haste):
                haste = 14
                gotStatus = True
        if object.status_inflict_enchant > 0:
            if (randint(0,100)) <= (object.status_inflict_enchant):
                enchant = 14
                gotStatus = True
        if object.status_inflict_regenerate > 0:
            if (randint(0,100)) <= (object.status_inflict_regenerate):
                regenerate = 14
                gotStatus = True
        if object.status_inflict_revive > 0:
            if (randint(0,100)) <= (object.status_inflict_revive):
                revive = 3
                gotStatus = True
                
        #Checking Cure Status
        if object.status_cure_poison > 0:
            if (randint(0,100)) <= (object.status_cure_poison):
                receiver.cured = True
                gotStatus = True
                poison = -28
        if object.status_cure_paralyze > 0:
            if (randint(0,100)) <= (object.status_cure_paralyze):
                receiver.cured = True
                gotStatus = True
                paralyze = -28
        if object.status_cure_tired > 0:
            if (randint(0,100)) <= (object.status_cure_tired):
                receiver.cured = True
                gotStatus = True
                tired = -28
        if object.status_cure_slow > 0:
            if (randint(0,100)) <= (object.status_cure_slow):
                receiver.cured = True
                gotStatus = True
                slow = -28
        if object.status_cure_mentalblock > 0:
            if (randint(0,100)) <= (object.status_cure_mentalblock):
                receiver.cured = True
                gotStatus = True
                mentalBlock = -28
        if object.status_cure_alergic > 0:
            if (randint(0,100)) <= (object.status_cure_alergic):
                receiver.cured = True
                gotStatus = True
                alergic = -28
                
        return poison,paralyze,tired,slow,mentalBlock,alergic,haste,enchant,regenerate,revive,gotStatus
    
    def updatePlayerItem(self, player, itemID, operation):
        if operation == NEW_ITEM:
            pass
        elif operation == LOST_ITEM:
            player.playerAccount.playerCharacter.removeItem(itemID)
            player.sendMessage(itemID,ITEM_REMOVE)
    
    def calculateItemDamage(self,attacker,receiver,originPos,targetPos,itemID):
        self.updatePlayerItem(attacker,itemID, LOST_ITEM)
        
        itemAnimation = ''
        hpDamage = 0
        mpDamage = 0
        poison = 0
        paralyze = 0
        tired = 0
        slow = 0
        mentalBlock = 0
        alergic = 0
        haste = 0
        enchant = 0
        regenerate = 0
        revive = 0

        item = self.items[itemID]
        monsterTarget = True
        loopCount = 1
        
        if item.inicial_target == 1 and attacker.identifier == 'HUMAN':
            monsterTarget = True
        elif item.inicial_target == 0 and attacker.identifier == 'HUMAN':
            monsterTarget = False
        elif item.inicial_target == 1 and attacker.identifier == 'NPC':
            monsterTarget = False
        elif item.inicial_target == 0 and attacker.identifier == 'NPC':
            monsterTarget = True
        if monsterTarget and item.target == 1: # All target and monster target
            loopCount = 13
        elif not monsterTarget and item.target == 1: # All target and player target
            loopCount = 5
            
        if (attacker == self.party_member_1 or attacker == self.party_member_2 or
            attacker == self.party_member_3 or attacker == self.party_member_4 or
            attacker == self.party_member_5):
            attacker = attacker.playerAccount.playerCharacter
        
        if attacker.alergic_status_counter > 0:
            itemAnimation = 'ALERGICFAIL'        
        elif attacker.paralyze_status_counter > 0:
            itemAnimation = 'MOVEFAIL'
        else:
            itemAnimation = str(item.animation)
            
        self.nextAction =     DELIMITER.join([str(item.target),        #(1) 0 - Single Attack, 1 - All Attack
                                              str(2),                  #(2) 0 - FIGHT, 1 - SKILL, 2 - ITEM
                                              str(item.icon),          #(3) Icon
                                              itemAnimation,           #(4) Animation
                                              str(item.animation_time),#(5) Animation Time
                                              str(originPos)           #(6) Origin
                                            ])

        while loopCount > 0:
            loopCount -= 1
            
            if item.target == 1:
                if monsterTarget:
                    targetPos = loopCount
                else:
                    targetPos = loopCount + 14
                receiver = self.findOriginSprite(targetPos)
            
            if (receiver == DEAD or
               itemAnimation == 'MOVEFAIL' or
               itemAnimation == 'ALERGICFAIL'):
                self.nextAction =     DELIMITER.join([self.nextAction,
                                              str(targetPos),  #Target
                                              'N',         #HP DAMAGE: 0 - MISS, N - Don't Show
                                              str(0),             #MP DAMAGE
                                              str(0),               #POISON: 0 - FAIL, >=1 - SUCCESS
                                              str(0),             #PARALYZE: 0 - FAIL, >=1 - SUCCESS
                                              str(0),                #TIRED: 0 - FAIL, >=1 - SUCCESS
                                              str(0),                 #SLOW: 0 - FAIL, >=1 - SUCCESS
                                              str(0),          #MENTALBLOCK: 0 - FAIL, >=1 - SUCCESS
                                              str(0),              #ALERGIC: 0 - FAIL, >=1 - SUCCESS
                                              str(0),                #HASTE: 0 - FAIL, >=1 - SUCCESS
                                              str(0),              #ENCHANT: 0 - FAIL, >=1 - SUCCESS
                                              str(0),           #REGENERATE: 0 - FAIL, >=1 - SUCCESS
                                              str(0),                #REVIVE: 0 - FAIL, >=1 - SUCCESS
                                              'NONE'
                                             ])
            
            else:
                hp = 0
                mp = 0
                hpDamage = 0
                mpDamage = 0
                auxDamage = 0
                poison = 0
                paralyze = 0
                tired = 0
                slow = 0
                mentalBlock = 0
                alergic = 0
                haste = 0
                enchant = 0
                regenerate = 0
                revive = 0
                gotStatus = False
                auxHpDamage = ''
                
                hp = attacker.inicialHP
                mp = attacker.inicialMP
                
                if (receiver == self.party_member_1 or receiver == self.party_member_2 or
                    receiver == self.party_member_3 or receiver == self.party_member_4 or
                    receiver == self.party_member_5):
                    receiver = receiver.playerAccount.playerCharacter
             
                    if item.attack <= 0:
                        if (randint(0,100)) >=  (int(receiver.relative_speed/2)):
                            #Calculate Physical Damage
                            hpDamage = (item.attack*-1) - receiver.relative_defense
                            hpDamage += int((randint(-20,20)*hpDamage)/100)
                            if hpDamage <= 0:
                                hpDamage = 1
                            hpDamage = self.calculateHPDamage(attacker,receiver,hpDamage,item)
                            mpDamage = self.calculateMPDamage(receiver,item)
                        else:
                            hpDamage = 0
                            mpDamage = 0
                    else:
                        hpDamage = (item.attack*-1)
                        hpDamage += int((randint(-20,20)*hpDamage)/100)
                        mpDamage = self.calculateMPDamage(receiver,item)
                
                if hpDamage != 0:
                    poison,paralyze,tired,slow,mentalBlock,alergic,haste,enchant,regenerate,revive,gotStatus = self.checkBadGoodStatus(item,receiver)
                
                auxHpDamage = str(hpDamage)
                
                if item.attack == 0 and not gotStatus:
                    auxHpDamage = '0'
                    hpDamage = 0
                elif item.attack == 0 and gotStatus:
                    auxHpDamage = 'N'
                    hpDamage = 0
                elif item.status_inflict_revive > 0 and not gotStatus:
                    auxHpDamage = '0'
                    hpDamage = 0
                    
                self.nextAction =     DELIMITER.join([self.nextAction,
                                                  str(targetPos),            #Target
                                                  auxHpDamage,               #HP DAMAGE: 0 - MISS, N - Don't Show
                                                  str(mpDamage),             #MP DAMAGE
                                                  str(poison),               #POISON: 0 - FAIL, >=1 - SUCCESS
                                                  str(paralyze),             #PARALYZE: 0 - FAIL, >=1 - SUCCESS
                                                  str(tired),                #TIRED: 0 - FAIL, >=1 - SUCCESS
                                                  str(slow),                 #SLOW: 0 - FAIL, >=1 - SUCCESS
                                                  str(mentalBlock),          #MENTALBLOCK: 0 - FAIL, >=1 - SUCCESS
                                                  str(alergic),              #ALERGIC: 0 - FAIL, >=1 - SUCCESS
                                                  str(haste),                #HASTE: 0 - FAIL, >=1 - SUCCESS
                                                  str(enchant),              #ENCHANT: 0 - FAIL, >=1 - SUCCESS
                                                  str(regenerate),           #REGENERATE: 0 - FAIL, >=1 - SUCCESS
                                                  str(revive)                #REVIVE: 0 - FAIL, ==1 - SUCCESS
                                                 ])

                self.updateDamage(originPos,targetPos,attacker,receiver,hpDamage,mpDamage,poison,paralyze,tired,slow,mentalBlock,alergic,
                                  haste,enchant,regenerate,revive)
                
        self.updateDamage(originPos,originPos,attacker,attacker,0,0,0,0,0,0,0,0,
                                  0,0,0,0)

        self.nextAction =     DELIMITER.join([self.nextAction,
                                              str(item.ID) #Item ID
                                             ])
        self.sendMessageAll(self.nextAction, FINAL_DAMAGE)
        timerEvent = Timer((item.animation_time/100)+TURN_AVERAGE_TIMER, self.freeNextAction)
        timerEvent.start()
    
    def calculateSkillDamage(self,attacker,receiver,originPos,targetPos,skillID):
        skillAnimation = ''
        enoughHP = True
        enoughMP = True
        lifeCostDamage = 0
        hpDamage = 0
        mpDamage = 0
        poison = 0
        paralyze = 0
        tired = 0
        slow = 0
        mentalBlock = 0
        alergic = 0
        haste = 0
        enchant = 0
        regenerate = 0
        revive = 0

        skill = self.skills[skillID]
        monsterTarget = True
        loopCount = 1
        
        if skill.inicial_target == 1 and attacker.identifier == 'HUMAN':
            monsterTarget = True
        elif skill.inicial_target == 0 and attacker.identifier == 'HUMAN':
            monsterTarget = False
        elif skill.inicial_target == 1 and attacker.identifier == 'NPC':
            monsterTarget = False
        elif skill.inicial_target == 0 and attacker.identifier == 'NPC':
            monsterTarget = True
        if monsterTarget and skill.target == 1: # All target and monster target
            loopCount = 13
        elif not monsterTarget and skill.target == 1: # All target and player target
            loopCount = 5
            
        if (attacker == self.party_member_1 or attacker == self.party_member_2 or
            attacker == self.party_member_3 or attacker == self.party_member_4 or
            attacker == self.party_member_5):
            attacker = attacker.playerAccount.playerCharacter
        
        if skill.kind == 1 and skill.mana_cost > attacker.inicialMP:
            skillAnimation = 'MPFAIL'
            enoughMP = False
        elif skill.kind == 0 and skill.life_cost > attacker.inicialHP and attacker.inicialHP <= 1:
            skillAnimation = 'HPFAIL'
            enoughHP = False
        elif skill.kind == 1 and attacker.mentalBlock_status_counter > 0:
            skillAnimation = 'MENTALBLOCKFAIL'
        elif attacker.paralyze_status_counter > 0:
            skillAnimation = 'MOVEFAIL'
        else:
            skillAnimation = str(skill.animation)
            
        self.nextAction =     DELIMITER.join([str(skill.target),        #(1) 0 - Single Attack, 1 - All Attack
                                              str(1),                   #(2) 0 - FIGHT, 1 - SKILL
                                              str(skill.icon),          #(3) Icon
                                              skillAnimation,           #(4) Animation
                                              str(skill.animation_time),#(5) Animation Time
                                              str(originPos)            #(6) Origin
                                            ])

        while loopCount > 0:
            loopCount -= 1
            
            if skill.target == 1:
                if monsterTarget:
                    targetPos = loopCount
                else:
                    targetPos = loopCount + 14
                receiver = self.findOriginSprite(targetPos)
            
            if (receiver == DEAD or
               skillAnimation == 'MOVEFAIL' or
               skillAnimation == 'MENTALBLOCKFAIL' or
               skillAnimation == 'HPFAIL' or
               skillAnimation == 'MPFAIL'):
                self.nextAction =     DELIMITER.join([self.nextAction,
                                              str(targetPos),  #Target
                                              'N',         #HP DAMAGE: 0 - MISS, N - Don't Show
                                              str(0),             #MP DAMAGE
                                              str(0),               #POISON: 0 - FAIL, >=1 - SUCCESS
                                              str(0),             #PARALYZE: 0 - FAIL, >=1 - SUCCESS
                                              str(0),                #TIRED: 0 - FAIL, >=1 - SUCCESS
                                              str(0),                 #SLOW: 0 - FAIL, >=1 - SUCCESS
                                              str(0),          #MENTALBLOCK: 0 - FAIL, >=1 - SUCCESS
                                              str(0),              #ALERGIC: 0 - FAIL, >=1 - SUCCESS
                                              str(0),                #HASTE: 0 - FAIL, >=1 - SUCCESS
                                              str(0),              #ENCHANT: 0 - FAIL, >=1 - SUCCESS
                                              str(0),           #REGENERATE: 0 - FAIL, >=1 - SUCCESS
                                              str(0),                #REVIVE: 0 - FAIL, >=1 - SUCCESS
                                              'NONE'
                                             ])
            
            else:
                magic = 0
                hp = 0
                mp = 0
                strenght = 0
                hpDamage = 0
                mpDamage = 0
                auxDamage = 0
                poison = 0
                paralyze = 0
                tired = 0
                slow = 0
                mentalBlock = 0
                alergic = 0
                haste = 0
                enchant = 0
                regenerate = 0
                revive = 0
                lifeCostDamage = 0
                gotStatus = False
                auxHpDamage = ''
                
                magic = attacker.relative_magic
                strenght = attacker.strenght
                hp = attacker.inicialHP
                mp = attacker.inicialMP
                
                if (receiver == self.party_member_1 or receiver == self.party_member_2 or
                    receiver == self.party_member_3 or receiver == self.party_member_4 or
                    receiver == self.party_member_5):
                    receiver = receiver.playerAccount.playerCharacter
                    
                if skill.kind == 0 and hp > 1:
                    lifeCostDamage = skill.life_cost
                    if skill.life_cost >= hp:
                        lifeCostDamage = hp-1
                    else:
                        lifeCostDamage = skill.life_cost
                        
                    if skill.attack <= 0:
                        if (randint(0,100)) >=  (int(receiver.relative_speed/2)):
                            #Calculate Physical Damage
                            hpDamage = ((skill.attack*strenght)*-1) - receiver.relative_defense
                            hpDamage += int((randint(-20,20)*hpDamage)/100)
                            if hpDamage <= 0:
                                hpDamage = 1
                            hpDamage = self.calculateHPDamage(attacker,receiver,hpDamage,skill)
                            mpDamage = self.calculateMPDamage(receiver,skill)
                        else:
                            hpDamage = 0
                            mpDamage = 0
                    elif skill.attack > 0:
                        hpDamage = ((skill.attack*-1)*strenght)
                        hpDamage += int((randint(-20,20)*hpDamage)/100)
                        mpDamage = self.calculateMPDamage(receiver,skill)
                
                elif skill.kind == 1 and skill.mana_cost <= mp and skillAnimation != 'MENTALBLOCKFAIL':
                    #Calculate Physical Damage
                    if skill.attack <= 0:
                        hpDamage = ((skill.attack*-1)*magic) - receiver.relative_magic_defense
                        if hpDamage <= 0:
                            hpDamage = 1
                    elif skill.attack > 0:
                        hpDamage = (skill.attack*magic)*-1
                    hpDamage += int((randint(-20,20)*hpDamage)/100)
                    hpDamage = self.calculateHPDamage(attacker,receiver,hpDamage,skill)
                    if hpDamage == 0:
                        hpDamage = 1
                    mpDamage = self.calculateMPDamage(receiver,skill)
                
                #Checking All Status from SKill
                if (skill.kind == 1 and enoughMP) or (skill.kind == 0 and hpDamage != 0 and enoughHP):
                    poison,paralyze,tired,slow,mentalBlock,alergic,haste,enchant,regenerate,revive,gotStatus = self.checkBadGoodStatus(skill,receiver)
                
                auxHpDamage = str(hpDamage)
                if skill.attack == 0 and not gotStatus:
                    auxHpDamage = '0'
                    hpDamage = 0
                elif skill.attack == 0 and gotStatus:
                    auxHpDamage = 'N'
                    hpDamage = 0
                elif skill.status_inflict_revive > 0 and not gotStatus:
                    auxHpDamage = '0'
                    hpDamage = 0
                    
                self.nextAction =     DELIMITER.join([self.nextAction,
                                                  str(targetPos),            #Target
                                                  auxHpDamage,               #HP DAMAGE: 0 - MISS, N - Don't Show
                                                  str(mpDamage),             #MP DAMAGE
                                                  str(poison),               #POISON: 0 - FAIL, >=1 - SUCCESS
                                                  str(paralyze),             #PARALYZE: 0 - FAIL, >=1 - SUCCESS
                                                  str(tired),                #TIRED: 0 - FAIL, >=1 - SUCCESS
                                                  str(slow),                 #SLOW: 0 - FAIL, >=1 - SUCCESS
                                                  str(mentalBlock),          #MENTALBLOCK: 0 - FAIL, >=1 - SUCCESS
                                                  str(alergic),              #ALERGIC: 0 - FAIL, >=1 - SUCCESS
                                                  str(haste),                #HASTE: 0 - FAIL, >=1 - SUCCESS
                                                  str(enchant),              #ENCHANT: 0 - FAIL, >=1 - SUCCESS
                                                  str(regenerate),           #REGENERATE: 0 - FAIL, >=1 - SUCCESS
                                                  str(revive)                #REVIVE: 0 - FAIL, ==1 - SUCCESS
                                                 ])

                self.updateDamage(originPos,targetPos,attacker,receiver,hpDamage,mpDamage,poison,paralyze,tired,slow,mentalBlock,alergic,
                                  haste,enchant,regenerate,revive)
                
        if skill.kind == 1 and enoughMP:
            self.updateDamage(originPos,originPos,attacker,attacker,0,skill.mana_cost,0,0,0,0,0,0,
                              0,0,0,0)
        elif skill.kind == 0 and enoughHP:
            self.updateDamage(originPos,originPos,attacker,attacker,lifeCostDamage,0,0,0,0,0,0,0,
                              0,0,0,0)
        else:
            self.updateDamage(originPos,originPos,attacker,attacker,0,0,0,0,0,0,0,0,
                              0,0,0,0)

        self.nextAction =     DELIMITER.join([self.nextAction,
                                              str(skill.ID) #Skill ID
                                             ])
        self.sendMessageAll(self.nextAction, FINAL_DAMAGE)
        timerEvent = Timer((skill.animation_time/100)+TURN_AVERAGE_TIMER, self.freeNextAction)
        timerEvent.start()
                
 
    def calculateFightDamage(self,attacker,receiver,originPos,targetPos):
        weapon = None
        playerAttack = 0
        hpDamage = 0
        mpDamage = 0
        auxDamage = 0
        poison = 0
        paralyze = 0
        tired = 0
        slow = 0
        mentalBlock = 0
        alergic = 0
        haste = 0
        enchant = 0
        regenerate = 0
        revive = 0
        gotStatus = False
        
        if (attacker == self.party_member_1 or attacker == self.party_member_2 or
            attacker == self.party_member_3 or attacker == self.party_member_4 or
            attacker == self.party_member_5):
            weapon = self.items[attacker.playerAccount.playerCharacter.equipped_RightHand]
            playerAttack = attacker.playerAccount.playerCharacter.relative_attack
        
        #Check if the enemy can dodge the attack
        if (randint(0,100)) >=  (int(receiver.relative_speed/2)):
            #Calculate Physical Damage
            hpDamage = playerAttack - receiver.relative_defense
            hpDamage += int((randint(-20,20)*hpDamage)/100)
            if hpDamage <= 0:
                hpDamage = 1
            hpDamage = self.calculateHPDamage(attacker,receiver,hpDamage,weapon)
            mpDamage = self.calculateMPDamage(receiver,weapon)
            
            #Checking All Status from Weapon
            poison,paralyze,tired,slow,mentalBlock,alergic,haste,enchant,regenerate,revive,gotStatus = self.checkBadGoodStatus(weapon,receiver)
            
        else:
            hpDamage = 0
            mpDamage = 0
            
        self.nextAction =     DELIMITER.join([str(0),                    #(1) 0 - Single Attack, 1 - All Attack
                                              str(0),                    #(2) 0 - FIGHT, 1 - SKILL
                                              str(weapon.icon),          #(3) Icon
                                              str(weapon.animation),     #(4) Animation
                                              str(weapon.animation_time),#(5) Animation Time
                                              str(originPos),            #(6) Origin
                                              str(targetPos),            #(7) Target
                                              str(hpDamage),             #(8) HP DAMAGE: 0 - MISS
                                              str(mpDamage),             #(9) MP DAMAGE
                                              str(poison),               #(10) POISON: 0 - FAIL, >=1 - SUCCESS
                                              str(paralyze),             #(11) PARALYZE: 0 - FAIL, >=1 - SUCCESS
                                              str(tired),                #(12) TIRED: 0 - FAIL, >=1 - SUCCESS
                                              str(slow),                 #(13) SLOW: 0 - FAIL, >=1 - SUCCESS
                                              str(mentalBlock),          #(14) MENTALBLOCK: 0 - FAIL, >=1 - SUCCESS
                                              str(alergic),              #(15) ALERGIC: 0 - FAIL, >=1 - SUCCESS
                                              str(haste),                #(16) HASTE: 0 - FAIL, >=1 - SUCCESS
                                              str(enchant),              #(17) ENCHANT: 0 - FAIL, >=1 - SUCCESS
                                              str(regenerate),           #(18) REGENERATE: 0 - FAIL, >=1 - SUCCESS
                                              str(revive)                #(19) REVIVE: 0 - FAIL, ==1 - SUCCESS
                            ])

        self.updateDamage(originPos,targetPos,attacker,receiver,hpDamage,mpDamage,poison,paralyze,tired,slow,mentalBlock,alergic,
                          haste,enchant,regenerate,revive)
        self.sendMessageAll(self.nextAction, FINAL_DAMAGE)
        timerEvent = Timer((weapon.animation_time/100)+TURN_AVERAGE_TIMER, self.freeNextAction)
        timerEvent.start()
    
    def findPlayerPosition(self, playerObj):
        if playerObj == self.party_member_1:
                return 14
        elif playerObj == self.party_member_2:
                return 15
        elif playerObj == self.party_member_3:
                return 16
        elif playerObj == self.party_member_4:
                return 17
        elif playerObj == self.party_member_5:
                return 18
        else:
            return 0
    
    def playerFight(self, attacker, targetPos):
        origin = self.findPlayerPosition(attacker)
                
        self.actionQuery.append(Action(0,origin,targetPos,0))
        if len(self.actionQuery) == 1:
            self.checkNextAction()
    
    def playerSkill(self, attacker, targetPos, skillID):
        origin = self.findPlayerPosition(attacker)
                
        self.actionQuery.append(Action(1,origin,targetPos,skillID))
        if len(self.actionQuery) == 1:
            self.checkNextAction()
            
    def playerItem(self, attacker, targetPos, itemID):
        origin = self.findPlayerPosition(attacker)

        self.actionQuery.append(Action(2,origin,targetPos,itemID))
        if len(self.actionQuery) == 1:
            self.checkNextAction()
            
    def monsterGeneralMove(self, monsterObject,originPos):
        skillID = 0
        target = 0
        skill = None
        if monsterObject.inicialHP > 0:
            
            skillID = monsterObject.sortSkills()
            skill = self.skills[skillID]
            if skill.inicial_target == 0:
                target = self.monsterSortList[randint(0,len(self.monsterSortList)-1)]
            else:
                target = self.playerSortList[randint(0,len(self.playerSortList)-1)]
            self.actionQuery.append(Action(1,originPos,target,skillID))
            if len(self.actionQuery) == 1:
                self.checkNextAction()
     
    def monster1Move(self):
        self.monsterGeneralMove(self.monster_1,1)
    def monster2Move(self):
        self.monsterGeneralMove(self.monster_2,2)
    def monster3Move(self):
        self.monsterGeneralMove(self.monster_3,3)
    def monster4Move(self):
        self.monsterGeneralMove(self.monster_4,4)
    def monster5Move(self):
        self.monsterGeneralMove(self.monster_5,5)
    def monster6Move(self):
        self.monsterGeneralMove(self.monster_6,6)
    def monster7Move(self):
        self.monsterGeneralMove(self.monster_7,7)
    def monster8Move(self):
        self.monsterGeneralMove(self.monster_8,8)
    def monster9Move(self):
        self.monsterGeneralMove(self.monster_9,9)
    def monster10Move(self):
        self.monsterGeneralMove(self.monster_10,10)
    def monster11Move(self):
        self.monsterGeneralMove(self.monster_11,11)
    def monster12Move(self):
        self.monsterGeneralMove(self.monster_12,12)
    def monster13Move(self):
        self.monsterGeneralMove(self.monster_13,13)
     
    def calculateLoadTime(self,player):
        waitSeconds = 0
        waitPercent = 0
        playerObject = self.findOriginSprite(player)
        if playerObject != DEAD:
            if player >= 14:
                if playerObject.playerAccount.playerCharacter.relative_speed == 0:
                    waitSeconds = 0
                    waitPercent = 0
                else:
                    waitSeconds = float(self.averageTurnTime) / float(playerObject.playerAccount.playerCharacter.relative_speed)
                    if waitSeconds < 1:
                        waitSeconds = 1
                    waitPercent = (float(self.averageTurnTime) / float(waitSeconds))/float(self.averageTurnTime)
                playerObject.sendMessage(str(waitPercent), TURN_LOAD_TIME)
     
    def calculateTurnWait(self, player):
        waitSeconds = 0
        waitPercent = 0
        playerObject = self.findOriginSprite(player)
        if playerObject != DEAD:
            if player > 0 and player <= 13:
                if playerObject.relative_speed == 0:
                    waitSeconds = 0
                    waitPercent = 0
                else:
                    waitSeconds = float(self.averageTurnTime) / float(playerObject.relative_speed)
                    if waitSeconds < 1:
                        waitSeconds = 1
                    waitPercent = (float(self.averageTurnTime) / float(waitSeconds))/float(self.averageTurnTime)
                if waitSeconds > 0:
                    if playerObject == self.monster_1 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster1Move)
                    elif playerObject == self.monster_2 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster2Move)
                    elif playerObject == self.monster_3 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster3Move)
                    elif playerObject == self.monster_4 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster4Move)
                    elif playerObject == self.monster_5 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster5Move)
                    elif playerObject == self.monster_6 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster6Move)
                    elif playerObject == self.monster_7 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster7Move)
                    elif playerObject == self.monster_8 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster8Move)
                    elif playerObject == self.monster_9 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster9Move)
                    elif playerObject == self.monster_10 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster10Move)
                    elif playerObject == self.monster_11 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster11Move)
                    elif playerObject == self.monster_12 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster12Move)
                    elif playerObject == self.monster_13 and playerObject.inicialHP > 0:
                        timerEvent = Timer(waitSeconds,self.monster13Move)
                    timerEvent.start()
            elif player >= 14:
                if playerObject.playerAccount.playerCharacter.relative_speed == 0:
                    waitSeconds = 0
                    waitPercent = 0
                else:
                    waitSeconds = float(self.averageTurnTime) / float(playerObject.playerAccount.playerCharacter.relative_speed)
                    if waitSeconds < 1:
                        waitSeconds = 1
                    waitPercent = float(float(self.averageTurnTime / waitSeconds))/float(self.averageTurnTime)
                playerObject.sendMessage(str(waitPercent), TURN_LOAD_TIME)
                if waitSeconds > 0:
                    timerEvent = CustomTimer(waitSeconds, player, playerObject)
                    timerEvent.start()
            
    def battleOpen(self):
        self.sendMessageAll(1,BATTLE_LOAD_COMPLETE)
        if self.party_member_1 and self.party_member_1.playerAccount.playerCharacter.inicialHP > 0:
            self.calculateTurnWait(14)
        if self.party_member_2 and self.party_member_2.playerAccount.playerCharacter.inicialHP > 0:
            self.calculateTurnWait(15)
        if self.party_member_3 and self.party_member_3.playerAccount.playerCharacter.inicialHP > 0:
            self.calculateTurnWait(16)
        if self.party_member_4 and self.party_member_4.playerAccount.playerCharacter.inicialHP > 0:
            self.calculateTurnWait(17)
        if self.party_member_5 and self.party_member_5.playerAccount.playerCharacter.inicialHP > 0:
            self.calculateTurnWait(18)
        for i in range (1,14):
            self.calculateTurnWait(i)
        self.statusThread = TaskThread(self.statusList, self.party_member_1, self.party_member_2,
                                       self.party_member_3,self.party_member_4,self.party_member_5,
                                       self.monster_1,self.monster_2,self.monster_3,self.monster_4,
                                       self.monster_5,self.monster_6,self.monster_7,self.monster_8,
                                       self.monster_9,self.monster_10,self.monster_11,self.monster_12,
                                       self.monster_13, self)
        self.statusThread.start()
    
    def calculateAverageTurnTime(self):
        speedSum = 0
        
        if self.monster_1.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_1.relative_speed
        if self.monster_2.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_2.relative_speed
        if self.monster_3.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_3.relative_speed
        if self.monster_4.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_4.relative_speed
        if self.monster_5.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_5.relative_speed
        if self.monster_6.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_6.relative_speed
        if self.monster_7.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_7.relative_speed
        if self.monster_8.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_8.relative_speed
        if self.monster_9.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_9.relative_speed
        if self.monster_10.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_10.relative_speed
        if self.monster_11.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_11.relative_speed
        if self.monster_12.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_12.relative_speed
        if self.monster_13.ID != 0:
            self.playersMonstersCount += 1
            speedSum += self.monster_13.relative_speed
        if self.party_member_1:
            self.playersMonstersCount += 1
            speedSum += self.party_member_1.playerAccount.playerCharacter.relative_speed
        if self.party_member_2:
            self.playersMonstersCount += 1
            speedSum += self.party_member_2.playerAccount.playerCharacter.relative_speed
        if self.party_member_3:
            self.playersMonstersCount += 1
            speedSum += self.party_member_3.playerAccount.playerCharacter.relative_speed
        if self.party_member_4:
            self.playersMonstersCount += 1
            speedSum += self.party_member_4.playerAccount.playerCharacter.relative_speed
        if self.party_member_5:
            self.playersMonstersCount += 1
            speedSum += self.party_member_5.playerAccount.playerCharacter.relative_speed
            
        self.averageTurnTime = int((speedSum/self.playersMonstersCount)*10)
        self.checkPlayersMonstersAlive()
    
    def battleInit(self):
        self.calculateAverageTurnTime()
        battleInitTimer = Timer(BATTLE_START_COUNTDOWN, self.battleOpen)
        battleInitTimer.start()
    
    def checkBattleWin(self):
        if (self.monster_1.inicialHP == 0 and self.monster_2.inicialHP == 0 and self.monster_3.inicialHP == 0 and
            self.monster_4.inicialHP == 0 and self.monster_5.inicialHP == 0 and self.monster_6.inicialHP == 0 and
            self.monster_7.inicialHP == 0 and self.monster_8.inicialHP == 0 and self.monster_9.inicialHP == 0 and
            self.monster_10.inicialHP == 0 and self.monster_11.inicialHP == 0 and self.monster_12.inicialHP == 0 and
            self.monster_13.inicialHP == 0):
            return True
        
    def checkBattleLose(self):
        playerDeadCount = 0
        if self.party_member_1:
            if self.party_member_1.playerAccount.playerCharacter.inicialHP == 0:
                playerDeadCount +=1
        else:
            playerDeadCount +=1
        if self.party_member_2:
            if self.party_member_2.playerAccount.playerCharacter.inicialHP == 0:
                playerDeadCount +=1
        else:
            playerDeadCount +=1
        if self.party_member_3:
            if self.party_member_3.playerAccount.playerCharacter.inicialHP == 0:
                playerDeadCount +=1
        else:
            playerDeadCount +=1
        if self.party_member_4:
            if self.party_member_4.playerAccount.playerCharacter.inicialHP == 0:
                playerDeadCount +=1
        else:
            playerDeadCount +=1
        if self.party_member_5:
            if self.party_member_5.playerAccount.playerCharacter.inicialHP == 0:
                playerDeadCount +=1
        else:
            playerDeadCount +=1
        
        if playerDeadCount == 5:
            return True
        else:
            return False
    
    def deactivateBattleWin(self):
        currentPlayer = None
        for iter in self.playerSortList:
            currentPlayer = self.findAnySprite(iter)
            if currentPlayer:
                if currentPlayer.playerAccount.playerCharacter.inicialHP <= 0:
                    currentPlayer.playerAccount.playerCharacter.inicialHP = 1
                currentPlayer.playerAccount.playerCharacter.inBattle = False
                currentPlayer.playerAccount.playerCharacter.battleID = -1
                currentPlayer.playerAccount.playerCharacter.battleStepCounter = 15
                currentPlayer.sendMessage(WON,DEACTIVATE_BATTLE)
            else:
                pass
        self.battles.remove(self)
        self.statusThread.shutdown()
        del self
        #END OF BATTLE
        
    def deactivateBattleLose(self):
        currentPlayer = None
        map = None
        posX = 20
        posY = 20
        for iter in self.playerSortList:
            currentPlayer = self.findAnySprite(iter)
            if currentPlayer:
                currentPlayer.playerAccount.playerCharacter.inicialHP = 1
                currentPlayer.playerAccount.playerCharacter.inBattle = False
                currentPlayer.playerAccount.playerCharacter.battleID = -1
                destinationMap = self.maps[self.findMap(currentPlayer.playerAccount.playerCharacter.reload_map)]
                changeMap.mapChange(currentPlayer,destinationMap,posX,posY,self.fact)
            else:
                pass
        self.battles.remove(self)
        self.statusThread.shutdown()
        del self
        #END OF BATTLE
            
    
    def splitExpGoldItems(self):
        expSplit = 0
        goldSplit = 0
        currentPlayer = None
        message = ''
        expSplit = int(self.expObtained/len(self.playerSortList))
        goldSplit = int(self.goldObtained/len(self.playerSortList))
        for iter in self.playerSortList:
            currentPlayer = self.findAnySprite(iter)
            currentPlayer.playerAccount.playerCharacter.exp += expSplit
            currentPlayer.playerAccount.playerCharacter.gold += goldSplit
            levelUp.checkLevelUp(currentPlayer)
            message = DELIMITER.join([str(expSplit),
                                      str(goldSplit)])
            currentPlayer.sendMessage(message,END_BATTLE_WON)
        timerEvent = Timer(DISAPPEAR_BATTLE_TIMER, self.deactivateBattleWin)
        timerEvent.start()
        
    def reduceGoldItems(self):
        currentPlayer = None
        expLost = 0
        goldLost = 0
        message = ''
        for iter in self.playerSortList:
            currentPlayer = self.findAnySprite(iter)
            expLost = int((currentPlayer.playerAccount.playerCharacter.exp*15)/100)
            goldLost = int((currentPlayer.playerAccount.playerCharacter.gold*30)/100)
            currentPlayer.playerAccount.playerCharacter.exp -= expLost
            currentPlayer.playerAccount.playerCharacter.gold -= goldLost
            message = DELIMITER.join([str(expLost),
                                      str(goldLost)])
            currentPlayer.sendMessage(message,END_BATTLE_LOSE)
        timerEvent = Timer(DISAPPEAR_BATTLE_TIMER, self.deactivateBattleLose)
        timerEvent.start()
            
            
    def freeNextAction(self):
        self.actionQuery.pop(0)
        if self.checkBattleWin():
            self.splitExpGoldItems()
        elif self.checkBattleLose():
            self.reduceGoldItems()
        else:
            self.checkNextAction()
    
    def findAnySprite(self, position):
        if position == 14 and self.party_member_1:
            if len(self.actionQuery) > 0:
                self.actionQuery[0].target = position
            return self.party_member_1
        elif position == 15 and self.party_member_2:
            if len(self.actionQuery) > 0:
                self.actionQuery[0].target = position
            return self.party_member_2
        elif position == 16 and self.party_member_3:
            if len(self.actionQuery) > 0:
                self.actionQuery[0].target = position
            return self.party_member_3
        elif position == 17 and self.party_member_4:
            if len(self.actionQuery) > 0:
                self.actionQuery[0].target = position
            return self.party_member_4
        elif position == 18 and self.party_member_5:
            if len(self.actionQuery) > 0:
                self.actionQuery[0].target = position
            return self.party_member_5
        else:
            return None
                
    def checkNextAction(self):
        attacker = None
        receiver = None
        self.calculateTurnWait(self.lastOrigin)
        self.lastOrigin = 0
        if len(self.actionQuery) > 0:
            attacker = self.findOriginSprite(self.actionQuery[0].origin)
            if self.actionQuery[0].target <19:
                if self.skills[self.actionQuery[0].skillID].status_inflict_revive > 0:
                    receiver = self.findAnySprite(self.actionQuery[0].target)
                    if not receiver:
                        self.freeNextAction()
                        return
                else:
                    receiver = self.findTargetSprite(self.actionQuery[0].target)
            if attacker != DEAD:
                if self.actionQuery[0].kind == 0:# FIGHT
                    self.calculateFightDamage(attacker,receiver,self.actionQuery[0].origin,self.actionQuery[0].target)
                elif self.actionQuery[0].kind == 1:# SKILL
                    self.calculateSkillDamage(attacker,receiver,self.actionQuery[0].origin,self.actionQuery[0].target, self.actionQuery[0].skillID)
                elif self.actionQuery[0].kind == 2:# ITEM
                    self.calculateItemDamage(attacker,receiver,self.actionQuery[0].origin,self.actionQuery[0].target, self.actionQuery[0].skillID)
            else:
                self.freeNextAction()

    def checkPlayersMonstersAlive(self):
        #Monsters
        if self.monster_1.inicialHP > 0:
            self.monsterSortList.append(1)
        if self.monster_2.inicialHP > 0:
            self.monsterSortList.append(2)
        if self.monster_3.inicialHP > 0:
            self.monsterSortList.append(3)
        if self.monster_4.inicialHP > 0:
            self.monsterSortList.append(4)
        if self.monster_5.inicialHP > 0:
            self.monsterSortList.append(5)
        if self.monster_6.inicialHP > 0:
            self.monsterSortList.append(6)
        if self.monster_7.inicialHP > 0:
            self.monsterSortList.append(7)
        if self.monster_8.inicialHP > 0:
            self.monsterSortList.append(8)
        if self.monster_9.inicialHP > 0:
            self.monsterSortList.append(9)
        if self.monster_10.inicialHP > 0:
            self.monsterSortList.append(10)
        if self.monster_11.inicialHP > 0:
            self.monsterSortList.append(11)
        if self.monster_12.inicialHP > 0:
            self.monsterSortList.append(12)
        if self.monster_13.inicialHP > 0:
            self.monsterSortList.append(13)
        
        #Players
        if self.party_member_1:
            if self.party_member_1.playerAccount.playerCharacter.inicialHP > 0:
                self.playerSortList.append(14)
        if self.party_member_2:
            if self.party_member_2.playerAccount.playerCharacter.inicialHP > 0:
                self.playerSortList.append(15)
        if self.party_member_3:
            if self.party_member_3.playerAccount.playerCharacter.inicialHP > 0:
                self.playerSortList.append(16)
        if self.party_member_4:
            if self.party_member_4.playerAccount.playerCharacter.inicialHP > 0:
                self.playerSortList.append(17)
        if self.party_member_5:
            if self.party_member_5.playerAccount.playerCharacter.inicialHP > 0:
                self.playerSortList.append(18)

    def playerChat(self, player, message):
        if player == self.party_member_1:
            self.sendMessageAll(DELIMITER2.join(['14', message]),BATTLE_CHAT)
        elif player == self.party_member_2:
            self.sendMessageAll(DELIMITER2.join(['15', message]),BATTLE_CHAT)
        elif player == self.party_member_3:
            self.sendMessageAll(DELIMITER2.join(['16', message]),BATTLE_CHAT)
        elif player == self.party_member_4:
            self.sendMessageAll(DELIMITER2.join(['17', message]),BATTLE_CHAT)
        elif player == self.party_member_5:
            self.sendMessageAll(DELIMITER2.join(['18', message]),BATTLE_CHAT)
        

class Action(object):

    def __init__(self, kind, origin, target, skillID):
        self.kind = kind        #0:FIGHT - 1:SKILL - 2:ITEM
        self.origin = origin    #ORIGIN
        self.target = target    #TARGET
        self.skillID = skillID  #SKILL ID
        
class Status(object):
    def __init__(self, targetSprite, targetPos):
        self.targetSprite = targetSprite
        self.targetPos = targetPos

