from threading import Thread
from pyglet.gl import *
import time

class VoxelEngine:
    def __init__(self, world, chunkmanager):
        self.world = world
        self.chunkmanager = chunkmanager

    def draw(self, dt, camera, at):
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        self.chunkmanager.draw(dt, camera, at)
        self.chunkmanager.update(dt, camera, at)
        # thread = Thread(target=self.chunkmanager.update, args=(dt, camera, at))
        # thread.start()

    def tick(self, dt):
        self.world.tick(dt)
