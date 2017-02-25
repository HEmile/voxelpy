import numpy as np

# Abstract base class
class World:
    def __init__(self, w, h, d):
        self.w = w
        self.h = h
        self.d = d

        self.minX = 0
        self.minY = 0
        self.minZ = 0

    def set(self, x, y, z, id):
        pass

    def get(self, x, y, z):
        pass

    def tick(self, dt):
        pass

    def __getitem__(self, item):
        x, y, z = item
        return self.get(x, y, z)

    def __setitem__(self, key, value):
        x, y, z = key
        self.set(x, y, z, value)


class ChunkWorld(World):
    def __init__(self, chunk_manager):
        super().__init__(0, 0, 0)
        chunks = chunk_manager.chunks
        self.chunks = chunks

        minChunkX = min(chunks.keys(), key=lambda x: x[0])[0]
        maxChunkX = max(chunks.keys(), key=lambda x: x[0])[0]
        self.w = (maxChunkX - minChunkX) * 16
        self.minX = 16 * minChunkX

        minChunkY = min(chunks.keys(), key=lambda x: x[1])[1]
        maxChunkY = max(chunks.keys(), key=lambda x: x[1])[1]
        self.h = (maxChunkY - minChunkY) * 16
        self.minY = 16 * minChunkY

        minChunkZ = min(chunks.keys(), key=lambda x: x[2])[2]
        maxChunkZ = max(chunks.keys(), key=lambda x: x[2])[2]
        self.d = (maxChunkZ - minChunkZ) * 16
        self.minZ = 16 * minChunkZ

    def chunk_at(self, x, y, z):
        return self.chunks.get((x >> 4, y >> 4, z >> 4), None)

    def make_chunk_at(self, x, y, z):
        chunk = np.zeros((16, 16, 16))
        self.chunks[(x >> 4, y >> 4, z >> 4)] = chunk
        return chunk

    def set(self, x, y, z, id):
        chunk = self.chunk_at(x, y, z)
        if chunk is None:
            chunk = self.make_chunk_at(x, y, z)
        chx = x & 0b1111
        chy = y & 0b1111
        chz = z & 0b1111
        chunk[chx][chy][chz] = id

    def get(self, x, y, z):
        chunk = self.chunk_at(x, y, z)
        if chunk is None:
            chunk = self.make_chunk_at(x, y, z)
        chx = x & 0b1111
        chy = y & 0b1111
        chz = z & 0b1111
        return chunk[chx, chy, chz]
