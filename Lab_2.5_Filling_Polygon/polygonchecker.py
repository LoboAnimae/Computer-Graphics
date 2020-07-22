
def color(r, g, b):
    return bytes([b, g, r])

def raycast(after, current_pixel):
    hit = 0
    try: 
        for x in after:
            if after[x + current_pixel] != color(255, 255, 255):
                continue
            else:
                hit += 1
    except IndexError:
        return hit
        



def paint(framebuffer):
    # We need the height of the framebuffer
    height = 0
    # We need the width of the framebuffer
    width = 0
    for y in framebuffer:
        height += 1
    
    for x in framebuffer[0]:
        width += 1
    

    # First we load the first line of the frame buffer
    for y in framebuffer:
        # Second, we load pixel by pixel
        for x in y:
            # We shoot a raycast in front of the pixel
            if raycast(y, x) % 2 == 0: 
                continue
            else:
                framebuffer[y][x] = color(255, 0, 0)
            
            

framebuffer = [800, 600]
paint(framebuffer)