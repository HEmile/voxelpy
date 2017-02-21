import pyglet
from pyglet.gl import *
import numpy as np

class VoxelEngine:
    def __init__(self, world):
        self.world = world
        self.vertex_list = None

        self.colors = (
            (70, 70, 70),
            (18, 124, 39),  # grass
            (107, 83, 28),  # dirt
            (70, 70, 70),
            (168, 142, 95),  # wood
            (88, 181, 74),  # leaves
            (0, 0, 0),  # bedrock
            (0, 256, 0),  # water
            (0, 256, 0),  # water
            (256, 0, 0),  # lava
            (256, 0, 0),  # lava
            (197, 172, 110),  # sand
            (90, 53, 18),  # gravel
            (90, 53, 18),  # gravel
            (90, 53, 18),  # gravel
            (90, 53, 18),  # gravel
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

        self.setup_chunk()

    def setup_chunk(self):
        vertex_list_bf = []
        colors = []
        indices = []

        count = 0
        # Loop through each voxel
        for x in range(0, 16):
            for y in range(0, 16):
                for z in range(0, 16):
                    voxel_type = self.world.get(x, y + 50, z)
                    if voxel_type > 0:
                        # We move to draw the cube at the right position
                        # glTranslated(x, y, z)
                        if voxel_type < 19:
                            color = self.colors[voxel_type - 1]
                            colors += [color[0], color[1], color[2]] * 8
                        else:
                            colors += [0, 256, 0] * 8

                        acc = 0
                        for indice in self.vertices:
                            if acc == 0:
                                indice += x
                                acc += 1
                            elif acc == 1:
                                indice += y
                                acc += 1
                            elif acc == 2:
                                indice += z
                                acc = 0
                            vertex_list_bf.append(indice)

                        for indice in self.indices:
                            indices.append(indice + 8*count)
                        count += 1
                        # Restore the matrix to its original state
                        # glTranslated(-x, -y, -z)
        self.vertex_list = pyglet.graphics.vertex_list_indexed(len(vertex_list_bf) // 3, indices,
                                                          ('v3f', vertex_list_bf), ('c3B', colors))

    def draw(self):
        self.vertex_list.draw(GL_QUADS)


    def tick(self, dt):
        self.world.tick(dt)
