import voxelpy.mc.colors as clrs
import pyglet

colors = clrs.create_colors()

_vertices = (
    (0, 0, 1),  # vertex 0
    (1, 0, 1),  # vertex 1
    (1, 1, 1),  # vertex 2
    (0, 1, 1),  # vertex 3
    (1, 0, 0),  # vertex 4
    (0, 0, 0),  # vertex 5
    (0, 1, 0),  # vertex 6
    (1, 1, 0),  # vertex 7
)
_indices = (
    0, 1, 2, 3,  # top face
    4, 5, 6, 7,  # bottom face
    1, 4, 7, 2,  # left face
    5, 0, 3, 6,  # right face
    3, 2, 7, 6,  # down face
    5, 4, 1, 0   # up face
)
vertices = []
for index in _indices:
    vertices += _vertices[index]
_normals = (
     (0, 0, 1),
     (0, 0, -1),
     (1, 0, 0),
     (-1, 0, 0),
     (0, 1, 0),
     (0, -1, 0)
)
normals = []
for i in range(6):
    normals += _normals[i] * 4


def build_chunk(chunk):
    vertex_list_bf = []
    colors = []
    offsetx = chunk.chunkX << 4
    offsety = chunk.chunkY << 4
    offsetz = chunk.chunkZ << 4

    count = 0
    # Loop through each voxel
    for x in range(0, 16):
        nx = x + offsetx
        for y in range(0, 16):
            ny = y + offsety
            for z in range(0, 16):
                voxel_type = chunk[x, y, z]
                if voxel_type > 0:
                    nz = z + offsetz
                    if voxel_type < len(colors) + 1:
                        color = colors[voxel_type - 1]
                        if color == (256, 256, 256) or color == (0, 0, 0) or color == (255, 255, 255):
                            print(voxel_type)
                            print(color)
                        colors += [color[0], color[1], color[2]] * 24
                    else:
                        colors += [0, 256, 0] * 24

                    acc = 0
                    for indice in vertices:
                        if acc == 0:
                            indice += nx
                            acc += 1
                        elif acc == 1:
                            indice += ny
                            acc += 1
                        elif acc == 2:
                            indice += nz
                            acc = 0
                        vertex_list_bf.append(indice)
                    count += 1
    return pyglet.graphics.vertex_list(len(vertex_list_bf) // 3,
                                              ('v3f', vertex_list_bf), ('c3B', colors),
                                              ('n3f', normals * count))