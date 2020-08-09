import lib.renderer as rd
import sys
import os
import tkinter
import tkinter.font as tkFont
from tkinter import filedialog
import time

#region DEFAULTVALUES

#endregion
input_file = ''

    
def browseFiles():
    file_name = filedialog.askopenfilename(initialdir='./', title='Seleccione un archivo...',
                                           filetypes=(("3D Object", "*.obj*"), ("All files", "*.*")))
    global input_file
    input_file = file_name
    input_file_label["text"] = input_file
    

    
def preprocess():
    obj = rd.renderer(800, 800)
    try:
        global input_file
        if input_file == '':
            raise Exception('File name can\'t be empty!')
        if input_file[len(input_file) - 4: len(input_file)] != '.obj':
            input_file += '.obj'
        obj.loadmodel(input_file, (0.4, 0.15), (1000, 1000))
        time.sleep(1.5)
        obj.write('output.bmp')
        output_label["text"] = 'Wrote output.bmp in local directory.'
    except Exception as e:
        output_label["text"] = e
    

root = tkinter.Tk()

title = tkinter.Label(root, text='Lab 3 - Models', justify = 'center', cursor = 'arrow')
sub_section_input = tkinter.Label(root, text = 'Seleccione un archivo...', pady = 20, cursor='arrow')
input_file_label = tkinter.Label(root)
button_input = tkinter.Button(root, text='Seleccionar Archivo', command=browseFiles, cursor='hand2')
submit = tkinter.Button(root, text='Procesar', cursor='hand2', command=preprocess)
output_label = tkinter.Label(root, text='The program might get stuck for a while. This is normal when processing.')
instructions = tkinter.Label(root, text='The models are in the Models folder. \nThe window will always be 800x800 to simplify processing.')

root.title('Laboratorio 3 - Andres Quan-Littow')
root.tk_setPalette('black')
title.grid(row=0, column=0, columnspan=1)
instructions.grid(row=1, column=0, columnspan=1)
sub_section_input.grid(row=2, column=0)
button_input.grid(row=2, column=1)
input_file_label.grid(row=1, column=1)
submit.grid(row=3, column=1)
output_label.grid(row=4, column=0)
sub_section_input.grid(row=2, column=0)
rows = 0
while rows < 2:
    root.rowconfigure(rows, weight=1)
    root.columnconfigure(rows, weight=1)
    rows +=1
    
root.mainloop()
