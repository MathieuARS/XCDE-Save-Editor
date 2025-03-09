#!/usr/bin/env python3
import struct
import os
import sys
from enum import IntEnum

class Character(IntEnum):
    """Character IDs for Xenoblade Chronicles: Definitive Edition"""
    NONE = 0
    SHULK = 1
    REYN = 2
    FIORA = 3
    DUNBAN = 4
    SHARLA = 5
    RIKI = 6
    MELIA = 7
    FIORA_2 = 8
    DICKSON = 9
    MUMKHAR = 10
    ALVIS = 11
    DUNBAN_2 = 12
    DUNBAN_3 = 13
    KINO = 14
    NENE = 15
    WUNWUN = 16
    TUTU = 17
    DRYDRY = 18
    FOFORA = 19
    FAIFA = 20
    HEKASA = 21
    SETSET = 22
    TEITEI = 23
    NONONA = 24
    DEKADEKA = 25
    EVELEN = 26
    TENTOO = 27

class ArtsLevelUnlocked(IntEnum):
    """Max level that arts can be unlocked to"""
    IV_BEGINNER = 0      # Up to level 4
    VII_INTERMEDIATE = 1 # Up to level 7
    X_EXPERT = 2         # Up to level 10
    XII_MASTER = 3       # Up to level 12

# Character positions in PartyMembers array
CHARACTER_POSITIONS = {
    Character.SHULK: 0,
    Character.REYN: 1,
    Character.FIORA: 2,
    Character.DUNBAN: 3,
    Character.SHARLA: 4,
    Character.RIKI: 5,
    Character.MELIA: 6,
    Character.FIORA_2: 7,
}

