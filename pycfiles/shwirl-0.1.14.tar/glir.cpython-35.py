# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/gloo/glir.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 50282 bytes
"""
Implementation to execute GL Intermediate Representation (GLIR)
"""
import os, sys, re, json, weakref
from distutils.version import LooseVersion
import numpy as np
from . import gl
from ..ext.six import string_types
from ..util import logger
_internalformats = [
 gl.Enum('GL_RED', 6403),
 gl.Enum('GL_R', 8194),
 gl.Enum('GL_R8', 33321),
 gl.Enum('GL_R16', 33322),
 gl.Enum('GL_R16F', 33325),
 gl.Enum('GL_R32F', 33326),
 gl.Enum('GL_RG', 33319),
 gl.Enum('GL_RG8', 333323),
 gl.Enum('GL_RG16', 333324),
 gl.Enum('GL_RG16F', 333327),
 gl.Enum('GL_RG32F', 33328),
 gl.Enum('GL_RGB', 6407),
 gl.Enum('GL_RGB8', 32849),
 gl.Enum('GL_RGB16', 32852),
 gl.Enum('GL_RGB16F', 34843),
 gl.Enum('GL_RGB32F', 34837),
 gl.Enum('GL_RGBA', 6408),
 gl.Enum('GL_RGBA8', 32856),
 gl.Enum('GL_RGBA16', 32859),
 gl.Enum('GL_RGBA16F', 34842),
 gl.Enum('GL_RGBA32F', 34836)]
_internalformats = dict([(enum.name, enum) for enum in _internalformats])
JUST_DELETED = 'JUST_DELETED'

def as_enum(enum):
    """ Turn a possibly string enum into an integer enum.
    """
    if isinstance(enum, string_types):
        try:
            enum = getattr(gl, 'GL_' + enum.upper())
        except AttributeError:
            try:
                enum = _internalformats[('GL_' + enum.upper())]
            except KeyError:
                raise ValueError('Could not find int value for enum %r' % enum)

        return enum


class _GlirQueueShare(object):
    __doc__ = 'This class contains the actual queues of GLIR commands that are\n    collected until a context becomes available to execute the commands.\n    \n    Instances of this class are further wrapped by GlirQueue to allow the\n    underlying queues to be transparently merged when GL objects become\n    associated.\n    \n    The motivation for this design is that it allows most glir commands to be\n    added directly to their final queue (the same one used by the context),\n    which reduces the effort required at draw time to determine the complete\n    set of GL commands to be issued.\n    \n    At the same time, all GLObjects begin with their own local queue to allow\n    commands to be queued at any time, even if the GLObject has\n    not been associated yet. This works as expected even for complex topologies\n    of GL objects, when some queues may only be joined at the last possible\n    moment.\n    '

    def __init__(self, queue):
        self._commands = []
        self._verbose = False
        self._associations = weakref.WeakKeyDictionary({queue: None})

    def command(self, *args):
        """ Send a command. See the command spec at:
        https://github.com/vispy/vispy/wiki/Spec.-Gloo-IR
        """
        self._commands.append(args)

    def set_verbose(self, verbose):
        """ Set verbose or not. If True, the GLIR commands are printed
        right before they get parsed. If a string is given, use it as
        a filter.
        """
        self._verbose = verbose

    def show(self, filter=None):
        """ Print the list of commands currently in the queue. If filter is
        given, print only commands that match the filter.
        """
        for command in self._commands:
            if command[0] is None:
                pass
            else:
                if filter and command[0] != filter:
                    pass
                else:
                    t = []
                    for e in command:
                        if isinstance(e, np.ndarray):
                            t.append('array %s' % str(e.shape))
                        else:
                            if isinstance(e, str):
                                s = e.strip()
                                if len(s) > 20:
                                    s = s[:18] + '... %i lines' % (e.count('\n') + 1)
                                t.append(s)
                            else:
                                t.append(e)

                    print(tuple(t))

    def clear(self):
        """ Pop the whole queue (and associated queues) and return a
        list of commands.
        """
        commands = self._commands
        self._commands = []
        return commands

    def flush(self, parser):
        """ Flush all current commands to the GLIR interpreter.
        """
        if self._verbose:
            show = self._verbose if isinstance(self._verbose, str) else None
            self.show(show)
        parser.parse(self._filter(self.clear(), parser))

    def _filter(self, commands, parser):
        """ Filter DATA/SIZE commands that are overridden by a 
        SIZE command.
        """
        resized = set()
        commands2 = []
        for command in reversed(commands):
            if command[0] == 'SHADERS':
                convert = parser.convert_shaders()
                if convert:
                    shaders = self._convert_shaders(convert, command[2:])
                    command = command[:2] + shaders
            else:
                if command[1] in resized:
                    if command[0] in ('SIZE', 'DATA'):
                        continue
                elif command[0] == 'SIZE':
                    resized.add(command[1])
            commands2.append(command)

        return list(reversed(commands2))

    def _convert_shaders(self, convert, shaders):
        return convert_shaders(convert, shaders)


