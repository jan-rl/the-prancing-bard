'''contains dictionaries with generators and monster stats and properties

is read by the create_monster and create_object functions. Examples:

rat_hole = {
    'char': '?',
    'name': 'rat hole',
    'color': 'white',
    'ai': 'GeneratorAI'
    }  

pixie = {'hp': 1, 'damage': 1,
    'death_function': 'monster_death', 
    'speed': 6,
    'ai': 'BasicMonster',
    'char': 'p',
    'name': 'pixie',
    'color': 'fuchsia'
    } 
'''

rat_hole = {
    'char': '?',
    'name': 'rat hole',
    'color': 'white',
    'ai': 'GeneratorAI'
    }  

dungeon_entrance = {
    'char': '?',
    'name': 'dungeon entrance',
    'color': 'white',
    'ai': 'GeneratorAI'
    } 

stairs_down = {
    'char': '?',
    'name': 'stairs down',
    'color': 'white',
    'ai': 'GeneratorAI'
    } 

cleft = {
    'char': '?',
    'name': 'cleft',
    'color': 'white',
    'ai': 'GeneratorAI'
    } 
    
monster_house = {
    'char': '?',
    'name': 'monster house',
    'color': 'white',
    'ai': 'GeneratorAI'
    } 
    
nest = {
    'char': '?',
    'name': 'nest',
    'color': 'white',
    'ai': 'GeneratorAIEnd'
    } 
#------------------------------------------------------------------------

rat = {'hp': 1, 'damage': 0,
    'death_function': 'monster_death', 
    'speed': 12,
    'ai': 'BasicMonster',
    'char': 'r',
    'name': 'rat',
    'color': 'lighter_sepia'
    }    
    
    
pixie = {'hp': 1, 'damage': 1,
    'death_function': 'monster_death', 
    'speed': 6,
    'ai': 'BasicMonster',
    'char': 'p',
    'name': 'pixie',
    'color': 'fuchsia'
    }    
    

    
leprechaun = {'hp': 1, 'damage': 1,
    'death_function': 'monster_death', 
    'speed': 3,
    'ai': 'BasicMonster',
    'char': 'l',
    'name': 'leprechaun',
    'color': 'green'
    }    
    
   
goblin = {'hp': 3, 'damage': 3,
    'death_function': 'monster_death', 
    'speed': 12,
    'ai': 'BasicMonster',
    'char': 'g',
    'name': 'goblin',
    'color': 'lighter_green'
    }    


bandit = {'hp': 5, 'damage': 5,
    'death_function': 'monster_death', 
    'speed': 12,
    'ai': 'BasicMonster',
    'char': 'H',
    'name': 'bandit',
    'color': 'yellow'
    }    
    
#-----------------------------------------------------------------

pied_rat = {'hp': 5, 'damage': 10,
    'death_function': 'monster_death', 
    'speed': 12,
    'ai': 'NoisyMonster',
    'char': 'R',
    'name': 'pied rat',
    'color': 'lighter_sepia'
    }    
      
pied_rat_boss = {'hp': 5, 'damage': 10,
    'death_function': 'boss_death', 
    'speed': 10,
    'ai': 'NoisyMonster',
    'char': 'R',
    'name': 'pied rat',
    'color': 'lighter_sepia'
    }   
    
commander = {'hp': 6, 'damage': 10,
    'death_function': 'monster_death', 
    'speed': 10,
    'ai': 'NoisyMonster',
    'char': 'C',
    'name': 'commander',
    'color': 'blue'
    }    

commander_boss = {'hp': 6, 'damage': 10,
    'death_function': 'boss_death', 
    'speed': 10,
    'ai': 'NoisyMonster',
    'char': 'C',
    'name': 'commander',
    'color': 'blue'
    }    

knocker = {'hp': 11, 'damage': 9,
    'death_function': 'monster_death', 
    'speed': 10,
    'ai': 'NoisyMonster',
    'char': 'O',
    'name': 'knocker',
    'color': 'dark_orange'
    }    
    
knocker_boss = {'hp': 11, 'damage': 9,
    'death_function': 'boss_death', 
    'speed': 10,
    'ai': 'NoisyMonster',
    'char': 'O',
    'name': 'knocker',
    'color': 'dark_orange'
    }    
                    
banshee = {'hp': 10, 'damage': 5,
    'death_function': 'monster_death', 
    'speed': 9,
    'ai': 'NoisyMonster',
    'char': '&',
    'name': 'banshee',
    'color': 'purple'
    }    
    
banshee_boss = {'hp': 10, 'damage': 5,
    'death_function': 'boss_death', 
    'speed': 9,
    'ai': 'NoisyMonster',
    'char': '&',
    'name': 'banshee',
    'color': 'purple'
    }    
    
cyclops_boss = {'hp': 15, 'damage': 11,
    'death_function': 'win', 
    'speed': 18,
    'ai': 'BasicMonster',
    'char': '@',
    'name': 'cyclops',
    'color': 'red'
    }    