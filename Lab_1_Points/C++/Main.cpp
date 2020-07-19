#include "Processor.h"
#include <iostream>
#include <fstream>

using std::cin;
using std::cout;
using std::endl;

using namespace processorns;

/*
// basic file operations
int main () {
  ofstream myfile;
  myfile.open ("example.txt");
  myfile << "Writing this to a file.\n";
  myfile.close();
  return 0;
}
*/

int width = 100, height = 100, x = 0, y = 0;
int red = 0, green = 0, blue = 0;
char changeValues = 'N';

void changeDefaultValues()
{

    try
    {
        cout << "\nYou\'ve chosen to change the values for the output. Please input the following values:" << endl;
        cout << "Width: ";
        cin >> width;
        cout << "\nHeight: ";
        cin >> height;
        cout << "\nX: ";
        cin >> x;
        while (x > width) {
            cout << "The value for X must be lower than that of the Width(Currently " << width << ")" << endl << "X: ";
            cin >> x;
        }
        cout << "\nY: ";
        cin >> y;
        while (y > height) {
            cout << "The value for Y must be lower than that of the Height(Currently " << height << ")" << endl << "Y: ";
            cin >> y;
        }

        cout << "\nNow input your colors:" << endl;
        cout << "R: ";
        cin >> red;
        while (red < 0 || red > 255)
        {
            cout << "\nThe value must be between 0 and 255" << endl;
            cout << "R: ";
            cin >> red;
        }
        cout << "\nG: ";
        cin >> green;
        while (green < 0 || green > 255)
        {
            cout << "\nThe value must be between 0 and 255" << endl;
            cout << "G: ";
            cin >> green;
        }
        cout << "\nB: ";
        cin >> blue;
        while (blue < 0 || blue > 255)
        {
            cout << "\nThe value must be between 0 and 255" << endl;
            cout << "B: ";
            cin >> blue;
        }
    }
    catch (const std::exception &e)
    {
        cout << "\nAn error has been found while adding your value: " << endl
             << e.what() << endl;
        changeDefaultValues();
    }
}

int main()
{
    // Main values

    cout << "\nHello and welcome to the program." << std::endl;
    cout << "\n\n---------------------------------" << endl;

    cout << "\nThe default values are: \n"
         << "Width: " << width << "\nHeight: " << height << "\nX: " << x << "\nY: " << y << "\nColors: RGB(" << red << ", " << green << ", " << blue << ")" << endl;
    cout << "-------------------------------------" << endl;

    cout << "\nWould you like to change these values? (Y/N) ";

    bool active = true;

    try
    {
        cin >> changeValues;
        if (changeValues == 'Y' || changeValues == 'y')
        {   
            changeDefaultValues();
        }
        else
        {
            cout << "\nValues have not been changed" << endl;
        }
    }
    catch (const std::exception &e)
    {
        cout << "\nAn error has been found while adding your value: " << endl
             << e.what() << endl;
        changeValues = 'N';
        active = false;
    }

    while (active)
    {
        int option;
        cout << "\nMenu: \n1. Generate Image \n2. Change Values \n3. Check Current Values\n4. Exit Program" << endl << ">> ";
        try
        {
            cin >> option;
            if (option == 1)
            {
            }
            else if (option == 2)
            {
                changeDefaultValues();
            }
            else if (option == 3)
            {
                cout << "-------------------------------" << endl;

                cout << "\n\nThe current values are: \n"
                     << "Width: " << width << "\nHeight: " << height << "\nX: " << x << "\nY: " << y << "\nColors: RGB(" << red << ", " << green << ", " << blue << ")" << endl;
                cout << "-------------------------------" << endl;
            }

            else
            {
                return -1;
            }
        }
        catch (const std::exception &e)
        {
            return -1;
        }
    }
}