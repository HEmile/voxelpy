import pyglet
from pyglet.gl import *
import math
import numpy as np
from pyglet.window import key

fps = pyglet.clock.ClockDisplay()
class Window(pyglet.window.Window):
    def __init__(self, engine):
        super(Window, self).__init__(resizable=True, caption='voxelpy', width=1800, height=1000)
        self.engine = engine

        self.camera = np.array([15., 80., 15.])

        self.at = [1., 1., 1.]
        self.up = [0., 1., 0.]

        self.horizontal_angle = 1
        self.vertical_angle = 1

        self.dt = 0
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.x_mouse_calibration = 0.01
        self.y_mouse_calibration = 0.01

        self.movement_w = 0.3
        self.movement_strafe = 0.1
        self.movement_s = 0.1

        pyglet.clock.schedule_interval(self.update, 1.0/128.0)
        pyglet.clock.set_fps_limit(128)

        super(Window, self).set_exclusive_mouse(True)

    def on_draw(self):
        pyglet.clock.tick()
        self.clear()
        self.setup_3D()
        self.setup_fog()
        self.engine.draw(0, self.camera, self.at)
        self.setup_2D()
        fps.draw()

    def update(self, dt):
        self.handle_movement(dt)
        self.engine.tick(dt)

    def setup_3D(self):
        pyglet.gl.glClearColor(0, 20, 200, 1)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, self.width / float(self.height), 0.2, 80)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.camera[0], self.camera[1], self.camera[2], self.at[0], self.at[1], self.at[2], self.up[0], self.up[1], self.up[2])

    def setup_fog(self):
        """ Configure the OpenGL fog properties.
        """
        # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
        # post-texturing color."
        glEnable(GL_FOG)
        # Set the fog color.
        glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
        # Say we have no preference between rendering speed and quality.
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        # Specify the equation used to compute the blending factor.
        glFogi(GL_FOG_MODE, GL_LINEAR)
        # How close and far away fog starts and ends. The closer the start and end,
        # the denser the fog in the fog range.
        glFogf(GL_FOG_START, 40.0)
        glFogf(GL_FOG_END, 90.0)

    def setup_2D(self):
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_mouse_motion(self, x, y, dx, dy):
        self.horizontal_angle -= self.x_mouse_calibration * dx
        self.vertical_angle += self.y_mouse_calibration * dy
        self.calculate_at()

    def handle_movement(self, dt):
        direction = self.at - self.camera
        right = np.cross(self.up, direction)
        if self.keys[key.W]:
            self.camera += self.movement_w * direction
        if self.keys[key.S]:
            self.camera -= self.movement_s * direction
        if self.keys[key.A]:
            self.camera += self.movement_strafe * right
        if self.keys[key.D]:
            self.camera -= self.movement_strafe * right
        self.calculate_at()

    def calculate_at(self):
        direction = np.array([math.cos(self.vertical_angle) * math.sin(self.horizontal_angle),
                                math.sin(self.vertical_angle),
                                math.cos(self.vertical_angle) * math.cos(self.horizontal_angle)])

        right = np.array([math.sin(self.horizontal_angle - 3.14 / 2), 0,
                          math.cos(self.horizontal_angle - 3.14 / 2)])

        self.at = self.camera + direction
        self.up = np.cross(right, direction)

    def run(self):
        pyglet.app.run()
