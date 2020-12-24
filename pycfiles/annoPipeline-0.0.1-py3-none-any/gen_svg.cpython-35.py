# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/gen_svg.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 3164 bytes
import os

def print_track(track_num, svg_out, figure_width):
    id_num = 3067
    x = 2.0744663
    y = 131
    for track in range(track_num):
        if track % 2 == 0:
            svg_out.write('  <rect\n')
            svg_out.write('     width="{0}"\n'.format(figure_width))
            svg_out.write('     height="40"\n')
            svg_out.write('     x="{0}"\n'.format(x))
            if track == 0:
                svg_out.write('     y="{0}"\n'.format(y))
            else:
                y = y + 40
                svg_out.write('     y="{0}"\n'.format(y))
            svg_out.write('     id="rect{0}"\n'.format(id_num))
            svg_out.write('     style="opacity:0.25;fill:#37c84f;fill-opacity:0.25;fill-rule:evenodd;')
            svg_out.write('stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:0.25" />\n')
        if track % 2 == 1:
            svg_out.write('  <rect\n')
            svg_out.write('     width="{0}"\n'.format(figure_width))
            svg_out.write('     height="40"\n')
            svg_out.write('     x="{0}"\n'.format(x))
            y = y + 40
            svg_out.write('     y="{0}"\n'.format(y))
            svg_out.write('     id="rect{0}"\n'.format(id_num))
            svg_out.write('     style="opacity:0.25;fill:#c8374f;fill-opacity:0.25;fill-rule:evenodd;')
            svg_out.write('stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:0.25" />\n')
        id_num += 1


def gen_svg(input_png, track_num, figure_height, figure_width):
    svg_out = open(input_png[:-4] + '.svg', 'w')
    svg_out.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   xmlns:xlink="http://www.w3.org/1999/xlink"\n   version="1.1"\n')
    svg_out.write('   width="{0}"\n'.format(figure_width))
    svg_out.write('   height="{0}"\n'.format(figure_height))
    svg_out.write('   viewBox="0 0 1860 {0}"\n'.format(figure_height))
    svg_out.write('   id="svg3055">\n  <metadata\n     id="metadata3061">\n    <rdf:RDF>\n      <cc:Work\n         rdf:about="">\n        <dc:format>image/svg+xml</dc:format>\n        <dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />\n        <dc:title></dc:title>\n      </cc:Work>\n    </rdf:RDF>\n  </metadata>\n  <defs\n     id="defs3059" />\n  <image\n')
    svg_out.write('     xlink:href="file://{0}/{1}"\n'.format(os.getcwd(), input_png))
    svg_out.write('     width="100%"\n     height="100%"\n     preserveAspectRatio="xMidYMin meet"\n     id="image3063" />\n')
    print_track(track_num, svg_out, figure_width)
    svg_out.write('</svg>')
    svg_out.close()