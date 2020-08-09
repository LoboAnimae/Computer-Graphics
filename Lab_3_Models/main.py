import lib.renderer as rd
import sys
import os
import time
from subprocess import call
    
try:
    if sys.argv[1] == '1':
        input_file = './Models/P_HH.obj'
    elif sys.argv[1] == '2':
        input_file = './Models/E_HH.obj'
    else:
        raise Exception('You must choose between 1 and 2 as your argument. USAGE: \npython main.py 1\npython main.py 2')
    obj = rd.renderer(800, 800)
    obj.loadmodel(input_file, (0.4, 0.15), (1000, 1000))
    obj.write('output.bmp')
    path = os.getcwd() + '\output.bmp'
    print('Wrote output to ' + path)
    
    exit(0)
except Exception as e:
    print(e)
    exit(1)