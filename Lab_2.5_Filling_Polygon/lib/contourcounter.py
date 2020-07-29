def greatercounter(contourp:list, point:list, index:int):
    """Allows to know the number of points in front of the given point. 

    Args:
        contourp (list): List of all the points
        point (list): X-Y-Values array of a singular point
        index (int): 0 if working on X. 1 if working on Y. 

    Returns:
        int: How many are behind, how many are in front
    """    
    cless = set()
    cmore = set()

    ops = 0 if index == 1 else 1

    for cpoint in contourp:
        if cpoint[ops] == point[ops]:
            if cpoint[index] < point[index]:
                cless.add(cpoint[index])
            if cpoint[index] > point[index]:
                cmore.add(cpoint[index])
    
    return len(cless), len(cmore)