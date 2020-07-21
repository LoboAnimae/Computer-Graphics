

class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()

        self.vertices = []
        self.faces = []
        self.read()

    def read(self):
        for line in self.lines:
            prefix, value = line.split(' ', 1)

            if prefix == 'v':
                # Vertice
                self.vertices.append(
                    list(map(float, value.split(' ')))
                )

            elif prefix == 'f':
                # faces
                self.faces.append(
                    [list(map(int, face.split('/')))
                     for face in value.split(' ')]
                )


m = Obj('./cube.obj')
print(m.vertices)
print(m.faces)
