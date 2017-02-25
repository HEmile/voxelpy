import voxelpy.mc.colors as clrs
import pyglet

mcolors = clrs.create_colors()

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

                    rendertop = True if z == 15 else chunk[x, y, z + 1] == 0
                    renderbottom = True if z == 0 else chunk[x, y, z - 1] == 0
                    renderleft = True if x == 15 else chunk[x + 1, y, z] == 0
                    renderright = True if x == 0 else chunk[x - 1, y, z] == 0
                    renderdown = True if y == 15 else chunk[x, y + 1, z] == 0
                    renderup = True if y == 0 else chunk[x, y - 1, z] == 0
                    render = [rendertop, renderbottom, renderleft, renderright, renderdown, renderup]

                    renderamt = sum(render)

                    if voxel_type < len(mcolors) + 1:
                        color = mcolors[voxel_type - 1]
                        # if color == (256, 256, 256) or color == (255, 255, 255):
                        #     print(voxel_type)
                        #     print(color)
                        colors += [color[0], color[1], color[2]] * 4 * renderamt
                    else:
                        colors += [0, 256, 0] * 4 * renderamt

                    acc = 0
                    fc_i = 0
                    ind = 0

                    for i in range(len(render)):
                        if render[i]:
                            acc = 0
                            for j in range(i*12, i*12 + 12):
                                indice = vertices[j]
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
    return vertex_list_bf, colors