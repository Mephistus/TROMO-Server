#!/usr/bin/env python

DELIMITER = ','

CHANNEL_CHANGE = 32

CHARACTER_DISCONNECT = 2

class ChangeMap(object):
    
    def __init__(self):
        pass
    
    def mapChange(self, player, destinationMap, posX,posY, factory):
        message = ''
        
        if destinationMap.name != '':
            player.playerAccount.playerCharacter.battleStepCounter = 15
            player.leaveChannel(factory.findChannel(player.playerAccount.playerCharacter.starting_Map))
            player.playerAccount.playerCharacter.starting_Map = destinationMap.name
            player.playerAccount.playerCharacter.starting_PosX = posX
            player.playerAccount.playerCharacter.starting_PosY = posY
            player.playerAccount.playerCharacter.tempX = posX
            player.playerAccount.playerCharacter.tempY = posY
            player.playerAccount.playerCharacter.lastX = posX
            player.playerAccount.playerCharacter.lastY = posY
            if destinationMap.hostile_place:
                player.playerAccount.playerCharacter.hostileArea = True
            else:
                player.playerAccount.playerCharacter.hostileArea = False
            player.sendMessage(1,CHANNEL_CHANGE)
        return