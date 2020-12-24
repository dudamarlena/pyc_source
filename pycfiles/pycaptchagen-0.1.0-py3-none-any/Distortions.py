# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Captcha/Visual/Distortions.py
# Compiled at: 2006-02-05 00:25:47
__doc__ = ' Captcha.Visual.Distortions\n\nDistortion layers for visual CAPTCHAs\n'
from Captcha.Visual import Layer
import ImageDraw, Image, random, math

class WigglyBlocks(Layer):
    """Randomly select and shift blocks of the image"""
    __module__ = __name__

    def __init__(self, blockSize=16, sigma=0.01, iterations=300):
        self.blockSize = blockSize
        self.sigma = sigma
        self.iterations = iterations
        self.seed = random.random()

    def render(self, image):
        r = random.Random(self.seed)
        for i in xrange(self.iterations):
            bx = int(r.uniform(0, image.size[0] - self.blockSize))
            by = int(r.uniform(0, image.size[1] - self.blockSize))
            block = image.crop((bx, by, bx + self.blockSize - 1, by + self.blockSize - 1))
            mx = int(math.floor(r.normalvariate(0, self.sigma)))
            my = int(math.floor(r.normalvariate(0, self.sigma)))
            image.paste(block, (bx + mx, by + my))


class WarpBase(Layer):
    """Abstract base class for image warping. Subclasses define a
       function that maps points in the output image to points in the input image.
       This warping engine runs a grid of points through this transform and uses
       PIL's mesh transform to warp the image.
       """
    __module__ = __name__
    filtering = Image.BILINEAR
    resolution = 10

    def getTransform(self, image):
        """Return a transformation function, subclasses should override this"""
        return lambda x, y: (
         x, y)

    def render(self, image):
        r = self.resolution
        xPoints = image.size[0] / r + 2
        yPoints = image.size[1] / r + 2
        f = self.getTransform(image)
        xRows = []
        yRows = []
        for j in xrange(yPoints):
            xRow = []
            yRow = []
            for i in xrange(xPoints):
                (x, y) = f(i * r, j * r)
                x = max(0, min(image.size[0] - 1, x))
                y = max(0, min(image.size[1] - 1, y))
                xRow.append(x)
                yRow.append(y)

            xRows.append(xRow)
            yRows.append(yRow)

        mesh = []
        for j in xrange(yPoints - 1):
            for i in xrange(xPoints - 1):
                mesh.append(((i * r, j * r, (i + 1) * r, (j + 1) * r), (xRows[j][i], yRows[j][i], xRows[(j + 1)][i], yRows[(j + 1)][i], xRows[(j + 1)][(i + 1)], yRows[(j + 1)][(i + 1)], xRows[j][(i + 1)], yRows[j][(i + 1)])))

        return image.transform(image.size, Image.MESH, mesh, self.filtering)


class SineWarp(WarpBase):
    """Warp the image using a random composition of sine waves"""
    __module__ = __name__

    def __init__(self, amplitudeRange=(
 3, 6.5), periodRange=(0.04, 0.1)):
        self.amplitude = random.uniform(*amplitudeRange)
        self.period = random.uniform(*periodRange)
        self.offset = (random.uniform(0, math.pi * 2 / self.period), random.uniform(0, math.pi * 2 / self.period))

    def getTransform(self, image):
        return lambda x, y, a=self.amplitude, p=self.period, o=self.offset: (math.sin((y + o[0]) * p) * a + x, math.sin((x + o[1]) * p) * a + y)