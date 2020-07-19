#include <iostream>

namespace processorns
{

    class Processor
    {
    public:
        Processor glInit();
        Processor glCreateWindow(int width, int height);
        Processor glViewPort(int x, int y, int width, int height);
        Processor glClear();
        Processor glClearColor();
        Processor glVertex(int x, int y);
        Processor glColor(int r, int g, int b);
        Processor glFinish();

    private:
        struct values
        {
            int width;
            int height;
            int x;
            int y;
        };
    };
} // namespace processorns
