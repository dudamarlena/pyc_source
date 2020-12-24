# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/ripl/slide2png.py
# Compiled at: 2017-03-01 09:16:28
# Size of source mod 2**32: 6095 bytes
"""
Create slides for a slideshow

Each slide is a heading plus a list of rows.

Each row is a list of text strings or image names.

This uses PIL to create an image for each slide.
"""
from PIL import Image, ImageDraw, ImageFont
from . import imagefind, image2exif
FONT = '/usr/share/fonts/TTF/Vera.ttf'
FONTSIZE = 36
WIDTH = 1024
HEIGHT = 768

class Slide2png:

    def __init__(self):
        self.pos = 0
        self.padding = 10
        self.cache = 'show'
        self.font = ImageFont.truetype(FONT, FONTSIZE)
        self.finder = imagefind.ImageFind()

    def interpret(self, msg):
        """ Load input """
        slides = msg.get('slides', [])
        self.cache = msg.get('folder', '.')
        self.gallery = msg.get('gallery', ['..'])
        self.finder.interpret(dict(galleries=(self.gallery)))
        slides = [slide for slide in slides]
        logname = msg.get('logname')
        if logname:
            self.write_slide_list(logname, slides)
        for slide in slides:
            image = self.draw_slide(slide)
            heading = slide['heading']['text']
            filename = self.get_image_name(heading)
            self.cache_image(filename, image)

    def write_slide_list(self, logname, slides):
        """ Write list of slides to logfile """
        with open('%s/%s' % (self.cache, logname), 'w') as (logfile):
            for slide in slides:
                heading = slide['heading']['text']
                filename = self.get_image_name(heading)
                print(('%s,%d' % (filename, slide.get('time', 0))), file=logfile)

    def draw_slide(self, slide):
        """ Return layout information for slide """
        image = Image.new('RGB', (WIDTH, HEIGHT), 'black')
        draw = ImageDraw.Draw(image)
        draw.font = self.font
        self.draw_slide_text(draw, slide)
        self.draw_slide_images(draw, slide, image)
        return image

    def draw_slide_text(self, draw, slide):
        heading = slide['heading']
        rows = slide['rows']
        left, top = heading['top'], heading['left']
        draw.text((left, top), (heading['text']), fill='gold')
        print(heading['text'])
        for row in rows:
            for item in row['items']:
                top, left = item['top'], item['left']
                text = item.get('text')
                if not text:
                    pass
                else:
                    draw.text((left, top), text, fill='white')

    def draw_slide_images(self, draw, slide, image):
        heading = slide['heading']
        rows = slide['rows']
        left, top = heading['top'], heading['left']
        for row in rows:
            for item in row['items']:
                top, left = item['top'], item['left']
                image_file = item.get('image')
                if not image_file:
                    pass
                else:
                    source = self.find_image(item)
                    if source:
                        print('Using {} for {}'.format(source, item['image']))
                        self.draw_image(image, item, source)
                    else:
                        draw.text((left, top), image_file, fill='white')

        print()

    def find_image(self, item):
        """ Try and find the image file 

        some magic here would be good.

        FIXME move elsewhere and make so everyone can use.

        interpreter that finds things?
        """
        image_file = item['image']
        return self.finder.find_image(image_file)

    def rotate(self, img):
        """ Rotate image if exif says it needs it """
        try:
            exif = image2exif.get_exif(img)
        except AttributeError:
            return img
        else:
            orientation = exif.get('Orientation', 1)
            landscape = img.height < img.width
            if orientation == 6 and landscape:
                print('ROTATING')
                return img.rotate(-90)
            else:
                return img

    def draw_image(self, image, item, source):
        """ Add an image to the image """
        top, left = item['top'], item['left']
        width, height = item['width'], item['height']
        image_file = item['image']
        img = Image.open(source)
        img = self.rotate(img)
        iwidth, iheight = img.size
        wratio = width / iwidth
        hratio = height / iheight
        ratio = min(wratio, hratio)
        img = img.resize((int(iwidth * ratio),
         int(iheight * ratio)), Image.ANTIALIAS)
        iwidth, iheight = img.size
        top += (height - iheight) // 2
        left += (width - iwidth) // 2
        image.paste(img, (left, top))

    def slugify(self, name):
        """ Turn name into a slug suitable for an image file name """
        slug = ''
        last = ''
        for char in name.replace('#', '').lower().strip():
            if not char.isalnum():
                char = '_'
            if last == '_':
                if char == '_':
                    continue
            slug += char
            last = char

        return slug

    def cache_image(self, name, image):
        with open(name, 'w') as (slide):
            image.save(name)
        return name

    def get_image_name(self, label):
        return '%s/%s.png' % (self.cache, self.slugify(label))