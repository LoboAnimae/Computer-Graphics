from lib.objectManager import Obj
from lib.converters import *
from lib.constants import *


class renderer(object):
    def __init__(self, width: int, height: int):
        self.wtdh = width
        self.hght = height
        self.createport()

    def createport(self):
        """Creates a viewport that can be used to paint stuff.
        """        
        r, g, b = CLEARCOLOR
        self.framebuffer = [
            [color(r, g, b) for x in range(self.wtdh)]
            for y in range(self.hght)
        ]

    def paintpoint(self, x: int, y: int):
        """Paints a single point somewhere in the framebuffer

        Args:
            x (int): X-Value of the Point
            y (int): Y-Value of the Point
        """        
        r, g, b = COLORCONST
        try:
            self.framebuffer[y][x] = color(r, g, b)
        except:
            pass

    def drawline(self, beg: list, end: list):
        """Draws a line by painting many points in a for loop

        Args:
            beg (list): Beginning point (Contains both X and Y values)
            end (list): Ending point (Contains both X and Y values)
        """        
        xbeg, ybeg = beg
        xend, yend = end
        d_x = finddiff(xbeg, xend)
        d_y = finddiff(ybeg, yend)
        m = d_y > d_x

        if m:
            xbeg, ybeg = ybeg, xbeg
            xend, yend = yend, xend

        if xbeg > xend:
            xbeg, xend = xend, xbeg
            ybeg, yend = yend, ybeg

        d_y = finddiff(ybeg, yend)
        d_x = finddiff(xbeg, xend)

        trans = 0
        thr = d_x

        y = ybeg

        for x in range(xbeg, xend + 1):
            if m:
                self.paintpoint(y, x)
            else:
                self.paintpoint(x, y)

            trans += d_y * 2
            if trans >= thr:
                y += 1 if ybeg < yend else -1
                thr += d_x * 2

    def loadmodel(self, objname: str, trans: float, size: float):
        """Loads a single model. Based on the class Dennis' example. 

        Args:
            objname (str): Name of the file of the object to be used. 
            trans (float): Translation to be used for the object. 
            size (float): Size of the object. Scale.
        """        
        loaded = Obj(objname)

        for fs in loaded.f:
            vcount = len(fs)

            for j in range(vcount):
                f1 = fs[j][0]
                f2 = fs[(j + 1) % vcount][0]

                v1 = loaded.v[f1 - 1]
                v2 = loaded.v[f2 - 1]

                xbeg = round((v1[0] + trans[0]) * size[0])
                ybeg = round((v1[1] + trans[1]) * size[1])
                xend = round((v2[0] + trans[0]) * size[0])
                yend = round((v2[1] + trans[1]) * size[1])

                self.drawline((xbeg, ybeg), (xend, yend))

    def write(self, outpf: str):
        """Writes the file

        Args:
            outpf (str): Name of the output file. 
        """        
        with open(outpf, 'bw') as output:
            output.write(char('B'))
            output.write(char('M'))
            output.write(dword(54 + self.wtdh * self.hght * 3))
            output.write(dword(0))
            output.write(dword(54))
            output.write(dword(40))
            output.write(dword(self.wtdh))
            output.write(dword(self.hght))
            output.write(word(1))
            output.write(word(24))
            output.write(dword(0))
            output.write(dword(self.wtdh * self.hght * 3))
            output.write(dword(0))
            output.write(dword(0))
            output.write(dword(0))
            output.write(dword(0))
            for x in range(self.hght):
                for y in range(self.wtdh):
                    output.write(self.framebuffer[x][y])


if __name__ == "__main__":
    print('Please run this with main.py. This is a module.')
    sys.exit(1)
