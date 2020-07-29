from lib.converters import char, word, dword, color
from lib.contourcounter import greatercounter


class Render(object):
    """Render object that generates an image. Code based off Denn1s' GitHub (Python simple renderer) and developed with his help. 

    Args:
        object (obj): Initial parameters
    """

    def __init__(self, width, height, col):
        self.__width = width
        self.__height = height
        self.__current_color = color(col[0], col[1], col[2])
        self.setbuffer()

    def setbuffer(self):
        """Creates the buffer
        """
        self.framebuffer = [
            [bytes([0, 0, 0]) for x in range(self.__width)]
            for y in range(self.__height)
        ]

    def write(self):
        """Writes the file at the end of the program. This is always the last function to run. 
        """
        with open('output.bmp', 'bw') as ofile:
            ofile.write(char('B'))
            ofile.write(char('M'))
            ofile.write(dword(3 * (64 + self.__width * self.__height)))
            ofile.write(dword(0))
            ofile.write(dword(64))
            ofile.write(dword(40))
            ofile.write(dword(self.__width))
            ofile.write(dword(self.__height))
            ofile.write(word(1))
            ofile.write(word(24))
            ofile.write(dword(0))
            ofile.write(dword(3 * (self.__width * self.__height)))
            ofile.write(dword(0))
            ofile.write(dword(0))
            ofile.write(dword(0))
            ofile.write(dword(0))

            # Write the buffer so that the file can have an output. 
            for x in range(self.__height):
                for y in range(self.__width):
                    ofile.write(self.framebuffer[x][y])

    def setpoint(self, x: int, y: int):
        """Paints a pixel in a defined point using the x and y coordinates. 

        Args:
            x (int): X-Coordinate of the point. 
            y (int): Y-Coordinate of the point. 
        """
        try:
            self.framebuffer[y][x] = self.__current_color
        except:
            # If the program excepts, then the image is outside of the frame. Don't do anything. 
            pass

    def contoury(self, start: list, end: list, polygon: list, color: list = None):
        """Generates the Y-Based figure, eliminating big, empty lines in them, where the vertices are. 

        Args:
            start (list): The start point of the line to be drawn (several lines allow for the shape to be painted).
            end (list): The end point of the line to be drawn.
            polygon (list): Polygon list containing all the vertices to be added to the exception list in the polygon. 
            color (list, optional): Color to be used to paint the figure. Defaults to None.

        Returns:
            points (list): Entire list of Y points to be painted later on. 
        """
        xi, yi = start
        xf, yf = end

        dy = abs(yf - yi)
        dx = abs(xf - xi)
        m = dy > dx

        if m:
            xi, yi = yi, xi
            xf, yf = yf, xf

        if xi > xf:
            xi, xf = xf, xi
            yi, yf = yf, yi

        dy = abs(yf - yi)
        dx = abs(xf - xi)

        os = 0
        th = dx

        y = yi

        points = []

        # Add all vertices to the buffer so that they aren't used
        pointsy = [x for x, y in polygon]
        for x in range(xi, xf + 1):
            if m:
                if y not in pointsy:
                    points.append([y, x])
                pointsy.append(y)
            else:
                if x not in pointsy:
                    points.append([x, y])
                pointsy.append(x)

            # Move the offset
            os += dy * 2
            if os >= th:
                y += 1 if yi < yf else -1
                th += dx * 2

        return points

    def contourx(self, start: list, end: list, polygon: list, color: list = None):
        """Generates the X-Based figure, eliminating big, empty lines in them, where the vertices are. 

        Args:
            start (list): The start point of the line to be drawn (several lines allow for the shape to be painted).
            end (list): The end point of the line to be drawn.
            polygon (list): Polygon list containing all the vertices to be added to the exception list in the polygon. 
            color (list, optional): Color to be used to paint the figure. Defaults to None.

        Returns:
            points (list): Entire list of X points to be painted later on. 
        """
        xi, yi = start
        xf, yf = end

        dy = abs(yf - yi)
        dx = abs(xf - xi)
        m = dy > dx

        if m:
            xi, yi = yi, xi
            xf, yf = yf, xf

        if xi > xf:
            xi, xf = xf, xi
            yi, yf = yf, yi

        dy = abs(yf - yi)
        dx = abs(xf - xi)

        os = 0
        th = dx

        y = yi

        points = []
        # Add all the vertices so that they are ignored
        pointsx = [y for x, y in polygon]
        for x in range(xi, xf + 1):
            if m:
                if x not in pointsx:
                    points.append([y, x])
                pointsx.append(x)
            else:
                if y not in pointsx:
                    points.append([x, y])
                pointsx.append(y)

            os += dy * 2
            if os >= th:
                y += 1 if yi < yf else -1
                th += dx * 2

        return points

    def fillpolygon(self, polygon: list):
        """Fills the polygon by creating several lines in between the vertices and lines. 

        Args:
            polygon (list): Container for all the different vertices to be used to draw the figure. 
        """
        xsp = []
        ysp = []

        for point in polygon:
            xsp.append(point[0])
            ysp.append(point[1])

        xmin = min(xsp)
        xmax = max(xsp)
        ymin = min(ysp)
        ymax = max(ysp)

        contourpx = []
        contourpy = []

        for i in range(len(polygon)):
            contourpx += self.contourx(polygon[i],
                                       polygon[(i + 1) % len(polygon)], polygon)
            contourpy += self.contoury(polygon[i],
                                       polygon[(i + 1) % len(polygon)], polygon)

        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                smallerx, biggerx = greatercounter(contourpx, (x, y), 0)
                smallery, biggery = greatercounter(contourpy, (x, y), 1)
                if smallerx % 2 != 0 and biggerx % 2 != 0:
                    self.setpoint(x, y)
                if smallery % 2 != 0 and biggery % 2 != 0:
                    self.setpoint(x, y)
                if (smallery == 0 and biggery == 0) and (smallerx == 0 and biggerx == 0):
                    pass
