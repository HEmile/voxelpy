import voxelpy.world as vpworld
import voxelpy.engine.engine as vpengine
import voxelpy.window as vpwindow

world = vpworld.World(10, 10, 10)
world.set(1, 1, 1, 2)
world.set(1, 3, 1, 2)
world.set(2, 1, 1, 2)

engine = vpengine.VoxelEngine(world)

window = vpwindow.Window(engine)
window.run()