class GlirQueue(object):
    __doc__ = ' Representation of a queue of GLIR commands\n    \n    One instance of this class is attached to each context object, and\n    to each gloo object. Internally, commands are stored in a shared queue \n    object that may be swapped out and merged with other queues when\n    ``associate()`` is called.\n    \n    Upon drawing (i.e. `Program.draw()`) and framebuffer switching, the\n    commands in the queue are pushed to a parser, which is stored at\n    context.shared. The parser can interpret the commands in Python,\n    send them to a browser, etc.    \n    '

    def __init__(self):
        self._shared = _GlirQueueShare(self)

    def command(self, *args):
        """ Send a command. See the command spec at:
        https://github.com/vispy/vispy/wiki/Spec.-Gloo-IR
        """
        self._shared.command(*args)

    def set_verbose(self, verbose):
        """ Set verbose or not. If True, the GLIR commands are printed
        right before they get parsed. If a string is given, use it as
        a filter.
        """
        self._shared.set_verbose(verbose)

    def clear(self):
        """ Pop the whole queue (and associated queues) and return a
        list of commands.
        """
        return self._shared.clear()

    def associate(self, queue):
        """Merge this queue with another. 
        
        Both queues will use a shared command list and either one can be used
        to fill or flush the shared queue.
        """
        assert isinstance(queue, GlirQueue)
        if queue._shared is self._shared:
            return
        self._shared._commands.extend(queue.clear())
        self._shared._verbose |= queue._shared._verbose
        self._shared._associations[queue] = None
        for ch in queue._shared._associations:
            ch._shared = self._shared
            self._shared._associations[ch] = None

        queue._shared = self._shared

    def flush(self, parser):
        """ Flush all current commands to the GLIR interpreter.
        """
        self._shared.flush(parser)


def convert_shaders(convert, shaders):
    """ Modify shading code so that we can write code once
    and make it run "everywhere".
    """
    out = []
    if convert == 'es2':
        for isfragment, shader in enumerate(shaders):
            has_version = False
            has_prec_float = False
            has_prec_int = False
            lines = []
            for line in shader.lstrip().splitlines():
                if line.startswith('#version'):
                    has_version = True
                    continue
                    if line.startswith('precision '):
                        has_prec_float = has_prec_float or 'float' in line
                        has_prec_int = has_prec_int or 'int' in line
                    lines.append(line.rstrip())

            if not has_prec_float:
                lines.insert(has_version, 'precision highp float;')
            if not has_prec_int:
                lines.insert(has_version, 'precision highp int;')
            out.append('\n'.join(lines))

    else:
        if convert == 'desktop':
            for isfragment, shader in enumerate(shaders):
                has_version = False
                lines = []
                for line in shader.lstrip().splitlines():
                    has_version = has_version or line.startswith('#version')
                    if line.startswith('precision '):
                        line = ''
                    for prec in (' highp ', ' mediump ', ' lowp '):
                        line = line.replace(prec, ' ')

                    lines.append(line.rstrip())

                if not has_version:
                    lines.insert(0, '#version 120\n')
                out.append('\n'.join(lines))

        else:
            raise ValueError('Cannot convert shaders to %r.' % convert)
    return tuple(out)


def as_es2_command(command):
    """ Modify a desktop command so it works on es2.
    """
    if command[0] == 'FUNC':
        return (command[0],
         re.sub('^gl([A-Z])', lambda m: m.group(1).lower(), command[1])) + command[2:]
    if command[0] == 'SHADERS':
        return command[:2] + convert_shaders('es2', command[2:])
    if command[0] == 'UNIFORM':
        return command[:-1] + (command[(-1)].tolist(),)
    return command


class BaseGlirParser(object):
    __doc__ = ' Base clas for GLIR parsers that can be attached to a GLIR queue.\n    '

    def __init__(self):
        self.capabilities = dict(gl_version='Unknown', max_texture_size=None)

    def is_remote(self):
        """ Whether the code is executed remotely. i.e. gloo.gl cannot
        be used.
        """
        raise NotImplementedError()

    def convert_shaders(self):
        """ Whether to convert shading code. Valid values are 'es2' and
        'desktop'. If None, the shaders are not modified.
        """
        raise NotImplementedError()

    def parse(self, commands):
        """ Parse the GLIR commands. Or sent them away.
        """
        raise NotImplementedError()


