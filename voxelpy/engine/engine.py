import pyglet
from pyglet.gl import *
import numpy as np
import voxelpy.mc.colors as clrs

class VoxelEngine:
    def __init__(self, world):
        self.world = world
        self.vertex_list = None

        self.colors = clrs.create_colors()

        vertices = (
            (0, 0, 1),  # vertex 0
            (1, 0, 1),  # vertex 1
            (1, 1, 1),  # vertex 2
            (0, 1, 1),  # vertex 3
            (1, 0, 0),  # vertex 4
            (0, 0, 0),  # vertex 5
            (0, 1, 0),  # vertex 6
            (1, 1, 0),  # vertex 7
        )
        indices = (
            0, 1, 2, 3,  # top face
            4, 5, 6, 7,  # bottom face
            1, 4, 7, 2,  # left face
            5, 0, 3, 6,  # right face
            3, 2, 7, 6,  # down face
            5, 4, 1, 0   # up face
        )
        self.vertices = []
        for index in indices:
            self.vertices += vertices[index]
        normals = (
             (0, 0, 1),
             (0, 0, -1),
             (1, 0, 0),
             (-1, 0, 0),
             (0, 1, 0),
             (0, -1, 0)
        )
        self.normals = []
        for i in range(6):
            self.normals += normals[i] * 4
        self.setup_chunk()

    def setup_chunk(self):
        vertex_list_bf = []
        colors = []

        count = 0
        # Loop through each voxel
        for x in range(0, 16):
            for y in range(0, 16):
                for z in range(0, 16):
                    voxel_type = self.world.get(x, y + 60, z)
                    if voxel_type > 0:
                        # We move to draw the cube at the right position
                        # glTranslated(x, y, z)
                        if voxel_type < len(self.colors) + 1:
                            color = self.colors[voxel_type - 1]
                            if color == (256, 256, 256) or color == (0, 0, 0) or color == (255, 255, 255):
                                print(voxel_type)
                                print(color)
                            colors += [color[0], color[1], color[2]] * 24
                        else:
                            colors += [0, 256, 0] * 24

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
                        count += 1
        self.vertex_list = pyglet.graphics.vertex_list(len(vertex_list_bf) // 3,
                                                          ('v3f', vertex_list_bf), ('c3B', colors),
                                                               ('n3f', self.normals * count))

    def draw(self):
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        self.vertex_list.draw(GL_QUADS)


    def tick(self, dt):
        self.world.tick(dt)
