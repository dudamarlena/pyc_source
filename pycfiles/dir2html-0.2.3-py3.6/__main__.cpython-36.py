# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dir2html/__main__.py
# Compiled at: 2018-11-21 04:57:05
# Size of source mod 2**32: 2220 bytes
import os, sys, argparse
from .render_template import render_template
from .get_images import get_images
from .copy_files import copy_files
from .get_assets import get_assets

def main():
    parser = argparse.ArgumentParser(description='Generate html album from images directory')
    parser.add_argument('-i', action='store', default='.')
    parser.add_argument('-o', action='store', default='./output')
    parser.add_argument('-t', action='store')
    parser.add_argument('-d', action='store')
    args = parser.parse_args()
    source_dir = args.i
    dest_dir = args.o
    title = args.t
    description = args.d
    if not os.path.isdir(source_dir):
        print('Error: source directory does not exists')
        sys.exit(1)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    images = get_images(source_dir)
    copy_files(images, dest_dir)
    assets_path = '{}/assets'.format(dest_dir)
    if not os.path.isdir(assets_path):
        os.makedirs(assets_path)
    assets = get_assets()
    copy_files(assets, assets_path)
    images_templates_list = []
    for img in images:
        img_rendering_dict = {'{{image-name}}':os.path.basename(img), 
         '{{image-file}}':os.path.basename(img)}
        images_templates_list.append(render_template('image-template', img_rendering_dict))

    rendered_images = ''.join(images_templates_list)
    album_rendering_dict = {'{{title}}':title, 
     '{{description}}':description, 
     '{{image-placeholder}}':str(rendered_images)}
    album_template = render_template('album-template', album_rendering_dict)
    with open('{}/index.html'.format(dest_dir), 'w') as (f):
        f.write(album_template)
    print('Done!')


if __name__ == '__main__':
    main()