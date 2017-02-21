import voxelpy.world as vpworld
import voxelpy.engine.engine as vpengine
import voxelpy.window as vpwindow
import voxelpy.minecraft as mc
import pickle

with open("../data/chunks.chk", 'rb') as file:
    chunks = pickle.load(file)
#
# world = vpworld.World(10, 10, 10)
# world.set(1, 1, 1, 2)
# world.set(1, 3, 1, 2)
# world.set(2, 1, 1, 2)
#
world = vpworld.ChunkWorld(chunks)
engine = vpengine.VoxelEngine(world)

window = vpwindow.Window(engine)
window.run()