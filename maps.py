'''module contains lists of MAP_WIDTH and MAP_HEIGHT chars, which can be converted to maps by
make_preset_map via get_map_char and the function here char_to_type
'''

def char_to_type(char):
    '''translates single characters from maps (below) to terrain type (see class Tile) of tile'''
    if char == '#':
        return 'rock wall'
    elif char == '+':
        return 'door'  
    
    elif char == ',':
        return 'grass'
    
    elif char == 'l':
        
        return 'lava'
    else:
        return 'empty'

grassland = [',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,g,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,g,,,,,,,,,,,,,,,,,,,,,,p,,,,,,,,,,,,,,,,,,,,,g,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,g,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',]


grassland2 = ['r,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,p,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',]

castle = [ ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,#####,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,#####,,,',
           ',,#   #,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,#   #,,,',
           ',,# g ##################################### g #,,,',
           ',,#   #                                   #   #,,,',
           ',,#                                           #,,,',
           ',,#####                                   #####,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',           
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       +,,,,,',
           ',,,,#                                       +,,,,,',
           ',,,,#                    p                  +,,,,,',
           ',,,,#                                       +,,,,,',
           ',,,,#                                       +,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',,,,#                                       #,,,,,',
           ',####                                       #,,,,,',
           ',######                                   #####,,,',
           ',##                                           #,,,',
           ',##   #                                   #   #,,,',
           ',## g ##################################### g #,,,',
           ',##   ##,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,#   #,,,',
           ',#######,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,#####,,,',
           ',#######,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
           ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,']
           
dungeon = ['                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '    g                     g                g      ',
           '                                                  ',
           '        #####         #####         #####         ',
           '        #####         #####         #####         ',
           '        #####         #####         #####         ',
           '        #####         #####         #####         ',
           '                                                  ',
           '                                                  ',           
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '     #####                          #####         ',
           '     #####                          #####    g    ',
           '  g  #####               p          #####         ',
           '     #####                          #####         ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '        #####         #####           #####       ',
           '        #####         #####           #####       ',
           '        #####         #####           #####       ',
           '        #####         #####           #####       ',
           '                                                  ',
           '    g                   g                    g    ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ']

hell = ['                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '    g                     g                g      ',
           '                                                  ',
           '        #####         #####         #####         ',
           '        #####         #####         #####         ',
           '        #####         #####         #####         ',
           '        #####         #####         #####         ',
           '                                                  ',
           '                                                  ',           
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '     #####                          #####         ',
           '     #####                          #####    g    ',
           '  g  #####               p          #####         ',
           '     #####                          #####         ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '        #####         #####           #####       ',
           '        #####         #####           #####       ',
           '        #####         #####           #####       ',
           '        #####         #####           #####       ',
           '                                                  ',
           '    g                   g                    g    ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ']
           
endless = [' g                      g                       g ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',           
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           ' g                       p                      g ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           '                                                  ',
           ' g                      g                       g ',
           '                                                  ']
  