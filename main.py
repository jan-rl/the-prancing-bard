#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# libtcod python tutorial
#

import libtcodpy as libtcod
import math
import textwrap
import shelve
import time
import random
import re

import winsound

#my modules
import monsters
import maps
import text
import tiles
import timer

#globals ;)

colorblind = False

available_notes = 'abcdefgh'#i

song_of_world = ''
for i in range(50):
    song_of_world = song_of_world + random.choice(available_notes)

bard_song = ''

directioner = [0,0]

dict_char_color = {  'a': [chr(14),'fuchsia'], 
                'b': [chr(13),'red'],
                'c': [chr(14),'orange'],
                'd': [chr(13),'yellow'],
                'e': [chr(14),'light_chartreuse'],
                'f': [chr(13),'dark_green'],
                'g': [chr(14),'cyan'],
                'h': [chr(13),'blue'],
                #'i': [chr(13),'white'],
                '-': ['-', 'white'],
                'X': ['X', 'dark_orange'],
                'S': ['S', 'lighter_sepia'],
                'C': ['C', 'blue']
            }

dict_direct = { 'a': (-1,-1), 
                'b': (0,-1),
                'c': (1,-1),
                'd': (1, 0),
                'e': (1, 1),
                'f': (0, 1),
                'g': (-1,1),
                'h': (-1,0)
                #'i': (0,0)
            }
            
gen_dict = {
    'grassland': 'rat_hole',
    'castle': 'dungeon_entrance',
    'dungeon': 'stairs_down',
    'cave': 'cleft',
    'hell': 'monster_house',
    'endless': 'nest'
    }

#actual size of the window
SCREEN_WIDTH = 70
SCREEN_HEIGHT = 50

#size of the map
MAP_WIDTH = 50
MAP_HEIGHT = 40

#sizes and coordinates relevant for the GUI
PANEL_HEIGHT = SCREEN_HEIGHT - MAP_HEIGHT
PANEL_WIDTH = 50
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = 8
MSG_WIDTH = PANEL_WIDTH - MSG_X
MSG_HEIGHT = PANEL_HEIGHT - 5

#GUI column on the right
COLUMN_HEIGHT = 50
COLUMN_WIDTH = 20
COLUMN_Y = 0
COLUMN_X = MAP_WIDTH

PLAYER_NAME = 'You'

FOV_ALGO = 0  #default FOV algorithm
FOV_LIGHT_WALLS = True  #light walls or not

LIMIT_FPS = 20  #20 frames-per-second maximum

#---------------------------------------------------------------------------------------------------------

