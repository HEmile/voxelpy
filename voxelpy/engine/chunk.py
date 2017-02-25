import numpy as np
import voxelpy.engine.chunk_render as render
from pyglet.gl import *
import time

class Chunk:
    def __init__(self, chunkX, chunkY, chunkZ, chunk_size=16, contents=None):
        self.chunkX, self.chunkY, self.chunkZ = chunkX, chunkY, chunkZ
        self.blocks = contents
        self.chunk_size = chunk_size

        self.needs_rebuild = False
        if not self.blocks:
            self.blocks = [[[0 for _ in range(chunk_size)] for _ in range(chunk_size)] for _ in range(chunk_size)]
            self.has_blocks = False
        else:
            self.needs_rebuild = True
            self.update_render_flags()

        self._vertex_list = None

    def should_render(self):
        return self.has_blocks and not self.needs_rebuild

    def set_mesh(self, vertex_list_bf, colors):
        self.vertex_list_bf = vertex_list_bf
        self.colors = colors
        self.needs_rebuild = False

    def build_mesh(self):
        self._vertex_list = pyglet.graphics.vertex_list(len(self.vertex_list_bf) // 3,
                             ('v3f', self.vertex_list_bf), ('c3B', self.colors))
        del self.vertex_list_bf
        del self.colors

    def update_render_flags(self):
        for id in self:
            if id != 0:
                self.has_blocks = True
                break

    def draw(self):
        if self._vertex_list:
            self._vertex_list.draw(GL_QUADS)

    def __getitem__(self, item):
        x, y, z = item
        return self.blocks[x][y][z]

    def __setitem__(self, key, value):
        self.needs_rebuild = True
        x, y, z = key
        self.blocks[x][y][z] = value

    def __iter__(self):
        for x in range(self.chunk_size):
            for y in range(self.chunk_size):
                for z in range(self.chunk_size):
                    yield self.blocks[x][y][z]

    def __getstate__(self):
        return self.chunkX, self.chunkY, self.chunkZ, self.blocks, self.chunk_size

    def __setstate__(self, state):
        self.chunkX, self.chunkY, self.chunkZ, self.blocks, self.chunk_size = state
        self.update_render_flags()
        self._vertex_list = None
        if self.has_blocks:
            self.needs_rebuild = True


def empty_chunk(chunkX, chunkY, chunkZ, chunk_size=16):
    return Chunk(chunkX, chunkY, chunkZ, chunk_size=chunk_size)


class ChunkManager:
    def __init__(self, chunks, rebuild_per_frame=1, render_dist=4):
        self.chunks = chunks
        self.rebuild_per_frame = rebuild_per_frame
        self.render_dist = render_dist
        self.rebuild = []
        self.update_flags = []
        self.render = []
        self.visibility = []
        self.build = []
        self.needs_update = True
        self.cmr = np.array([-1, -1, -1])
        self.lock = False

    def draw(self, dt, camera, at):
        if len(self.build) > 0:
            chunk = self.build.pop()
            chunk.build_mesh()
        self._render()

    def update(self, dt, camera, at):
        if self.lock:
            return
        self.lock = True
        if not (camera == self.cmr).all():
            self.cmr = np.array([camera[0], camera[1], camera[2]])
            self._update_visibility(camera)
            self.needs_update = True
        self._update_rebuild()
        self.lock = False

    def _update_rebuild(self):
        count = 0
        while len(self.rebuild) > 0:
            if count >= self.rebuild_per_frame:
                break
            chunk = self.rebuild.pop(0)
            chunk.set_mesh(*render.build_chunk(chunk))
            chunk.update_render_flags()
            self.build.append(chunk)
            count += 1

    def _update_visibility(self, camera):
        camera_chx = int(camera[0]) >> 4
        camera_chy = int(camera[1]) >> 4
        camera_chz = int(camera[2]) >> 4
        radius_sq = self.render_dist * self.render_dist
        visibility = []
        self.rebuild = []

        for chx in range(camera_chx - self.render_dist, camera_chx + self.render_dist):
            for chy in range(camera_chy - self.render_dist, camera_chy + self.render_dist):
                for chz in range(camera_chz - self.render_dist, camera_chz + self.render_dist):
                    dx = chx - camera_chx
                    dy = chy - camera_chy
                    dz = chz - camera_chz
                    dist_sq = dx*dx + dy*dy + dz*dz
                    if dist_sq < radius_sq:
                        chunk = self.chunks.get((chx, chy, chz), None)
                        if chunk and chunk.should_render:
                            visibility.append(chunk)
                            if chunk.needs_rebuild:
                                self.rebuild.append(chunk)
        self.visibility = visibility

    def _render(self):
        for chunk in self.visibility:
            if chunk.should_render():
                chunk.draw()
