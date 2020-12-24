# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/color_png.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 3906 bytes
import os
from subprocess import call
from annogesiclib.gen_svg import gen_svg
from annogesiclib.helper import Helper

class ColorPNG(object):

    def _convert_svg(self, imagemagick_path, out_path, screenshot, svg_file, log):
        call([imagemagick_path,
         os.path.join(out_path, screenshot),
         os.path.join(out_path, svg_file)])
        log.write('\t' + ' '.join([imagemagick_path, os.path.join(out_path, screenshot), os.path.join(out_path, svg_file)]) + '\n')

    def _convert_png(self, imagemagick_path, out_path, screenshot, png_file, log):
        call([imagemagick_path, '-background', 'none',
         os.path.join(out_path, screenshot),
         os.path.join(out_path, png_file)])
        log.write('\t' + ' '.join([imagemagick_path, '-background', 'none', os.path.join(out_path, screenshot), os.path.join(out_path, png_file)]) + '\n')

    def generate_color_png(self, track_num, out_folder, imagemagick_path, log):
        """generation of color png based on tracks"""
        out_folder = os.path.join(out_folder, 'screenshots')
        for strain in os.listdir(out_folder):
            if os.path.isdir(os.path.join(out_folder, strain)):
                for strand in ['forward', 'reverse']:
                    print('Running for {0}_{1}'.format(strain, strand))
                    out_path = os.path.join(out_folder, strain, strand)
                    log.write('Converting png file in {0} to svg.\n'.format(out_path))
                    log.write('Colorizing svg files.\nMake sure the version of ImageMagick is at least 6.9.0-0.\n')
                    for screenshot in os.listdir(out_path):
                        if screenshot.endswith('.png'):
                            print('Converting {0} to svg files and Painting tracks now'.format(screenshot))
                            svg_file = screenshot.replace('.png', '.svg')
                            self._convert_svg(imagemagick_path, out_path, screenshot, svg_file, log)
                            with open(os.path.join(out_path, svg_file), 'r') as (f_h):
                                for line in f_h:
                                    line = line.strip()
                                    if line.startswith('<svg'):
                                        line = line.split(' ')
                                        height = line[(-1)].split('=')[(-1)][1:-2]
                                        width = line[1].split('=')[(-1)][1:-1]
                                        break

                            gen_svg(os.path.join(out_path, screenshot), track_num, height, width)

                    log.write('All colorization for {0} is done.\n'.format(out_path))
                    log.write('Converting svg file in {0} to png.\n'.format(out_path))
                    for screenshot in os.listdir(out_path):
                        if screenshot.endswith('.svg'):
                            print('Converting {0} to png files now...'.format(screenshot))
                            png_file = screenshot.replace('.svg', '.png')
                            self._convert_png(imagemagick_path, out_path, screenshot, png_file, log)

                    Helper().remove_all_content(out_path, '.svg', 'file')
                    log.write('All conversion for {0} is done.\n'.format(out_path))