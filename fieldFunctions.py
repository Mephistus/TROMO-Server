# Copyright (c) 2010 Cassio Maciel.

from random import randint

DELIMITER = ','

NEW_ITEM = 1
LOST_ITEM = 0

ITEM_REMOVE = 26
USE_FIELD_ITEM = 7

class FieldFunctions(object):
    
    def __init__(self):
        self.action = ''
    
    def updateDamage(self,targetSprite,hpDamage,mpDamage):
        targetSprite.inicialMP -= mpDamage
        if targetSprite.inicialMP <= 0:
            targetSprite.inicialMP = 0
        if targetSprite.inicialMP > targetSprite.mp:
            targetSprite.inicialMP = targetSprite.mp
        
        targetSprite.inicialHP -= hpDamage
        if targetSprite.inicialHP > targetSprite.hp:
            targetSprite.inicialHP = targetSprite.hp
        if targetSprite.inicialHP <= 0:
            targetSprite.inicialHP = 1
    
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
    
    def updatePlayerItem(self, player, itemID, operation):
        if operation == NEW_ITEM:
            pass
        elif operation == LOST_ITEM:
            player.playerAccount.playerCharacter.removeItem(itemID)
            player.sendMessage(itemID,ITEM_REMOVE)
    
    def calculateItemDamage(self, item, party, channel, attacker, areaServer):
        self.updatePlayerItem(attacker,item.ID, LOST_ITEM)
        monsterTarget = False
        loopCount = 1
        
        if item.inicial_target == 1 and attacker.identifier == 'HUMAN':
            monsterTarget = True
        elif item.inicial_target == 0 and attacker.identifier == 'HUMAN':
            monsterTarget = False
        elif item.inicial_target == 1 and attacker.identifier == 'NPC':
            monsterTarget = False
        elif item.inicial_target == 0 and attacker.identifier == 'NPC':
            monsterTarget = True
            
        if monsterTarget:
            return False
        
        elif not monsterTarget and item.target == 1: # All target and player target
            loopCount = 5

        while loopCount > 0:
            loopCount -= 1
            hp = 0
            mp = 0
            hpDamage = 0
            mpDamage = 0
            auxDamage = 0
            message = ''
            receiver = None
            receiverID = 0
            
            #hp = attacker.inicialHP
            #mp = attacker.inicialMP
            
            if item.target == 0: # Single target and player target
                receiver = attacker.playerAccount.playerCharacter
                receiverID = attacker.id
            else:
                if loopCount == 1 and party.party_member_1:
                    receiver = party.party_member_1.playerAccount.playerCharacter
                    receiverID = party.party_member_1.id
                elif loopCount == 2 and party.party_member_2:
                    receiver = party.party_member_2.playerAccount.playerCharacter
                    receiverID = party.party_member_2.id
                elif loopCount == 3 and party.party_member_3:
                    receiver = party.party_member_3.playerAccount.playerCharacter
                    receiverID = party.party_member_3.id
                elif loopCount == 4 and party.party_member_4:
                    receiver = party.party_member_4.playerAccount.playerCharacter
                    receiverID = party.party_member_4.id
                elif loopCount == 5 and party.party_member_5:
                    receiver = party.party_member_5.playerAccount.playerCharacter
                    receiverID = party.party_member_5.id
                else:
                    continue
         
            if item.attack <= 0:
                if (randint(0,100)) >=  (int(receiver.relative_speed/2)):
                    #Calculate Physical Damage
                    hpDamage = (item.attack*-1) - receiver.relative_defense
                    hpDamage += int((randint(-20,20)*hpDamage)/100)
                    if hpDamage <= 0:
                        hpDamage = 1
                    hpDamage = self.calculateHPDamage(None,receiver,hpDamage,item)
                    mpDamage = self.calculateMPDamage(receiver,item)
                else:
                    hpDamage = 0
                    mpDamage = 0
            else:
                hpDamage = (item.attack*-1)
                hpDamage += int((randint(-20,20)*hpDamage)/100)
                mpDamage = self.calculateMPDamage(receiver,item)

            self.updateDamage(receiver,hpDamage,mpDamage)
            
            message = DELIMITER.join([str(item.animation),
                                      str(receiverID)])
            
            channel.sendMessage(areaServer,message,USE_FIELD_ITEM)
        
    def calculateSkillDamage(self, skill, party, channel, attacker, areaServer):
        
        self.updateDamage(attacker.playerAccount.playerCharacter,skill.life_cost,skill.mana_cost)
        
        monsterTarget = False
        loopCount = 1
        
        if skill.inicial_target == 1 and attacker.identifier == 'HUMAN':
            monsterTarget = True
        elif skill.inicial_target == 0 and attacker.identifier == 'HUMAN':
            monsterTarget = False
        elif skill.inicial_target == 1 and attacker.identifier == 'NPC':
            monsterTarget = False
        elif skill.inicial_target == 0 and attacker.identifier == 'NPC':
            monsterTarget = True
            
        if monsterTarget:
            return False
        
        elif not monsterTarget and skill.target == 1: # All target and player target
            loopCount = 5

        while loopCount > 0:
            loopCount -= 1
            hp = 0
            mp = 0
            hpDamage = 0
            mpDamage = 0
            auxDamage = 0
            message = ''
            receiver = None
            receiverID = 0
            
            #hp = attacker.inicialHP
            #mp = attacker.inicialMP
            
            if skill.target == 0: # Single target and player target
                receiver = attacker.playerAccount.playerCharacter
                receiverID = attacker.id
            else:
                if loopCount == 1 and party.party_member_1:
                    receiver = party.party_member_1.playerAccount.playerCharacter
                    receiverID = party.party_member_1.id
                elif loopCount == 2 and party.party_member_2:
                    receiver = party.party_member_2.playerAccount.playerCharacter
                    receiverID = party.party_member_2.id
                elif loopCount == 3 and party.party_member_3:
                    receiver = party.party_member_3.playerAccount.playerCharacter
                    receiverID = party.party_member_3.id
                elif loopCount == 4 and party.party_member_4:
                    receiver = party.party_member_4.playerAccount.playerCharacter
                    receiverID = party.party_member_4.id
                elif loopCount == 5 and party.party_member_5:
                    receiver = party.party_member_5.playerAccount.playerCharacter
                    receiverID = party.party_member_5.id
                else:
                    continue
         
            if skill.attack <= 0:
                if (randint(0,100)) >=  (int(receiver.relative_speed/2)):
                    #Calculate Physical Damage
                    hpDamage = (skill.attack*-1) - receiver.relative_defense
                    hpDamage += int((randint(-20,20)*hpDamage)/100)
                    if hpDamage <= 0:
                        hpDamage = 1
                    hpDamage = self.calculateHPDamage(None,receiver,hpDamage,skill)
                    mpDamage = self.calculateMPDamage(receiver,skill)
                else:
                    hpDamage = 0
                    mpDamage = 0
            else:
                hpDamage = (skill.attack*-1)
                hpDamage += int((randint(-20,20)*hpDamage)/100)
                mpDamage = self.calculateMPDamage(receiver,skill)

            self.updateDamage(receiver,hpDamage,mpDamage)
            
            message = DELIMITER.join([str(skill.animation),
                                      str(receiverID)])
            
            channel.sendMessage(areaServer,message,USE_FIELD_ITEM)
    
        