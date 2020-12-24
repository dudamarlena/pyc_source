# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miranda/.virtualenvs/vf_utils/lib/python3.6/site-packages/vf_createproducts_core/compose.py
# Compiled at: 2018-10-05 17:13:25
# Size of source mod 2**32: 3972 bytes
"""
Copyright (2017) Raydel Miranda 

This file is part of "VillaFlores Product Creator".

    "VillaFlores Product Creator" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "VillaFlores Product Creator" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "VillaFlores Product Creator".  If not, see <http://www.gnu.org/licenses/>.
"""
import base64, logging, os, shutil, subprocess, tempfile
from colorama import init, Fore, Style
from lxml import etree
init()
NS = {'svg':'http://www.w3.org/2000/svg', 
 'xlink':'http://www.w3.org/1999/xlink'}
logger = logging.getLogger('vf_productcreate')
xml_tree_memoization = {}
image_memoization = {}

def compose(images, template, output, verbose=False):
    """
    Compose images from combinations of a set of images and a template.

    :param images: A list of 2-tuples in the form (image, template_layer_id)
    :param template: The template (svg file)
    :param output:  The result image.
    :param verbose:  Print the process.
    :return:
    """
    svg_temp_name = None
    for image, image_layer_id in images:
        if not image_memoization.get(image, False):
            image_file = open(image, 'rb')
            encoded_string = base64.b64encode(image_file.read())
            image_memoization.update({image: encoded_string})
        encoded_string = image_memoization[image]
        with open(template) as (svg_file):
            if not xml_tree_memoization.get(template, False):
                xml_tree_memoization.update({template: etree.parse(svg_file)})
            else:
                svg = xml_tree_memoization[template]
                svg_image = svg.xpath(('.//svg:image[@id="{}"]'.format(image_layer_id)), namespaces=NS)
                if len(svg_image) == 0:
                    if verbose:
                        print('Error loading layer, check that the layer id is as expected.')
                    return
                svg_image[0].attrib['{http://www.w3.org/1999/xlink}href'] = 'data:image/{};base64,{}'.format(os.path.splitext(image)[1][1:], str(encoded_string)[1:])
                svg_image[0].attrib['style'] = 'overflow:visible;opacity:100;'
                svg_temp_dir = tempfile.mktemp(dir=(tempfile.gettempdir()))
                if svg_temp_name is None:
                    svg_temp_name = '{}.svg'.format(svg_temp_dir)
                try:
                    svg.write(svg_temp_name)
                except etree.SerialisationError as err:
                    if verbose:
                        logger.exception(Fore.RED + err)
                        logger.exception(Style.RESET_ALL)
                    else:
                        logger.error(Fore.RED + 'Error generating: ' + Fore.CYAN + '{}'.format(svg_temp_name))

        template = svg_temp_name
        proc = subprocess.Popen(['convert', svg_temp_name, output], stderr=(subprocess.PIPE), stdout=(subprocess.PIPE))
        out, err = proc.communicate()
        if err != b'':
            logger.error(err)
        else:
            if verbose:
                logger.info(out)

    shutil.os.remove(svg_temp_name)