import time
import struct


class Renderer:
    def __init__(self, builders:dict):
        """Initializes the class
        Args:
            builders (dict): Brings the parameters needed to start the object
        Raises:
            Exception: Throws an exception if the object couldn't be created
        """           
        if self.glinit(builders):
            print('Parameters introduced correctly.')
            self.__f = open(self.__file_name, 'bw')
            self.gl_create_window(builders['width'], builders['height'])
        else:
            raise Exception('Parameters couldn\'t be used to create object')

    def glinit(self, builders:dict):
        """Initializes the object formally
        Args:
            builders (dict): Parameters
        Returns:
            bool: returns true if it was well made
        """        
        try:
            self.__canvas = (builders['width'], builders['height'])
            self.__viewport = (builders['viewport_x'], builders['viewport_y'],
                               builders['viewport_coords'][0], builders['viewport_coords'][1])
            self.__point = (builders['point'][0], builders['point'][1])
            self.__rgb = (builders['rgb'][0],
                          builders['rgb'][1], builders['rgb'][2])
            self.__file_name = time.strftime("%H%M%S") + '_output_BMP_file.bmp'
            self.__clear_color = [builders['clear'][2],
                                  builders['clear'][1], builders['clear'][0]]
            self.__point_color = [builders['point_color'][2],
                                  builders['point_color'][1], builders['point_color'][0]]
            return True
        except:
            return False

    def convert(self, argument:int, conversion_type:int):
        """Converts the different values to different struct types
        Args:
            argument (int): value to be processed
            conversion_type (int): What kind of data type must be taken back
        Returns:
            struct: Converted value
        """        
        if conversion_type == 1:
            return struct.pack('=c', argument.encode('ascii'))
        elif conversion_type == 2:
            return struct.pack('=l', argument)
        elif conversion_type == 3:
            return struct.pack('=h', argument)

    def gl_create_window(self, width:int, height:int):
        """Creates a window so that stuff can be drawn.
        Args:
            width (int): The frame width
            height (int): The frame height
        """
        # File Header
        self.__f.write(self.convert('B', 1))
        self.__f.write(self.convert('M', 1))
        self.__f.write(self.convert(
            (14 + 40 + width + height), 2))
        self.__f.write(self.convert(0, 2))
        self.__f.write(self.convert(54, 2))

        # Image Header
        self.__f.write(self.convert(40, 2))
        self.__f.write(self.convert(width, 2))
        self.__f.write(self.convert(height, 2))
        self.__f.write(self.convert(1, 3))
        self.__f.write(self.convert(24, 3))
        self.__f.write(self.convert(0, 2))
        self.__f.write(self.convert((width * height * 3), 2))
        self.__f.write(self.convert(0, 2))
        self.__f.write(self.convert(0, 2))
        self.__f.write(self.convert(0, 2))
        self.__f.write(self.convert(0, 2))

        try:
            self.__framebuffer = [
                [bytes([self.__rgb[2], self.__rgb[1], self.__rgb[0]])  # TODO: CHANGE THE COLOR SO THAT IT CAN BE CHOSEN BY THE USER
                 for i in range(width)]
                for j in range(height)
            ]

            self.gl_view_port(
                self.__viewport[2], self.__viewport[3], self.__viewport[0], self.__viewport[1])
            return True
        except:
            return False

    def gl_view_port(self, x:int, y:int, height:int, width:int):
        """Allows the viewport to be created inside the frame
        Args:
            x (int): X-Value position of the bottom left corner
            y (int): Y-Value position of the bottom left corner
            height (int): Height of the viewport
            width (int): Width of the viewport
        """        
        for x in range(width):
            for y in range(height):
                self.__framebuffer[y + self.__viewport[3]][x +
                                                           self.__viewport[2]] = bytes([255, 255, 255])

        self.gl_vertex(self.__point[0], self.__point[1])

    def gl_clear(self):
        """Allows the frame to clean itself with a single color
        Returns:
            bool: True if it was able to do so
        """        
        try:
            self.__f_clear = open('cleared_picture.bmp', 'bw')
            self.__f_clear.write(self.convert('B', 1))
            self.__f_clear.write(self.convert('M', 1))
            self.__f_clear.write(self.convert(
                (14 + 40 + self.__canvas[0] + self.__canvas[1]), 2))
            self.__f_clear.write(self.convert(0, 2))
            self.__f_clear.write(self.convert(54, 2))

            # Image Header
            self.__f_clear.write(self.convert(40, 2))
            self.__f_clear.write(self.convert(self.__canvas[0], 2))
            self.__f_clear.write(self.convert(self.__canvas[1], 2))
            self.__f_clear.write(self.convert(1, 3))
            self.__f_clear.write(self.convert(24, 3))
            self.__f_clear.write(self.convert(0, 2))
            self.__f_clear.write(self.convert(
                (self.__canvas[0] * self.__canvas[1] * 3), 2))
            self.__f_clear.write(self.convert(0, 2))
            self.__f_clear.write(self.convert(0, 2))
            self.__f_clear.write(self.convert(0, 2))
            self.__f_clear.write(self.convert(0, 2))

            self.__framebuffer = [
                [bytes([self.__clear_color[2], self.__clear_color[1], self.__clear_color[0]])  # TODO: CHANGE THE COLOR SO THAT IT CAN BE CHOSEN BY THE USER
                for i in range(self.__canvas[0])]
                for j in range(self.__canvas[1])
            ]

            for x in range(self.__canvas[0]):
                for y in range(self.__canvas[1]):
                    self.__f_clear.write(self.__framebuffer[y][x])
            self.__f_clear.close()
            return True
        except:
            return False

    def gl_clear_color(self, r:int, g:int, b:int):
        """Allows the clear color to be changed
        Args:
            r (int): RED value for the clear
            g (int): GREEN value for the clear
            b (int): BLUE value for the clear
        Returns:
            bool: TRUE if changed
        """        
        try:
            self.__clear_color = [b, g, r]
            return True
        except:
            return False

    def gl_vertex(self, x:float, y:float):
        """Allows the point to be generated somewhere inside the viewport
        Args:
            x (float): Must be between -1 and 1 and relative to the width. 
            y (float): Must be between -1 and 1 and relative to the width.
        """        
        y_index = int(
            self.__viewport[2] + self.__viewport[1]/2 + (y * (self.__viewport[1]/2)))
        x_index = int(
            self.__viewport[3] + self.__viewport[0]/2 + (x * (self.__viewport[0]/2)))
        self.__framebuffer[int(x_index)][int(
            y_index)] = bytes(self.__point_color)

    def gl_color(self, r:int, g:int, b:int):
        """Changes the color on run-time
        Args:
            g (int): GREEN value for the point
            r (int): RED value for the point
            b (int): BLUE value for the point
        """        
        self.__point_color = [b, g, r]

    def gl_finish(self):
        """Ends the program and closes any files. 
        """        
        for x in range(self.__canvas[0]):
            for y in range(self.__canvas[1]):
                self.__f.write(self.__framebuffer[y][x])
        self.__f.close()

        print('Generated ' + str(self.__file_name))
