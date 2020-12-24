# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\ScreenPositionServer.py
# Compiled at: 2009-07-15 18:56:28
"""Handle 3D perspective projection (server-side)"""
import Pyro.core, sys, os, string, VisionEgg.Core, VisionEgg.FlowControl, VisionEgg.SphereMap, VisionEgg.Textures, VisionEgg.PyroHelpers
from VisionEgg.PyroApps.ScreenPositionGUI import ScreenPositionParameters

class ScreenPositionMetaController(Pyro.core.ObjBase):
    """Encapsulates all parameters controlling screen position"""

    def __init__(self, presentation, projection):
        Pyro.core.ObjBase.__init__(self)
        self.meta_params = ScreenPositionParameters()
        if not isinstance(presentation, VisionEgg.FlowControl.Presentation):
            raise ValueError('Expecting instance of VisionEgg.FlowControl.Presentation')
        if not isinstance(projection, VisionEgg.Core.PerspectiveProjection):
            raise ValueError('Expecting instance of VisionEgg.Core.PerspectiveProjection')
        self.p = presentation
        self.proj = projection

    def get_parameters(self):
        return self.meta_params

    def set_parameters(self, new_parameters):
        if isinstance(new_parameters, ScreenPositionParameters):
            self.meta_params = new_parameters
        else:
            raise ValueError('Argument to set_parameters must be instance of ScreenPositionParameters')
        self.update()

    def update(self):
        left = self.meta_params.left
        right = self.meta_params.right
        bottom = self.meta_params.bottom
        top = self.meta_params.top
        near = self.meta_params.near
        far = self.meta_params.far
        eye = (
         self.meta_params.eye[0],
         self.meta_params.eye[1],
         self.meta_params.eye[2])
        center = (
         self.meta_params.center[0],
         self.meta_params.center[1],
         self.meta_params.center[2])
        up = (
         self.meta_params.up[0],
         self.meta_params.up[1],
         self.meta_params.up[2])
        temp = VisionEgg.Core.PerspectiveProjection(left, right, bottom, top, near, far)
        temp.look_at(eye, center, up)
        self.proj.parameters.matrix = temp.get_matrix()

    def go(self):
        self.p.parameters.enter_go_loop = 1

    def quit_server(self):
        self.p.parameters.quit = 1


if __name__ == '__main__':
    pyro_server = VisionEgg.PyroHelpers.PyroServer()
    screen = VisionEgg.Core.Screen.create_default()
    filename = os.path.join(VisionEgg.config.VISIONEGG_SYSTEM_DIR, 'data/az_el.png')
    texture = VisionEgg.Textures.Texture(filename)
    sphere_map = VisionEgg.SphereMap.SphereMap(texture=texture, shrink_texture_ok=1, stacks=100, slices=100)
    temp = ScreenPositionParameters()
    projection = VisionEgg.Core.PerspectiveProjection(temp.left, temp.right, temp.bottom, temp.top, temp.near, temp.far)
    viewport = VisionEgg.Core.Viewport(screen=screen, stimuli=[sphere_map], projection=projection)
    p = VisionEgg.FlowControl.Presentation(viewports=[viewport])
    projection_controller = ScreenPositionMetaController(p, projection)
    pyro_server.connect(projection_controller, 'projection_controller')
    p.add_controller(None, None, pyro_server.create_listener_controller())
    p.run_forever()