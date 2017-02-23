import pyglet
from pyglet.gl import *
import pymouse
import math
import numpy as np
from pyglet.window import key

fps = pyglet.clock.ClockDisplay()
class Window(pyglet.window.Window):
    def __init__(self, engine):
        super(Window, self).__init__(resizable=True, caption='voxelpy', width=1800, height=1000)
        self.engine = engine
        # self.set_mouse_visible(False)

        self.camera = np.array([5., 20., 5.])

        self.at = [1., 1., 1.]
        self.up = [0., 1., 0.]

        self.horizontal_angle = 1
        self.vertical_angle = 1
        self.mouse = pymouse.PyMouse()
        self.regMouseMove = True

        self.dt = 0
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.x_mouse_calibration = 0.01
        self.y_mouse_calibration = 0.01

        self.movement_w = 0.1
        self.movement_strafe = 0.05
        self.movement_s = 0.06

        pyglet.clock.schedule_interval(self.update, 1.0/128.0)
        pyglet.clock.set_fps_limit(128)

    def on_draw(self):
        pyglet.clock.tick()
        self.clear()
        fps.draw()
        self.setup_3D()
        self.engine.draw()

    def update(self, dt):
        self.handle_movement(dt)
        self.engine.tick(dt)

    def setup_3D(self):
        pyglet.gl.glClearColor(0, 20, 200, 1)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, self.width / float(self.height), 0.2, 50)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.camera[0], self.camera[1], self.camera[2], self.at[0], self.at[1], self.at[2], self.up[0], self.up[1], self.up[2])

    def on_mouse_motion(self, x, y, dx, dy):
        if self.regMouseMove:
            self.horizontal_angle -= self.x_mouse_calibration * dx
            self.vertical_angle += self.y_mouse_calibration * dy
            direction = np.array([math.cos(self.vertical_angle) * math.sin(self.horizontal_angle),
                                math.sin(self.vertical_angle),
                                math.cos(self.vertical_angle) * math.cos(self.horizontal_angle)])

            right = np.array([math.sin(self.horizontal_angle - 3.14 / 2), 0,
                              math.cos(self.horizontal_angle - 3.14 / 2)])

            self.at = self.camera + direction
            self.up = np.cross(right, direction)
            wx, wy = self.get_location()
            self.mouse.move(int(wx + self.width / 2), int(wy + self.height / 2))
            self.regMouseMove = False
        else:
            self.regMouseMove = True

    def handle_movement(self, dt):
        direction = self.at - self.camera
        right = np.cross(self.up, direction)
        if self.keys[key.W]:
            self.camera += self.movement_w * direction
            self.at += self.movement_w * direction
        if self.keys[key.S]:
            self.camera -= self.movement_s * direction
            self.at -= self.movement_s * direction
        if self.keys[key.A]:
            self.camera += self.movement_strafe * right
            self.at += self.movement_strafe * right
        if self.keys[key.D]:
            self.camera -= self.movement_strafe * right
            self.at -= self.movement_strafe * right

    def run(self):
        pyglet.app.run()
