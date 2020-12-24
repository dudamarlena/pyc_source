# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/gloo/globject.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 4016 bytes
"""
Base gloo object

On queues
---------

The queue on the GLObject can be associated with other queues. These
can be queues of other gloo objects, or of the canvas.context. Queues that are
associated behave as if they are a single queue; this allows GL commands for
two or more interdependent GL objects to be combined such that they are always
sent to the same context together.

A program associates the textures/buffers when they are set via __setitem__. A
FrameBuffer does so when assigning buffers. A program associates itself
with the canvas.context in draw(). A FrameBuffer does the same in
activate().

Example:

    prog1, prog2 = Program(), Program()
    tex1, tex2 = Texture(), Texture()

    prog1.glir.associate(tex1.glir)  # prog1 and tex1 now share a queue
    prog2.glir.associate(tex2.glir)  # prog2 and tex2 now share a queue

    # this causes prog1, tex1, and canvas.context to all share a queue:
    canvas.context.glir.associate(prog1.glir)
    # and now all objects share a single queue
    canvas.context.glir.associate(prog2.glir)
 
Now, when the canvas flushes its queue, it takes all the pending commands
from prog1, prog2, tex1, and tex2. 
"""
from .glir import GlirQueue

class GLObject(object):
    __doc__ = ' Generic GL object that represents an object on the GPU.\n    \n    When a GLObject is instantiated, it is associated with the currently\n    active Canvas, or with the next Canvas to be created if there is\n    no current Canvas\n    '
    _GLIR_TYPE = 'DummyGlirType'
    _idcount = 0

    def __init__(self):
        """ Initialize the object in the default state """
        GLObject._idcount += 1
        self._id = GLObject._idcount
        self._glir = GlirQueue()
        self._glir.command('CREATE', self._id, self._GLIR_TYPE)

    def __del__(self):
        self.delete()

    def delete(self):
        """ Delete the object from GPU memory. 

        Note that the GPU object will also be deleted when this gloo
        object is about to be deleted. However, sometimes you want to
        explicitly delete the GPU object explicitly.
        """
        if hasattr(self, '_glir'):
            self._glir.command('DELETE', self._id)
            self._glir._deletable = True
            del self._glir

    @property
    def id(self):
        """ The id of this GL object used to reference the GL object
        in GLIR. id's are unique within a process.
        """
        return self._id

    @property
    def glir(self):
        """ The glir queue for this object.
        """
        return self._glir