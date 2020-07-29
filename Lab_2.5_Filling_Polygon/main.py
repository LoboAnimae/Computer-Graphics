"""Allows the user to render a specific set of figures.

"""
from lib.renderer import Render
import sys

RED = '\033[0;37;41m'
NORMAL = '\033[0;37;48m'
GREEN = '\033[0;30;42m'


try:
    # Try to grab the arguments necessary for the program
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    color = [0, 0, 0]
    color[2] = 255 if int(sys.argv[3]) > 255 else int(sys.argv[3])
    color[2] = 0 if int(sys.argv[3]) < 0 else int(sys.argv[3])
    color[0] = 255 if int(sys.argv[4]) > 255 else int(sys.argv[4])
    color[0] = 0 if int(sys.argv[4]) < 0 else int(sys.argv[4])
    color[1] = 255 if int(sys.argv[5]) > 255 else int(sys.argv[5])
    color[1] = 0 if int(sys.argv[5]) < 0 else int(sys.argv[5])
    print(GREEN)
    print('Your values have been set as: \nWidth: %d\nHeight: %d\nColor: RGB(%d, %d, %d)'
          % (width, height, color[0], color[1], color[2]))
except Exception as e:
    # If the arguments couldn't be found, use the default ones
    width = 800
    height = 600
    color = [255, 255, 255]

    print(RED)
    print(e)
    print('The values couldn\'t be added... Using defaults.')
finally:
    print(NORMAL)
    print('\n\n\nGenerating your image...')


try:

    # Create the object
    obj = Render(width, height, color)

    # Paint the shapes
    obj.fillpolygon([(165, 380), (185, 360), (180, 330), (207, 345), (233, 330),
                     (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)])
    obj.fillpolygon([(377, 249), (411, 197), (436, 249)])
    obj.fillpolygon([(321, 335), (288, 286), (339, 251), (374, 302)])
    obj.fillpolygon([(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179), (672, 192), (659, 214),
                     (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180), (682, 175), (708, 120), (735, 148), (739, 170)])

    # If everything went well, write the file
    obj.write()
    print(GREEN)
    print('A file has been generated!')


except Exception as e:
    print(RED)
    print(e)
finally:
    print(NORMAL)
    print('\n             , ,' + '\n            /| |\\' + '\n           / | | \\' + '\n           | | | |     Neeaah, That\'s all folks !' + '\n           \ | | /' + '\n            \|w|/          /' + '\n            /_ _\         /      , ' + '\n /\       _:()_():_       /]' + '\n ||_     : ._=Y=_  :     / /' +
          '\n[)(_\,   \',__\W/ _,\'    /  \\' + '\n[) \_/\    _/\'=\'\      /-/\)' + '\n[_| \ \  ///  \ \'._  / /' + '\n :;  \ \///   / |  \'` /' + '\n;::   \ `|:   : |\',_.\'' + '\n"""    \_|:   : |   ' + '\n         |:   : |\'".' + '\n         /`._.\'  \/' + '\n        /  /|   /' + '\n       |  \ /  /' + '\n       \'. \'. /' + '\n         \'. \'' + '\n          / \ \\' + '\n         / / \\\'=, ' + '\n  .----\' /   \ (\__ ' + '\n (((____/     \ \  )' + '\n               \'.\_))')
    print('Ending program...')
