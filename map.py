#!/usr/bin/env python
# Copyright (c) 2010 Cassio Maciel.

import os
import yaml
import kinterbasdb
import sys
import traceback

DELIMITER = ','

class Map(object):
    
    def __init__(self,arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,arg10,arg11,arg12,arg13,
                 arg14,arg15,arg16,arg17,arg18,arg19):
        self.ID = arg1
        self.name = arg2
        self.x_size = arg3
        self.y_size = arg4
        if (arg5 == 'Yes'):
            self.hostile_place = True
        else:
            self.hostile_place = False
        self.monster_ocurrence = arg6
        self.signature = arg7
        self.up_exit_1mapName,self.up_exit_1posX, self.up_exit_1posY  = self.splitValue(arg8)
        self.up_exit_2mapName,self.up_exit_2posX, self.up_exit_2posY  = self.splitValue(arg9)
        self.up_exit_3mapName,self.up_exit_3posX, self.up_exit_3posY  = self.splitValue(arg10)
        self.left_exit_1mapName,self.left_exit_1posX, self.left_exit_1posY  = self.splitValue(arg11)
        self.left_exit_2mapName,self.left_exit_2posX, self.left_exit_2posY  = self.splitValue(arg12)
        self.left_exit_3mapName,self.left_exit_3posX, self.left_exit_3posY  = self.splitValue(arg13)
        self.down_exit_1mapName,self.down_exit_1posX, self.down_exit_1posY  = self.splitValue(arg14)
        self.down_exit_2mapName,self.down_exit_2posX, self.down_exit_2posY  = self.splitValue(arg15)
        self.down_exit_3mapName,self.down_exit_3posX, self.down_exit_3posY  = self.splitValue(arg16)
        self.right_exit_1mapName,self.right_exit_1posX, self.right_exit_1posY  = self.splitValue(arg17)
        self.right_exit_2mapName,self.right_exit_2posX, self.right_exit_2posY  = self.splitValue(arg18)
        self.right_exit_3mapName,self.right_exit_3posX, self.right_exit_3posY  = self.splitValue(arg19)
        self.monster_party_list = []
        
    def splitValue(self, message):
        test1 = ''
        test2 = ''
        test3 = ''
        value = []
        try:
        # split the message by a delimiter
            value = message.split(DELIMITER)
            try:
                test1,test2,test3 = value
            except:
                return 'NONE','0','0'
            return value
        except:
        # if the message is a integer don't split
            return 'NONE','0','0'
    
    def loadParties(self, con):
        cur = con.cursor()
        cur.execute("SELECT monster_party_id FROM monster_party_list WHERE map_id="+str(self.ID))
        for row in cur:
            self.monster_party_list.append(Party(row[0]))
        
    
    def changeMap(self, exit):
        if exit == 1:
                return self.up_exit_1mapName, int(self.up_exit_1posX), int(self.up_exit_1posY)
        elif exit == 2:
                return self.up_exit_2mapName,int(self.up_exit_2posX),int(self.up_exit_2posY)
        elif exit == 3:
                return self.up_exit_3mapName,int(self.up_exit_3posX),int(self.up_exit_3posY)
        elif exit == 4:
                return self.left_exit_1mapName,int(self.left_exit_1posX),int(self.left_exit_1posY)
        elif exit == 5:
                return self.left_exit_2mapName,int(self.left_exit_2posX),int(self.left_exit_2posY)
        elif exit == 6:
                return self.left_exit_3mapName,int(self.left_exit_3posX),int(self.left_exit_3posY)
        elif exit == 7:
                return self.down_exit_1mapName,int(self.down_exit_1posX),int(self.down_exit_1posY)
        elif exit == 8:
                return self.down_exit_2mapName,int(self.down_exit_2posX),int(self.down_exit_2posY)
        elif exit == 9:
                return self.down_exit_3mapName,int(self.down_exit_3posX),int(self.down_exit_3posY)
        elif exit == 10:
                return self.right_exit_1mapName,int(self.right_exit_1posX),int(self.right_exit_1posY)
        elif exit == 11:
                return self.right_exit_2mapName,int(self.right_exit_2posX),int(self.right_exit_2posY)
        elif exit == 12:
                return self.right_exit_3mapName,int(self.right_exit_3posX),int(self.right_exit_3posY)
        
        return '',0,0
        
class Party(object):
    
    def __init__(self, ID):
        self.ID = ID
