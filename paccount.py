# Copyright (c) 2010 Cassio Maciel.

import os
import yaml
import kinterbasdb
import sys
import traceback

DELIMITER2 = ','

from pcharacter import PlayerCharacter

def formatExceptionInfo(maxTBlevel=5):
         cla, exc, trbk = sys.exc_info()
         excName = cla.__name__
         try:
             excArgs = exc.__dict__["args"]
         except KeyError:
             excArgs = "<no args>"
         excTb = traceback.format_tb(trbk, maxTBlevel)
         return (excName, excArgs, excTb)

class PlayerAccount(object):

    def __init__(self):
        self.client_ID = None
        self.ID = 0
        self.pName = ''
        self.account_name = ''
        self.account_password = ''
        self.primary_email = ''
        self.secondary_email = ''
        self.gender = ''
        self.birth_date = ''
        self.country = ''
        self.city = ''
        self.created_account_date = None
        self.last_logon_date = None
        self.status = 0
        self.kick_day_count = 0
        self.account_type = 0
        self.total_minutes_played = 0
        self.character_1_ID = 0
        self.character_2_ID = 0
        self.character_3_ID = 0
        self.character_4_ID = 0
        self.character_5_ID = 0
        self.character_6_ID = 0
        self.character_7_ID = 0
        self.character_8_ID = 0
        self.xGold = 0
        self.playerCharacter = None
        

    def populateAccount(self, cur):
        for row in cur:
            self.ID = row[0]
            self.pName = row[1]
            self.account_name = row[2]
            self.account_password = row[3]
            self.primary_email = row[4]
            self.secondary_email = row[5]
            self.gender = row[6]
            self.birth_date = row[7]
            self.country =row[8]
            self.city = row[9]
            self.created_account_date = row[10]
            self.last_logon_date = row[11]
            self.status = row[12]
            self.kick_day_count = row[13]
            self.account_type = row[14]
            self.total_minutes_played = row[15]
            self.character_1_ID = row[16]
            self.character_2_ID = row[17]
            self.character_3_ID = row[18]
            self.character_4_ID = row[19]
            self.character_5_ID = row[20]
            self.character_6_ID = row[21]
            self.character_7_ID = row[22]
            self.character_8_ID = row[23]
            self.xGold = row[24]
        

    def checkLogin (self, con, name, password):
        cur = con.cursor()
        cur.execute("SELECT * FROM player_account WHERE account_name='"+name+"' AND account_password='"+password+"'")
        self.populateAccount(cur)
        if self.ID == 0:
            #Username and Password Don't Match
            return None
        else:
            #Username and Password Match
            return self
    
    def loadCharacterList(self):
        message = DELIMITER2.join(
                                    [
                                     str(self.character_1_ID),
                                     str(self.character_2_ID),
                                     str(self.character_3_ID),
                                     str(self.character_4_ID),
                                     str(self.character_5_ID),
                                     str(self.character_6_ID),
                                     str(self.character_7_ID),
                                     str(self.character_8_ID),
                                     ])
        return message
    
    def loadCharacterInfo(self, con, pos):
        cur = con.cursor()
        if pos == '1':
            cur.execute("SELECT inicial_outfithead_id, name, clevel, class FROM game_character WHERE id="+str(self.character_1_ID))
        if pos == '2':
            cur.execute("SELECT inicial_outfithead_id, name, clevel, class FROM game_character WHERE id="+str(self.character_2_ID))
        if pos == '3':
            cur.execute("SELECT inicial_outfithead_id, name, clevel, class FROM game_character WHERE id="+str(self.character_3_ID))
        if pos == '4':
            cur.execute("SELECT inicial_outfithead_id, name, clevel, class FROM game_character WHERE id="+str(self.character_4_ID))
        if pos == '5':
            cur.execute("SELECT inicial_outfithead_id, name, clevel, class FROM game_character WHERE id="+str(self.character_5_ID))
        if pos == '6':
            cur.execute("SELECT inicial_outfithead_id, name, clevel, class FROM game_character WHERE id="+str(self.character_6_ID))
        if pos == '7':
            cur.execute("SELECT inicial_outfithead_id, name, clevel, class FROM game_character WHERE id="+str(self.character_7_ID))
        if pos == '8':
            cur.execute("SELECT inicial_outfithead_id, name, clevel, class FROM game_character WHERE id="+str(self.character_8_ID))
        for row in cur:
            message = DELIMITER2.join([str(row[0]), row[1], str(row[2]), str(row[3]), pos])
            return message
        
    def validateName(self, con, name):
        if len(name) < 3: #Checking if the name Lenght is inferior to 3
            return 0
        if name == '':     #Checking if the name is not empty
            return 0
        try:               #Checking if the name is not a number
            aux = int(name)
        except:
            cur = con.cursor()
            cur.execute("SELECT * from validated_names WHERE UPPER(name)=UPPER('"+name+"')")
            for row in cur:
                return 0
            return 1
        return 0
    
    def insertNewCharacter (self, con, name, gender, strenght, physical, mind, agility, charPos):
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO game_character VALUES(1, 20, 20,'entrymap',"+str(physical*2.5)+","+
                            str(mind*2)+", 1, 2, 3,'"+name+"', 1,"+str(gender)+","+
                            str(physical*2.5)+","+str(mind*2)+", 0,"+str(strenght)+","+
                            str(physical)+","+str(mind)+","+str(agility)+
                            ", 0, 0, 0, 0, 0, 0, 100, 0, 0, 3, 'entrymap')")
            con.commit()
            
            cur.execute("SELECT id FROM game_character WHERE name='"+name+"'")
            for row in cur:
                charID = row[0]
                newItems = [('1', '1', str(row[0])),
                    ('2', '1', str(row[0])),
                    ('3', '1', str(row[0])),
                    ('4', '1', str(row[0])),
                    ('5', '1', str(row[0])),
                    ('6', '1', str(row[0]))
                    ]
                
            cur.executemany("INSERT INTO item_list(item_id, quantity, character_id) VALUES(?,?,?)", newItems)
            if charPos == 1:
                cur.execute("UPDATE player_account SET character_1_id="+str(charID)+" WHERE id="+str(self.ID))
                self.character_1_ID = charID 
                cur.execute("INSERT INTO validated_names(name, character_id) VAlUES('"+name+"',"+str(charID)+")")
                con.commit()
                return True
            if charPos == 2:
                cur.execute("UPDATE player_account SET character_2_id="+str(charID)+" WHERE id="+str(self.ID))
                self.character_2_ID = charID
                cur.execute("INSERT INTO validated_names(name, character_id) VAlUES('"+name+"',"+str(charID)+")")
                con.commit()
                return True
            if charPos == 3:
                cur.execute("UPDATE player_account SET character_3_id="+str(charID)+" WHERE id="+str(self.ID))
                self.character_3_ID = charID
                cur.execute("INSERT INTO validated_names(name, character_id) VAlUES('"+name+"',"+str(charID)+")")
                con.commit()
                return True
            if charPos == 4:
                cur.execute("UPDATE player_account SET character_4_id="+str(charID)+" WHERE id="+str(self.ID))
                self.character_4_ID = charID
                cur.execute("INSERT INTO validated_names(name, character_id) VAlUES('"+name+"',"+str(charID)+")")
                con.commit()
                return True
            if charPos == 5:
                cur.execute("UPDATE player_account SET character_5_id="+str(charID)+" WHERE id="+str(self.ID))
                self.character_5_ID = charID
                cur.execute("INSERT INTO validated_names(name, character_id) VAlUES('"+name+"',"+str(charID)+")")
                con.commit()
                return True
            if charPos == 6:
                cur.execute("UPDATE player_account SET character_6_id="+str(charID)+" WHERE id="+str(self.ID))
                self.character_6_ID = charID
                cur.execute("INSERT INTO validated_names(name, character_id) VAlUES('"+name+"',"+str(charID)+")")
                con.commit()
                return True
            if charPos == 7:
                cur.execute("UPDATE player_account SET character_7_id="+str(charID)+" WHERE id="+str(self.ID))
                self.character_7_ID = charID
                cur.execute("INSERT INTO validated_names(name, character_id) VAlUES('"+name+"',"+str(charID)+")")
                con.commit()
                return True
            if charPos == 8:
                cur.execute("UPDATE player_account SET character_8_id="+str(charID)+" WHERE id="+str(self.ID))
                self.character_8_ID = charID
                cur.execute("INSERT INTO validated_names(name, character_id) VAlUES('"+name+"',"+str(charID)+")")
                con.commit()
                return True
            con.rollback()
            return False
        except:
            print '!!!!!!!!!!!!Exception caught on PlayerAccount() in insertNewCharacter()!!!!!!!!!!!!'
            print formatExceptionInfo()
            con.rollback()
            return False
    
    def createNewCharacter(self, con, name, gender, strenght, physical, mind, agility):
        gen = 0
        stre = 0 
        phy = 0
        min = 0
        agi = 0
        insertOK = False
        ret = self.validateName(con, name)
        if ret == 0:
            return 0
        try:
            gen = int(gender)
            stre = int(strenght)
            phy = int(physical)
            min = int(mind)
            agi = int(agility)
        except:
            return 0
        if gen != 0 and gen != 1:
            print gen
            return 0
        if (((stre + phy + min + agi) != 30)
           or (stre > 10 or stre < 0)
           or (phy > 10 or phy < 0)
           or (min > 10 or min < 0)
           or (agi > 10 or agi < 0)):
            return 0
        if insertOK == False and self.character_1_ID == 0:
            insertOK = self.insertNewCharacter(con, name, gen, stre, phy, min, agi, 1)
        if insertOK == False and self.character_2_ID == 0:
            insertOK = self.insertNewCharacter(con, name, gen, stre, phy, min, agi, 2)
        if insertOK == False and self.character_3_ID == 0:
            insertOK = self.insertNewCharacter(con, name, gen, stre, phy, min, agi, 3)
        if insertOK == False and self.character_4_ID == 0:
            insertOK = self.insertNewCharacter(con, name, gen, stre, phy, min, agi, 4)
        if insertOK == False and self.character_5_ID == 0:
            insertOK = self.insertNewCharacter(con, name, gen, stre, phy, min, agi, 5)
        if insertOK == False and self.character_6_ID == 0:
            insertOK = self.insertNewCharacter(con, name, gen, stre, phy, min, agi, 6)
        if insertOK == False and self.character_7_ID == 0:
            insertOK = self.insertNewCharacter(con, name, gen, stre, phy, min, agi, 7)
        if insertOK == False and self.character_8_ID == 0:
            insertOK = self.insertNewCharacter(con, name, gen, stre, phy, min, agi, 8)
        
        if insertOK == False:
            return 0
        
        return 1

    def organizeChars(self, charPos):
        if charPos == 1:
            ret = self.character_1_ID
            self.character_1_ID = self.character_2_ID
            self.character_2_ID = self.character_3_ID
            self.character_3_ID = self.character_4_ID
            self.character_4_ID = self.character_5_ID
            self.character_5_ID = self.character_6_ID
            self.character_6_ID = self.character_7_ID
            self.character_7_ID = self.character_8_ID
            self.character_8_ID = 0
            return ret
        if charPos == 2:
            ret = self.character_2_ID
            self.character_2_ID = self.character_3_ID
            self.character_3_ID = self.character_4_ID
            self.character_4_ID = self.character_5_ID
            self.character_5_ID = self.character_6_ID
            self.character_6_ID = self.character_7_ID
            self.character_7_ID = self.character_8_ID
            self.character_8_ID = 0
            return ret
        if charPos == 3:
            ret = self.character_3_ID
            self.character_3_ID = self.character_4_ID
            self.character_4_ID = self.character_5_ID
            self.character_5_ID = self.character_6_ID
            self.character_6_ID = self.character_7_ID
            self.character_7_ID = self.character_8_ID
            self.character_8_ID = 0
            return ret
        if charPos == 4:
            ret = self.character_4_ID
            self.character_4_ID = self.character_5_ID
            self.character_5_ID = self.character_6_ID
            self.character_6_ID = self.character_7_ID
            self.character_7_ID = self.character_8_ID
            self.character_8_ID = 0
            return ret
        if charPos == 5:
            ret = self.character_5_ID
            self.character_5_ID = self.character_6_ID
            self.character_6_ID = self.character_7_ID
            self.character_7_ID = self.character_8_ID
            self.character_8_ID = 0
            return ret
        if charPos == 6:
            ret = self.character_6_ID
            self.character_6_ID = self.character_7_ID
            self.character_7_ID = self.character_8_ID
            self.character_8_ID = 0
            return ret
        if charPos == 7:
            ret = self.character_7_ID
            self.character_7_ID = self.character_8_ID
            self.character_8_ID = 0
            return ret
        if charPos == 8:
            ret = self.character_8_ID
            self.character_8_ID = 0
            return ret
    pass

    def deleteCharacter(self, con, charPos):
        
        #Return Error if the character doesn't exist
        if (charPos < 1) or (charPos > 8):
            return 0
        
        try:    
            cur = con.cursor()
            
            charPos = self.organizeChars(charPos)
                
            cur.execute("UPDATE player_account SET character_1_id="+str(self.character_1_ID)+
                            ",character_2_id="+str(self.character_2_ID)+
                            ",character_3_id="+str(self.character_3_ID)+
                            ",character_4_id="+str(self.character_4_ID)+
                            ",character_5_id="+str(self.character_5_ID)+
                            ",character_6_id="+str(self.character_6_ID)+
                            ",character_7_id="+str(self.character_7_ID)+
                            ",character_8_id="+str(self.character_8_ID)+
                            " WHERE id="+str(self.ID))
            
            cur.execute("DELETE FROM item_list WHERE character_id = "+str(charPos))
            cur.execute("DELETE FROM habilities_list WHERE character_id = "+str(charPos))
            cur.execute("DELETE FROM magic_list WHERE character_id = "+str(charPos))
            cur.execute("DELETE FROM validated_names WHERE character_id = "+str(charPos))
            cur.execute("DELETE FROM game_character WHERE id = "+str(charPos))
            con.commit()
        
        except:
            print '!!!!!!!!!!!!Exception caught on PlayerAccount() in deleteCharacter()!!!!!!!!!!!!'
            print formatExceptionInfo()
            con.rollback()
            return 0
        return 1
        

    def loginCharacter(self, con, charPos):
        
        #Return Error if the character doesn't exist
        if (charPos < 1) or (charPos > 8):
            return 0
        #Return Error if the character doesn't exist
        if charPos == 1 and self.character_1_ID == 0:
            return 0
        if charPos == 2 and self.character_2_ID == 0:
            return 0
        if charPos == 3 and self.character_3_ID == 0:
            return 0
        if charPos == 4 and self.character_4_ID == 0:
            return 0
        if charPos == 5 and self.character_5_ID == 0:
            return 0
        if charPos == 6 and self.character_6_ID == 0:
            return 0
        if charPos == 7 and self.character_7_ID == 0:
            return 0
        if charPos == 8 and self.character_8_ID == 0:
            return 0
        
        try:
            #creates a new instance of PlayerCharacter
            self.playerCharacter = PlayerCharacter(self.xGold)
            
            if charPos == 1:
                return self.playerCharacter.populate(con, self.character_1_ID)
            elif charPos == 2:
                return self.playerCharacter.populate(con, self.character_2_ID)
            elif charPos == 3:
                return self.playerCharacter.populate(con, self.character_3_ID)
            elif charPos == 4:
                return self.playerCharacter.populate(con, self.character_4_ID)
            elif charPos == 5:
                return self.playerCharacter.populate(con, self.character_5_ID)
            elif charPos == 6:
                return self.playerCharacter.populate(con, self.character_6_ID)
            elif charPos == 7:
                return self.playerCharacter.populate(con, self.character_7_ID)
            elif charPos == 8:
                return self.playerCharacter.populate(con, self.character_8_ID)
            
        except:
            print '!!!!!!!!!!!!Exception caught on PlayerAccount() in loginCharacter()!!!!!!!!!!!!'
            print formatExceptionInfo()
            return 0
        
        return 1
            
            
            
            
            
            
            
            
            
            
            
            
            
        