class GlirParser(BaseGlirParser):
    __doc__ = ' A class for interpreting GLIR commands using gloo.gl\n\n    We make use of relatively light GLIR objects that are instantiated\n    on CREATE commands. These objects are stored by their id in a\n    dictionary so that commands like ACTIVATE and DATA can easily\n    be executed on the corresponding objects.\n    '

    def __init__(self):
        super(GlirParser, self).__init__()
        self._objects = {}
        self._invalid_objects = set()
        self._classmap = {'Program': GlirProgram, 
         'VertexBuffer': GlirVertexBuffer, 
         'IndexBuffer': GlirIndexBuffer, 
         'Texture1D': GlirTexture1D, 
         'Texture2D': GlirTexture2D, 
         'Texture3D': GlirTexture3D, 
         'RenderBuffer': GlirRenderBuffer, 
         'FrameBuffer': GlirFrameBuffer}
        self.env = {}

    def is_remote(self):
        return False

    def convert_shaders(self):
        if '.es' in gl.current_backend.__name__:
            return 'es2'
        else:
            return 'desktop'

    def _parse(self, command):
        """ Parse a single command.
        """
        cmd, id_, args = command[0], command[1], command[2:]
        if cmd == 'CURRENT':
            self.env.clear()
            self._gl_initialize()
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        elif cmd == 'FUNC':
            args = [as_enum(a) for a in args]
            try:
                getattr(gl, id_)(*args)
            except AttributeError:
                logger.warning('Invalid gl command: %r' % id_)

        if cmd == 'CREATE':
            if args[0] is not None:
                klass = self._classmap[args[0]]
                self._objects[id_] = klass(self, id_)
            else:
                self._invalid_objects.add(id_)
        else:
            if cmd == 'DELETE':
                ob = self._objects.get(id_, None)
                if ob is not None:
                    self._objects[id_] = JUST_DELETED
                    ob.delete()
            else:
                ob = self._objects.get(id_, None)
                if ob == JUST_DELETED:
                    return
                if ob is None:
                    if id_ not in self._invalid_objects:
                        raise RuntimeError('Cannot %s object %i because it does not exist' % (
                         cmd, id_))
                    return
                if cmd == 'DRAW':
                    ob.draw(*args)
                else:
                    if cmd == 'TEXTURE':
                        ob.set_texture(*args)
                    else:
                        if cmd == 'UNIFORM':
                            ob.set_uniform(*args)
                        else:
                            if cmd == 'ATTRIBUTE':
                                ob.set_attribute(*args)
                            else:
                                if cmd == 'DATA':
                                    ob.set_data(*args)
                                else:
                                    if cmd == 'SIZE':
                                        ob.set_size(*args)
                                    else:
                                        if cmd == 'ATTACH':
                                            ob.attach(*args)
                                        else:
                                            if cmd == 'FRAMEBUFFER':
                                                ob.set_framebuffer(*args)
                                            else:
                                                if cmd == 'SHADERS':
                                                    ob.set_shaders(*args)
                                                else:
                                                    if cmd == 'WRAPPING':
                                                        ob.set_wrapping(*args)
                                                    else:
                                                        if cmd == 'INTERPOLATION':
                                                            ob.set_interpolation(*args)
                                                        else:
                                                            logger.warning('Invalid GLIR command %r' % cmd)

    def parse(self, commands):
        """ Parse a list of commands.
        """
        to_delete = []
        for id_, val in self._objects.items():
            if val == JUST_DELETED:
                to_delete.append(id_)

        for id_ in to_delete:
            self._objects.pop(id_)

        for command in commands:
            self._parse(command)

    def get_object(self, id_):
        """ Get the object with the given id or None if it does not exist.
        """
        return self._objects.get(id_, None)

    def _gl_initialize(self):
        """ Deal with compatibility; desktop does not have sprites
        enabled by default. ES has.
        """
        if '.es' in gl.current_backend.__name__:
            pass
        else:
            GL_VERTEX_PROGRAM_POINT_SIZE = 34370
            GL_POINT_SPRITE = 34913
            gl.glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
            gl.glEnable(GL_POINT_SPRITE)
        if self.capabilities['max_texture_size'] is None:
            self.capabilities['gl_version'] = gl.glGetParameter(gl.GL_VERSION)
            self.capabilities['max_texture_size'] = gl.glGetParameter(gl.GL_MAX_TEXTURE_SIZE)
            this_version = self.capabilities['gl_version'].split(' ')[0]
            this_version = LooseVersion(this_version)
            if this_version < '2.1' and os.getenv('VISPY_IGNORE_OLD_VERSION', '').lower() != 'true':
                logger.warning('OpenGL version 2.1 or higher recommended, got %s. Some functionality may fail.' % self.capabilities['gl_version'])


def glir_logger(parser_cls, file_or_filename):
    from ..util.logs import NumPyJSONEncoder

    class cls(parser_cls):

        def __init__(self, *args, **kwargs):
            parser_cls.__init__(self, *args, **kwargs)
            if isinstance(file_or_filename, string_types):
                self._file = open(file_or_filename, 'w')
            else:
                self._file = file_or_filename
            self._file.write('[]')
            self._empty = True

        def _parse(self, command):
            parser_cls._parse(self, command)
            self._file.seek(self._file.tell() - 1)
            if self._empty:
                self._empty = False
            else:
                self._file.write(',\n')
            json.dump(as_es2_command(command), self._file, cls=NumPyJSONEncoder)
            self._file.write(']')

    return cls


