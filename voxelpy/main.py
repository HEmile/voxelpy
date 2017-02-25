import voxelpy.world as vpworld
import voxelpy.engine.engine as vpengine
import voxelpy.window as vpwindow
import voxelpy.minecraft as mc
import voxelpy.engine.chunk as chunk
import pickle

chunks = mc.load_region('../regions/r.0.0.mca')
with open("../data/chunks.chk", 'wb') as file:
    pickle.dump(chunks, file)

# with open("../data/chunks.chk", 'rb') as file:
#     chunks = pickle.load(file)
#
# chnkmngr = chunk.ChunkManager(chunks)
# world = vpworld.ChunkWorld(chnkmngr)
# engine = vpengine.VoxelEngine(world, chnkmngr)
#
# window = vpwindow.Window(engine)
# window.run()

