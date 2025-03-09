# Xenoblade Chronicles: Definitive Edition Save Editor

A Python tool for modifying Xenoblade Chronicles: Definitive Edition save files. This editor allows you to change character levels, XP, AP, and arts levels without needing to use the more complex C# library.

## Features

- View character stats (Level, XP, AP)
- Modify individual character stats
- Set all characters to the same level at once
- View arts levels and max unlock levels
- Modify arts levels and max unlock thresholds
- Set all arts to max level at once

## Requirements

- Python 3.6 or higher

## Installation

1. Download the `xcde_editor.py` script
2. Place it in a directory with your save files or where you have access to them

## Save File Location

- On Nintendo Switch: Save files are stored on the console (requires custom firmware to access)
- On Yuzu or Ryujinx emulators: Save files are typically located in the emulator's save directory
  - Save file format: `bfsgame0xx.sav` (where xx is the save slot number)

## Usage

### View Character Information

```bash
python xcde_editor.py path/to/your/savefile.sav
```

### Modify a Specific Character's XP

```bash
python xcde_editor.py path/to/your/savefile.sav <character_id> <new_xp>
```

Example:
```bash
python xcde_editor.py bfsgame01.sav 1 500000
```
This sets Shulk's (ID 1) XP to 500,000.

### Modify a Character's Level

```bash
python xcde_editor.py path/to/your/savefile.sav level <character_id> <new_level>
```

Example:
```bash
python xcde_editor.py bfsgame01.sav level 2 99
```
This sets Reyn's (ID 2) level to 99.

### Set All Characters to the Same Level

```bash
python xcde_editor.py path/to/your/savefile.sav alllevel <new_level>
```

Example:
```bash
python xcde_editor.py bfsgame01.sav alllevel 99
```
This sets all characters to level 99.

### Modify a Character's AP

```bash
python xcde_editor.py path/to/your/savefile.sav ap <character_id> <new_ap>
```

Example:
```bash
python xcde_editor.py bfsgame01.sav ap 1 99999
```
This sets Shulk's AP to 99,999.

### Set All Arts to a Specific Level

```bash
python xcde_editor.py path/to/your/savefile.sav allartlevel <new_level>
```

Example:
```bash
python xcde_editor.py bfsgame01.sav allartlevel 12
```
This sets all arts to level 12 (max level).

### Set Max Unlock Level for All Arts

```bash
python xcde_editor.py path/to/your/savefile.sav allartmax <new_max_level>
```

Max level values:
- 0: IV_BEGINNER (up to level 4)
- 1: VII_INTERMEDIATE (up to level 7)
- 2: X_EXPERT (up to level 10)
- 3: XII_MASTER (up to level 12)

Example:
```bash
python xcde_editor.py bfsgame01.sav allartmax 3
```
This allows all arts to be upgraded to level 12 (XII_MASTER).

## Character IDs

| ID | Character |
|---|---|
| 1 | SHULK |
| 2 | REYN |
| 3 | FIORA |
| 4 | DUNBAN |
| 5 | SHARLA |
| 6 | RIKI |
| 7 | MELIA |
| 8 | FIORA_2 |
| 9 | DICKSON |
| 10 | MUMKHAR |
| 11 | ALVIS |
| 12 | DUNBAN_2 |
| 13 | DUNBAN_3 |
| 14 | KINO |
| 15 | NENE |

## Safety Features

- The editor automatically creates a backup of your save file before making changes
- Modified saves are written to a new file with `.modified` extension to avoid overwriting your original
- All modifications include validation to help prevent corruption

## Advanced Usage

If you need more advanced save editing functionality, consider checking out the original C# library this editor is based on at [damysteryman/XCDESave](https://github.com/damysteryman/XCDESave).

## Credits

This editor is based on the save file structure reverse-engineered by damysteryman's XCDESave C# library. The Python implementation provides a simplified interface for the most common editing needs.

## License

This tool is provided under the GNU General Public License v3, the same as the original C# library it's based on.

## Warning

- Modifying save files could potentially corrupt them or lead to issues in the game. Always use the backups if something goes wrong.
- This editor doesn't modify checksums (if any exist in the save file), which might cause issues in some game versions.
