class World:
    def __init__(self, w, h, d):
        self.w = w
        self.h = h
        self.d = d

        self.voxels = []
        for _ in range(self.w):
            self.voxels.append([[0 for _ in range(self.d)] for _ in range(self.h)])

    def set(self, x, y, z, id):
        self.voxels[x][y][z] = id

    def tick(self, dt):
        pass