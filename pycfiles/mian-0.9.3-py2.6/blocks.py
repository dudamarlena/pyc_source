# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mian/blocks.py
# Compiled at: 2011-10-06 17:43:19
"""
Minecraft block names and hex values from
http://www.minecraftwiki.net/wiki/Data_values
"""
UNUSED_NAME = '<unused>'
BLOCK_TYPES = {'\x00': [
          'Air'], 
   '\x01': [
          'Stone'], 
   '\x02': [
          'Grass'], 
   '\x03': [
          'Dirt'], 
   '\x04': [
          'Cobblestone'], 
   '\x05': [
          'Wooden plank',
          'Wood',
          'Log'], 
   '\x06': [
          'Sapling'], 
   '\x07': [
          'Bedrock',
          'Adminium'], 
   '\x08': [
          'Water'], 
   '\t': [
        'Stationary water'], 
   '\n': [
        'Lava'], 
   '\x0b': [
          'Stationary lava'], 
   '\x0c': [
          'Sand'], 
   '\r': [
        'Gravel'], 
   '\x0e': [
          'Gold ore'], 
   '\x0f': [
          'Iron ore'], 
   '\x10': [
          'Coal ore'], 
   '\x11': [
          'Wood',
          'Log'], 
   '\x12': [
          'Leaves'], 
   '\x13': [
          'Sponge'], 
   '\x14': [
          'Glass'], 
   '\x15': [
          'Lapis lazuli ore',
          'Red cloth'], 
   '\x16': [
          'Lapis lazuli block',
          'Orange cloth'], 
   '\x17': [
          'Dispenser',
          'Yellow cloth'], 
   '\x18': [
          'Sandstone',
          'Lime cloth'], 
   '\x19': [
          'Note block',
          'Green cloth'], 
   '\x1a': [
          'Bed',
          'Aqua green cloth'], 
   '\x1b': [
          'Powered rail'], 
   '\x1c': [
          'Detector rail'], 
   '\x1d': [
          'Sticky Piston'], 
   '\x1e': [
          'Cobweb'], 
   '\x1f': [
          'Tall grass'], 
   ' ': [
       'Dead Shrubs'], 
   '!': [
       'Piston'], 
   '"': [
       'Piston extension'], 
   '#': [
       'Wool',
       'All colors cloth'], 
   '$': [
       'Block moved by piston'], 
   '%': [
       'Yellow flower'], 
   '&': [
       'Red rose'], 
   "'": [
       'Brown mushroom'], 
   '(': [
       'Red mushroom'], 
   ')': [
       'Gold block'], 
   '*': [
       'Iron block'], 
   '+': [
       'Double stone slab',
       'Double slab',
       'Double step'], 
   ',': [
       'Stone slab',
       'Step'], 
   '-': [
       'Brick'], 
   '.': [
       'TNT'], 
   '/': [
       'Bookshelf'], 
   '0': [
       'Moss stone',
       'Mossy cobblestone'], 
   '1': [
       'Obsidian'], 
   '2': [
       'Torch'], 
   '3': [
       'Fire'], 
   '4': [
       'Monster spawner',
       'Mob spawner'], 
   '5': [
       'Wooden stairs'], 
   '6': [
       'Chest'], 
   '7': [
       'Redstone wire'], 
   '8': [
       'Diamond ore',
       'Emerald ore'], 
   '9': [
       'Diamond block',
       'Emerald block'], 
   ':': [
       'Workbench'], 
   ';': [
       'Crops'], 
   '<': [
       'Farmland',
       'Soil'], 
   '=': [
       'Furnace'], 
   '>': [
       'Burning furnace'], 
   '?': [
       'Sign post'], 
   '@': [
       'Wooden door'], 
   'A': [
       'Ladder'], 
   'B': [
       'Minecart tracks',
       'Rails'], 
   'C': [
       'Cobblestone stairs'], 
   'D': [
       'Wall sign'], 
   'E': [
       'Lever'], 
   'F': [
       'Stone pressure plate'], 
   'G': [
       'Iron door'], 
   'H': [
       'Wooden pressure plate'], 
   'I': [
       'Redstone ore'], 
   'J': [
       'Glowing redstone ore'], 
   'K': [
       'Redstone torch [off]'], 
   'L': [
       'Redstone torch [on]'], 
   'M': [
       'Stone button'], 
   'N': [
       'Snow'], 
   'O': [
       'Ice'], 
   'P': [
       'Snow block'], 
   'Q': [
       'Cactus'], 
   'R': [
       'Clay'], 
   'S': [
       'Sugar cane',
       'Reed',
       'Bamboo',
       'Papyrus'], 
   'T': [
       'Jukebox'], 
   'U': [
       'Fence'], 
   'V': [
       'Pumpkin'], 
   'W': [
       'Netherrack',
       'Bloodstone',
       'Hellstone',
       'Netherstone',
       'Red mossy cobblestone'], 
   'X': [
       'Soul sand',
       'Hell mud',
       'Mud',
       'Nethermud',
       'Slow sand'], 
   'Y': [
       'Glowstone',
       'Lightstone',
       'Brittle gold',
       'Brightstone',
       'Australium',
       'Brimstone'], 
   'Z': [
       'Portal'], 
   '[': [
       'Jack-o-lantern'], 
   '\\': [
        'Cake block'], 
   ']': [
       'Redstone repeater [off]'], 
   '^': [
       'Redstone repeater [on]'], 
   '_': [
       'Locked chest'], 
   '`': [
       'Trapdoor'], 
   'a': [
       'Hidden Silverfish',
       'Silverfish'], 
   'b': [
       'Stone Bricks'], 
   'c': [
       'Huge Brown Mushroom'], 
   'd': [
       'Huge Red Mushroom'], 
   'e': [
       'Iron Bars'], 
   'f': [
       'Glass Pane'], 
   'g': [
       'Melon'], 
   'h': [
       'Pumpkin Stem'], 
   'i': [
       'Melon Stem'], 
   'j': [
       'Vines'], 
   'k': [
       'Fence Gate'], 
   'l': [
       'Brick Stairs'], 
   'm': [
       'Stone Brick Stairs'], 
   'n': [
       'Mycelium'], 
   'o': [
       'Lily Pad'], 
   'p': [
       'Nether Brick'], 
   'q': [
       'Nether Brick Fence'], 
   'r': [
       'Nether Brick Stairs'], 
   's': [
       'Nether Wart'], 
   't': [
       'Enchantment Table'], 
   'u': [
       'Brewing Stand'], 
   'v': [
       'Cauldron'], 
   'w': [
       UNUSED_NAME], 
   'x': [
       UNUSED_NAME], 
   'y': [
       UNUSED_NAME], 
   'z': [
       UNUSED_NAME], 
   '{': [
       UNUSED_NAME], 
   '|': [
       UNUSED_NAME], 
   '}': [
       UNUSED_NAME], 
   '~': [
       UNUSED_NAME], 
   '\x7f': [
          UNUSED_NAME], 
   b'\x80': [
           UNUSED_NAME], 
   b'\x81': [
           UNUSED_NAME], 
   b'\x82': [
           UNUSED_NAME], 
   b'\x83': [
           UNUSED_NAME], 
   b'\x84': [
           UNUSED_NAME], 
   b'\x85': [
           UNUSED_NAME], 
   b'\x86': [
           UNUSED_NAME], 
   b'\x87': [
           UNUSED_NAME], 
   b'\x88': [
           UNUSED_NAME], 
   b'\x89': [
           UNUSED_NAME], 
   b'\x8a': [
           UNUSED_NAME], 
   b'\x8b': [
           UNUSED_NAME], 
   b'\x8c': [
           UNUSED_NAME], 
   b'\x8d': [
           UNUSED_NAME], 
   b'\x8e': [
           UNUSED_NAME], 
   b'\x8f': [
           UNUSED_NAME], 
   b'\x90': [
           UNUSED_NAME], 
   b'\x91': [
           UNUSED_NAME], 
   b'\x92': [
           UNUSED_NAME], 
   b'\x93': [
           UNUSED_NAME], 
   b'\x94': [
           UNUSED_NAME], 
   b'\x95': [
           UNUSED_NAME], 
   b'\x96': [
           UNUSED_NAME], 
   b'\x97': [
           UNUSED_NAME], 
   b'\x98': [
           UNUSED_NAME], 
   b'\x99': [
           UNUSED_NAME], 
   b'\x9a': [
           UNUSED_NAME], 
   b'\x9b': [
           UNUSED_NAME], 
   b'\x9c': [
           UNUSED_NAME], 
   b'\x9d': [
           UNUSED_NAME], 
   b'\x9e': [
           UNUSED_NAME], 
   b'\x9f': [
           UNUSED_NAME], 
   b'\xa0': [
           UNUSED_NAME], 
   b'\xa1': [
           UNUSED_NAME], 
   b'\xa2': [
           UNUSED_NAME], 
   b'\xa3': [
           UNUSED_NAME], 
   b'\xa4': [
           UNUSED_NAME], 
   b'\xa5': [
           UNUSED_NAME], 
   b'\xa6': [
           UNUSED_NAME], 
   b'\xa7': [
           UNUSED_NAME], 
   b'\xa8': [
           UNUSED_NAME], 
   b'\xa9': [
           UNUSED_NAME], 
   b'\xaa': [
           UNUSED_NAME], 
   b'\xab': [
           UNUSED_NAME], 
   b'\xac': [
           UNUSED_NAME], 
   b'\xad': [
           UNUSED_NAME], 
   b'\xae': [
           UNUSED_NAME], 
   b'\xaf': [
           UNUSED_NAME], 
   b'\xb0': [
           UNUSED_NAME], 
   b'\xb1': [
           UNUSED_NAME], 
   b'\xb2': [
           UNUSED_NAME], 
   b'\xb3': [
           UNUSED_NAME], 
   b'\xb4': [
           UNUSED_NAME], 
   b'\xb5': [
           UNUSED_NAME], 
   b'\xb6': [
           UNUSED_NAME], 
   b'\xb7': [
           UNUSED_NAME], 
   b'\xb8': [
           UNUSED_NAME], 
   b'\xb9': [
           UNUSED_NAME], 
   b'\xba': [
           UNUSED_NAME], 
   b'\xbb': [
           UNUSED_NAME], 
   b'\xbc': [
           UNUSED_NAME], 
   b'\xbd': [
           UNUSED_NAME], 
   b'\xbe': [
           UNUSED_NAME], 
   b'\xbf': [
           UNUSED_NAME], 
   b'\xc0': [
           UNUSED_NAME], 
   b'\xc1': [
           UNUSED_NAME], 
   b'\xc2': [
           UNUSED_NAME], 
   b'\xc3': [
           UNUSED_NAME], 
   b'\xc4': [
           UNUSED_NAME], 
   b'\xc5': [
           UNUSED_NAME], 
   b'\xc6': [
           UNUSED_NAME], 
   b'\xc7': [
           UNUSED_NAME], 
   b'\xc8': [
           UNUSED_NAME], 
   b'\xc9': [
           UNUSED_NAME], 
   b'\xca': [
           UNUSED_NAME], 
   b'\xcb': [
           UNUSED_NAME], 
   b'\xcc': [
           UNUSED_NAME], 
   b'\xcd': [
           UNUSED_NAME], 
   b'\xce': [
           UNUSED_NAME], 
   b'\xcf': [
           UNUSED_NAME], 
   b'\xd0': [
           UNUSED_NAME], 
   b'\xd1': [
           UNUSED_NAME], 
   b'\xd2': [
           UNUSED_NAME], 
   b'\xd3': [
           UNUSED_NAME], 
   b'\xd4': [
           UNUSED_NAME], 
   b'\xd5': [
           UNUSED_NAME], 
   b'\xd6': [
           UNUSED_NAME], 
   b'\xd7': [
           UNUSED_NAME], 
   b'\xd8': [
           UNUSED_NAME], 
   b'\xd9': [
           UNUSED_NAME], 
   b'\xda': [
           UNUSED_NAME], 
   b'\xdb': [
           UNUSED_NAME], 
   b'\xdc': [
           UNUSED_NAME], 
   b'\xdd': [
           UNUSED_NAME], 
   b'\xde': [
           UNUSED_NAME], 
   b'\xdf': [
           UNUSED_NAME], 
   b'\xe0': [
           UNUSED_NAME], 
   b'\xe1': [
           UNUSED_NAME], 
   b'\xe2': [
           UNUSED_NAME], 
   b'\xe3': [
           UNUSED_NAME], 
   b'\xe4': [
           UNUSED_NAME], 
   b'\xe5': [
           UNUSED_NAME], 
   b'\xe6': [
           UNUSED_NAME], 
   b'\xe7': [
           UNUSED_NAME], 
   b'\xe8': [
           UNUSED_NAME], 
   b'\xe9': [
           UNUSED_NAME], 
   b'\xea': [
           UNUSED_NAME], 
   b'\xeb': [
           UNUSED_NAME], 
   b'\xec': [
           UNUSED_NAME], 
   b'\xed': [
           UNUSED_NAME], 
   b'\xee': [
           UNUSED_NAME], 
   b'\xef': [
           UNUSED_NAME], 
   b'\xf0': [
           UNUSED_NAME], 
   b'\xf1': [
           UNUSED_NAME], 
   b'\xf2': [
           UNUSED_NAME], 
   b'\xf3': [
           UNUSED_NAME], 
   b'\xf4': [
           UNUSED_NAME], 
   b'\xf5': [
           UNUSED_NAME], 
   b'\xf6': [
           UNUSED_NAME], 
   b'\xf7': [
           UNUSED_NAME], 
   b'\xf8': [
           UNUSED_NAME], 
   b'\xf9': [
           UNUSED_NAME], 
   b'\xfa': [
           UNUSED_NAME], 
   b'\xfb': [
           UNUSED_NAME], 
   b'\xfc': [
           UNUSED_NAME], 
   b'\xfd': [
           UNUSED_NAME], 
   b'\xfe': [
           UNUSED_NAME], 
   b'\xff': [
           UNUSED_NAME]}