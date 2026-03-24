# Copyright (c) 2010 Cassio Maciel.

import os
import yaml
import kinterbasdb
import sys
import traceback

from threading import Timer
from item import Item
from random import randint

DELIMITER = ','
DELIMITER2 = ':'

MOVE_TIMER = 0.1
BALOON_TIMER = 6.5

#Classes
APPRENTICE = 0
WARRIOR = 1
MAGE = 2
ARCHER = 3
BARBARIAN = 4
KNIGHT = 5
PALADIN = 6
ELEMENTALIST = 7
NECROMANCER = 8
CLERIC = 9
ASSASSIN = 10
RANGER = 11
HUNTER = 12

def formatExceptionInfo(maxTBlevel=5):
         cla, exc, trbk = sys.exc_info()
         excName = cla.__name__
         try:
             excArgs = exc.__dict__["args"]
         except KeyError:
             excArgs = "<no args>"
         excTb = traceback.format_tb(trbk, maxTBlevel)
         return (excName, excArgs, excTb)

class PlayerCharacter(object):

    def __init__(self, accountXGold):
        #Basic Attributes
        self.ID = 0
        self.starting_PosX = 0
        self.starting_PosY = 0
        self.starting_Map = 0
        self.inicialHP = 0
        self.inicialMP = 0
        self.inicialOutFitHeadID = 0
        self.inicialOutFitBodyID = 0
        self.inicialOutFitLegID = 0
        self.name = ''
        self.cLevel = 0
        self.gender = 0
        self.hp = 0
        self.mp = 0
        self.cClass = 0
        self.strenght = 0
        self.physical = 0
        self.mind = 0
        self.agility = 0
        self.equipped_RightHand = 0
        self.equipped_LeftHand = 0
        self.equipped_Body = 0
        self.equipped_Head = 0
        self.equipped_Accessory = 0
        self.skill_list = []
        self.magic_list = []
        self.item_list = []
        self.exp = 0
        self.nextExp = 0
        self.gold = 0
        self.xGold = accountXGold
        self.remaining_attributes = 0
        
        #Secondary Attibutes
        self.attack = 0
        self.defense = 0
        self.magic_defense = 0
        self.magic = 0
        self.speed = 0
        self.strenghtBonus = 0
        self.physicalBonus = 0
        self.mindBonus = 0
        self.agilityBonus = 0
        
        #Battle Relative Secondary Attributes
        self.relative_attack = 0
        self.relative_defense = 0
        self.relative_magic_defense = 0
        self.relative_magic = 0
        self.relative_speed = 0
        
        #Elemental Resistances
        self.elemental_resist_electricity = 0
        self.elemental_resist_fire = 0
        self.elemental_resist_water = 0
        self.elemental_resist_earth = 0
        self.elemental_resist_wind = 0
        self.elemental_resist_ice = 0
        self.elemental_resist_dark = 0
        self.elemental_resist_light = 0
        
        #Status Resistances
        self.status_resist_poison = 0
        self.status_resist_paralyze = 0
        self.status_resist_tired = 0
        self.status_resist_slow = 0
        self.status_resist_mentalblock = 0
        self.status_resist_alergic = 0
        
        #Status counters
        self.poison_status_counter = 0 #>1 = With Status, 0 = Reverted
        self.paralyze_status_counter = 0 #>1 = With Status, 0 = Reverted
        self.tired_status_counter = 0 #>1 = With Status, 0 = Reverted
        self.slow_status_counter = 0 #>1 = With Status, 0 = Reverted
        self.mentalBlock_status_counter = 0 #>1 = With Status, 0 = Reverted
        self.alergic_status_counter = 0 #>1 = With Status, 0 = Reverted
        self.haste_status_counter = 0 #>1 = With Status, 0 = Reverted
        self.enchant_status_counter = 0 #>1 = With Status, 0 = Reverted
        self.regenerate_status_counter = 0 #>1 = With Status, 0 = Reverted
        self.revive_status_counter = 0 #>1 = Revived
        
        #Other
        self.cured = False
        self.tempX = 0
        self.tempY = 0
        self.lastX = 0
        self.lastY = 0
        self.blockTrigger = False # True = cannot move yet, False = can move
        self.baloonBlocker = 0 # > 0 cannot disappear baloon
        self.inAParty = False
        self.partyID = -1 #Party ID
        self.battleStepCounter = 15 #0 = Battle triggered, >0 = Counting
        self.hostileArea = False
        self.inBattle = False
        self.battleID = -1 #Battle ID
        
        self.identifier = 'PLAYER'
    
    def populate(self, con, charPos):
        try:
            cur = con.cursor()
                
            cur.execute("SELECT * FROM game_character WHERE id="+str(charPos))
                
            for row in cur:
                self.ID = row[0]
                self.starting_PosX = row[1]
                self.starting_PosY = row[2]
                self.starting_Map = row[3]
                self.inicialHP = row[4]
                self.inicialMP = row[5]
                self.inicialOutFitHeadID = row[6]
                self.inicialOutFitBodyID = row[7]
                self.inicialOutFitLegID = row[8]
                self.name = row[9]
                self.cLevel = row[10]
                self.gender = row[11]
                self.hp = row[12]
                self.mp = row[13]
                self.cClass = row[14]
                self.strenght = row[15]
                self.physical = row[16]
                self.mind = row[17]
                self.agility = row[18]
                self.equipped_RightHand = row[19]
                self.equipped_LeftHand = row[20]
                self.equipped_Body = row[21]
                self.equipped_Head = row[22]
                self.equipped_Accessory = row[23]
                self.exp = row[24]
                self.nextExp = row[25]
                self.gold = row[26]
                self.remaining_attributes = row[27]
                self.initial_direction = row[28]
                self.reload_map = row[29]
                
                self.tempX = self.starting_PosX
                self.tempY = self.starting_PosY
                
            cur.execute("SELECT item_id, quantity FROM item_list WHERE character_id="+str(charPos))
            for row in cur:
                self.item_list.append(Item(row[0],row[1]))
                    
                    
            cur.execute("SELECT hability_number, hlevel FROM habilities_list WHERE character_id="+str(charPos))
                
            for row in cur:
                self.skill_list.append(Skill(row[0],row[1]))
                    
            cur.execute("SELECT magic_number, mlevel FROM magic_list WHERE character_id="+str(charPos))
                
            for row in cur:
                self.magic_list.append(Magic(row[0],row[1]))
            
        except:
            print '!!!!!!!!!!!!Exception caught on PlayerCharacter() in populate()!!!!!!!!!!!!'
            print formatExceptionInfo()
            return 0
        return 1
    
    #Check if the Outfit exists in player inventory
    def checkOutfitItem(self, itemID, item):
        for iter in self.item_list:
            if iter.ID == itemID:   
                if item.outfit_gender != 0 and item.outfit_gender != self.gender+1:
                    return False
                elif (item.class_restriction == 1 and (
                   self.cClass != 1 and self.cClass != 4 and
                   self.cClass != 5 and self.cClass != 6)):
                    return False
                elif (item.class_restriction == 2 and (
                   self.cClass != 2 and self.cClass != 7 and
                   self.cClass != 8 and self.cClass != 9)):
                    return False
                elif (item.class_restriction == 3 and (
                   self.cClass != 3 and self.cClass != 10 and
                   self.cClass != 11 and self.cClass != 12)):
                    return False
                elif item.class_restriction > 3 and item.class_restriction != self.cClass:
                    return False
                else:
                    if item.outfit_type == 0:
                        self.inicialOutFitHeadID = item.spc_id
                    elif item.outfit_type == 1:
                        self.inicialOutFitBodyID = item.spc_id
                    elif item.outfit_type == 2:
                        self.inicialOutFitLegID = item.spc_id
                    return True
                    break
                
        return False
    
    def moveTrigger(self):
        self.blockTrigger = False
    
    def checkLegitMove(self, dir):
        if not self.blockTrigger and not self.inBattle:
            timerEvent = Timer(MOVE_TIMER, self.moveTrigger)
            if dir == '1':
                self.tempX = self.starting_PosX+1
            elif dir == '2':
                self.tempY = self.starting_PosY+1
            elif dir == '3':
                self.tempX = self.starting_PosX-1
            elif dir == '4':
                self.tempY = self.starting_PosY-1
            else:
                return False
            self.blockTrigger = True
            timerEvent.start()
            return True
        return False
    
    def checkBattle(self):
        if self.hostileArea:
            self.battleStepCounter = self.battleStepCounter - randint(1,5)
            if self.battleStepCounter <= 0:
                self.battleStepCounter = 15
                return True
            else:
                return False
        return False
    
    def completeMove(self):
            self.starting_PosX = self.tempX
            self.starting_PosY = self.tempY
                
    
    def baloonTrigger(self):
        self.baloonBlocker  = self.baloonBlocker - 1
    
    def baloonTimerStart(self):
        timerEvent = Timer(BALOON_TIMER, self.baloonTrigger)
        self.baloonBlocker = self.baloonBlocker + 1
        timerEvent.start()
        
    def requestCHMIHability(self):
        response = '0:0'
        part = ''
        for iter in self.skill_list:
            part = DELIMITER2.join([str(iter.ID),str(iter.level)])
            response = DELIMITER.join([response,part])
        return response
    
    def requestCHMIMagic(self):
        response = '0:0'
        part = ''
        for iter in self.magic_list:
            part = DELIMITER2.join([str(iter.ID),str(iter.level)])
            response = DELIMITER.join([response,part])
        return response
    
    def requestCHMIItem(self):
        response = '0:0'
        part = ''
        for iter in self.item_list:
            part = DELIMITER2.join([str(iter.ID),str(iter.quantity)])
            response = DELIMITER.join([response,part])
        return response
                
    def updateBonuses(self, eRhand, eLhand, eBody, eHead, eAcc):
        
        #Strenght Bonus Calculation
        if (self.strenght + (eRhand.strenght + eLhand.strenght + eBody.strenght + eHead.strenght + eAcc.strenght)) <= 0:
            self.strenghtBonus = (self.strenght * -1) + 1
        elif (self.strenght + (eRhand.strenght + eLhand.strenght + eBody.strenght + eHead.strenght + eAcc.strenght)) > 0:
            self.strenghtBonus = (eRhand.strenght + eLhand.strenght + eBody.strenght + eHead.strenght + eAcc.strenght)
            
        #Physical Bonus Calculation
        if (self.physical + (eRhand.physical + eLhand.physical + eBody.physical + eHead.physical + eAcc.physical)) <= 0:
            self.physicalBonus = (self.physical * -1) + 1
        elif (self.physical + (eRhand.physical + eLhand.physical + eBody.physical + eHead.physical + eAcc.physical)) > 0:
            self.physicalBonus = (eRhand.physical + eLhand.physical + eBody.physical + eHead.physical + eAcc.physical)
            
        #Mind Bonus Calculation
        if (self.mind + (eRhand.mind + eLhand.mind + eBody.mind + eHead.mind + eAcc.mind)) <= 0:
            self.mindBonus = (self.mind * -1) + 1
        elif (self.strenght + (eRhand.mind + eLhand.mind + eBody.mind + eHead.mind + eAcc.mind)) > 0:
            self.mindBonus = (eRhand.mind + eLhand.mind + eBody.mind + eHead.mind + eAcc.mind)
        
        #Agility Bonus Calculation
        if (self.agility + (eRhand.agility + eLhand.agility + eBody.agility + eHead.agility + eAcc.agility)) <= 0:
            self.agilityBonus = (self.agility * -1) + 1
        elif (self.agility + (eRhand.agility + eLhand.agility + eBody.agility + eHead.agility + eAcc.agility)) > 0:
            self.agilityBonus = (eRhand.agility + eLhand.agility + eBody.agility + eHead.agility + eAcc.agility)
    
    def updateStatusHpMp(self, eRhand, eLhand, eBody, eHead, eAcc):

        #Native HP AND MP, By Level And Class
        if self.cClass == APPRENTICE:
            self.hp = int((self.physical + self.physicalBonus)*(self.cLevel)*(2.5))
            self.mp = int((self.mind + self.mindBonus)*(self.cLevel)*(2))
            
        #HP Increase By Equipment
        if eRhand.life_increase > 0:
            self.hp = self.hp + int((self.hp * eRhand.life_increase)/100)
        elif eRhand.life_increase < 0:
            self.hp = self.hp + int((eRhand.life_increase)*-1)
        if eLhand.life_increase > 0:
            self.hp = self.hp + int((self.hp * eLhand.life_increase)/100)
        elif eLhand.life_increase < 0:
            self.hp = self.hp + int((eLhand.life_increase)*-1)
        if eBody.life_increase > 0:
            self.hp = self.hp + int((self.hp * eBody.life_increase)/100)
        elif eBody.life_increase < 0:
            self.hp = self.hp + int((eBody.life_increase)*-1)
        if eHead.life_increase > 0:
            self.hp = self.hp + int((self.hp * eHead.life_increase)/100)
        elif eHead.life_increase < 0:
            self.hp = self.hp + int((eHead.life_increase)*-1)
        if eAcc.life_increase > 0:
            self.hp = self.hp + int((self.hp * eAcc.life_increase)/100)
        elif eAcc.life_increase < 0:
            self.hp = self.hp + int((eAcc.life_increase)*-1)
            
        #MP Increase By Equipment
        if eRhand.mana_increase > 0:
            self.mp = self.mp + int((self.mp * eRhand.mana_increase)/100)
        elif eRhand.mana_increase < 0:
            self.mp = self.mp + int((eRhand.mana_increase)*-1)
        if eLhand.mana_increase > 0:
            self.mp = self.mp + int((self.mp * eLhand.mana_increase)/100)
        elif eLhand.mana_increase < 0:
            self.mp = self.mp + int((eLhand.mana_increase)*-1)
        if eBody.mana_increase > 0:
            self.mp = self.mp + int((self.mp * eBody.mana_increase)/100)
        elif eBody.mana_increase < 0:
            self.mp = self.mp + int((eBody.mana_increase)*-1)
        if eHead.mana_increase > 0:
            self.mp = self.mp + int((self.mp * eHead.mana_increase)/100)
        elif eHead.mana_increase < 0:
            self.mp = self.mp + int((eHead.mana_increase)*-1)
        if eAcc.mana_increase > 0:
            self.mp = self.mp + int((self.mp * eAcc.mana_increase)/100)
        elif eAcc.mana_increase < 0:
            self.mp = self.mp + int((eAcc.mana_increase)*-1)
            
        #Correcting if initial HP/MP is greater than base HP/MP
        if self.inicialHP > self.hp:
            self.inicialHP = self.hp
        if self.inicialMP > self.mp:
            self.inicialMP = self.mp
    
    def updateSecondaryStatus(self, eRhand, eLhand, eBody, eHead):
        
        #Attack Calculation
        if self.equipped_RightHand <= 0:
            self.attack = int(self.strenght + self.strenghtBonus)
            
        elif self.equipped_RightHand > 0:
            self.attack = int((self.strenght + self.strenghtBonus)*(eRhand.attack))*-1
            
        #Defense Calculation
        if (self.equipped_LeftHand <= 0 and self.equipped_Body <= 0 and self.equipped_Head <= 0):
            self.defense = int(self.physical + self.physicalBonus)
            
        elif ((self.equipped_LeftHand > 0) or (self.equipped_Body > 0) or (self.equipped_Head > 0)):
            self.defense = int((self.physical + self.physicalBonus)*(eLhand.armor_rating + eBody.armor_rating + eHead.armor_rating))
            
        #Magic Defense Calculation
        if (self.equipped_LeftHand <= 0 and self.equipped_Body <= 0 and self.equipped_Head <= 0):
            self.magic_defense = int((self.physical + self.physicalBonus + self.mind + self.mindBonus)/2)
            
        elif ((self.equipped_LeftHand > 0) or (self.equipped_Body > 0) or (self.equipped_Head > 0)):
            self.magic_defense = int(((self.physical + self.physicalBonus + self.mind +
                             self.mindBonus)/2)*(eLhand.armor_rating + eBody.armor_rating + eHead.armor_rating))
            
        #Magic Calculation
        self.magic = self.mind + self.mindBonus
        
        #Speed Calculation
        self.speed = self.agility + self.agilityBonus
        
        #Relative Calculation
        self.relative_attack = self.attack
        self.relative_defense = self.defense
        self.relative_magic_defense = self.magic_defense
        self.relative_magic = self.magic
        self.relative_speed = self.speed
            
            
    def updateStatusResistances(self, eLhand, eBody, eHead, eAcc):
        
        #Elemental Resistances
        self.elemental_resist_electricity = (eLhand.elemental_damage_electricity + eBody.elemental_damage_electricity
                        + eHead.elemental_damage_electricity + eAcc.elemental_damage_electricity)
        self.elemental_resist_fire = (eLhand.elemental_damage_fire + eBody.elemental_damage_fire
                        + eHead.elemental_damage_fire + eAcc.elemental_damage_fire)
        self.elemental_resist_water = (eLhand.elemental_damage_water + eBody.elemental_damage_water
                        + eHead.elemental_damage_water + eAcc.elemental_damage_water)
        self.elemental_resist_earth = (eLhand.elemental_damage_earth + eBody.elemental_damage_earth
                        + eHead.elemental_damage_earth + eAcc.elemental_damage_earth)
        self.elemental_resist_wind = (eLhand.elemental_damage_wind + eBody.elemental_damage_wind
                        + eHead.elemental_damage_wind + eAcc.elemental_damage_wind)
        self.elemental_resist_ice = (eLhand.elemental_damage_ice + eBody.elemental_damage_ice
                        + eHead.elemental_damage_ice + eAcc.elemental_damage_ice)
        self.elemental_resist_dark = (eLhand.elemental_damage_dark + eBody.elemental_damage_dark
                        + eHead.elemental_damage_dark + eAcc.elemental_damage_dark)
        self.elemental_resist_dark = (eLhand.elemental_damage_light + eBody.elemental_damage_light
                        + eHead.elemental_damage_light + eAcc.elemental_damage_light)
        #Status Resistances
        self.status_resist_poison = (eLhand.status_inflict_poison + eBody.status_inflict_poison
                        + eHead.status_inflict_poison + eAcc.status_inflict_poison)*-1
        self.status_resist_paralyze = (eLhand.status_inflict_paralyze + eBody.status_inflict_paralyze
                        + eHead.status_inflict_paralyze + eAcc.status_inflict_paralyze)*-1
        self.status_resist_tired = (eLhand.status_inflict_tired + eBody.status_inflict_tired
                        + eHead.status_inflict_tired + eAcc.status_inflict_tired)*-1
        self.status_resist_slow = (eLhand.status_inflict_slow + eBody.status_inflict_slow
                        + eHead.status_inflict_slow + eAcc.status_inflict_slow)*-1
        self.status_resist_mentalblock = (eLhand.status_inflict_mentalblock + eBody.status_inflict_mentalblock
                        + eHead.status_inflict_mentalblock + eAcc.status_inflict_mentalblock)*-1
        self.status_resist_alergic = (eLhand.status_inflict_alergic + eBody.status_inflict_alergic
                        + eHead.status_inflict_alergic + eAcc.status_inflict_alergic)*-1
          
    
    def updateStatus(self, eRhand, eLhand, eBody, eHead, eAcc):
        try:
            self.updateBonuses(eRhand, eLhand, eBody, eHead, eAcc)
            self.updateSecondaryStatus(eRhand, eLhand, eBody, eHead)
            self.updateStatusResistances(eLhand, eBody, eHead, eAcc)
            self.updateStatusHpMp(eRhand, eLhand, eBody, eHead, eAcc)
            return True
        except:
            print '!!!!!!!!!!!!Exception caught on PlayerCharacter() in updateStatus()!!!!!!!!!!!!'
            print formatExceptionInfo()
            return False
     
    def validateItem(self, item, equip_type=-1):
        if item.ID == 0 or item.ID == -1: #if player is unequipping
                return 0
        for iter in self.item_list:
            if iter.ID == item.ID:   
                if (item.class_restriction == 1 and (
                   self.cClass != 1 and self.cClass != 4 and
                   self.cClass != 5 and self.cClass != 6)):
                    return -1
                elif (item.class_restriction == 2 and (
                   self.cClass != 2 and self.cClass != 7 and
                   self.cClass != 8 and self.cClass != 9)):
                    return -1
                elif (item.class_restriction == 3 and (
                   self.cClass != 3 and self.cClass != 10 and
                   self.cClass != 11 and self.cClass != 12)):
                    return -1
                elif item.class_restriction > 3 and item.class_restriction != self.cClass:
                    return -1
                elif item.level_required > self.cLevel:
                    return -1
                elif item.kind != 3:
                    return -1
                elif item.equip_type != equip_type and equip_type != -1:
                    return -1
                else:
                    return 1
                    break
        return -1
            
    def validateEquip(self, eRhand, eLhand, eBody, eHead, eAcc):
        ret = -2
        if eRhand.ID != self.equipped_RightHand:
            ret = self.validateItem(eRhand, 0)
        if eLhand.ID != self.equipped_LeftHand:
            ret = self.validateItem(eLhand, 1)
        if eBody.ID != self.equipped_Body:
            ret = self.validateItem(eBody, 3)
        if eHead.ID != self.equipped_Head:
            ret = self.validateItem(eHead, 2)
        if eAcc.ID != self.equipped_Accessory:
            ret = self.validateItem(eAcc, 4)
        if ret == -2:
            return 0
        else:
            return ret
        
    def updateEquip(self, eRhand, eLhand, eBody, eHead, eAcc):
        ret = -1
        try:
            ret = self.validateEquip(eRhand, eLhand, eBody, eHead, eAcc)
            if ret > -1:
                #if ok, update all equipment
                self.equipped_RightHand = eRhand.ID
                self.equipped_LeftHand = eLhand.ID
                self.equipped_Body = eBody.ID
                self.equipped_Head = eHead.ID
                self.equipped_Accessory = eAcc.ID
            return ret
        except:
            print '!!!!!!!!!!!!Exception caught on PlayerCharacter() in updateEquip()!!!!!!!!!!!!'
            print formatExceptionInfo()
            return -1
            
    def validateBattleSkill(self, skillID, skill):
        for iter in self.skill_list:
            if iter.ID == skillID:
                if skill.use_as == 0 or skill.use_as == 2:
                    return True
        return False
    
    def validateBattleMagic(self, magicID, magic):
        for iter in self.magic_list:
            if iter.ID == magicID:
                if magic.use_as == 0 or magic.use_as == 2:
                    return True
                return True
        return False
    
    def validateBattleItem(self, itemID, item):
        for iter in self.item_list:
            if iter.ID == itemID:
                if item.use_as == 0 or item.use_as == 2:
                    return True
                return True
        return False
    
    def validateFieldItem(self, itemID, item):
        for iter in self.item_list:
            if iter.ID == itemID:
                if item.use_as == 1 or item.use_as == 2:
                    return True
                return True
        return False
    
    def validateFieldSkill(self, skillID, skill):
        if skill.kind == 0 and self.inicialHP <= skill.life_cost:
            return False
        elif skill.kind == 1 and self.inicialMP < skill.mana_cost:
            return False
        elif skill.kind == 0:
            for iter in self.skill_list:
                if iter.ID == itemID:
                    if skill.use_as == 1 or skill.use_as == 2:
                        return True
                    return True
        elif skill.kind == 1:
            for iter in self.magic_list:
                if iter.ID == skillID:
                    if skill.use_as == 1 or skill.use_as == 2:
                        return True
                    return True
            return False
    
    def removeItem(self, itemID):
        i = 0
        for iter in self.item_list:
            if iter.ID == itemID:
                self.item_list[i].quantity -= 1
                if self.item_list[i].quantity == 0:
                    self.item_list.pop(i)
            i+=1
    
class Item(object):
    
    def __init__(self, ID, quantity):
        self.ID = ID
        self.quantity = quantity
        
class Skill(object):
    
    def __init__(self, ID, level):
        self.ID = ID
        self.level = level
        
class Magic(object):
    
    def __init__(self, ID, level):
        self.ID = ID
        self.level = level

