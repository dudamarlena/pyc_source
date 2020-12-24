# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lazy_slides/generate.py
# Compiled at: 2012-03-18 04:32:48
from reportlab.pdfgen import canvas

def generate_slides(tags, tag_map, outfile, args):
    """Generate a beamer slideshow.

    :param tags: The tags used to find the images in the slideshow.
    :param filenames: The filenames of the images for the slideshow.
    :param outfile: The name of the file into which the results should
      be saved.
    """
    c = canvas.Canvas(outfile)
    for tag in tags:
        c.setPageSize((args.image_width,
         args.image_height))
        c.drawImage(tag_map[tag], 0, 0, width=args.image_width, height=args.image_height)
        c.showPage()

    c.save()