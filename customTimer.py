# Copyright (c) 2010 Cassio Maciel.

import os
import yaml
import kinterbasdb
import sys
import traceback

from threading import Timer
from random import randint
from threading import Thread

import time

DELIMITER = '|'
BATTLE_START_COUNTDOWN = 4.0

#Subchannels for Client Requests
PLAYER_FIGHT = 17

#Subchannels for Client Messages
BATTLE_LOAD_COMPLETE = 20
TURN_LOAD_TIME = 21
PLAYER_PHASE = 22
FINAL_DAMAGE = 23
BATTLE_CHAT = 24
BATTLE_HP_MP_UPDATE = 25

class CustomTimer(Thread):
    
    def __init__(self, seconds, request=None, arg1=None, arg2=None):
        self.runTime = seconds
        self.request = request
        self.arg1 = arg1
        self.arg2 = arg2
        Thread.__init__(self)
    def run(self):
        if self.request >13:
            time.sleep(self.runTime)
            self.arg1.sendMessage("COMECOU PHASE", PLAYER_PHASE)
        
        