class XCDESaveEditor:
    # Important offsets in the save file
    PARTY_MEMBERS_OFFSET = 0x152368
    PARTY_MEMBER_SIZE = 0x138
    EXP_OFFSET_IN_MEMBER = 0x04
    LEVEL_OFFSET_IN_MEMBER = 0x00
    AP_OFFSET_IN_MEMBER = 0x08
    
    # Arts levels offset and size
    ARTS_LEVELS_OFFSET = 0x1536E8
    ARTS_LEVEL_SIZE = 2
    TOTAL_ARTS = 188
    
    def __init__(self, save_path):
        """Initialize the editor with the path to the save file"""
        self.save_path = save_path
        self.backup_path = save_path + ".backup"
        
        # Read the save file
        with open(save_path, 'rb') as f:
            self.save_data = bytearray(f.read())
        
        # Create a backup
        self._create_backup()
    
    def _create_backup(self):
        """Create a backup of the original save file"""
        if not os.path.exists(self.backup_path):
            with open(self.backup_path, 'wb') as f:
                f.write(self.save_data)
            print(f"Backup created at {self.backup_path}")
    
    def get_character_position(self, character_id):
        """Get the position of a character in the PartyMembers array"""
        char_enum = Character(character_id)
        return CHARACTER_POSITIONS.get(char_enum, character_id - 1)
    
    def get_character_exp(self, character_id):
        """Get the current XP for a specific character"""
        position = self.get_character_position(character_id)
        offset = self.PARTY_MEMBERS_OFFSET + (position * self.PARTY_MEMBER_SIZE) + self.EXP_OFFSET_IN_MEMBER
        return struct.unpack("<I", self.save_data[offset:offset+4])[0]
    
    def get_character_level(self, character_id):
        """Get the current level for a specific character"""
        position = self.get_character_position(character_id)
        offset = self.PARTY_MEMBERS_OFFSET + (position * self.PARTY_MEMBER_SIZE) + self.LEVEL_OFFSET_IN_MEMBER
        return struct.unpack("<I", self.save_data[offset:offset+4])[0]
    
    def get_character_ap(self, character_id):
        """Get the current AP for a specific character"""
        position = self.get_character_position(character_id)
        offset = self.PARTY_MEMBERS_OFFSET + (position * self.PARTY_MEMBER_SIZE) + self.AP_OFFSET_IN_MEMBER
        return struct.unpack("<I", self.save_data[offset:offset+4])[0]
    
    def set_character_exp(self, character_id, new_exp):
        """Set a new XP value for a specific character"""
        position = self.get_character_position(character_id)
        offset = self.PARTY_MEMBERS_OFFSET + (position * self.PARTY_MEMBER_SIZE) + self.EXP_OFFSET_IN_MEMBER
        self.save_data[offset:offset+4] = struct.pack("<I", new_exp)
    
    def set_character_level(self, character_id, new_level):
        """Set a new level for a specific character"""
        position = self.get_character_position(character_id)
        offset = self.PARTY_MEMBERS_OFFSET + (position * self.PARTY_MEMBER_SIZE) + self.LEVEL_OFFSET_IN_MEMBER
        self.save_data[offset:offset+4] = struct.pack("<I", new_level)
    
    def set_all_character_levels(self, new_level):
        """Set the same level for all characters"""
        # Set for main characters (1-15)
        for char_id in range(1, 16):
            try:
                self.set_character_level(char_id, new_level)
            except Exception as e:
                print(f"Warning: Could not set level for character {char_id}: {e}")
        return True
    
    def set_character_ap(self, character_id, new_ap):
        """Set a new AP value for a specific character"""
        position = self.get_character_position(character_id)
        offset = self.PARTY_MEMBERS_OFFSET + (position * self.PARTY_MEMBER_SIZE) + self.AP_OFFSET_IN_MEMBER
        self.save_data[offset:offset+4] = struct.pack("<I", new_ap)
    
    def get_art_level(self, art_index):
        """Get the current level of an art"""
        if art_index < 0 or art_index >= self.TOTAL_ARTS:
            raise ValueError(f"Art index must be between 0 and {self.TOTAL_ARTS-1}")
        
        offset = self.ARTS_LEVELS_OFFSET + (art_index * self.ARTS_LEVEL_SIZE)
        return self.save_data[offset]
    
    def get_art_max_unlock(self, art_index):
        """Get the max unlock level of an art"""
        if art_index < 0 or art_index >= self.TOTAL_ARTS:
            raise ValueError(f"Art index must be between 0 and {self.TOTAL_ARTS-1}")
        
        offset = self.ARTS_LEVELS_OFFSET + (art_index * self.ARTS_LEVEL_SIZE) + 1
        return ArtsLevelUnlocked(self.save_data[offset])
    
    def set_art_level(self, art_index, new_level):
        """Set a new level for an art"""
        if art_index < 0 or art_index >= self.TOTAL_ARTS:
            raise ValueError(f"Art index must be between 0 and {self.TOTAL_ARTS-1}")
        if new_level < 0 or new_level > 12:
            raise ValueError("Art level must be between 0 and 12")
        
        offset = self.ARTS_LEVELS_OFFSET + (art_index * self.ARTS_LEVEL_SIZE)
        self.save_data[offset] = new_level
    
    def set_art_max_unlock(self, art_index, new_max_unlock):
        """Set a new max unlock level for an art"""
        if art_index < 0 or art_index >= self.TOTAL_ARTS:
            raise ValueError(f"Art index must be between 0 and {self.TOTAL_ARTS-1}")
        if isinstance(new_max_unlock, int):
            if new_max_unlock < 0 or new_max_unlock > 3:
                raise ValueError("Max unlock level must be between 0 and 3")
            unlock_value = new_max_unlock
        else:
            unlock_value = int(ArtsLevelUnlocked(new_max_unlock))
        
        offset = self.ARTS_LEVELS_OFFSET + (art_index * self.ARTS_LEVEL_SIZE) + 1
        self.save_data[offset] = unlock_value
    
    def set_all_arts_levels(self, new_level):
        """Set all arts to the same level"""
        if new_level < 0 or new_level > 12:
            raise ValueError("Art level must be between 0 and 12")
        
        for i in range(self.TOTAL_ARTS):
            self.set_art_level(i, new_level)
        return True
    
    def set_all_arts_max_unlock(self, new_max_unlock):
        """Set all arts to the same max unlock level"""
        if isinstance(new_max_unlock, int):
            if new_max_unlock < 0 or new_max_unlock > 3:
                raise ValueError("Max unlock level must be between 0 and 3")
            unlock_value = new_max_unlock
        else:
            unlock_value = int(ArtsLevelUnlocked(new_max_unlock))
        
        for i in range(self.TOTAL_ARTS):
            self.set_art_max_unlock(i, unlock_value)
        return True
    
    def save(self, output_path=None):
        """Save the modified save file"""
        if output_path is None:
            output_path = self.save_path
        
        with open(output_path, 'wb') as f:
            f.write(self.save_data)
        print(f"Save file written to {output_path}")

    def get_character_name(self, character_id):
        """Get the name of a character from its ID"""
        try:
            return Character(character_id).name
        except ValueError:
            return f"Unknown Character ({character_id})"

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  1. View character stats: python test.py <save_file>")
        print("  2. Modify character XP: python test.py <save_file> <character_id> <new_xp>")
        print("  3. Modify character level: python test.py <save_file> level <character_id> <new_level>")
        print("  4. Modify character AP: python test.py <save_file> ap <character_id> <new_ap>")
        print("  5. Modify ALL characters level: python test.py <save_file> alllevel <new_level>")
        print("  6. Set level for ALL arts: python test.py <save_file> allartlevel <new_level>")
        print("  7. Set max unlock level for ALL arts: python test.py <save_file> allartmax <new_max_level>")
        print("\nCharacter IDs:")
        for char in Character:
            if char != Character.NONE:
                print(f"  {int(char)}: {char.name}")
        sys.exit(1)

    save_file = sys.argv[1]
    
    if not os.path.exists(save_file):
        print(f"Error: Save file '{save_file}' not found.")
        sys.exit(1)
    
    editor = XCDESaveEditor(save_file)
    
    if len(sys.argv) == 2:
        # Just display character stats
        print("Character Stats:")
        print("-" * 50)
        for char_id in range(1, 16):  # Main characters are usually 1-15
            try:
                char_name = editor.get_character_name(char_id)
                level = editor.get_character_level(char_id)
                exp = editor.get_character_exp(char_id)
                ap = editor.get_character_ap(char_id)
                
                print(f"{char_id}: {char_name}")
                print(f"  Level: {level}")
                print(f"  XP: {exp}")
                print(f"  AP: {ap}")
                print("-" * 50)
            except Exception as e:
                pass  # Skip characters that might cause errors
    
    elif len(sys.argv) == 4 and sys.argv[2] == "alllevel":
        # Modify all characters' levels
        try:
            new_level = int(sys.argv[3])
        except ValueError:
            print("Error: Level must be a number.")
            sys.exit(1)
        
        try:
            editor.set_all_character_levels(new_level)
            
            # Save with a new filename to be safe
            modified_save = save_file + ".modified"
            editor.save(modified_save)
            
            print(f"Set all characters to level {new_level}")
            print(f"Modified save written to: {modified_save}")
        except Exception as e:
            print(f"Error modifying levels: {e}")
            sys.exit(1)
    
    elif len(sys.argv) == 4 and sys.argv[2] == "allartlevel":
        # Set level for all arts
        try:
            new_level = int(sys.argv[3])
        except ValueError:
            print("Error: Level must be a number.")
            sys.exit(1)
        
        try:
            editor.set_all_arts_levels(new_level)
            
            # Save with a new filename to be safe
            modified_save = save_file + ".modified"
            editor.save(modified_save)
            
            print(f"Set all arts to level {new_level}")
            print(f"Modified save written to: {modified_save}")
        except Exception as e:
            print(f"Error modifying arts: {e}")
            sys.exit(1)
    
    elif len(sys.argv) == 4 and sys.argv[2] == "allartmax":
        # Set max unlock level for all arts
        try:
            new_max = int(sys.argv[3])
        except ValueError:
            print("Error: Max level must be a number.")
            sys.exit(1)
        
        try:
            editor.set_all_arts_max_unlock(new_max)
            
            # Save with a new filename to be safe
            modified_save = save_file + ".modified"
            editor.save(modified_save)
            
            print(f"Set all arts to max unlock level {new_max}")
            print(f"Modified save written to: {modified_save}")
        except Exception as e:
            print(f"Error modifying arts: {e}")
            sys.exit(1)
    
    elif len(sys.argv) == 4:
        # Modify a character's XP
        try:
            char_id = int(sys.argv[2])
            new_xp = int(sys.argv[3])
        except ValueError:
            print("Error: Character ID and XP must be numbers.")
            sys.exit(1)
        
        try:
            char_name = editor.get_character_name(char_id)
            old_xp = editor.get_character_exp(char_id)
            old_level = editor.get_character_level(char_id)
            
            editor.set_character_exp(char_id, new_xp)
            
            # Save with a new filename to be safe
            modified_save = save_file + ".modified"
            editor.save(modified_save)
            
            print(f"Modified {char_name}'s XP from {old_xp} to {new_xp}")
            print(f"Current level: {old_level}")
            print(f"Modified save written to: {modified_save}")
            print("Note: You may need to adjust the level separately if you want it to match the new XP value.")
        except Exception as e:
            print(f"Error modifying character: {e}")
            sys.exit(1)
    
    elif len(sys.argv) == 5 and sys.argv[2] == "level":
        # Modify a character's level
        try:
            char_id = int(sys.argv[3])
            new_level = int(sys.argv[4])
        except ValueError:
            print("Error: Character ID and level must be numbers.")
            sys.exit(1)
        
        try:
            char_name = editor.get_character_name(char_id)
            old_level = editor.get_character_level(char_id)
            
            editor.set_character_level(char_id, new_level)
            
            # Save with a new filename to be safe
            modified_save = save_file + ".modified"
            editor.save(modified_save)
            
            print(f"Modified {char_name}'s level from {old_level} to {new_level}")
            print(f"Modified save written to: {modified_save}")
        except Exception as e:
            print(f"Error modifying character: {e}")
            sys.exit(1)
    
    elif len(sys.argv) == 5 and sys.argv[2] == "ap":
        # Modify a character's AP
        try:
            char_id = int(sys.argv[3])
            new_ap = int(sys.argv[4])
        except ValueError:
            print("Error: Character ID and AP must be numbers.")
            sys.exit(1)
        
        try:
            char_name = editor.get_character_name(char_id)
            old_ap = editor.get_character_ap(char_id)
            
            editor.set_character_ap(char_id, new_ap)
            
            # Save with a new filename to be safe
            modified_save = save_file + ".modified"
            editor.save(modified_save)
            
            print(f"Modified {char_name}'s AP from {old_ap} to {new_ap}")
            print(f"Modified save written to: {modified_save}")
        except Exception as e:
            print(f"Error modifying character: {e}")
            sys.exit(1)
    else:
        print("Invalid arguments. Use the script without arguments to see usage instructions.")