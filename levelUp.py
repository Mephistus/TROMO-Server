#!/usr/bin/env python

LEVEL1TO15 = 20
LEVEL16TO135 = 40
LEVEL36TO50 = 70
LEVEL51TO80 = 120
LEVEL81TO98 = 180
LEVEL99 = 250

class LevelUp(object):
    
    def __init__(self):
        pass
    
    def checkLevelUp(self, player):
        myPlayer = player.playerAccount.playerCharacter
        
        if myPlayer.exp >= myPlayer.nextExp:
            if myPlayer.cLevel <= 15:
                myPlayer.nextExp += myPlayer.exp+int((myPlayer.exp*LEVEL1TO15)/100)
            elif myPlayer.cLevel <= 35 and myPlayer.cLevel >= 16:
                myPlayer.nextExp += myPlayer.exp+(int((myPlayer.exp*LEVEL16TO135)/100))
            elif myPlayer.cLevel <= 50 and myPlayer.cLevel >= 36:
                myPlayer.nextExp += myPlayer.exp+int((myPlayer.exp*LEVEL36TO50)/100)
            elif myPlayer.cLevel <= 80 and myPlayer.cLevel >= 51:
                myPlayer.nextExp += myPlayer.exp+int((myPlayer.exp*LEVEL51TO80)/100)
            elif myPlayer.cLevel <= 98 and myPlayer.cLevel >= 81:
                myPlayer.nextExp += myPlayer.exp+int((myPlayer.exp*LEVEL81TO98)/100)
            elif myPlayer.cLevel == 99:
                myPlayer.nextExp += myPlayer.exp+int((myPlayer.exp*LEVEL99)/100)
                
            myPlayer.cLevel += 1
            myPlayer.remaining_attributes += 5
            
    def levelUpAddStrenght(self, player):
        myPlayer = player.playerAccount.playerCharacter
        
        if myPlayer.remaining_attributes > 0:
            myPlayer.strenght += 1
            myPlayer.remaining_attributes -= 1
            return True
        return False
        
    def levelUpAddPhysical(self, player):
        myPlayer = player.playerAccount.playerCharacter
        
        if myPlayer.remaining_attributes > 0:
            myPlayer.physical += 1
            myPlayer.remaining_attributes -= 1
            return True
        return False
        
    def levelUpAddMind(self, player):
        myPlayer = player.playerAccount.playerCharacter
        
        if myPlayer.remaining_attributes > 0:
            myPlayer.mind += 1
            myPlayer.remaining_attributes -= 1
            return True
        return False
    
    def levelUpAddAgility (self, player):
        myPlayer = player.playerAccount.playerCharacter
        
        if myPlayer.remaining_attributes > 0:
            myPlayer.agility += 1
            myPlayer.remaining_attributes -= 1
            return True
        return False
    
    