class Object:
    '''this is a generic object the player, a monster, an item, the stairs
    it's always represented by a character on screen.'''
    def __init__(self, x, y, char, name, color, blocks=False, always_visible=False, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.always_visible = always_visible
        self.fighter = fighter
        if self.fighter:  #let the fighter component know who owns it
            self.fighter.owner = self

        self.ai = ai
        if self.ai:  #let the AI component know who owns it
            self.ai.owner = self

    def move(self, dx, dy):
        '''moves the object if not blocked'''
        #check if leaving the map
        if self.x + dx < 0 or self.x + dx >= MAP_WIDTH or self.y + dy < 0 or self.y + dy >= MAP_HEIGHT:
            return
        #move by the given amount, if the destination is not blocked
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            
    def move_towards(self, target_x, target_y):
        '''calculates the movement of a smart object and calls move then'''
        # #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        # distance = math.sqrt(dx ** 2 + dy ** 2)

        ddx = 0 
        ddy = 0
        if dx > 0:
            ddx = 1
        elif dx < 0:
            ddx = -1
        if dy > 0:
            ddy = 1
        elif dy < 0:
            ddy = -1
        if not is_blocked(self.x + ddx, self.y + ddy):
            self.move(ddx, ddy)
        else:
            if ddx != 0:
                if not is_blocked(self.x + ddx, self.y):
                    self.move(ddx, 0)
                    return
            if ddy != 0:
                if not is_blocked(self.x, self.y + ddy):
                    self.move(0, ddy)
                    return
    
    def distance_to(self, other):
        '''returns the distance of object to another object'''
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        '''returns the distance of object to some coordinates'''
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def send_to_back(self):
        '''make this object be drawn first, so all others appear above it if they're in the same tile.'''
        global objects
        objects.remove(self)
        objects.insert(0, self)

    def draw(self):
        '''draws the object to console "con", only called by render_all'''
        #only show if it's visible to the player; or it's set to "always visible" and on an explored tile
        if (libtcod.map_is_in_fov(fov_map, self.x, self.y) or
                (self.always_visible and map[self.x][self.y].explored)):
            #set the color and then draw the character that represents this object at its position
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        '''erase the character that represents this object, BUGGY and NOT needed cause render_all'''
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            #char = map[self.x][self.y].char_light
            #color = map[self.x][self.y].color_light
            libtcod.console_put_char_ex(con, self.x, self.y, '.', libtcod.grey, libtcod.black)
            
    def delete(self):
        '''triggers easy removal of object and clears the char'''
        for obj in objects:
            if self in objects:
                objects.remove(self)
        self.clear()

class Fighter:
    '''component of object to make it attacking and attackable contains
    combat-related properties and methods (monster, player, NPC).'''
    def __init__(self, hp, damage, death_function=None):

        self.base_hp = hp
        self.hp = hp  
        self.base_damage = damage
        self.death_function = death_function

    @property
    def max_hp(self):
        '''the maximum possible hp of a fighter'''
        return self.base_hp
        
    @property
    def damage(self):
        '''return actual damage, by summing up the bonuses from all equipped items. Unmodified in TPB'''
        return self.base_damage
    
    def attack(self, target):
        '''call take_damage on target'''
        target.fighter.take_damage(self.damage)
         
    def take_damage(self, damage):
        '''is called by attacker and checks status of owner and deals damage. triggers fighter.death_function upon hp <= 0'''
        #apply damage if possible    
        if damage > 0:
            self.hp -= damage
            if self.owner == player:
                message('You get ' + str(damage) + ' damage.', libtcod.red)
     
        #check for death. if there's a death function, call it
        if self.hp <= 0:
            self.hp = 0
            function = self.death_function
            if function is not None:
                function(self.owner)

class PlayerAI:
    '''Is actually the one who plays TPB. Needed to be scheduled. Takes keyboard input and calls handle_keys
    Renders screen and exits game, kind of the actual main loop together with play_game.
    '''
    def __init__(self, ticker, speed):
        self.ticker = ticker
        self.speed = speed
        self.ticker.schedule_turn(self.speed, self)
        
    def take_turn(self):
        '''called by scheduler on the players turn, contains the quasi main loop'''
        global key, mouse, fov_recompute
        action_speed = self.speed
        
        while True:
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
            #render the screen
            render_all()
            libtcod.console_flush()
            
            player_action = handle_keys()
            
            if player_action == 'exit' or game_state == 'exit':
                break
                main_menu()
            
            if player_action != 'didnt-take-turn':
                fov_recompute = True
                break
            
        self.ticker.schedule_turn(action_speed, self)
                        
class BasicMonster:
    '''AI for a basic monster. Schedules the turn depending on speed and decides whether to move or attack.
    Owned by all monsters apart from bosses.
    '''
    def __init__(self, ticker, speed):
        self.ticker = ticker
        self.speed = speed
        self.ticker.schedule_turn(self.speed, self)
    
    def take_turn(self):
        '''checks whether monster and player are still alive, decides on move or attack'''
        #a basic monster takes its turn.
        monster = self.owner
        
        if not monster.fighter: #most likely because monster is dead
            return
        #stop when the player is already dead
        if game_state == 'dead':
            return
        
        #move towards player if far away
        if monster.distance_to(player) >= 2:
            (x,y) = monster.x, monster.y
            monster.move_towards(player.x, player.y)
            if monster.x == x and monster.y == y: #not moved?
                monster.move(libtcod.random_get_int(0,-1,1), libtcod.random_get_int(0,-1,1)) #try again randomly
            
        #close enough, attack! (if the player is still alive.)
        elif player.fighter.hp > 0:
            monster.fighter.attack(player)
        
        #schedule next turn
        self.ticker.schedule_turn(self.speed, self)            
            
class Corpse:
    '''given to monster upon their death, ticker to count down for corpse to disappear with delay'''
    def __init__(self, ticker, owner, speed=60): #corpse ceasess after 10 turns
        self.ticker = ticker
        self.owner = owner
        self.speed = speed
        self.ticker.schedule_turn(self.speed, self)
    
    def take_turn(self):
        self.owner.delete()
            
                   
class NoisyMonster:
    '''AI for bosses and monsters who can make noise, decides on movement or attack and makes noise sometimes'''
    
    def __init__(self, ticker, speed=6):
        self.ticker = ticker
        self.speed = speed
        self.ticker.schedule_turn(self.speed, self)
        
    def take_turn(self):
        '''only difference to BasicMonster is the small chance to call make_noise'''
        monster = self.owner
       
        if not monster.fighter: #most likely because monster is dead
            return
        #stop when the player is already dead
        if game_state == 'dead':
            return
       
        #move towards player if far away
        if monster.distance_to(player) >= 2:
            monster.move_towards(player.x, player.y)

        #close enough, attack! (if the player is still alive.)
        elif player.fighter.hp > 0:
            monster.fighter.attack(player)
        
        #with 3 % prob the monster makes noise on its turn
        if libtcod.random_get_int(0,0,100) <= 3:
            self.make_noise()
        
        #schedule next turn
        self.ticker.schedule_turn(self.speed, self)            
            
    def make_noise(self):
        '''includes the disturbance to the melody, customized by owner.name according to dict'''
        dict_com = {
        'pied rat': ['squieks','S'],
        'commander': ['commands','C'],
        'knocker': ['knocks','X'],
        'banshee': ['wails','---']
        }
        #instert disturbance
        continue_song_of_world(dict_com[self.owner.name][1])
        #let the player know
        message('The ' + self.owner.name + ' ' + dict_com[self.owner.name][0] + '!') 
        
class EndlessTicker:
    '''Timer object which runs in highscore mode only controling monster difficulty by turns passed, by increasing dungeon level'''
    def __init__(self, ticker, speed=1000): #every approx 150 turns the dungeon level is increased
        self.ticker = ticker
        self.speed = speed
        self.ticker.schedule_turn(self.speed, self)
        
    def take_turn(self):
        global dungeon_level
        
        #influences the GeneratorAIEnd for monster spaw decision
        dungeon_level += 1

        self.ticker.schedule_turn(self.speed, self)            
        
class GeneratorAIEnd:
    '''ticker scheduled as AI of spawn points in highscore mode
    Decides every turn on whether to spawn a monster and which
    '''
    def __init__(self, ticker, speed=6):
        self.ticker = ticker
        self.speed = speed
        self.ticker.schedule_turn(self.speed, self)
    
    def take_turn(self):
        #only spawn monster with 10 % prob
        if libtcod.random_get_int(0,0,100) <= 10:  
            
            free_spots_around = [] #set up list of free spots around the generator
            
            for i in range(-1,2):
                for j in range(-1,2):
                    x = self.owner.x+i
                    y = self.owner.y+j
                    if not is_blocked(x, y):
                        free_spots_around.append([x,y])
            
            choice = [] #choose a spot if there are free spots
            
            if free_spots_around:
                choice = free_spots_around[ libtcod.random_get_int(0,0,len(free_spots_around)-1) ]
                     
            #decide on which monster to spawn with [probability, depending on dungeon level]
            #dungeon levels for highscore mode are always > 4
            monster_chances = {}
            monster_chances['rat'] = from_dungeon_level([[70, 5],[60, 6],[55, 7],[60, 8],[60, 9] ])
            monster_chances['goblin'] = from_dungeon_level([[10, 5],[10, 6],[5, 7],[10, 8],[10, 9] ])
            monster_chances['pixie'] = from_dungeon_level([[20, 5],[20, 6],[20, 7],[20, 8],[20, 9] ])
            monster_chances['bandit'] = from_dungeon_level([[10, 6],[20, 7],[10, 8],[10, 9] ])
            monster_chances['pied_rat'] = from_dungeon_level([[1, 7],[1, 8],[5, 11] ])
            monster_chances['banshee'] = from_dungeon_level([[1, 10] ])
            monster_chances['commander'] = from_dungeon_level([[1, 8] ])
            monster_chances['knocker'] = from_dungeon_level([[1, 11] ])
            
            #decide on a monster
            monster = random_choice(monster_chances)        
        
            if choice and monster:
                create_monster(monster, choice[0], choice[1])
      
        self.ticker.schedule_turn(self.speed, self)            
        
        
class GeneratorAI:
    '''ticker scheduled as AI of spawn points in highscore mode
    Decides every turn on whether to spawn a monster and which
    '''
    def __init__(self, ticker, speed=6):
        self.ticker = ticker
        self.speed = speed
        self.ticker.schedule_turn(self.speed, self)
    
    def take_turn(self):
        #only spawn monster with 10 % prob    
        if libtcod.random_get_int(0,0,100) <= 10:    
            
            free_spots_around = [] #set up list of free spots around the generator
            
            for i in range(-1,2):
                for j in range(-1,2):
                    x = self.owner.x+i
                    y = self.owner.y+j
                    if not is_blocked(x, y):
                        free_spots_around.append([x,y])
            
            choice = [] #choose a spot if there are free spots
            
            if free_spots_around:
                choice = free_spots_around[  libtcod.random_get_int(0,0,len(free_spots_around)-1)  ]
        
            #checking for dungeon levels is not elegant cause [probability, depending on dungeon level] already
            if dungeon_level == 0:
                #assigns monsters, bosses and their probability to levels
                #let boss appear, when 40 points scored and make sure only one boss appears
                x = 0
                boss = False
                for obj in objects:
                    if obj.name == 'pied rat':
                        boss = True
                if score > 40 and not boss:                
                    x = 10
                
                monster_chances = {}
                monster_chances['rat'] = from_dungeon_level([[85, 0]])
                monster_chances['goblin'] = from_dungeon_level([[15, 0]])
                monster_chances['pied_rat_boss'] = from_dungeon_level([[x, 0]])
                
            elif dungeon_level == 1:
                x = 0
                boss = False
                for obj in objects:
                    if obj.name == 'commander':
                        boss = True
                if score > 50 and not boss:                
                    x = 10
                monster_chances = {}
                monster_chances['rat'] = from_dungeon_level([[75, 0]])
                monster_chances['goblin'] = from_dungeon_level([[15, 0]])
                monster_chances['pixie'] = from_dungeon_level([[10, 0]])
                monster_chances['commander_boss'] = from_dungeon_level([[x, 0]])
            
            elif dungeon_level == 2:
                x = 0
                boss = False
                for obj in objects:
                    if obj.name == 'knocker':
                        boss = True
                if score > 60 and not boss:                
                    x = 10
                monster_chances = {}
                monster_chances['rat'] = from_dungeon_level([[60, 0]])
                monster_chances['bandit'] = from_dungeon_level([[15, 0]])
                monster_chances['pixie'] = from_dungeon_level([[20, 0]])
                monster_chances['leprechaun'] = from_dungeon_level([[7, 0]])
                monster_chances['knocker_boss'] = from_dungeon_level([[x, 0]])
            
            elif dungeon_level == 3:
                x = 0
                boss = False
                for obj in objects:
                    if obj.name == 'banshee':
                        boss = True
                if score > 70 and not boss:                
                    x = 10
                monster_chances = {}
                monster_chances['rat'] = from_dungeon_level([[55, 0]])
                monster_chances['bandit'] = from_dungeon_level([[15, 0]])
                monster_chances['pixie'] = from_dungeon_level([[30, 0]])
                monster_chances['banshee_boss'] = from_dungeon_level([[x, 0]])
            
            elif dungeon_level == 4:
                x = 0
                boss = False
                for obj in objects:
                    if obj.name == 'cyclops':
                        boss = True
                if score > 80 and not boss:                
                    x = 10
                monster_chances = {}
                monster_chances['rat'] = from_dungeon_level([[60, 0]])
                monster_chances['bandit'] = from_dungeon_level([[30, 0]])
                monster_chances['pixie'] = from_dungeon_level([[20, 0]])
                monster_chances['banshee'] = from_dungeon_level([[1, 0]])
                monster_chances['pied_rat'] = from_dungeon_level([[1, 0]])
                monster_chances['commander'] = from_dungeon_level([[1, 0]])
                monster_chances['knocker'] = from_dungeon_level([[1, 0]])
                monster_chances['cyclops_boss'] = from_dungeon_level([[x, 0]])
            
            monster = random_choice(monster_chances)        
            
            if choice and monster:
                create_monster(monster, choice[0], choice[1])
            
        self.ticker.schedule_turn(self.speed, self)            


def random_choice_index(chances):  
    '''choose one option from list of chances, returning its index
    the dice will land on some number between 1 and the sum of the chances'''
    dice = libtcod.random_get_int(0, 1, sum(chances))

    #go through all chances, keeping the sum so far
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        #see if the dice landed in the part that corresponds to this choice
        if dice <= running_sum:
            return choice
        choice += 1

def random_choice(chances_dict):
    '''choose one option from dictionary of chances, returning its key'''
    chances = chances_dict.values()
    strings = chances_dict.keys()

    return strings[random_choice_index(chances)]

def from_dungeon_level(table):
    '''returns a value that depends on level. the table specifies what value occurs after each level, default is 0.'''
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value
    return 0
   
            
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def make_map(var):
    '''selects which map to make depending on dungeon level. var is doing nothing. 
    Highscore mode is executed on dungeon levels > 4'''
    global dungeon_level
    
    #general function for decision, which map to make
    if dungeon_level == 0:
        make_preset_map('grassland')
        place_preset_objects('grassland')
        
    elif dungeon_level == 1:
        make_preset_map('castle')
        place_preset_objects('castle')
        
    elif dungeon_level == 2:
        make_preset_map('dungeon')
        place_preset_objects('dungeon')
    
    elif dungeon_level == 3:
        make_cave()
        place_cave_objects()
        
    elif dungeon_level == 4:
        make_preset_map('hell')
        place_preset_objects('hell')
        
    else: #highscore mode
        make_preset_map('hell')
        place_preset_objects('endless')

def is_blocked(x, y):
    '''called to check if coordinates are blocked by
    -being outside the map
    -blocked tile
    -monster blocking a tile
    returns boolean
    '''
    #check if outside the map, it's blocked out there
    if x > MAP_WIDTH or y > MAP_HEIGHT or x < 0 or y < 0:
        return True
    
    #first test the map tile
    if map[x][y].blocked:
        return True
    #now check for any blocking objects
    for object in objects:
        if object.blocks and object.x == x and object.y == y:
            return True
    
    return False

#------------------------------------------------------------------------------------------
   
def make_cave():
    '''starting function to make cellular automaton for cave level'''
    global map
    #fill map with "blocked wall" tiles
    map = [[ tiles.Tile(True, type = 'empty')
             for y in range(MAP_HEIGHT) ]
           for x in range(MAP_WIDTH) ]
    
    #randomly blank 55 % of the tiles
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if libtcod.random_get_int(0,0,100) <= 40:
                map[x][y].change_type('ice')

    #5 iterations ;)
    map = cellular_iteration(map)
    map = cellular_iteration(map)
    map = cellular_iteration(map)
    map = cellular_iteration(map)
    map = cellular_iteration(map)
     
def cellular_iteration(map):
    '''the iteration function over the random map. 4-5 rule chooses depending on neighbors''' 
    map_c = map[:]
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if map[x][y].type == 'empty':
                neighbors = tile_neighbors(x,y,map)
                if count_empty(neighbors) < 4:
                    map_c[x][y].change_type('ice')
            
            elif map[x][y].type == 'ice':
                neighbors = tile_neighbors(x,y,map)
                if count_empty(neighbors) >= 5:
                    map_c[x][y].change_type('empty')
    return map_c
    
def tile_neighbors(x, y, map):
    '''returns all neighbors of a tile x,y in map. part of cellular automaton'''
    neighbors = []
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:
                continue
            if x+i > 0 and x+i < MAP_WIDTH and y+j > 0 and y+j < MAP_HEIGHT:
                neighbors.append(map[x+i][y+j]) 
    return neighbors
    
def count_empty(list_of_neighbors):
    '''returns number of empy tiles in list of neighbors. part of cellular automaton'''
    empty = 0
    for i in list_of_neighbors:
        if i.name == 'empty':
            empty += 1
    return empty
   
def place_cave_objects():
    '''places the generators and players in the cave. has to check for non blocked spots around the starting area'''
    global objects
    
    generators = ['g','g','g','i','i','i','i','i']
    random.shuffle(generators)
    
    coordinates = [ [4,4], [25,4], [46,4],
                    [4,19,], [46,19],
                    [4,36], [25,36], [46,36]
                    ]
    random.shuffle(coordinates)
    
    while generators:
        i = generators.pop()
        j = coordinates.pop()
        if i == 'g':
            (x,y) = j
            if is_blocked(j[0],j[1]):
                (x,y) = find_non_blocked(j[0],j[1])
            
            objects.append(create_object('cleft', x, y))
    
    if not is_blocked(25,20):
        player.x = 25
        player.y = 20
    else:
        (x,y) = find_non_blocked(25,20)
        player.x = x
        player.y = y
    
    
def find_non_blocked(x, y):
    '''checks a 10x10 square for starting area, whether a free spot can be found to set player/generator'''
    #gather all spots
    set = []
    for i in range(-7,7):
        for j in range(-7,7):
            set.append([i,j])
    
    while True:
        d = set.pop() #check all spots
        if not is_blocked(x+d[0],y+d[1]):
            return x+d[0],y+d[1]
            break
        if not d:
            return 0,0
            break
  
#--------------------------------------------------------------------------------------------   

def get_map_char(location_name, x, y):
    '''helper function to check maps.py for list with location_name checks coordinates and returns char
    e.g. maps.temple and would give maps.temple[y][x] == "+"'''
    i = getattr(maps, location_name)
    return i[y][x]
   
def make_preset_map(location_name):
    '''fills map with tiles according to layout in maps.py using get_map_char and maps.type_to_char'''
    global map
    map = []
    
    #fill map with tiles according to preset maps.py (objects kept blank)
    map = [[ tiles.Tile(True, type = maps.char_to_type( get_map_char(location_name, x, y ) ) )
             for y in range(MAP_HEIGHT) ]
           for x in range(MAP_WIDTH) ]  
    
    #only for one stage, ugly here should be somewhere else
    if location_name == 'hell':
        map = make_lavapools(map)
        
def make_lavapools(map):
    '''make heightmap of 3 height levels and put it on map as three levels depp of lava'''
    test = libtcod.heightmap_new(MAP_WIDTH, MAP_HEIGHT)
    test2 = libtcod.heightmap_new(MAP_WIDTH, MAP_HEIGHT)
    test3 = libtcod.heightmap_new(MAP_WIDTH, MAP_HEIGHT)
    
    noise = libtcod.noise_new(2)
    
    libtcod.heightmap_add_fbm(test2, noise, 1, 1, 0.0, 0.0, 10, 0.0, 1.0)
    libtcod.heightmap_add_fbm(test3, noise, 2, 2, 0.0, 0.0,  5, 0.0, 1.0)
    
    libtcod.heightmap_multiply_hm(test2, test3, test)
    libtcod.heightmap_normalize(test, mi=0, ma=1)
    
    #assign different levels 0-4 to hightmap floats
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if libtcod.heightmap_get_value(test, x, y) < 0.2:
                libtcod.heightmap_set_value(test, x, y, 0)
            elif libtcod.heightmap_get_value(test, x, y) >= 0.2 and libtcod.heightmap_get_value(test, x, y) < 0.4:
                libtcod.heightmap_set_value(test, x, y, 1)
            elif libtcod.heightmap_get_value(test, x, y) >= 0.4 and libtcod.heightmap_get_value(test, x, y) < 0.6:
                libtcod.heightmap_set_value(test, x, y, 2)
            elif libtcod.heightmap_get_value(test, x, y) >= 0.6 and libtcod.heightmap_get_value(test, x, y) < 0.8:
                libtcod.heightmap_set_value(test, x, y, 3)
            elif libtcod.heightmap_get_value(test, x, y) >= 0.8:
                libtcod.heightmap_set_value(test, x, y, 4)
    
    #create a differnet color darkness to lava levels
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            for z in range(int(int(libtcod.heightmap_get_value(test, x, y))-1)):
                map[x][y].change_type('lava')
                if z < 1:
                    map[x][y].color_light = 'flame'
                elif z < 2:
                    map[x][y].color_light = 'darker_flame'
                elif z < 3:
                    map[x][y].color_light = 'darkest_flame'
    
    #clean up and return map
    libtcod.heightmap_delete(test)
    return map

def place_preset_objects(location_name):
    '''checks maps.py and generates objects from the respective character. Such as generators and player startin position'''
    global objects
    
    #the list of objects with just the player
    objects = [player]
    
    generators = []
    
    #this bit contains the number of generators for the respective level and fills the rest with dummies
    if location_name == 'grassland':
        generators = ['g','g', 'i', 'i']
    elif location_name == 'castle':
        generators = ['g','g', 'i', 'i']
    elif location_name == 'dungeon':
        generators = ['g','g','g','i','i','i','i','i']
    elif location_name == 'cave':
        generators = ['g','g','g','i','i','i','i','i']
    elif location_name == 'hell':
        generators = ['g','g','g','g','g','i','i','i']
    elif location_name == 'endless':
        generators = ['g','g','g','g','g','g','i','i']
    
    random.shuffle(generators)
    
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            i = get_map_char(location_name, x, y)
            
            if i == 'r': #not used for testing only
                create_monster('rat', x, y)
            
            elif i == 'g':
                j = generators.pop()
                if j == 'g':
                    objects.append(create_object(gen_dict[location_name], x, y))
            
            elif i == 'p':
                player.x = x
                player.y = y

                
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def create_monster(type, x, y):
    '''function to easily create a monster of a type at coordinates x,y
    Translates the parameters of monsters.py and puts components ai, fighter,death_function, stats together
    '''
    # storage of data from monsters.py
    a = getattr(monsters, type)
 
    # creating fighter component
    fighter_component = Fighter(hp=a['hp'], damage=a['damage'], death_function=DEATH_DICT[a['death_function']])                
    
    #creating ai needs more info because of arguments
    if a['ai'] == 'BasicMonster':
        ai_component = BasicMonster(ticker, speed=a['speed'])
    elif a['ai'] == 'NoisyMonster':
        ai_component = NoisyMonster(ticker, speed=a['speed'])

    #create the monster    
    monster = Object(x, y, a['char'], a['name'], getattr(libtcod, a['color']), blocks=True, fighter=fighter_component, ai=ai_component)
    objects.append(monster)
    
    #[should be somewhere else] give a message and make some noise when noisy monster arrives
    if monster.ai.__class__.__name__ == 'NoisyMonster':
        message('A boss has appeared.', libtcod.sky)
        monster.ai.make_noise()
    
    if monster.name == 'cyclops':
        message('The cyclops has appeared. Beware!', libtcod.gold)
        
def create_object(type, x=0, y=0):
    '''function to easily create an object of a type at coordinates x,y
    Translates the parameters of monsters.py and puts components together
    '''
    a = getattr(monsters, type)
    
    ai_component = None
    
    if 'ai' in a:
        if a['ai'] == 'GeneratorAI':
            ai_component = GeneratorAI(ticker)
        if a['ai'] == 'GeneratorAIEnd':
            ai_component = GeneratorAIEnd(ticker)
    
    obj = Object(x, y, a['char'], a['name'], getattr(libtcod, a['color']), ai=ai_component )
   
    if 'blocks' in a:
        obj.blocks = a['blocks']
        
    #is returned and needs to be appended to objects
    return obj

#-----------------------------------------------------------------------------------------------------------------            
            
def get_names_under_mouse():
    '''returns a string with the names of all objects under the mouse plus their stats if fighters'''

    (x, y) = (mouse.cx, mouse.cy)
    names = []
    #create a list with the names of all objects at the mouse's coordinates
    for obj in reversed(objects):
        if obj.x == x and obj.y == y and libtcod.map_is_in_fov(fov_map, x, y):
            names.append(obj.name)
            if obj.fighter:
                names.append('hp: ' + str(obj.fighter.hp))
                names.append('attack: ' + str(obj.fighter.damage))
        
    #get terrain type unter mouse (terrain, walls, etc..)
    if libtcod.map_is_in_fov(fov_map, x, y):
        if not map[x][y].name == 'empty':
            names.append(map[x][y].name)
    
    #names = ', '.join(names)  #join the names, separated by commas
    return names#.capitalize()
    #returns list
    
def render_all():
    '''main render function for consoles con (map), panel (messages), column (keys, directoins) plus mouseover console
    draws all objects and tiles in FOV
    '''
    global fov_map, fov_recompute, mouse, dungeon_level

    if fov_recompute:
        #recompute FOV if needed (the player moved or something)
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, 100, FOV_LIGHT_WALLS, FOV_ALGO)
        libtcod.console_clear(con)
        
        #go through all tiles, and set their background color according to the FOV
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                
                if libtcod.map_is_in_fov(fov_map, x, y):
                    #it's visible
                    libtcod.console_put_char_ex(con, x, y, map[x][y].char_light , getattr(libtcod, map[x][y].color_light), libtcod.black)
                   
    #draw all objects in the list, except the player. we want it to
    #always appear over all other objects! so it's drawn later.
    for object in objects:
        if object != player:
            object.draw()
    player.draw()

    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)

    
