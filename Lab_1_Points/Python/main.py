"""Entry Point of the program
Raises:
    Exception: Object coulnd't be created
    Exception: Object couldn't accept values
Returns:
    An image
"""

from operations import Renderer

# region GLOBAL VARIABLES

image_width = 0
image_height = 0
sub_image_width = 0
sub_image_heigth = 0
point_coordinates = [0, 0]
viewport_upper_left = [0, 0]
rgb = [0, 0, 0]
clear_color = [0, 0, 0]
point_color = [0, 0, 0]

# endregion

def entry_point(failure=False):
    """Entry point of the program. It's whatever the user sees for the 
       first time and allows the values to be changed or not. 
    Args:
        failure (bool, optional): If the program fails, act differently. Defaults to False.
    """
    if failure:
        print('\033[1;37;41m')
        failure_var = 'Something went wrong. Restarting program...'

        border = '-'
        for i in failure_var:
            border = border + '-'

        print('\n\n\n\n' + border + '\n' +
              failure_var + '\n' + border + '\n\n\n\n')
        print('\033[0;37;40m')

    try:
        print('Hello, and welcome to the program.')
        printing_menu = 'In this program, you will be able to generate a single picture with a certain'
        border = ''
        for i in printing_menu:
            border = border + '-'
        print(border + '\n' + printing_menu)
        print('background of your choosing. \nDo you wish to start the program with the default values?(Y/N)\n' + border)
        option = input('>>> ')
        if option == 'y' or option == 'Y':
            print('Default values have been set')
            set_values()
        else:
            choose_values()
    except Exception as e:
        print('An error has occurred: ' + str(e))
        entry_point(True)


def choose_values():
    """Let's the user use new values for the program
    """
    print('Please input your values:')
    width = int(input('Input your width: '))
    height = int(input('Input your height: '))
    try:
        sub_width = int(
            input('Input your viewport sub-width (PRESS ENTER TO NOT CREATE A VIEWPORT): '))
    except:
        warning = '\nA VIEWPORT WILL NOT BE CREATED. SKIPPING VIEWPORT VALUES\n'
        border = ''
        for i in warning:
            border = border + '-'
        print('\033[1;37;41m')
        print(border + warning + border)
        print('\033[0;37;40m')
        sub_width = ''
    if sub_width == '':
        sub_width = width
        sub_height = height
        viewport_x = 0
        viewport_y = 0
    else:
        while sub_width > width:
            sub_width = int(
                input('Input your viewport sub-width (SUB-WIDTH CAN\'T BE BIGGER THAN WIDTH (' + str(width) + ')): '))
        try:
            sub_height = int(input('Input your viewport sub-height: '))
            while sub_height > height:
                sub_height = int(input(
                    'Input your viewport sub-height (It can\'t be higher than Height(' + str(height) + '): '))
        except:
            sub_height = sub_width
        try:
            viewport_x = int(
                input('Please input the X-Value of the bottom-left corner: '))
            while width - sub_width < viewport_x:
                viewport_x = int(
                    input('Please input the X-Value of the bottom-left corner (Given your values, this value must be equal or less than ' + str(width - sub_width) + ' without being negative): '))
        except:
            viewport_x = 0
        try:
            viewport_y = int(
                input('Please input the Y-Value of the bottom-left corner: '))
            while height - sub_height < viewport_y:
                viewport_y = int(
                    input('Please input the Y-Value of the bottom-left corner (Given your values, this value must be equal or less than ' + str(height - sub_height) + ' without being negative): '))
        except:
            viewport_y = 0

    x = float(input('Input your X-value (Must be between -1 and 1): '))
    while x < -1 or x > 1:
        x = float(input(
            'The X-value must be between -1 and 1: '))
    y = float(input('Input your Y-value: '))
    while y < -1 or y > 1:
        y = float(input(
            'The Y-value must be between -1 and 1: '))
    print('\033[0;31;40m')
    red = int(input('Please input your RED value: '))
    while red < 0 or red > 255:
        red = int(input('Your RED value must be a number between 0 and 255: '))
    print('\033[0;32;40m')
    green = int(input('Please input your GREEN value: '))
    while green < 0 or green > 255:
        green = int(
            input('Your GREEN value must be a number between 0 and 255: '))
    print('\033[0;34;40m')
    blue = int(input('Please input your BLUE value: '))
    while blue < 0 or blue > 255:
        blue = int(input('Your BLUE value must be a number between 0 and 255: '))
    print('\033[0;37;40m')

    red_point = int(input('Please input your RED value (For your point): '))
    while red_point < 0 or red_point > 255:
        red_point = int(
            input('Your RED value must be a number between 0 and 255 (For your point): '))
    print('\033[0;32;40m')
    green_point = int(
        input('Please input your GREEN value (For your point): '))
    while green_point < 0 or green_point > 255:
        green_point = int(
            input('Your GREEN value must be a number between 0 and 255 (For your point): '))
    print('\033[0;34;40m')
    blue_point = int(input('Please input your BLUE value (For your point): '))
    while blue_point < 0 or blue_point > 255:
        blue_point = int(
            input('Your BLUE value must be a number between 0 and 255 (For your point): '))
    print('\033[0;37;40m')

    clear_color = [0, 0, 0]
    try:
        print('What do you wish your clear color to be?')
        clear_color[0] = int(input('RED: '))
        clear_color[1] = int(input('GREEN: '))
        clear_color[2] = int(input('BLUE: '))
    except:
        clear_color = [255, 255, 255]
    set_values(width, height, sub_width, sub_height, x, y,
               viewport_x, viewport_y, red, green, blue, red_point, green_point, blue_point, clear_color)