class GlirObject(object):

    def __init__(self, parser, id_):
        self._parser = parser
        self._id = id_
        self._handle = -1
        self.create()

    @property
    def handle(self):
        return self._handle

    @property
    def id(self):
        return self._id

    def __repr__(self):
        return '<%s %i at 0x%x>' % (self.__class__.__name__, self.id, id(self))


class GlirProgram(GlirObject):
    UTYPEMAP = {'float': 'glUniform1fv', 
     'vec2': 'glUniform2fv', 
     'vec3': 'glUniform3fv', 
     'vec4': 'glUniform4fv', 
     'int': 'glUniform1iv', 
     'ivec2': 'glUniform2iv', 
     'ivec3': 'glUniform3iv', 
     'ivec4': 'glUniform4iv', 
     'bool': 'glUniform1iv', 
     'bvec2': 'glUniform2iv', 
     'bvec3': 'glUniform3iv', 
     'bvec4': 'glUniform4iv', 
     'mat2': 'glUniformMatrix2fv', 
     'mat3': 'glUniformMatrix3fv', 
     'mat4': 'glUniformMatrix4fv', 
     'sampler1D': 'glUniform1i', 
     'sampler2D': 'glUniform1i', 
     'sampler3D': 'glUniform1i'}
    ATYPEMAP = {'float': 'glVertexAttrib1f', 
     'vec2': 'glVertexAttrib2f', 
     'vec3': 'glVertexAttrib3f', 
     'vec4': 'glVertexAttrib4f'}
    ATYPEINFO = {'float': (1, gl.GL_FLOAT, np.float32), 
     'vec2': (2, gl.GL_FLOAT, np.float32), 
     'vec3': (3, gl.GL_FLOAT, np.float32), 
     'vec4': (4, gl.GL_FLOAT, np.float32), 
     'int': (1, gl.GL_INT, np.int32), 
     'bool': (1, gl.GL_BOOL, np.int32)}

    def create(self):
        self._handle = gl.glCreateProgram()
        self._validated = False
        self._linked = False
        self._handles = {}
        self._unset_variables = set()
        self._samplers = {}
        self._attributes = {}
        self._known_invalid = set()

    def delete(self):
        gl.glDeleteProgram(self._handle)

    def activate(self):
        """ Avoid overhead in calling glUseProgram with same arg.
        Warning: this will break if glUseProgram is used somewhere else.
        Per context we keep track of one current program.
        """
        if self._handle != self._parser.env.get('current_program', False):
            self._parser.env['current_program'] = self._handle
            gl.glUseProgram(self._handle)

    def deactivate(self):
        """ Avoid overhead in calling glUseProgram with same arg.
        Warning: this will break if glUseProgram is used somewhere else.
        Per context we keep track of one current program.
        """
        if self._parser.env.get('current_program', 0) != 0:
            self._parser.env['current_program'] = 0
            gl.glUseProgram(0)

    def set_shaders(self, vert, frag):
        """ This function takes care of setting the shading code and
        compiling+linking it into a working program object that is ready
        to use.
        """
        self._linked = False
        vert_handle = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        frag_handle = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        for code, handle, type_ in [(vert, vert_handle, 'vertex'),
         (
          frag, frag_handle, 'fragment')]:
            gl.glShaderSource(handle, code)
            gl.glCompileShader(handle)
            status = gl.glGetShaderParameter(handle, gl.GL_COMPILE_STATUS)
            if not status:
                errors = gl.glGetShaderInfoLog(handle)
                errormsg = self._get_error(code, errors, 4)
                raise RuntimeError('Shader compilation error in %s:\n%s' % (
                 type_ + ' shader', errormsg))

        gl.glAttachShader(self._handle, vert_handle)
        gl.glAttachShader(self._handle, frag_handle)
        gl.glLinkProgram(self._handle)
        if not gl.glGetProgramParameter(self._handle, gl.GL_LINK_STATUS):
            raise RuntimeError('Program linking error:\n%s' % gl.glGetProgramInfoLog(self._handle))
        gl.glDetachShader(self._handle, vert_handle)
        gl.glDetachShader(self._handle, frag_handle)
        gl.glDeleteShader(vert_handle)
        gl.glDeleteShader(frag_handle)
        self._unset_variables = self._get_active_attributes_and_uniforms()
        self._handles = {}
        self._known_invalid = set()
        self._linked = True

    def _get_active_attributes_and_uniforms(self):
        """ Retrieve active attributes and uniforms to be able to check that
        all uniforms/attributes are set by the user.
        Other GLIR implementations may omit this.
        """
        regex = re.compile('(?P<name>\\w+)\\s*(\\[(?P<size>\\d+)\\])\\s*')
        cu = gl.glGetProgramParameter(self._handle, gl.GL_ACTIVE_UNIFORMS)
        ca = gl.glGetProgramParameter(self.handle, gl.GL_ACTIVE_ATTRIBUTES)
        attributes = []
        uniforms = []
        for container, count, func in [(attributes, ca, gl.glGetActiveAttrib),
         (
          uniforms, cu, gl.glGetActiveUniform)]:
            for i in range(count):
                name, size, gtype = func(self._handle, i)
                m = regex.match(name)
                if m:
                    name = m.group('name')
                    for i in range(size):
                        container.append(('%s[%d]' % (name, i), gtype))

                else:
                    container.append((name, gtype))

        return set([v[0] for v in attributes] + [v[0] for v in uniforms])

    def _parse_error(self, error):
        """ Parses a single GLSL error and extracts the linenr and description
        Other GLIR implementations may omit this.
        """
        error = str(error)
        m = re.match('(\\d+)\\((\\d+)\\)\\s*:\\s(.*)', error)
        if m:
            return (int(m.group(2)), m.group(3))
        m = re.match('ERROR:\\s(\\d+):(\\d+):\\s(.*)', error)
        if m:
            return (int(m.group(2)), m.group(3))
        m = re.match('(\\d+):(\\d+)\\((\\d+)\\):\\s(.*)', error)
        if m:
            return (int(m.group(2)), m.group(4))
        return (None, error)

    def _get_error(self, code, errors, indentation=0):
        """Get error and show the faulty line + some context
        Other GLIR implementations may omit this.
        """
        results = []
        lines = None
        if code is not None:
            lines = [line.strip() for line in code.split('\n')]
        for error in errors.split('\n'):
            error = error.strip()
            if not error:
                pass
            else:
                linenr, error = self._parse_error(error)
                if None in (linenr, lines):
                    results.append('%s' % error)
                else:
                    results.append('on line %i: %s' % (linenr, error))
                    if linenr > 0 and linenr < len(lines):
                        results.append('  %s' % lines[(linenr - 1)])

        results = [' ' * indentation + r for r in results]
        return '\n'.join(results)

    def set_texture(self, name, value):
        """ Set a texture sampler. Value is the id of the texture to link.
        """
        if not self._linked:
            raise RuntimeError('Cannot set uniform when program has no code')
        handle = self._handles.get(name, -1)
        if handle < 0:
            if name in self._known_invalid:
                return
            handle = gl.glGetUniformLocation(self._handle, name)
            self._unset_variables.discard(name)
            self._handles[name] = handle
            if handle < 0:
                self._known_invalid.add(name)
                logger.info('Variable %s is not an active uniform' % name)
                return
        self.activate()
        tex = self._parser.get_object(value)
        if tex == JUST_DELETED:
            return
        if tex is None:
            raise RuntimeError('Could not find texture with id %i' % value)
        unit = len(self._samplers)
        if name in self._samplers:
            unit = self._samplers[name][(-1)]
        self._samplers[name] = (
         tex._target, tex.handle, unit)
        gl.glUniform1i(handle, unit)

    def set_uniform(self, name, type_, value):
        """ Set a uniform value. Value is assumed to have been checked.
        """
        if not self._linked:
            raise RuntimeError('Cannot set uniform when program has no code')
        handle = self._handles.get(name, -1)
        count = 1
        if handle < 0:
            if name in self._known_invalid:
                return
            handle = gl.glGetUniformLocation(self._handle, name)
            self._unset_variables.discard(name)
            if not type_.startswith('mat'):
                count = value.nbytes // (4 * self.ATYPEINFO[type_][0])
            if count > 1:
                for ii in range(count):
                    if '%s[%s]' % (name, ii) in self._unset_variables:
                        self._unset_variables.discard('%s[%s]' % (name, ii))

            self._handles[name] = handle
            if handle < 0:
                self._known_invalid.add(name)
                logger.info('Variable %s is not an active uniform' % name)
                return
            funcname = self.UTYPEMAP[type_]
            func = getattr(gl, funcname)
            self.activate()
            if type_.startswith('mat'):
                transpose = False
                func(handle, 1, transpose, value)
        else:
            func(handle, count, value)

    def set_attribute(self, name, type_, value):
        """ Set an attribute value. Value is assumed to have been checked.
        """
        if not self._linked:
            raise RuntimeError('Cannot set attribute when program has no code')
        handle = self._handles.get(name, -1)
        if handle < 0:
            if name in self._known_invalid:
                return
            handle = gl.glGetAttribLocation(self._handle, name)
            self._unset_variables.discard(name)
            self._handles[name] = handle
            if handle < 0:
                self._known_invalid.add(name)
                if value[0] != 0 and value[2] > 0:
                    return
                logger.info('Variable %s is not an active attribute' % name)
                return
            self.activate()
            if value[0] == 0:
                funcname = self.ATYPEMAP[type_]
                func = getattr(gl, funcname)
                self._attributes[name] = (
                 0, handle, func, value[1:])
        else:
            vbo_id, stride, offset = value
            size, gtype, dtype = self.ATYPEINFO[type_]
            vbo = self._parser.get_object(vbo_id)
            if vbo == JUST_DELETED:
                return
            if vbo is None:
                raise RuntimeError('Could not find VBO with id %i' % vbo_id)
            func = gl.glVertexAttribPointer
            args = (size, gtype, gl.GL_FALSE, stride, offset)
            self._attributes[name] = (vbo.handle, handle, func, args)

    def _pre_draw(self):
        self.activate()
        for tex_target, tex_handle, unit in self._samplers.values():
            gl.glActiveTexture(gl.GL_TEXTURE0 + unit)
            gl.glBindTexture(tex_target, tex_handle)

        for vbo_handle, attr_handle, func, args in self._attributes.values():
            if vbo_handle:
                gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_handle)
                gl.glEnableVertexAttribArray(attr_handle)
                func(attr_handle, *args)
            else:
                gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
                gl.glDisableVertexAttribArray(attr_handle)
                func(attr_handle, *args)

        if not self._validated:
            self._validated = True
            self._validate()

    def _validate(self):
        if self._unset_variables:
            logger.info('Program has unset variables: %r' % self._unset_variables)
        gl.glValidateProgram(self._handle)
        if not gl.glGetProgramParameter(self._handle, gl.GL_VALIDATE_STATUS):
            raise RuntimeError('Program validation error:\n%s' % gl.glGetProgramInfoLog(self._handle))

    def _post_draw(self):
        global USE_TEX_3D
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        if USE_TEX_3D:
            gl.glBindTexture(GL_TEXTURE_3D, 0)
            gl.glBindTexture(GL_TEXTURE_1D, 0)

    def draw(self, mode, selection):
        """ Draw program in given mode, with given selection (IndexBuffer or
        first, count).
        """
        if not self._linked:
            raise RuntimeError('Cannot draw program if code has not been set')
        gl.check_error('Check before draw')
        mode = as_enum(mode)
        if len(selection) == 3:
            id_, gtype, count = selection
            if count:
                self._pre_draw()
                ibuf = self._parser.get_object(id_)
                ibuf.activate()
                gl.glDrawElements(mode, count, as_enum(gtype), None)
                ibuf.deactivate()
        else:
            first, count = selection
        if count:
            self._pre_draw()
            gl.glDrawArrays(mode, first, count)
        gl.check_error('Check after draw')
        self._post_draw()


