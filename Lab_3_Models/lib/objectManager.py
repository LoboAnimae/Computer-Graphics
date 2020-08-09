"""
Returns an object type read-file
"""
class Obj(object):
    def __init__(self, fileInput):
        with open(fileInput) as inp:
            self.inputLines = inp.read().splitlines()

            self.v = []
            self.f = []
            self.read()

    def read(self):
        for x in self.inputLines:
            if x:
                prtype, inpts = x.split(' ', 1)

                if prtype == 'v':
                    self.v.append(list(map(float, inpts.split(' '))))
                elif prtype == 'f':
                    self.f.append([list(map(int, face.split('/'))) for face in inpts.split(' ')])