import numpy as np


class World:
    def __init__(self, w, h, d):
        self.w = w
        self.h = h
        self.d = d

        self.minX = 0
        self.minY = 0
        self.minZ = 0

        self.voxels = []
        for _ in range(self.w):
            self.voxels.append([[0 for _ in range(self.d)] for _ in range(self.h)])

    def set(self, x, y, z, id):
        self.voxels[x][y][z] = id

    def get(self, x, y, z):
        return self.voxels[x][y][z]

    def tick(self, dt):
        pass


class ChunkWorld(World):
    def __init__(self, chunks):
        super().__init__(0, 0, 0)
        self.chunks = chunks
        self.h = next(iter(chunks.values())).shape[1]
        self.chunkw, self.chunkh, self.chunkd = next(iter(chunks.values())).shape
        minChunkX = min(chunks.keys(), key=lambda x: x[0])[0]
        maxChunkX = max(chunks.keys(), key=lambda x: x[0])[0]
        self.w = (maxChunkX - minChunkX) * 16
        self.minX = 16 * minChunkX

        minChunkZ = min(chunks.keys(), key=lambda x: x[1])[1]
        maxChunkZ = max(chunks.keys(), key=lambda x: x[1])[1]
        self.d = (maxChunkZ - minChunkZ) * 16
        self.minZ = 16 * minChunkZ

    def chunk_at(self, x, z):
        return self.chunks.get((x >> 4, z >> 4), None)

    def make_chunk_at(self, x, z):
        chunk = np.zeros((self.chunkw, self.chunkh, self.chunkd))
        self.chunks[(x >> 4, z >> 4)] = chunk
        return chunk

    def set(self, x, y, z, id):
        chunk = self.chunk_at(x, z)
        if chunk is None:
            chunk = self.make_chunk_at(x, z)
        chx = x & 0b1111
        chz = z & 0b1111
        chunk[chx][y][chz] = id

    def get(self, x, y, z):
        chunk = self.chunk_at(x, z)
        if chunk is None:
            chunk = self.make_chunk_at(x, z)
        chx = x & 0b1111
        chz = z & 0b1111
        return chunk[chx, y, chz]
