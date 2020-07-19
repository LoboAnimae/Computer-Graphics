#include "Processor.h"
#include <iostream>
#include <fstream>

using namespace processorns;

// Global variables

// RGB values
struct color
{
    int red = 0;
    int blue = 0;
    int green = 0;
};

struct values
{
    int width = 1;
    int height = 1;
    int x = 0;
    int y = 0;
};

Processor
glInit()
{
}
Processor glCreateWindow(int width, int height) {}
Processor glViewPort(int x, int y, int width, int height) {}
Processor glClear()
{
    for (int i = 0; i <= values.width; i++)
    {
        /* code */
    }
}
Processor glClearColor() {}
Processor glVertex(int x, int y) {}
Processor glColor(int r, int g, int b) {}
Processor glFinish() {}