#------------------------------------------------------------------------------------------ 
    #prepare to render the GUI panel
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    
    for k in range(len(song_of_world)):
        if not colorblind:
            libtcod.console_put_char_ex(panel, 0+k, 3, dict_char_color[song_of_world[k]][0] , getattr(libtcod, dict_char_color[song_of_world[k]][1]), libtcod.black)
        else:
            libtcod.console_put_char_ex(panel, 0+k, 3, song_of_world[k] , getattr(libtcod, dict_char_color[song_of_world[k]][1]), libtcod.black)
        
    index_occ = 0
    if bard_song:
        index_occ = [m.start() for m in re.finditer(bard_song, song_of_world)]

    if index_occ:
        for l in range(len(index_occ)):
            for j in range(len(bard_song)):
    #print index_occ
                libtcod.console_put_char_ex(panel, 0+index_occ[l]+j, 2, chr(25) , libtcod.white, libtcod.black)
    
    #print the game messages, one line at a time
    y = 5
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1
    
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, 'Melody of the World')
    
    #make_GUI_frame(panel, 0, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT)

    #blit the contents of "panel" to the root console
    libtcod.console_blit(panel, 0, 0, PANEL_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

#------------------------------------------------------------------------------------------ 
    #prepare to render the GUI column on the right  
    # libtcod.console_set_default_background(column, libtcod.black)
    libtcod.console_clear(column)
    
    if not colorblind:
        load_sprite_to_console('column', column)
    else:
        load_sprite_to_console('column_c', column)
    
    i = 0
    for k in bard_song:
        if not colorblind:
            libtcod.console_put_char_ex(column, 7+i, 24, dict_char_color[bard_song[i]][0] , getattr(libtcod, dict_char_color[bard_song[i]][1]), libtcod.black)
        else:
            libtcod.console_put_char_ex(column, 7+i, 24, bard_song[i] , getattr(libtcod, dict_char_color[bard_song[i]][1]), libtcod.black)    
        i += 1
    
    if dungeon_level >= 5:
        libtcod.console_print_ex(column, 1, COLUMN_HEIGHT-3, libtcod.BKGND_NONE, libtcod.LEFT, 'Score: ' + str(score))
    #libtcod.console_print_ex(column, 1, COLUMN_HEIGHT-2, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon Level: ' + str(dungeon_level))
     
    #libtcod.console_print_ex(column, 9+directioner[0], 38+directioner[1], libtcod.BKGND_NONE, libtcod.LEFT, chr(9)) 
    libtcod.console_put_char_ex(column, 9+directioner[0], 38+directioner[1], '@' , libtcod.white, libtcod.black)
    
    #blit the contents of "column" to the root console
    libtcod.console_blit(column, 0, 0, COLUMN_WIDTH, COLUMN_HEIGHT, 0, COLUMN_X, COLUMN_Y)
    
#------------------------------------------------------------------------------------------  
    #get info under mouse as console window attached to the mouse pointer
    if get_names_under_mouse():
        (x, y) = (mouse.cx, mouse.cy) #is ok here because blit is on root
        libtcod.console_set_default_background(info, libtcod.black)
        libtcod.console_clear(info)
        libtcod.console_set_default_foreground(info, libtcod.white)
        
        pile = get_names_under_mouse()
        height = len(pile)
        j = 0
        max_len = 1
        
        for thing in pile:
            if len(thing) > max_len:
                max_len = len(thing)
        for thing in pile:
            libtcod.console_print_rect_ex(info, 0, j, max_len, height, libtcod.BKGND_NONE, libtcod.LEFT, thing)        
            j += 1
        
        #make_GUI_frame(info, x, y, 30, height)
        libtcod.console_blit(info, 0, 0, max_len, height, 0, x+1, y+1)

#----------------------------------------------------------------------------------------------
  
def make_GUI_frame(console, x, y, dx, dy):
    '''creates a white frame line around the console of dimensions x,y,dx,dy'''
    #sides
    for i in range(dx-1):
        libtcod.console_print_ex(console, i, 0, libtcod.BKGND_NONE, libtcod.LEFT, chr(196))
    for i in range(dx-1):
        libtcod.console_print_ex(console, i, dy-1, libtcod.BKGND_NONE, libtcod.LEFT, chr(196))
    for i in range(dy-1):
        libtcod.console_print_ex(console, 0, i, libtcod.BKGND_NONE, libtcod.LEFT, chr(179))
    for i in range(dy-1):
        libtcod.console_print_ex(console, dx-1, i, libtcod.BKGND_NONE, libtcod.LEFT, chr(179))

    #corners
    libtcod.console_print_ex(console, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, chr(218))
    libtcod.console_print_ex(console, dx-1, 0, libtcod.BKGND_NONE, libtcod.LEFT, chr(191))
    libtcod.console_print_ex(console, 0, dy-1, libtcod.BKGND_NONE, libtcod.LEFT, chr(192))
    libtcod.console_print_ex(console, dx-1, dy-1, libtcod.BKGND_NONE, libtcod.LEFT, chr(217))

def message(new_msg, color = libtcod.white):
    '''creates a message in the apnel console of text ad color'''
    #split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

    for line in new_msg_lines:
    
        #if the buffer is full, remove the first line to make room for the new one
        if len(game_msgs) == MSG_HEIGHT:
            del game_msgs[0]

        #add the new line as a tuple, with the text and the color
        game_msgs.append( (line, color) )

def player_move_or_attack(dx, dy):
    '''called on keypress, decides whether player can move or attackes if monster on that tile'''
    global fov_recompute

    #the coordinates the player is moving to/attacking
    x = player.x + dx
    y = player.y + dy

    #try to find an attackable object there
    target = None
    npc = None
    for object in objects:
        if object.fighter and object.x == x and object.y == y and object.ai.__class__.__name__ != 'BasicNPC':
            target = object
            break
        elif object.fighter and object.x == x and object.y == y and object.ai.__class__.__name__ == 'BasicNPC':
            npc = object
            break
            
    #attack if target found, move otherwise
    if target is not None:
        player.fighter.attack(target)
        fov_recompute = True
    elif npc is not None:
        message('You listen to the words of ' + npc.name + '.', libtcod.orange)
        message(npc.spoiler_text)    
    else:
        player.move(dx, dy)
        fov_recompute = True

        
def menu(header, options, width):
    '''generic function to create a selection menu, is used for msg_box and name_menu'''
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')
    
    #calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(0, 0, 0, width, SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height + 2

    #create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)
    
    #cursos position
    c_pos = 0
    
    while True:
        libtcod.console_print_rect_ex(window, 1, 1, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
        #print the header, with auto-wrap
        libtcod.console_set_default_foreground(window, libtcod.white)
        
        #print all the options
        y = header_height
        letter_index = ord('a')
        run = 0
        for option_text in options:
            text = option_text
            
            if run == c_pos:
                libtcod.console_set_default_background(window, libtcod.dark_yellow)
                libtcod.console_print_ex(window, 1, y+1, libtcod.BKGND_SET, libtcod.LEFT, text)
                
            else:
                libtcod.console_set_default_background(window, libtcod.black)
                libtcod.console_print_ex(window, 1, y+1, libtcod.BKGND_SET, libtcod.LEFT, text)        
            y += 1
            letter_index += 1
            run += 1

        #blit the contents of "window" to the root console
        x = SCREEN_WIDTH/2 - width/2
        y = SCREEN_HEIGHT/2 - height/2
        
        make_GUI_frame(window, x, y, width, height)
        
        libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)

        #present the root console to the player and wait for a key-press
        libtcod.console_flush()
            
        key = libtcod.console_wait_for_keypress(True)
        key = libtcod.console_wait_for_keypress(True)
        
        if key.vk == libtcod.KEY_ESCAPE:
            return None
            break
        elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8 or chr(key.c) == 'k':
            c_pos -= 1
            if c_pos < 0:
                c_pos = len(options)-1
                
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2 or chr(key.c) == 'j':
            c_pos += 1
            if c_pos == len(options):
                c_pos = 0
        
        elif key.vk == libtcod.KEY_ENTER:               
            #convert the ASCII code to an index; if it corresponds to an option, return it
            index = c_pos
            #if index >= 0 and index < len(options): 
            return index
            break
        
def msgbox(text, width=30):
    '''use menu() as a sort of "message box"'''
    menu(text, [], width)  

    
def name_menu():
    '''allowes player to enter his name for highscore, called upon death in highscore mode'''
    global PLAYER_NAME
    
    img = libtcod.image_load('story2.png')
    
    for i in range(1):
            time.sleep(0.2)
    
    while not libtcod.console_is_window_closed():
        for i in range(1):
            time.sleep(0.2)
        #show the background image, at twice the regular console resolution
        libtcod.image_blit_2x(img, 0, 0, 0)
        #show the game's title, and some credits!
        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-6, libtcod.BKGND_NONE, libtcod.CENTER, 'Enter your name for highscore:')
        #show options and wait for the player's choice
        PLAYER_NAME = enter_text_menu('', 25, 16)
        
        #write score and player name to txt
        f = open('Highscores.txt', 'a')
        f.write('\n' + PLAYER_NAME + ' ' + str(score)) 
        f.close()
        break
        
    highscore_screen()
  