class GlirBuffer(GlirObject):
    _target = None
    _usage = gl.GL_DYNAMIC_DRAW

    def create(self):
        self._handle = gl.glCreateBuffer()
        self._buffer_size = 0
        self._bufferSubDataOk = False

    def delete(self):
        gl.glDeleteBuffer(self._handle)

    def activate(self):
        gl.glBindBuffer(self._target, self._handle)

    def deactivate(self):
        gl.glBindBuffer(self._target, 0)

    def set_size(self, nbytes):
        if nbytes != self._buffer_size:
            self.activate()
            gl.glBufferData(self._target, nbytes, self._usage)
            self._buffer_size = nbytes

    def set_data(self, offset, data):
        self.activate()
        nbytes = data.nbytes
        check_ati_bug = not self._bufferSubDataOk and gl.current_backend is gl.gl2 and sys.platform.startswith('win')
        if check_ati_bug:
            gl.check_error('periodic check')
        try:
            gl.glBufferSubData(self._target, offset, data)
            if check_ati_bug:
                gl.check_error('glBufferSubData')
            self._bufferSubDataOk = True
        except Exception:
            if offset == 0 and nbytes == self._buffer_size:
                gl.glBufferData(self._target, data, self._usage)
                logger.debug('Using glBufferData instead of ' + 'glBufferSubData (known ATI bug).')
            else:
                raise


