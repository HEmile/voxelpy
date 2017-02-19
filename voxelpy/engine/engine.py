import pyglet
from pyglet.gl import *


class VoxelEngine:
    def __init__(self, world):
        self.world = world

        self.colors = (
            (107, 83, 28),  # dirt
            (18, 124, 39),  # grass
            (168, 142, 95),  # wood
            (88, 181, 74),  # leaves
        )

        self.vertices = (
            0, 0, 0,  # vertex 0
            0, 0, 1,  # vertex 1
            0, 1, 0,  # vertex 2
            0, 1, 1,  # vertex 3
            1, 0, 0,  # vertex 4
            1, 0, 1,  # vertex 5
            1, 1, 0,  # vertex 6
            1, 1, 1,  # vertex 7
        )
        self.indices = (
            0, 1, 3, 2,  # top face
            4, 5, 7, 6,  # bottom face
            0, 4, 6, 2,  # left face
            1, 5, 7, 3,  # right face
            0, 1, 5, 4,  # down face
            2, 3, 7, 6,  # up face
        )

    def draw(self):
        w, h, d = self.world.w, self.world.h, self.world.d
        voxels = self.world.voxels
        # Loop through each voxel
        for x in range(w):
            for y in range(h):
                for z in range(d):
                    voxel_type = voxels[x][y][z]
                    if voxel_type != 0:
                        # We move to draw the cube at the right position
                        glTranslated(x, y, z)
                        glColor3ub(*self.colors[voxel_type - 1])
                        # Draw the cube
                        pyglet.graphics.draw_indexed(8, GL_QUADS,
                                                     self.indices, ('v3i', self.vertices))
                        # Restore the matrix to its original state
                        glTranslated(-x, -y, -z)

    def tick(self, dt):
        self.world.tick(dt)
