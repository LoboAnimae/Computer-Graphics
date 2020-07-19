

from struct import pack

# region CONSTANTS
BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
# endregion

def char(c):
    """Converts 

    Args:
        c ([type]): [description]

    Returns:
        [type]: [description]
    """    
    return pack('=c', c.encode('ascii'))

def word(c):
    return pack('=h', c)

def dword(c):
    return pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])