class GlirVertexBuffer(GlirBuffer):
    _target = gl.GL_ARRAY_BUFFER


class GlirIndexBuffer(GlirBuffer):
    _target = gl.GL_ELEMENT_ARRAY_BUFFER


class GlirTexture(GlirObject):
    _target = None
    _types = {np.dtype(np.int8): gl.GL_BYTE, 
     np.dtype(np.uint8): gl.GL_UNSIGNED_BYTE, 
     np.dtype(np.int16): gl.GL_SHORT, 
     np.dtype(np.uint16): gl.GL_UNSIGNED_SHORT, 
     np.dtype(np.int32): gl.GL_INT, 
     np.dtype(np.uint32): gl.GL_UNSIGNED_INT, 
     np.dtype(np.float32): gl.GL_FLOAT}

    def create(self):
        self._handle = gl.glCreateTexture()
        self._shape_formats = 0

    def delete(self):
        gl.glDeleteTexture(self._handle)

    def activate(self):
        gl.glBindTexture(self._target, self._handle)

    def deactivate(self):
        gl.glBindTexture(self._target, 0)

    def _get_alignment(self, width):
        """Determines a textures byte alignment.

        If the width isn't a power of 2
        we need to adjust the byte alignment of the image.
        The image height is unimportant

        www.opengl.org/wiki/Common_Mistakes#Texture_upload_and_pixel_reads
        """
        alignments = [
         4, 8, 2, 1]
        for alignment in alignments:
            if width % alignment == 0:
                return alignment

    def set_wrapping(self, wrapping):
        self.activate()
        wrapping = [as_enum(w) for w in wrapping]
        if len(wrapping) == 3:
            GL_TEXTURE_WRAP_R = 32882
            gl.glTexParameterf(self._target, GL_TEXTURE_WRAP_R, wrapping[0])
        if len(wrapping) >= 2:
            gl.glTexParameterf(self._target, gl.GL_TEXTURE_WRAP_S, wrapping[(-2)])
        gl.glTexParameterf(self._target, gl.GL_TEXTURE_WRAP_T, wrapping[(-1)])

    def set_interpolation(self, min, mag):
        self.activate()
        min, mag = as_enum(min), as_enum(mag)
        gl.glTexParameterf(self._target, gl.GL_TEXTURE_MIN_FILTER, min)
        gl.glTexParameterf(self._target, gl.GL_TEXTURE_MAG_FILTER, mag)


