# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pymage/sprites.py
# Compiled at: 2007-08-10 19:47:38
__doc__ = '\nDefines game sprites\n\n:Variables:\n    im : `ImageManager`\n        Global image manager\n'
import warnings, pygame
from pygame.locals import *
from pymage import resman
__author__ = 'Ross Light'
__date__ = 'May 22, 2006'
__all__ = ['getImage',
 'ImageManager',
 'im',
 'Sprite',
 'Animation']
__docformat__ = 'reStructuredText'

def getImage(image, tryIM=True):
    """
    Retrieves an image.
    
    Provides a standard way to either pass an image or a string to a function.
    
    :Parameters:
        image : string
            Name of the image resource
        tryIM : bool
            Whether to use the image manager.  If ``False`` or the image manager
            cannot find it, the image is assumed to be a path.
    :Returns: The image requested
    :ReturnType: ``pygame.Surface``
    """
    if isinstance(image, pygame.Surface):
        return image
    else:
        if tryIM:
            try:
                return im.load(image)
            except KeyError:
                pass

        return pygame.image.load(image)


class ImageManager(resman.Submanager):
    """Game image manager."""
    resourceType = resman.ImageResource

    def loadImage(self, *args, **kw):
        """
        Loads an image from disk, using a cached representation, if possible.
        
        .. Warning::
           `loadImage` method is deprecated, in favor of the new Submanager
           API.  Use `load` instead.
        
        :Parameters:
            key : string
                Name of the image resource
        :Returns: The image requested
        :ReturnType: ``pygame.Surface``
        """
        warnings.warn('loadImage is deprecated; use load.', DeprecationWarning, stacklevel=2)
        return self.load(*args, **kw)


im = ImageManager()

class Sprite(pygame.sprite.Sprite, object):
    """
    Abstract superclass for sprites.
    
    :CVariables:
        hpadding : int
            The horizontal padding for the collision box.  See `collideBox`.
        vpadding : int
            The vertical padding for the collision box.  See `collideBox`.
        angleTolerance : float
            The angle tolerance for using the initial image
        clamp : bool
            Whether to clamp the sprite to the screen boundaries
    :IVariables:
        image : ``pygame.Surface``
            The sprite's image
        rect : ``pygame.Rect``
            The sprite's position
        angle : float
            The sprite's angle (in counterclockwise degrees)
        area : ``pygame.Rect``
            The clamping area
    """
    hpadding = vpadding = 0
    angleTolerance = 0.5
    clamp = True

    def __init__(self, image=None):
        """
        Initializes a sprite.
        
        :Parameters:
            image : string
                The initial image to use
        """
        pygame.sprite.Sprite.__init__(self)
        if image is None:
            image = self.image
        self.setImage(image)
        self.rect = self.image.get_rect()
        self.area = pygame.display.get_surface().get_rect()
        self.angle = 0.0
        return

    def setImage(self, image, tryIM=True):
        """
        Changes the current image and the revert image variables.
        
        :Parameters:
            image : string
                The image name
            tryIM : bool
                Whether to use the image manager
        """
        self.image = self._image = getImage(image, tryIM).convert_alpha()

    def collideBox(self):
        """
        Returns the box used for checking with the `touches` method.
        
        By default, this uses the `hpadding` and `vpadding` to construct an
        inset box.  Override to have a different collide box.
        
        :Returns: The collision box
        :ReturnType: ``pygame.Rect``
        """
        return self.rect.inflate(self.hpadding * -2, self.vpadding * -2)

    def touches(self, other):
        """
        Returns whether the other sprite is actually touching the receiver.
        
        :Parameters:
            other : `Sprite`
                The sprite to test collision with
        :ReturnType: bool
        """
        return self.collideBox().colliderect(other.collideBox())

    def updateWithVector(self, vector, clamp=None):
        """
        Moves the sprite with the given vector.
        
        :Parameters:
            vector : `pymage.vector.Vector`
                The vector describing where to move
            clamp : bool
                Whether to clamp to `area`.  If not specified, this depends on
                the `clamp` attribute.
        """
        self.rect.x += vector.x
        self.rect.y += vector.y
        if clamp is None:
            clamp = self.clamp
        if clamp:
            self.rect = self.rect.clamp(self.area)
        return

    def rotateImage(self):
        """Rotates the sprite's image to the proper angle."""
        if abs(self.angle) < self.angleTolerance:
            self.image = self._image
        else:
            self.image = pygame.transform.rotate(self._image, self.angle)
        self.rect.size = self.image.get_size()


class Animation(Sprite):
    """
    Superclass for ambient animations.
    
    :IVariables:
        frames : list of ``pygame.Surface``s or strings
            Individual frames of the animation
        loop : bool
            Whether the animation should continuously play or whether it should
            kill itself after one run
    """
    loop = False

    def __init__(self, frames=None, loop=None):
        """
        Initializes an animation.
        
        :Parameters:
            frames : list of ``pygame.Surface``s or strings
                The individual frames of the animation.  If not specified, the
                `frames` class variable is used.
            loop : bool
                Whether the animation should continuously play or whether it
                should kill itself after one run.  If not specified, it uses
                the `loop` class variable.
        """
        if frames is None:
            frames = self.frames
        self.frames = list(frames)
        if loop is not None:
            self.loop = loop
        self.frameNum = 0
        super(Animation, self).__init__(frames[0])
        return

    def update(self):
        """
        Updates the sprite.
        
        Default implementation advances to the next frame.
        """
        self.advance()

    def advance(self):
        """Advances to the next frame and dies if it reaches the end."""
        self.frameNum += 1
        if self.frameNum >= len(self.frames):
            if self.loop:
                self.frameNum = 0
            else:
                self.kill()
        else:
            self.setImage(self.frames[self.frameNum])