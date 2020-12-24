# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/transforms/base_transform.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 7434 bytes
"""
API Issues to work out:

  - MatrixTransform and STTransform both have 'scale' and 'translate'
    attributes, but they are used in very different ways. It would be nice
    to keep this consistent, but how?

  - Need a transform.map_rect function that returns the bounding rectangle of
    a rect after transformation. Non-linear transforms might need to work
    harder at this, but we can provide a default implementation that
    works by mapping a selection of points across a grid within the original
    rect.
"""
from __future__ import division
from ..shaders import Function
from ...util.event import EventEmitter

class BaseTransform(object):
    __doc__ = '\n    BaseTransform is a base class that defines a pair of complementary\n    coordinate mapping functions in both python and GLSL.\n\n    All BaseTransform subclasses define map() and imap() methods that map\n    an object through the forward or inverse transformation, respectively.\n\n    The two class variables glsl_map and glsl_imap are instances of\n    shaders.Function that define the forward- and inverse-mapping GLSL\n    function code.\n\n    Optionally, an inverse() method returns a new transform performing the\n    inverse mapping.\n\n    Note that although all classes should define both map() and imap(), it\n    is not necessarily the case that imap(map(x)) == x; there may be instances\n    where the inverse mapping is ambiguous or otherwise meaningless.\n\n    '
    glsl_map = None
    glsl_imap = None
    Linear = None
    Orthogonal = None
    NonScaling = None
    Isometric = None

    def __init__(self):
        self._inverse = None
        self._dynamic = False
        self.changed = EventEmitter(source=self, type='transform_changed')
        if self.glsl_map is not None:
            self._shader_map = Function(self.glsl_map)
        if self.glsl_imap is not None:
            self._shader_imap = Function(self.glsl_imap)

    def map(self, obj):
        """
        Return *obj* mapped through the forward transformation.

        Parameters
        ----------
            obj : tuple (x,y) or (x,y,z)
                  array with shape (..., 2) or (..., 3)
        """
        raise NotImplementedError()

    def imap(self, obj):
        """
        Return *obj* mapped through the inverse transformation.

        Parameters
        ----------
            obj : tuple (x,y) or (x,y,z)
                  array with shape (..., 2) or (..., 3)
        """
        raise NotImplementedError()

    @property
    def inverse(self):
        """ The inverse of this transform. 
        """
        if self._inverse is None:
            self._inverse = InverseTransform(self)
        return self._inverse

    @property
    def dynamic(self):
        """Boolean flag that indicates whether this transform is expected to 
        change frequently.
        
        Transforms that are flagged as dynamic will not be collapsed in 
        ``ChainTransform.simplified``. This allows changes to the transform
        to propagate through the chain without requiring the chain to be
        re-simplified.
        """
        return self._dynamic

    @dynamic.setter
    def dynamic(self, d):
        self._dynamic = d

    def shader_map(self):
        """
        Return a shader Function that accepts only a single vec4 argument
        and defines new attributes / uniforms supplying the Function with
        any static input.
        """
        return self._shader_map

    def shader_imap(self):
        """
        see shader_map.
        """
        return self._shader_imap

    def _shader_object(self):
        """ This method allows transforms to be assigned directly to shader
        template variables. 
        
        Example::
        
            code = 'void main() { gl_Position = $transform($position); }'
            func = shaders.Function(code)
            tr = STTransform()
            func['transform'] = tr  # use tr's forward mapping for $function
        """
        return self.shader_map()

    def update(self, *args):
        """
        Called to inform any listeners that this transform has changed.
        """
        self.changed(*args)

    def __mul__(self, tr):
        """
        Transform multiplication returns a new transform that is equivalent to
        the two operands performed in series.

        By default, multiplying two Transforms `A * B` will return
        ChainTransform([A, B]). Subclasses may redefine this operation to
        return more optimized results.

        To ensure that both operands have a chance to simplify the operation,
        all subclasses should follow the same procedure. For `A * B`:

        1. A.__mul__(B) attempts to generate an optimized transform product.
        2. If that fails, it must:

               * return super(A).__mul__(B) OR
               * return NotImplemented if the superclass would return an
                 invalid result.

        3. When BaseTransform.__mul__(A, B) is called, it returns 
           NotImplemented, which causes B.__rmul__(A) to be invoked.
        4. B.__rmul__(A) attempts to generate an optimized transform product.
        5. If that fails, it must:

               * return super(B).__rmul__(A) OR
               * return ChainTransform([B, A]) if the superclass would return
                 an invalid result.

        6. When BaseTransform.__rmul__(B, A) is called, ChainTransform([A, B])
           is returned.
        """
        return tr.__rmul__(self)

    def __rmul__(self, tr):
        return ChainTransform([tr, self])

    def __repr__(self):
        return '<%s at 0x%x>' % (self.__class__.__name__, id(self))


class InverseTransform(BaseTransform):

    def __init__(self, transform):
        BaseTransform.__init__(self)
        self._inverse = transform
        self.map = transform.imap
        self.imap = transform.map

    @property
    def Linear(self):
        return self._inverse.Linear

    @property
    def Orthogonal(self):
        return self._inverse.Orthogonal

    @property
    def NonScaling(self):
        return self._inverse.NonScaling

    @property
    def Isometric(self):
        return self._inverse.Isometric

    @property
    def shader_map(self):
        return self._inverse.shader_imap

    @property
    def shader_imap(self):
        return self._inverse.shader_map

    def __repr__(self):
        return '<Inverse of %r>' % repr(self._inverse)


from .chain import ChainTransform