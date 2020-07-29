from struct import pack


def char(param: str):
    """Converts a string into a single char. The string must be of length 1.

    Args:
        param (str): Parameter to be converted. 

    Returns:
        Bytes: Converted parameter
    """
    return pack('=c', param.encode('ascii'))


def word(param: int):
    """Converts an int into a word to be used anywhere. 

    Args:
        param (int): Parameter to be converted. 

    Returns:
        Bytes: Converted parameter
    """
    return pack('=h', param)


def dword(param: int):
    """Convers an int parameter into a dword to be used anywhere. 

    Args:
        param (int): Parameter to be converted. 

    Returns:
        Bytes: Converted parameter
    """
    return pack('=l', param)


def color(r: int, g: int, b: int):
    """Returns the color in such a way as to allow the operative system to recognize the correct colors (given how Windows interprets colors)

    Args:
        r (int): RED value to be used
        g (int): GREEN value to be used
        b (int): BLUE value to be used

    Returns:
        Bytes: Representing the correct colors to be used in the correct order, in byte form. 
    """
    return bytes([b, g, r])