GL_SAMPLER_1D = gl.Enum('GL_SAMPLER_1D', 35677)
GL_TEXTURE_1D = gl.Enum('GL_TEXTURE_1D', 3552)

class GlirTexture1D(GlirTexture):
    _target = GL_TEXTURE_1D

    def set_size(self, shape, format, internalformat):
        format = as_enum(format)
        if internalformat is not None:
            internalformat = as_enum(internalformat)
        else:
            internalformat = format
        if (shape, format, internalformat) != self._shape_formats:
            self.activate()
            self._shape_formats = (shape, format, internalformat)
            glTexImage1D(self._target, 0, internalformat, format, gl.GL_BYTE, shape[:1])

    def set_data(self, offset, data):
        self.activate()
        shape, format, internalformat = self._shape_formats
        x = offset[0]
        gtype = self._types.get(np.dtype(data.dtype), None)
        if gtype is None:
            raise ValueError('Type %r not allowed for texture' % data.dtype)
        alignment = self._get_alignment(data.shape[(-1)])
        if alignment != 4:
            gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, alignment)
        glTexSubImage1D(self._target, 0, x, format, gtype, data)
        if alignment != 4:
            gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 4)


class GlirTexture2D(GlirTexture):
    _target = gl.GL_TEXTURE_2D

    def set_size(self, shape, format, internalformat):
        format = as_enum(format)
        internalformat = format if internalformat is None else as_enum(internalformat)
        if (shape, format, internalformat) != self._shape_formats:
            self._shape_formats = (
             shape, format, internalformat)
            self.activate()
            gl.glTexImage2D(self._target, 0, internalformat, format, gl.GL_UNSIGNED_BYTE, shape[:2])

    def set_data(self, offset, data):
        self.activate()
        shape, format, internalformat = self._shape_formats
        y, x = offset
        gtype = self._types.get(np.dtype(data.dtype), None)
        if gtype is None:
            raise ValueError('Type %r not allowed for texture' % data.dtype)
        alignment = self._get_alignment(data.shape[(-2)] * data.shape[(-1)])
        if alignment != 4:
            gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, alignment)
        gl.glTexSubImage2D(self._target, 0, x, y, format, gtype, data)
        if alignment != 4:
            gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 4)


GL_SAMPLER_3D = gl.Enum('GL_SAMPLER_3D', 35679)
GL_TEXTURE_3D = gl.Enum('GL_TEXTURE_3D', 32879)
USE_TEX_3D = False

def _check_pyopengl_3D():
    """Helper to ensure users have OpenGL for 3D texture support (for now)"""
    global USE_TEX_3D
    USE_TEX_3D = True
    try:
        import OpenGL.GL as _gl
    except ImportError:
        raise ImportError('PyOpenGL is required for 3D texture support')

    return _gl


def glTexImage3D(target, level, internalformat, format, type, pixels):
    _gl = _check_pyopengl_3D()
    border = 0
    assert isinstance(pixels, (tuple, list))
    depth, height, width = pixels
    _gl.glTexImage3D(target, level, internalformat, width, height, depth, border, format, type, None)


def glTexImage1D(target, level, internalformat, format, type, pixels):
    _gl = _check_pyopengl_3D()
    border = 0
    assert isinstance(pixels, (tuple, list))
    width = pixels[0]
    _gl.glTexImage1D(target, level, internalformat, width, border, format, type, None)


