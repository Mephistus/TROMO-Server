# Copyright (c) 2010 Cassio Maciel.

from random import randint

class Monster(object):
    
    def __init__(self,arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,
                 arg10,arg11,arg12,arg13,arg14,arg15,arg16,arg17,arg18,
                 arg19,arg20,arg21,arg22,arg23,arg24,arg25,arg26,arg27,
                 arg28,arg29,arg30,arg31,arg32,arg33,arg34,arg35,arg36,
                 arg37,arg38,arg39,arg40,arg41,arg42,arg43,arg44,arg45):
        self.ID = arg1
        self.name = arg2
        self.monster_level = arg3
        self.hp = arg4
        self.mp = arg5
        self.strenght = arg6
        self.attack = arg6
        self.defense = arg7
        self.magic_defense = arg8
        self.magic = arg9
        self.speed = arg10
        self.gold = arg11
        self.experience = arg12
        self.elemental_resist_electricity = arg13
        self.elemental_resist_fire = arg14
        self.elemental_resist_water = arg15
        self.elemental_resist_earth = arg16
        self.elemental_resist_wind = arg17
        self.elemental_resist_ice = arg18
        self.elemental_resist_dark = arg19
        self.elemental_resist_light = arg20
        self.elemental_damage_electricity = arg21
        self.elemental_damage_fire = arg22
        self.elemental_damage_water = arg23
        self.elemental_damage_earth = arg24
        self.elemental_damage_wind = arg25
        self.elemental_damage_ice = arg26
        self.elemental_damage_dark = arg27
        self.elemental_damage_light = arg28
        self.status_resist_poison = arg29 
        self.status_resist_paralyze = arg30
        self.status_resist_tired = arg31 
        self.status_resist_slow = arg32 
        self.status_resist_mentalblock = arg33 
        self.status_resist_alergic = arg34 
        self.treasure_1_id = arg35
        self.treasure_1_chance = arg36
        self.treasure_2_id = arg37
        self.treasure_2_chance = arg38
        self.treasure_3_id = arg39
        self.treasure_3_chance = arg40
        self.treasure_4_id = arg41
        self.treasure_4_chance = arg42
        self.treasure_5_id = arg43
        self.treasure_5_chance = arg44
        self.grapphic = arg45
        
        self.relative_attack = arg6
        self.relative_defense = arg7
        self.relative_magic_defense = arg8
        self.relative_magic = arg9
        self.relative_speed = arg10
        
        self.inicialHP = arg4
        self.inicialMP = arg5
        
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
        
        self.cured = False
        
        self.skill_list = []
        
        self.identifier = 'NPC'
        
        
    def loadSkills(self, con):
        cur = con.cursor()
        cur.execute("SELECT skill_id FROM monster_skill_list WHERE monster_id="+str(self.ID))
        for row in cur:
            self.skill_list.append(Skill(row[0]))
            
    def sortSkills(self):
        return self.skill_list[randint(0,len(self.skill_list)-1)].ID
    
class Skill(object):
    
    def __init__(self, ID):
        self.ID = ID

        
