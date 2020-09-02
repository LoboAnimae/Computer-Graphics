"""
Andrés Quan Littow      -       17652
Proyecto 1
Basado en el código de Dennis
Simplificado y modificado para poder:
    1. Leer más modelos
    2. Menos errores de lectura de otros archivos
    3. Organización y modularidad
    4. Menos utilización de memoria RAM 

KNOWN BUGS:
    1. Problemas cuando algún modelo o color utiliza el RGB(0, 255, 0), gracias a que este color se utiliza para las capas.
    2. Problemas con aquellos modelos que solo utilizen 2 datos por vértice. 


ADVERTENCIA. EL PROGRAMA CREARÁ MUCHAS IMÁGENES TEMPORALES. 
"""
from tools import *
from collections import namedtuple
import math
import os
V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])


class Render(object):
    def __init__(self):
        self.framebuffer = []
        self.zbuffer = []
        self.act_vx = []
        self.act_txt = None
        self.act_shr = None
        self.light = V3(0, 0, 1)

    def return_arr(self):
        try:
            while True:
                self.triangle()
        except StopIteration:
            pass

    def modelmat(self, translation, multiplier, rotation):
        translation = V3(*translation)
        multiplier = V3(*multiplier)
        rotation = V3(*rotation)
        transmt = [
            [1, 0, 0, translation.x],
            [0, 1, 0, translation.y],
            [0, 0, 1, translation.z],
            [0, 0, 0, 1],
        ]
        temp = rotation.x
        rotmtx = [
            [1, 0, 0, 0],
            [0, math.cos(temp), -math.sin(temp), 0],
            [0, math.sin(temp),  math.cos(temp), 0],
            [0, 0, 0, 1]
        ]
        temp = rotation.y
        rotmty = [
            [math.cos(temp), 0,  math.sin(temp), 0],
            [0, 1,       0, 0],
            [-math.sin(temp), 0,  math.cos(temp), 0],
            [0, 0,       0, 1]
        ]
        temp = rotation.z
        rotmtz = [
            [math.cos(temp), -math.sin(temp), 0, 0],
            [math.sin(temp),  math.cos(temp), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        rotmt = matrix_multiplication(
            rotmtx, rotmty)
        rotmt = matrix_multiplication(
            rotmt, rotmtz)
        multmt = [
            [multiplier.x, 0, 0, 0],
            [0, multiplier.y, 0, 0],
            [0, 0, multiplier.z, 0],
            [0, 0, 0, 1],
        ]
        tempM = matrix_multiplication(transmt, rotmt)
        tempM = matrix_multiplication(tempM, multmt)
        self.objc = tempM

    def viewmat(self, x, y, z, orig):
        temp = [
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0, 0, 0, 1]
        ]
        focal = [
            [1, 0, 0, -orig.x],
            [0, 1, 0, -orig.y],
            [0, 0, 1, -orig.z],
            [0, 0, 0, 1]
        ]
        self.vw = matrix_multiplication(temp, focal)

    def proymat(self, multiplier):
        self.proy = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, multiplier, 1]
        ]

    def viewport(self, x=0, y=0):
        self.vp = [
            [self.width/2, 0, 0, x + self.width/2],
            [0, self.height/2, 0, y + self.height/2],
            [0, 0, 128, 128],
            [0, 0, 0, 1]
        ]

    def camera(self, eye, orig, rp):
        z = norm(sub(eye, orig))
        x = norm(cross(rp, z))
        y = norm(cross(z, x))
        self.viewmat(x, y, z, orig)
        self.proymat(-1 / length(sub(eye, orig)))
        self.viewport()

    def set_frame(self, width, height):
        self.width = width
        self.height = height

    def create_buffer(self, r, g, b):
        self.framebuffer = [
            [color(r, g, b) for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]

    def fill_buffer(self, r, g, b):
        r = round(r * 255)
        g = round(g * 255)
        b = round(b * 255)
        self.create_buffer(r, g, b)

    def outputf(self, filename):
        f = open(filename, 'bw')
        with open(filename, 'bw') as outf:
            outf.write(char('B'))
            outf.write(char('M'))
            outf.write(dword(14 + 40 + self.width * self.height * 3))
            outf.write(dword(0))
            outf.write(dword(14 + 40))
            outf.write(dword(40))
            outf.write(dword(self.width))
            outf.write(dword(self.height))
            outf.write(word(1))
            outf.write(word(24))
            outf.write(dword(0))
            outf.write(dword(self.width * self.height * 3))
            outf.write(dword(0))
            outf.write(dword(0))
            outf.write(dword(0))
            outf.write(dword(0))
            for x in range(self.width):
                for y in range(self.height):
                    outf.write(self.framebuffer[y][x])

    def paint_point(self, x, y, mycolor=None):
        try:
            self.framebuffer[x][y] = mycolor or color(255, 255, 255)
        except:
            pass

    def triangle(self):
        A = next(self.act_vx)
        B = next(self.act_vx)
        C = next(self.act_vx)
        if self.act_txt:
            texta = next(self.act_vx)
            textb = next(self.act_vx)
            textc = next(self.act_vx)
            normala = next(self.act_vx)
            normalb = next(self.act_vx)
            normalc = next(self.act_vx)
        xMin, xMax, yMin, yMax = bbox(A, B, C)
        normal = norm(cross(sub(B, A), sub(C, A)))
        intensity = dot(normal, self.light)
        if intensity < 0:
            return
        for x in range(xMin, xMax + 1):
            for y in range(yMin, yMax + 1):
                w, v, u = barycentric(A, B, C, V2(x, y))
                if w < 0 or v < 0 or u < 0:
                    continue
                if self.act_txt:
                    tx = texta.x * w + textb.x * u + textc.x * v
                    ty = texta.y * w + textb.y * u + textc.y * v
                    uncolor = self.act_shr(
                        self,
                        triangle=(A, B, C),
                        bar=(w, v, u),
                        texture_coords=(tx, ty),
                        varying_normals=(normala, normalb, normalc)
                    )
                else:
                    uncolor = color(round(255 * intensity), 0, 0)
                z = A.z * w + B.z * u + C.z * v
                if x < 0 or y < 0:
                    continue
                if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[y][x]:
                    self.paint_point(x, y, uncolor)
                    self.zbuffer[y][x] = z

    def transform(self, vertex):
        temp = [
            [vertex.x],
            [vertex.y],
            [vertex.z],
            [1]
        ]

        transvx = matrix_multiplication(
            self.proy, self.vp)
        transvx = matrix_multiplication(
            transvx, self.vw)
        transvx = matrix_multiplication(
            transvx, self.objc)
        transvx = matrix_multiplication(
            transvx, temp)

        transvx = [
            transvx[0][0],
            transvx[1][0],
            transvx[2][0]
        ]

        return V3(*transvx)

    def load(self, inputf, translation=(0, 0, 0), size=(1, 1, 1), rotation=(0, 0, 0)):
        self.modelmat(translation, size, rotation)
        objc = Obj(inputf)
        vxbuffer = []

        for face in objc.f:
            vertices_count = len(face)
            if vertices_count == 3:
                for fin in face:
                    vx = self.transform(V3(*objc.v[fin[0]-1]))
                    vxbuffer.append(vx)
                if self.act_txt:
                    for fin in face:
                        try:
                            textvx = V3(*objc.vt[fin[1]-1])
                        except:
                            textvx = V2(*objc.vt[fin[1]-1])

                        vxbuffer.append(textvx)
                    for fin in face:
                        try:
                            normvx = V3(*objc.norms[fin[2]-1])
                        except:
                            normvx = V2(*objc.norms[fin[2]-1])
                        vxbuffer.append(normvx)
            elif vertices_count == 4:
                for fin in [0, 1, 2]:
                    fin = face[fin]
                    vx = self.transform(V3(*objc.v[fin[0]-1]))
                    vxbuffer.append(vx)
                if self.act_txt:
                    for fin in range(0, 3):
                        fin = face[fin]
                        try:
                            textvx = V3(*objc.vt[fin[1]-1])
                        except:
                            textvx = V2(*objc.vt[fin[1]-1])
                        vxbuffer.append(textvx)

                    for fin in range(0, 3):
                        fin = face[fin]
                        try:
                            normvx = V3(*objc.norms[fin[2]-1])
                        except:
                            normvx = V2(*objc.norms[fin[2]-1])
                        vxbuffer.append(normvx)
                for fin in [3, 0, 2]:
                    fin = face[fin]
                    vx = self.transform(V3(*objc.v[fin[0]-1]))
                    vxbuffer.append(vx)
                if self.act_txt:
                    for fin in [3, 0, 2]:
                        fin = face[fin]
                        try:
                            textvx = V3(*objc.vt[fin[1]-1])
                        except:
                            textvx = V2(*objc.vt[fin[1]-1])
                        vxbuffer.append(textvx)

                    for fin in [3, 0, 2]:
                        fin = face[fin]
                        try:
                            normvx = V3(*objc.norms[fin[2]-1])
                        except:
                            normvx = V2(*objc.norms[fin[2]-1])
                        vxbuffer.append(normvx)
        self.act_vx = iter(vxbuffer)


def gourad(render, **kwargs):
    w, v, u = kwargs['bar']
    tx, ty = kwargs['texture_coords']
    tcolor = render.act_txt.colordisc(tx, ty)
    nA, nB, nC = kwargs['varying_normals']
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w * iA + u * iB + v * iC

    return color(
        int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0,
        int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
        int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
    )


def shader(render, **kwargs):
    w, v, u = kwargs['bar']
    tx, ty = kwargs['texture_coords']
    grey = int(ty * 256)
    tcolor = color(grey, 150, 150)
    nA, nB, nC = kwargs['varying_normals']
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w * iA + u * iB + v * iC
    if intensity > 0.85:
        intensity = 1
    elif intensity > 0.60:
        intensity = 0.80
    elif intensity > 0.45:
        intensity = 0.60
    elif intensity > 0.30:
        intensity = 0.45
    elif intensity > 0.15:
        intensity = 0.30
    else:
        intensity = 0

    return color(
        int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0,
        int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
        int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
    )


def flatten_image(image1, image2):
    r1 = Render()
    r1.set_frame(1000, 1000)
    r1.fill_buffer(1, 1, 1)
    t1 = TextureProcessor(image1)
    r1.act_txt = t1
    r1.camera(V3(1, 0, 0), V3(0, 0, 0), V3(0, 0, 0))
    for y in range(len(t1.units)):
        for x in range(len(t1.units[y])):
            r1.paint_point(x, y, r1.act_txt.colordisc(y/1000, x/1000))
    r2 = Render()
    r2.set_frame(1000, 1000)
    r2.fill_buffer(1, 1, 1)
    t2 = TextureProcessor(image2)
    r2.act_txt = t2
    r2.camera(V3(1, 0, 0), V3(0, 0, 0), V3(0, 0, 0))
    for y in range(len(t2.units)):
        for x in range(len(t2.units[y])):
            r1.paint_point(x, y, r2.act_txt.colordisc(y/1000, x/1000) if r2.act_txt.colordisc(
                y/1000, x/1000) != color(0, 255, 0) else r1.act_txt.colordisc(y/1000, x/1000))
    del r2
    r1.outputf('superimposed.bmp')


def loadmodel(model, modeltexture, modeltranslate=V3(0, 0, 0), modelscale=V3(1, 1, 1), modelrotate=V3(0, 0, 0), buffer=(0, 1, 0), cameraeye=V3(1, 0, 5), cameracenter=V3(0, 0, 0), cameraup=V3(0, 1, 0), outputf='outf'):
    outputf = outputf + '.bmp'
    r = Render()
    print('Rendering model ' + str(model))
    r.set_frame(1000, 1000)
    r.fill_buffer(buffer[0], buffer[1], buffer[2])
    t = TextureProcessor(modeltexture)
    r.act_txt = t
    r.act_shr = gourad
    r.camera(cameraeye, cameracenter, cameraup)
    r.load(model, modeltranslate, modelscale, modelrotate)
    r.return_arr()
    r.outputf(outputf)


def main():
    # Draw the background
    print('Rendering Background...')
    r = Render()
    r.set_frame(1000, 1000)
    r.fill_buffer(1, 1, 1)
    t = TextureProcessor('background.bmp')
    r.act_txt = t
    r.camera(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
    for y in range(len(t.units)):
        for x in range(len(t.units[y])):
            r.paint_point(x, y, r.act_txt.colordisc(y/1000, x/1000))
    r.outputf('superimposed.bmp')

    del r
    del t

    # Draw the helmet
    loadmodel('./Models/MasterChief/Master_Chief_Helmet.obj', './Models/MasterChief/chief_helm_d.bmp', V3(0.50, -
                                                                                                          0.60, 0), V3(0.9, 0.9, 0.9), V3(0.15, -0.15, 2), (0, 1, 0), V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0), 'helmet')
    # Shooting ship
    loadmodel('./Models/Star Ships/StarSparrow01.obj', './Models/Star Ships/Textures/StarSparrow_Black.bmp',
              V3(0.5, -0.5, 0), V3(0.05, 0.05, 0.05), V3(-1, 0, 1), (0, 1, 0), V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0), 'ship1')
    # Parked Ship
    loadmodel('./Models/Star Ships/StarSparrow09.obj', './Models/Star Ships/Textures/StarSparrow_Orange.bmp',
              V3(-0.5, -0.5, 0), V3(0.1, 0.1, 0.1), V3(1, 0.5, 0), (0, 1, 0), V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0), 'ship2')
    # Rifle on the ground
    loadmodel('./Models/deadrifle/m4a1.obj', './Models/deadrifle/text.bmp', V3(-0.6, 0.55, 0), V3(0.02,
                                                                                                  0.02, 0.02), V3(-0.15, -0.15, 0), (0, 1, 0), V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0), 'rifle')
    loadmodel('./Models/Rock/rock_v2.obj', './Models/Rock/base.bmp', V3(-0.75, -0.28, 0), V3(0.002,
                                                                                             0.002, 0.002), V3(1, 1, 0), (0, 1, 0), V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0), 'rock1')
    loadmodel('./Models/Rock/rock_v2.obj', './Models/Rock/base.bmp', V3(-0.45, -0.87, 0), V3(0.0075,
                                                                                             0.0075, 0.0075), V3(0.7, 1, 0), (0, 1, 0), V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0), 'rock2')
    loadmodel('./Models/Rock/rock_v2.obj', './Models/Rock/base.bmp', V3(-0.80, 0, 0), V3(0.0035,
                                                                                         0.0035, 0.0035), V3(1, 1, 0), (0, 1, 0), V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0), 'rock3')
    print('Flattening image...')
    flatten_image('superimposed.bmp', 'helmet.bmp')
    flatten_image('superimposed.bmp', 'ship1.bmp')
    flatten_image('superimposed.bmp', 'ship2.bmp')
    flatten_image('superimposed.bmp', 'rifle.bmp')
    flatten_image('superimposed.bmp', 'rock1.bmp')
    flatten_image('superimposed.bmp', 'rock2.bmp')
    flatten_image('superimposed.bmp', 'rock3.bmp')

    print('Removing temp files...')
    os.remove('./helmet.bmp')
    os.remove('./ship1.bmp')
    os.remove('./ship2.bmp')
    os.remove('./rifle.bmp')
    os.remove('./rock1.bmp')
    os.remove('./rock2.bmp')
    os.remove('./rock3.bmp')

    print('Output has been written to superimposed.bmp !')


#
main()
