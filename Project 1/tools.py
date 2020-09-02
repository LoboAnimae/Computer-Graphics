import struct 
from collections import namedtuple

V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])

def color(r, g, b):
  return bytes([b, g, r])

def try_int(s, base=10, val=None):
  try:
    return int(s, base)
  except ValueError:
    return val


class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.v = []
        self.vt = []
        self.norms = []
        self.f = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                try:
                    prefix, value = line.split(' ', 1)
                except:
                    prefix = ''
                # if value == '':
                #     print('hello')
                if value !='':
                    value = value.strip()
                    if prefix == 'v':
                        self.v.append(list(map(float, value.split(' '))))
                    if prefix == 'vt':
                        self.vt.append(list(map(float, value.split(' '))))   
                    elif prefix == 'vn':
                        self.norms.append(list(map(float, value.split(' '))))                 
                    elif prefix == 'f':
                        self.f.append([list(map(try_int, face.split('/'))) for face in value.split(' ')])
                    elif prefix == 'g':
                        pass
                    elif prefix == 's':
                        pass
# loads a texture (24 bit bmp) to memory
class TextureProcessor(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        image = open(self.path, "rb")
        # we ignore all the header stuff
        image.seek(2 + 4 + 4)  # skip BM, skip bmp size, skip zeros
        header_size = struct.unpack("=l", image.read(4))[0]  # read header size
        image.seek(2 + 4 + 4 + 4 + 4)
        
        self.width = struct.unpack("=l", image.read(4))[0]  # read width
        self.height = struct.unpack("=l", image.read(4))[0]  # read width
        self.units = []
        image.seek(header_size)
        for y in range(self.height):
            self.units.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                self.units[y].append(color(r,g,b))
        image.close()

    def colordisc(self, tx, ty, intensity=1):
        x = int(tx * self.width)
        y = int(ty * self.height)
        # return self.pixels[y][x]
        try:
            return bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, self.units[y][x]))
        except:
            pass  # what causes this



def matrix_multiplication(a,b):
    c = []
    for i in range(0,len(a)):
        temp=[]
        for j in range(0,len(b[0])):
            s = 0
            for k in range(0,len(a[0])):
                s += a[i][k]*b[k][j]
            temp.append(s)
        c.append(temp)
    return c

def char(c):
    return struct.pack('=c', c.encode('ascii'))
def word(c):
    return struct.pack('=h', c)
def dword(c):
    return struct.pack('=l', c)
def color(r, g, b):
    return bytes([b, g, r])

def sum(v0, v1):
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)


def sub(v0, v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)


def mul(v0, k):
    return V3(v0.x * k, v0.y * k, v0.z * k)


def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z


def length(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5


def norm(v0):
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)


def cross(u, w):
    return V3(
        u.y * w.z - u.z * w.y,
        u.z * w.x - u.x * w.z,
        u.x * w.y - u.y * w.x,
    )


def bbox(*vertices):
    xs = [vertex.x for vertex in vertices]
    ys = [vertex.y for vertex in vertices]
    xs.sort()
    ys.sort()

    xMin = round(xs[0])
    xMax = round(xs[-1])
    yMin = round(ys[0])
    yMax = round(ys[-1])

    return xMin, xMax, yMin, yMax


def barycentric(A, B, C, P):
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )

    if abs(cz) < 1:
        return -1, -1, -1

    u = cx / cz
    v = cy / cz
    w = 1 - (cx + cy) / cz
    
    return  w, v, u



def gourad(render, **kwargs):
    w, v, u = kwargs['bar']
    tx, ty = kwargs['texture_coords']
    tcolor = render.active_texture.colordisc(tx, ty)
    nA, nB, nC = kwargs['varying_normals']
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w*iA + u*iB + v*iC
    return color(
        int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0,
        int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
        int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
    )


def fragment(render, **kwargs):
    w, v, u = kwargs['bar']
    tx, ty = kwargs['texture_coords']
    grey = int(ty * 256)
    tcolor = color(grey, 150, 150)
    nA, nB, nC = kwargs['varying_normals']
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w*iA + u*iB + v*iC
    if (intensity > 0.85):
        intensity = 1
    elif (intensity > 0.60):
        intensity = 0.80
    elif (intensity > 0.45):
        intensity = 0.60
    elif (intensity > 0.30):
        intensity = 0.45
    elif (intensity > 0.15):
        intensity = 0.30
    else:
        intensity = 0

    return color(
        int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0,
        int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
        int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
    )