def enter_text_menu(header, width, max_length): #many thanks to Aukustus and forums for poviding this code. 
    '''used in name_menue as loop for entering characters'''
    # the 80 should be the width of the game window, in my game it's 80
    con = libtcod.console_new(80, 3)

    libtcod.console_set_default_foreground(con, libtcod.white)

    libtcod.console_print_rect(con, 5, 0, width, 3, header)
    libtcod.console_print_ex(con, 5, 1, libtcod.BKGND_NONE, libtcod.LEFT, 'Name:')
    timer = 0
    input = ''
    x = 11
    cx = 15
    cy = SCREEN_HEIGHT/2 - 3

    while True:
        key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)

        timer += 1
        if timer % (LIMIT_FPS // 4) == 0:
            if timer % (LIMIT_FPS // 2) == 0:
                timer = 0
                libtcod.console_print_ex(con, x, 1, libtcod.BKGND_NONE, libtcod.LEFT, ' ')
            else:
                libtcod.console_print_ex(con, x, 1, libtcod.BKGND_NONE, libtcod.LEFT, '_')
        if key.vk == libtcod.KEY_BACKSPACE:
            if len(input) > 0:
                libtcod.console_print_ex(con, x, 1, libtcod.BKGND_NONE, libtcod.LEFT, ' ')
                input = input[:-1]
                x -= 1

        elif key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER:
            break

        elif key.c > 0 and len(input) < max_length:
            letter = chr(key.c)
            if re.match("^[A-Za-z0-9-']*$", str(letter)) or str(letter) == ' ':
                libtcod.console_print_ex(con, x, 1, libtcod.BKGND_NONE, libtcod.LEFT, letter)
                input += letter
                x += 1

        libtcod.console_blit(con, 5, 0, width, 3, 0, cx, cy, 1.0, 1.0)
        libtcod.console_flush()
        
    return input  
  
   
def handle_keys():
    '''constantly called in PlayerAI to check player keyboard input and act or return "didnt-take-turn"'''
    global key, colorblind, mouse, game_state, bard_song, directioner

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        choice = menu('Do you want to quit?', ['Yes', 'No'], 24)
        if choice == 0:                
            game_state = 'exit'
            return 'exit' #exit game
        else:
            return 'didnt-take-turn'
          
    if game_state == 'playing':
        #movement keys
        if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8 or chr(key.c) == 'k' or chr(key.c) == 'e':
            player_move_or_attack(0, -1)
            play_note('b')
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2 or chr(key.c) == 'j' or chr(key.c) == 'c':
            player_move_or_attack(0, 1)
            play_note('f')
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4 or chr(key.c) == 'h' or chr(key.c) == 's':
            player_move_or_attack(-1, 0)
            play_note('h')
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6 or chr(key.c) == 'l' or chr(key.c) == 'f':
            player_move_or_attack(1, 0)
            play_note('d')
        elif key.vk == libtcod.KEY_HOME or key.vk == libtcod.KEY_KP7 or chr(key.c) == 'z' or chr(key.c) == 'w':
            player_move_or_attack(-1, -1)
            play_note('a')
        elif key.vk == libtcod.KEY_PAGEUP or key.vk == libtcod.KEY_KP9 or chr(key.c) == 'u' or chr(key.c) == 'r':
            player_move_or_attack(1, -1)
            play_note('c')
        elif key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_KP1 or chr(key.c) == 'b' or chr(key.c) == 'x':
            player_move_or_attack(-1, 1)
            play_note('g')
        elif key.vk == libtcod.KEY_PAGEDOWN or key.vk == libtcod.KEY_KP3 or chr(key.c) == 'n' or chr(key.c) == 'v':
            player_move_or_attack(1, 1)
            play_note('e')
        elif key.vk == libtcod.KEY_KP5 or chr(key.c) == '.' or chr(key.c) == 'd':
            #play_note('i')
            bard_song = ''
            directioner = [0,0]
            return 0  #do nothing ie wait for the monster to come to you
        else:
            #test for other keys
            key_char = chr(key.c)
            if key_char == 't':
                colorblind = not colorblind
                  
            if key_char == 'M':
                blast_damage('up')
                blast_damage('down')
                blast_damage('left')
                blast_damage('right')
                return 0
                  
            if key_char == '?':
                show_help()
                
            return 'didnt-take-turn'

def load_sprite_to_console(key, console):
    '''used for blast effect, puts .xp file data from shelve sprites['key'] on a console'''
    file = shelve.open('sprites')
    xp = file[key] 
    file.close()
   
    xp_file_layer = xp['layer_data'][0]
    
    if not xp_file_layer['width'] or not xp_file_layer['height']:
        raise AttributeError('Attempted to call load_layer_to_console on data that didn\'t have a width or height key, check your data')

    for x in range(xp_file_layer['width']):
        for y in range(xp_file_layer['height']):
			cell_data = xp_file_layer['cells'][x][y]
			fore_color = libtcod.Color(cell_data['fore_r'], cell_data['fore_g'], cell_data['fore_b'])
			back_color = libtcod.Color(cell_data['back_r'], cell_data['back_g'], cell_data['back_b'])
			libtcod.console_put_char_ex(console, x, y, cell_data['keycode'], fore_color, back_color)

    libtcod.console_set_key_color(console, libtcod.Color(255, 0, 255 ))
    
def put_on_score(x):
    '''modify score'''
    global score
    score += x

    
def show_help():
    '''overlay of help screen to the GUI'''
    load_sprite_to_console('help',help)
    libtcod.console_blit(help, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()
    libtcod.console_wait_for_keypress(True)
    libtcod.console_wait_for_keypress(True)
       
def play_note(color_string):
    '''called on directional movement and checks direction and adds note to song.'''
    global bard_song, directioner
    
    bard_song += color_string
    direction_sum(color_string)
         
    render_all()
    libtcod.console_flush() 
    
    winsound.PlaySound("SystemExit", winsound.SND_ASYNC)
    
    if bard_song not in song_of_world:
        bard_song = ''
        directioner = [0,0]
    
    if len(bard_song) == 5:
        blast_effect(check_direct())
        blast_damage(check_direct())
        bard_song = ''
        directioner = [0,0]
 
def check_direct():
    '''determines direction of effect and damage by directioner, returns direction string'''
    up = [  'up', [0,-1], 
            [-1,-2], [0,-2] ,[1,-2],
            [-1,-3], [0,-3] ,[1,-3],
            [-2,-4], [-1,-4] ,[0,-4], [1,-4], [2,-4], 
            [-2,-5], [-1,-5] ,[0,-5], [1,-5], [2,-5]
            ]
            
    down = [  'down', [0, 1], 
            [-1,2], [0,2] ,[1,2],
            [-1,3], [0,3] ,[1,3],
            [-2,4], [-1,4] ,[0,4], [1,4], [2,4], 
            [-2,5], [-1,5] ,[0,5], [1,5], [2,5]
            ]
    
    right = [  'right', [1,0], 
            [2,-1], [2,0] ,[2,1],
            [3,-1], [3,0] ,[3,1],
            [4,-2], [4,-1] ,[4,0], [4,1], [4,2], 
            [5,-2], [5,-1] ,[5,0], [5,1], [5,2]
            ]
    
    left = [  'left', [-1,0], 
            [-2,-1], [-2,0] ,[-2,1],
            [-3,-1], [-3,0] ,[-3,1],
            [-4,-2], [-4,-1] ,[-4,0], [-4,1], [-4,2], 
            [-5,-2], [-5,-1] ,[-5,0], [-5,1], [-5,2]
            ]
    
    up_left = [  'up_left', [-1,-1], 
            [-2,-2], 
            [-3,-2] ,[-2,-3],
            [-3,-3], 
            [-4,-4] ,[-4,-3], [-3,-4],
            [-5,-5], [-5,-4] ,[-5,-3], [-4,-5], [-3,-5]
            ]
    
    up_right = [  'up_right', [1,-1], 
            [2,-2], 
            [3,-2] ,[2,-3],
            [3,-3], 
            [4,-4] ,[4,-3], [3,-4],
            [5,-5], [5,-4] ,[5,-3], [4,-5], [3,-5]
            ]
            
    down_left = [  'down_left', [-1,1], 
            [-2,2], 
            [-3,2] ,[-2,3],
            [-3,3], 
            [-4,4] ,[-4,3], [-3,4],
            [-5,5], [-5,4] ,[-5,3], [-4,5], [-3,5]
            ]
            
    down_right = [  'down_right', [1,1], 
            [2,2], 
            [3,2] ,[2,3],
            [3,3], 
            [4,4] ,[4,3], [3,4],
            [5,5], [5,4] ,[5,3], [4,5], [3,5]
            ]
    
    directions = []
    directions.append(up)
    directions.append(down)
    directions.append(right)
    directions.append(left)
    directions.append(up_right)
    directions.append(up_left)
    directions.append(down_right)
    directions.append(down_left)
    
    for i in directions:
        if directioner in i:
            return i[0]
            
    return None 

def blast_damage(dir_string):
    '''uses dir string to do damage in rectangle in proper direction'''
    diagonal = False  
    
    if dir_string == None:
        return
    
    elif dir_string == 'up':
        (x1,x2) = player.x-2, player.x+2
        (y1,y2) = player.y-26, player.y-1

    elif dir_string == 'down':
        (x1,x2) = player.x-2, player.x+2
        (y1,y2) = player.y+1, player.y+26

    elif dir_string == 'left':
        (x1,x2) = player.x-26, player.x-1
        (y1,y2) = player.y-2, player.y+2
        
    elif dir_string == 'right':
        (x1,x2) = player.x+1, player.x+26
        (y1,y2) = player.y-2, player.y+2

    elif dir_string == 'up_left':
        diagonal = True
        direct = [-1,-1]
        
        start = [
        [player.x-2, player.y],
        [player.x-1, player.y],
        [player.x-1, player.y-1],
        [player.x, player.y-1],
        [player.x, player.y-2]
        ]
        
        collection = start
        
    elif dir_string == 'up_right':
        diagonal = True
        direct = [1,-1]
        
        start = [
        [player.x+2, player.y],
        [player.x+1, player.y],
        [player.x+1, player.y-1],
        [player.x, player.y-1],
        [player.x, player.y-2]
        ]    
        collection = start
    
    elif dir_string == 'down_left':
        diagonal = True
        direct = [-1,1]
        
        start = [
        [player.x-2, player.y],
        [player.x-1, player.y],
        [player.x-1, player.y+1],
        [player.x, player.y+1],
        [player.x, player.y+2]
        ]
        
        collection = start
    
    elif dir_string == 'down_right':
        diagonal = True
        direct = [1,1]
        
        start = [
        [player.x+2, player.y],
        [player.x+1, player.y],
        [player.x+1, player.y+1],
        [player.x, player.y+1],
        [player.x, player.y+2]
        ] 
        collection = start[:]
       
    if not diagonal:
        for obj in objects:
            if obj.x <= x2 and obj.x >= x1 and obj.y <= y2 and obj.y >= y1 and obj.fighter:
                obj.fighter.take_damage(5)
    else:               
        for point in start[:]:
            new = point
            for i in range(20):
                new = [new[0]+direct[0], new[1]+direct[1]]
                collection.append(new)
                
        for obj in objects:
            if obj.fighter:
                coord = [obj.x, obj.y]
                if coord in collection:
                    obj.fighter.take_damage(5)
         
def blast_effect(dir_string):
    '''uses dir string to display and animate blast effect in proper direction'''
    #code is repetitive but condensing with dicrtionary is way too slow
    if dir_string == None:
        return
        
    elif dir_string == 'up':

        frame = 1
        sprite = 'blastns'
        while frame < 8:
                        
            new = libtcod.console_new(5,25)
            load_sprite_to_console(sprite + str(frame) ,new)
            libtcod.console_blit(new, 0, 0, 5, 25, 0, player.x-2, player.y-25, 1, 1)
            
            libtcod.console_flush()      
            render_all()
            for i in range(1):
                time.sleep(0.1)
            frame += 1
        
        for obj in objects:
            obj.clear()
        
    elif dir_string == 'down':

        frame = 1
        sprite = 'blastns'
        while frame < 8:
                        
            new = libtcod.console_new(5,25)
            load_sprite_to_console(sprite + str(frame) ,new)
            libtcod.console_blit(new, 0, 0, 5, 25, 0, player.x-2, player.y+1, 1, 1)
            
            libtcod.console_flush()      
            render_all()
            for i in range(1):
                time.sleep(0.1)
            frame += 1
        
        for obj in objects:
            obj.clear()
            
    elif dir_string == 'left':    

        frame = 1
        sprite = 'blastwe'
        while frame < 8:
                        
            new = libtcod.console_new(25,5)
            load_sprite_to_console(sprite + str(frame) ,new)
            libtcod.console_blit(new, 0, 0, 25, 5, 0, player.x-25, player.y-2, 1, 1)
            
            libtcod.console_flush()      
            render_all()
            for i in range(1):
                time.sleep(0.1)
            frame += 1
        
        for obj in objects:
            obj.clear()
        
    elif dir_string == 'right':
        
        frame = 1
        sprite = 'blastwe'
        while frame < 8:
                        
            new = libtcod.console_new(25,5)
            load_sprite_to_console(sprite + str(frame) ,new)
            libtcod.console_blit(new, 0, 0, 25, 5, 0, player.x+1, player.y-2, 1, 1)
            
            libtcod.console_flush()      
            render_all()
            for i in range(1):
                time.sleep(0.1)
            frame += 1
        
        for obj in objects:
            obj.clear()
        
    elif dir_string == 'up_left':    

        frame = 1
        sprite = 'blastse'
        while frame < 8:
                        
            new = libtcod.console_new(20,20)
            load_sprite_to_console(sprite + str(frame) ,new)
            libtcod.console_blit(new, 0, 0, 20, 20, 0, player.x-20, player.y-20, 1, 1)
            
            libtcod.console_flush()      
            render_all()
            for i in range(1):
                time.sleep(0.1)
            frame += 1
        
        for obj in objects:
            obj.clear()
             
    elif dir_string == 'up_right':
   
        frame = 1
        sprite = 'blastne'
        while frame < 8:
                        
            new = libtcod.console_new(20,20)
            load_sprite_to_console(sprite + str(frame) ,new)
            libtcod.console_blit(new, 0, 0, 20, 20, 0, player.x+1, player.y-20, 1, 1)
            
            libtcod.console_flush()      
            render_all()
            for i in range(1):
                time.sleep(0.1)
            frame += 1
        
        for obj in objects:
            obj.clear()
        
    elif dir_string == 'down_left':
        
        frame = 1
        sprite = 'blastne'
        while frame < 8:
                        
            new = libtcod.console_new(20,20)
            load_sprite_to_console(sprite + str(frame) ,new)
            libtcod.console_blit(new, 0, 0, 20, 20, 0, player.x-20, player.y+1, 1, 1)
            
            libtcod.console_flush()      
            render_all()
            for i in range(1):
                time.sleep(0.1)
            frame += 1
        
        for obj in objects:
            obj.clear()
        
    elif dir_string == 'down_right':

        frame = 1
        sprite = 'blastse'
        while frame < 8:
                        
            new = libtcod.console_new(20,20)
            load_sprite_to_console(sprite + str(frame) ,new)
            libtcod.console_blit(new, 0, 0, 20, 20, 0, player.x, player.y, 1, 1)
            
            libtcod.console_flush()      
            render_all()
            for i in range(1):
                time.sleep(0.1)
            frame += 1
        
        for obj in objects:
            obj.clear()    
            
def direction_sum(color_string):
    '''evaluates color_string and translates it to direction for directioner'''
    global directioner
    
    directioner[0] += dict_direct[color_string][0]
    directioner[1] += dict_direct[color_string][1]
  
  
def player_death(player):
    '''called on player death hp < 0. sets game_state to dead, breaking all loops'''
    #the game ended!
    global game_state, PLAYER_NAME
    #in case it gets called on many events happening the same loop
    if game_state == 'dead':
        return

    game_state = 'dead'

    #for added effect, transform the player into a corpse!
    player.char = '%'        
    player.color = libtcod.dark_red
    #create corpse that can be found and used in bone files 
    player.blocks = False
    
    player.fighter = None
    player.name = 'remains of ' + player.name    
    if dungeon_level < 5:
        msgbox('You died!')
    else:
        msgbox('You died! Your score: ' + str(score))
        name_menu()
        
def monster_death(monster):
    '''calles upon death of normal monsters tranforming them to corpses'''
    #transform it into a nasty corpse! it doesn't block, can't be
    #attacked and doesn't move
       
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    
    #gain points on monster defeated
    put_on_score(monster.fighter.base_hp)
    
    monster.fighter = None
    monster.ai = Corpse(ticker, monster)
    monster.name = 'remains of ' + monster.name
    
    try:
        monster.send_to_back()    
    except:
        pass

def boss_death(monster):
    '''calles on death on bosses to advance to the next stage'''
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    
    render_all()
    libtcod.console_flush()
    #boss defeated advance to next level
    msgbox('You defeated the ' + monster.name + ' and advance to the next level.')
    #transform it into a nasty corpse! it doesn't block, can't be
    #attacked and doesn't move
       
    monster.fighter = None
    monster.name = 'remains of ' + monster.name
    monster.send_to_back()   
    new_game(dungeon_level+1)
    
    
def win(monster):    
    '''used as death function of the final boss to win on his defeat. creates win screen and breaks the player loop'''
    global game_state
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    
    render_all()
    libtcod.console_flush()
    #boss defeated advance to next level
    msgbox('You defeated the ' + monster.name + ' and win the game!')
    #transform it into a nasty corpse! it doesn't block, can't be
    #attacked and doesn't move
    #message('The ' + monster.name + ' is dead!', libtcod.orange)
       
    monster.fighter = None
    monster.name = 'remains of ' + monster.name
    monster.send_to_back()   
    
    libtcod.console_set_default_background(0, libtcod.black)
    libtcod.console_clear(0)
    
    img = libtcod.image_load('win.png')

    #show the background image, at twice the regular console resolution
    libtcod.image_blit_2x(img, 0, 0, 0)
    
    for i in range(1):
        time.sleep(0.5)
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_print_rect(0, 5, 5, 20, 50, text.win)
    
    #present the root console to the player and wait for a key-press
    libtcod.console_flush()    
    
    key = libtcod.console_wait_for_keypress(True)
    game_state = 'exit'

    
DEATH_DICT = {
    'monster_death': monster_death,
    'win': win,
    'boss_death': boss_death
    }

class SongProgression:
    '''Timer item to constantly move the song of world once per turn'''
    def __init__(self, ticker, speed=6):
        self.ticker = ticker
        self.speed = speed
        self.ticker.schedule_turn(self.speed, self)
        
    def take_turn(self):
        continue_song_of_world()
        self.ticker.schedule_turn(self.speed, self)
       
def continue_song_of_world(noise=None):
    '''appends 'noise' from monsters or random available notes to song of world, therefore not in song progression'''
    global song_of_world
    if not noise:
        song_of_world = song_of_world[1:]
        song_of_world = song_of_world + random.choice(available_notes)
    elif noise:
        song_of_world = song_of_world[len(noise):]
        song_of_world = song_of_world + noise
    
def create_player():
    '''create the player and set him as global item'''
    global player
    #create object representing the player
    fighter_component = Fighter(hp=PLAYER_STATS['hp'], 
                                damage=PLAYER_STATS['damage'], 
                                death_function=player_death)
    ai_component = PlayerAI(ticker, 6)
    player = Object(0, 0, '@', PLAYER_NAME, libtcod.white, blocks=True, fighter=fighter_component, ai=ai_component)
    
def new_game(level):
    '''create a new game, set everything to start, call make_map. called for every stage and used for endless mode with level > 4'''
    global game_msgs, game_state, dungeon_level, bard_song
    global PLAYER_STATS, objects, ticker, score, song_of_world, directioner
    
    PLAYER_STATS = {'hp': 10,
                'damage': 1
                }
    
    objects = []    
    score = 0
    directioner = [0,0]
    bard_song = ''
    song_of_world = ''
    
    for i in range(50):
        song_of_world = song_of_world + random.choice(available_notes)  
    
    ticker = timer.Ticker()
    song_prog = SongProgression(ticker)
    create_player()
    dungeon_level = level
    
    if dungeon_level > 4:
        level_prog = EndlessTicker(ticker)
    
    make_map('var')
    initialize_fov()
    game_state = 'playing'

    #create the list of game messages and their colors, starts empty
    game_msgs = []

    #a warm welcoming message!
    if dungeon_level == 0:
        message(text.welcome, libtcod.white)
    elif dungeon_level > 0 and dungeon_level < 5:
        message('You descend to the next level and feel healed.', libtcod.white)
    elif dungeon_level >= 5:
        message('Welcome to highscore mode. Score as much as you can.', libtcod.white)
        

    
def initialize_fov():
    '''refreshes the FOV of player and allows new rendering by render_all'''
    global fov_recompute, fov_map
    fov_recompute = True

    #create the FOV map, according to the generated map
    fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
            
    libtcod.console_clear(con)  #unexplored areas start black (which is the default background color)

def play_game():
    '''called on game start from main_menu, containes the loop controlling the scheduler, checks game states'''
    global key, mouse
    
    player_action = None
    
    mouse = libtcod.Mouse()
    key = libtcod.Key()
    
    #main loop
    while not libtcod.console_is_window_closed():
        # libtcod.console_flush()
        if game_state == 'dead' or game_state == 'exit':
            break
       
        ticker.ticks += 1
        #print ticker.ticks
        if not game_state == 'dead':
            ticker.next_turn()    
       
         
def intro_screen():
    '''just putting the label up first'''
    img = libtcod.image_load('label.png')

    #show the background image, at twice the regular console resolution
    libtcod.image_blit_2x(img, 0, 0, 0)

    #present the root console to the player and wait for a key-press
    libtcod.console_flush()    
    key = libtcod.console_wait_for_keypress(True)

    # go on to main menu
    main_menu()
        
def story_screen():
    '''one screen to give some con text'''
    libtcod.console_set_default_background(0, libtcod.black)
    libtcod.console_clear(0)
    
    img = libtcod.image_load('story.png')

    #show the background image, at twice the regular console resolution
    libtcod.image_blit_2x(img, 0, 0, 0)
    
    for i in range(1):
        time.sleep(0.5)
    libtcod.console_set_default_foreground(0, libtcod.white)

    libtcod.console_print_rect(0, 5, 5, 20, 50, text.story)
    
    #present the root console to the player and wait for a key-press
    libtcod.console_flush()    
    key = libtcod.console_wait_for_keypress(True)

    # go on to play the game
    new_game(0)
    play_game()
        
        
def main_menu():
    '''the title screen and main menu'''
    img = libtcod.image_load('title5.png')

    while not libtcod.console_is_window_closed():
        for i in range(1):
            time.sleep(0.6)
        #show the background image, at twice the regular console resolution
        libtcod.image_blit_2x(img, 0, 0, 0)

        #show the game's title, and some credits!
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-4, libtcod.BKGND_NONE, libtcod.CENTER,
                                 '')
        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, SCREEN_WIDTH/2, SCREEN_HEIGHT-2, libtcod.BKGND_NONE, libtcod.CENTER, 'made for 7drl 2016 | by Jan | v 1.1')
        
        options = ['New Game', 'Play Highscore Mode', 'View Highscores', 'Quit']
        
        #show options and wait for the player's choice
        choice = menu('', options, 24)
        
        if choice == 0:  #new game
            story_screen()
        elif choice == 1:  #toggle color/letters
            new_game(5)
            play_game()
        elif choice == 2:
            highscore_screen()
        elif choice == 3:  #quit
            break
  
def highscore_screen():
    '''highscore screen from main_menu or after death in highscore mode'''
    libtcod.console_set_default_background(0, libtcod.black)
    libtcod.console_clear(0)
    
    content = ''
    
    f = open("Highscores.txt", "r");
    for line in f.readlines():
        content += line
    f.close()

    img = libtcod.image_load('story.png')

    #show the background image, at twice the regular console resolution
    libtcod.image_blit_2x(img, 0, 0, 0)
    
    for i in range(1):
        time.sleep(0.5)
    libtcod.console_set_default_foreground(0, libtcod.white)

    libtcod.console_print_rect(0, 5, 5, 20, 50, content)
    
    #present the root console to the player and wait for a key-press
    libtcod.console_flush()    
    key = libtcod.console_wait_for_keypress(True)

  
libtcod.console_set_custom_font('terminal16x16_gs_ro.png', libtcod.FONT_LAYOUT_ASCII_INROW)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'The Prancing Bard 7drl', False)#, libtcod.RENDERER_OPENGL)
libtcod.sys_set_fps(LIMIT_FPS)
help = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.console_new(PANEL_WIDTH, PANEL_HEIGHT)
column = libtcod.console_new(COLUMN_WIDTH, COLUMN_HEIGHT)
info = libtcod.console_new(30, 20)

intro_screen()