def glTexSubImage1D(target, level, xoffset, format, type, pixels):
    _gl = _check_pyopengl_3D()
    width = pixels.shape[:1]
    _gl.glTexSubImage1D(target, level, xoffset, width[0], format, type, pixels)


def glTexSubImage3D(target, level, xoffset, yoffset, zoffset, format, type, pixels):
    _gl = _check_pyopengl_3D()
    depth, height, width = pixels.shape[:3]
    _gl.glTexSubImage3D(target, level, xoffset, yoffset, zoffset, width, height, depth, format, type, pixels)


class GlirTexture3D(GlirTexture):
    _target = GL_TEXTURE_3D

    def set_size(self, shape, format, internalformat):
        format = as_enum(format)
        if internalformat is not None:
            internalformat = as_enum(internalformat)
        else:
            internalformat = format
        if (shape, format, internalformat) != self._shape_formats:
            self.activate()
            self._shape_formats = (shape, format, internalformat)
            glTexImage3D(self._target, 0, internalformat, format, gl.GL_BYTE, shape[:3])

    def set_data(self, offset, data):
        self.activate()
        shape, format, internalformat = self._shape_formats
        z, y, x = offset
        gtype = self._types.get(np.dtype(data.dtype), None)
        if gtype is None:
            raise ValueError('Type not allowed for texture')
        alignment = self._get_alignment(data.shape[(-3)] * data.shape[(-2)] * data.shape[(-1)])
        if alignment != 4:
            gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, alignment)
        glTexSubImage3D(self._target, 0, x, y, z, format, gtype, data)
        if alignment != 4:
            gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 4)


class GlirRenderBuffer(GlirObject):

    def create(self):
        self._handle = gl.glCreateRenderbuffer()
        self._shape_format = 0

    def delete(self):
        gl.glDeleteRenderbuffer(self._handle)

    def activate(self):
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, self._handle)

    def deactivate(self):
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, 0)

    def set_size(self, shape, format):
        if isinstance(format, string_types):
            format = GlirFrameBuffer._formats[format][1]
        if (
         shape, format) != self._shape_format:
            self._shape_format = (
             shape, format)
            self.activate()
            gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, format, shape[1], shape[0])


class GlirFrameBuffer(GlirObject):
    _formats = {'color': (gl.GL_COLOR_ATTACHMENT0, gl.GL_RGBA), 
     'depth': (gl.GL_DEPTH_ATTACHMENT, gl.GL_DEPTH_COMPONENT16), 
     'stencil': (gl.GL_STENCIL_ATTACHMENT, gl.GL_STENCIL_INDEX8)}

    def create(self):
        self._handle = gl.glCreateFramebuffer()
        self._validated = False

    def delete(self):
        gl.glDeleteFramebuffer(self._handle)

    def set_framebuffer(self, yes):
        if yes:
            self.activate()
            if not self._validated:
                self._validated = True
                self._validate()
        else:
            self.deactivate()

    def activate(self):
        stack = self._parser.env.setdefault('fb_stack', [0])
        if stack[(-1)] != self._handle:
            stack.append(self._handle)
            gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._handle)

    def deactivate(self):
        stack = self._parser.env.setdefault('fb_stack', [0])
        while self._handle in stack:
            stack.remove(self._handle)

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, stack[(-1)])

    def attach(self, attachment, buffer_id):
        attachment = GlirFrameBuffer._formats[attachment][0]
        self.activate()
        if buffer_id == 0:
            gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, attachment, gl.GL_RENDERBUFFER, 0)
        else:
            buffer = self._parser.get_object(buffer_id)
            if buffer == JUST_DELETED:
                return
            if buffer is None:
                raise ValueError('Unknown buffer with id %i for attachement' % buffer_id)
            else:
                if isinstance(buffer, GlirRenderBuffer):
                    buffer.activate()
                    gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, attachment, gl.GL_RENDERBUFFER, buffer.handle)
                    buffer.deactivate()
                else:
                    if isinstance(buffer, GlirTexture2D):
                        buffer.activate()
                        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, attachment, gl.GL_TEXTURE_2D, buffer.handle, 0)
                        buffer.deactivate()
                    else:
                        raise ValueError('Invalid attachment: %s' % type(buffer))
        self._validated = False
        self.deactivate()

    def _validate(self):
        res = gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER)
        if res == gl.GL_FRAMEBUFFER_COMPLETE:
            return
        _bad_map = {0: 'Target not equal to GL_FRAMEBUFFER', 
         gl.GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT: 'FrameBuffer attachments are incomplete.', 
         
         gl.GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT: 'No valid attachments in the FrameBuffer.', 
         
         gl.GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS: 'attachments do not have the same width and height.', 
         
         gl.GL_FRAMEBUFFER_UNSUPPORTED: 'Combination of internal formats used by attachments is not supported.'}
        raise RuntimeError(_bad_map.get(res, 'Unknown framebuffer error: %r.' % res))