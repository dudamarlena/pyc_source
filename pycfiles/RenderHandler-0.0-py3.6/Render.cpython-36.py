# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\RenderHandler\Render.py
# Compiled at: 2018-06-03 23:39:31
# Size of source mod 2**32: 10475 bytes
import ModernGL, os, numpy as np, glob2, cv2, shutil
from ShapeNetHandler.custom_objloader import Obj
from PIL import Image
from pyrr import Matrix44

class ModernGL_Wrapper(object):

    def __init__(self, params):
        self._ModernGL_Wrapper__init_params(params)
        self._ModernGL_Wrapper__init_program()

    def __init_params(self, params):
        self.VIEWPORT_WIDTH = params['viewport_width']
        self.VIEWPORT_HEIGHT = params['viewport_height']
        self._background_params = params['background']
        self._object_params = params['object']
        self._shader_dir = params['shader_dir']

    def __load_shaders(self):
        vertex_shader_path = os.path.join(self._shader_dir, 'shader.vert')
        fragment_shader_path = os.path.join(self._shader_dir, 'shader.frag')
        with open(vertex_shader_path) as (infile):
            vertex_shader_source = infile.read()
        with open(fragment_shader_path) as (infile):
            fragment_shader_source = infile.read()
        self.vertex_shader = self._ctx.vertex_shader(vertex_shader_source)
        self.fragment_shader = self._ctx.fragment_shader(fragment_shader_source)

    def __init_program(self):
        self._ctx = ModernGL.create_standalone_context()
        self._ctx.enable(ModernGL.DEPTH_TEST)
        self._ModernGL_Wrapper__load_shaders()
        self._program = self._ctx.program([self.vertex_shader, self.fragment_shader])
        self._fbo = self._ctx.framebuffer(self._ctx.renderbuffer((self.VIEWPORT_WIDTH, self.VIEWPORT_HEIGHT)), self._ctx.depth_renderbuffer((self.VIEWPORT_WIDTH, self.VIEWPORT_HEIGHT)))
        self._fbo.use()

    def __generate_transforms_and_rotations(self, render_point, scale_factor=2, translate=None):

        def generate_rotation(theta, azimuth, elevation):
            return Matrix44.from_z_rotation(theta) * Matrix44.from_y_rotation(azimuth) * Matrix44.from_x_rotation(elevation)

        def get_transform(rotation_matrix44, scale_factor, translate):
            scale_matrix44 = Matrix44.from_scale(np.ones(3) * scale_factor)
            transform_matrix44 = rotation_matrix44 * scale_matrix44
            if translate is not None:
                translate_matrix44 = np.zeros((4, 4))
                translate_matrix44[:3, 3] = translate
                transform_matrix44 = transform_matrix44 + translate_matrix44
            return transform_matrix44

        rotation_matrix44 = generate_rotation(*render_point)
        transform_matrix44 = get_transform(rotation_matrix44, scale_factor, translate)
        rotation_matrix33 = rotation_matrix44[:3, :3]
        return (
         transform_matrix44, rotation_matrix33)

    def __get_ambient_light(self, source='object'):
        ambient_lighting_params = self.__dict__['_{}_params'.format(source)]['lighting']['ambient']
        ambient_light_val = np.random.uniform(ambient_lighting_params['min'], ambient_lighting_params['max']) if ambient_lighting_params['random'] else ambient_lighting_params['default']
        return ambient_light_val

    def __render_background(self, train_or_test_set):
        translate_vec = [
         0, 0, 0, 1]
        scale = 1
        background_transform = np.identity(4) * scale
        background_transform[:, 3] = translate_vec
        ambient_light_val = self._ModernGL_Wrapper__get_ambient_light(source='background')
        self._program.uniforms['Transform'].write(background_transform.astype('float32').tobytes())
        self._program.uniforms['AmbientLight'].value = ambient_light_val
        self._program.uniforms['UseTexture'].value = True
        self._program.uniforms['NormColoring'].value = False
        background_textures = self._background_params['preloaded_textures'][train_or_test_set]
        while True:
            random_texture_i = np.random.randint(len(background_textures))
            random_preloaded_background = background_textures[random_texture_i]
            try:
                texture_image, texture_size, texture_bytes = random_preloaded_background
                background_texture = self._ctx.texture(size=texture_size, components=3, data=texture_bytes)
            except:
                print('\n\n**Background Render Error!')
                print('See Render.py in RenderHandler, lines 120-122')
            else:
                background_texture.build_mipmaps()
            break

        background_model = Obj.open('{}/model/background_plane.obj'.format(self._background_params['background_obj_dir']))
        packed_background = background_model.pack('vx vy vz nx ny nz tx ty tz')
        background_VBO = self._ctx.buffer(packed_background)
        background_VAO = self._ctx.simple_vertex_array(self._program, background_VBO, ['in_vert', 'in_norm', 'in_text'])
        background_texture.use()
        background_VAO.render()
        background_VAO.release()
        background_VBO.release()
        background_texture.release()

    def __render_object(self, model_object, render_point, transform44):
        packed_model, model_textures = model_object
        ambient_light_val = self._ModernGL_Wrapper__get_ambient_light(source='object')
        self._program.uniforms['Transform'].write(transform44.astype('float32').tobytes())
        self._program.uniforms['AmbientLight'].value = ambient_light_val
        self._program.uniforms['Color'].value = self._object_params['color']
        self._program.uniforms['UseTexture'].value = self._use_texture
        self._program.uniforms['NormColoring'].value = self._norm_coloring
        object_textures = []
        if model_textures is not None:
            for model_texture in model_textures:
                texture_image, texture_size, texture_bytes = model_texture
                try:
                    object_texture = self._ctx.texture(texture_size, 3, texture_bytes)
                    object_texture.build_mipmaps()
                    object_textures.append(object_texture)
                except:
                    continue

        else:
            with Image.open('textures/wood.jpg') as (im):
                texture_image = im
                texture_size = im.size
                texture_bytes = im.tobytes()
            texture = self._ctx.texture(texture_size, 3, texture_bytes)
            texture.build_mipmaps()
            object_textures.append(texture)
        object_VBO = self._ctx.buffer(packed_model)
        object_VAO = self._ctx.simple_vertex_array(self._program, object_VBO, ['in_vert', 'in_norm', 'in_text'])
        for object_texture in object_textures:
            object_texture.use()

        object_VAO.render()
        object_VAO.release()
        object_VBO.release()
        for object_texture in object_textures:
            object_texture.release()

    def render(self, model_object, render_point, source_light_position, scale_factor, use_texture=False, texture_background=True, train_or_test_set='training'):
        self._use_texture = use_texture
        self._texture_background = texture_background
        self._norm_coloring = False if self._use_texture else True
        (self._ctx.clear)(*self._background_params['color'])
        transform44, rotation33 = self._ModernGL_Wrapper__generate_transforms_and_rotations(render_point, scale_factor)
        self._program.uniforms['NormalTransform'].write(rotation33.astype('float32').tobytes())
        self._program.uniforms['LightPos'].value = source_light_position
        if self._texture_background:
            self._ModernGL_Wrapper__render_background(train_or_test_set)
        self._ModernGL_Wrapper__render_object(model_object, render_point, transform44)

    def get_image(self, bytes_only=False):
        """
            # TODO: Look into opencv2 for faster alternative
            # Start here: https://stackoverflow.com/questions/17170752/python-opencv-load-image-from-byte-string
            # And here for fun: https://www.codingforentrepreneurs.com/blog/install-opencv-3-for-python-on-windows/
        """
        pixels = self._fbo.read(components=3, alignment=1)
        image = Image.frombytes('RGB', self._fbo.size, pixels).transpose(Image.FLIP_TOP_BOTTOM)
        return image