def main():
    """Main Section of the program
    """
    menu = 'Please select one of the following: '
    option1 = '1. Generate BMP Image'
    option2 = '2. Change Image Values'
    option3 = '3. Check Current Values'
    option25 = '4. Clear the buffer'
    option4 = '5. Exit Program'
    choice = 0
    runtime = True
    
    while runtime:
        print(menu + '\n' + option1 + '\n' +
              option2 + '\n' + option3 + '\n' + option25 + '\n' + option4)
        while choice < 1 or choice > 5:
            try:
                choice = int(input('>>> '))
            except Exception as e:
                print('Invalid choice type.')
                main()
        if choice == 1:
            builders = {
                'width': image_width,
                'height': image_height,
                'viewport_x': sub_image_width,
                'viewport_y': sub_image_heigth,
                'point': point_coordinates,
                'viewport_coords': viewport_upper_left,
                'rgb': rgb,
                'clear': clear_color,
                'point_color': point_color
            }
            image_creator = Renderer(builders)
            choice = 0

        elif choice == 2:
            choose_values()
            choice = 0
        elif choice == 3:
            show_values()
            choice = 0

        elif choice == 4:
            try:

                red = int(input('RED: '))
                while red < 0 or red > 255:
                    red = int(input('RED must be between 0 and 255: '))

                green = int(input('GREEN: '))
                while green < 0 or green > 255:
                    green = int(input('GREEN must be between 0 and 255: '))
                blue = int(input('BLUE: '))
                while blue < 0 or blue > 255:
                    blue = int(input('BLUE must be between 0 and 255: '))
                if change_value_clear(red, green, blue):
                    print('Values set succesfully')
                else:
                    raise Exception('Values couldn\'t be set')

            except:
                raise Exception(
                    'Couldn\'t set values! Please generate an image before you try to change the clear color!')
            finally:
                choice = 0

        elif choice == 5:
            exit(0)
        else:
            print('You somehow ended here. Congrats.')
            entry_point(True)
            choice = 0


def change_value_clear(r, g, b):
    """Allows the user to change the clear values
    Args:
        r (int): Value for red
        g (int): Value for green
        b (int): Value for blue
    Returns:
        bool: returns True if nothing bad has happened
    """    
    global clear_color
    clear_color = [r, g, b]
    return True


def set_values(width=200, height=200, sub_width=50, sub_height=50, x=-0.5, y=-0.5, viewport_x=5, viewport_y=10, red=0, green=0, blue=0, red_point=255, green_point=0, blue_point=0, clear_color_array=[255, 255, 255]):
    """Allows the user to change the values used in the program 
    Args:
        width (int, optional): Width of the entire frame. Defaults to 200.
        height (int, optional): Height of the entire frame. Defaults to 200.
        sub_width (int, optional): Width of the viewport. Defaults to 50.
        sub_height (int, optional): Height of the viewport. Defaults to 50.
        x (float, optional): X-Value of the point. Defaults to -0.5.
        y (float, optional): Y-VAlue of the point. Defaults to -0.5.
        viewport_x (int, optional): Bottom-Left corner position of the viewport. Defaults to 5.
        viewport_y (int, optional): Bottom-Left corner height position of the viewport. Defaults to 10.
        red (int, optional): RED value for the frame. Defaults to 0.
        green (int, optional): GREEN value for the frame. Defaults to 0.
        blue (int, optional): BLUE value for the frame. Defaults to 0.
        red_point (int, optional): RED value for the point. Defaults to 255.
        green_point (int, optional): GREEN value for the point. Defaults to 0.
        blue_point (int, optional): BLUE value for the point. Defaults to 0.
        clear_color_array (list, optional): Array with the clear value codes. Defaults to [255, 255, 255].
    """    
    try:
        global image_width
        global image_height
        global sub_image_width
        global sub_image_heigth
        global point_coordinates
        global viewport_upper_left
        global rgb
        global point_color
        global clear_color

        image_width = width
        image_height = height
        sub_image_width = sub_width
        sub_image_heigth = sub_height
        point_coordinates = [x, y]
        viewport_upper_left = [viewport_x, viewport_y]
        rgb = [red, green, blue]
        point_color = [red_point, green_point, blue_point]
        clear_color = clear_color_array
        show_values()
    except Exception as e:
        print('\nAn error has occurred: ' + str(e))
        entry_point(True)


def show_values():
    """Prints out the saved program values
    """
    print('\033[0;30;47m')
    print()
    print('----------------------------------------------------------------')
    print('Values have been set as:')
    print('Image size: ' + str(image_width) + 'x' + str(image_height))
    if sub_image_width != 0 and sub_image_heigth != 0:
        print('Viewport Size: ' + str(sub_image_width) +
              'x' + str(sub_image_heigth))
        print('Viewport Upper Left Corner: (' +
              str(viewport_upper_left[0]) + ', ' + str(viewport_upper_left[1]) + ')')
    print('Point\'s Coordinates: (' +
          str(point_coordinates[0]) + ', ' + str(point_coordinates[1]) + ')')
    print('Colors: RGB(\033[0;31;47m' + str(rgb[0]) + ',\033[0;32;47m ' +
          str(rgb[1]) + ',\033[0;34;47m ' + str(rgb[2]) + '\033[0;30;47m)')
    print('Point Colors: RGB(%d, %d, %d)' %
          (point_color[0], point_color[1], point_color[2]))
    print('Clear Colors: RGB(%d, %d, %d)' %
          (clear_color[0], clear_color[1], clear_color[2]))
    print('----------------------------------------------------------------')
    print()
    print('\033[0;37;40m')

    main()


entry_point()