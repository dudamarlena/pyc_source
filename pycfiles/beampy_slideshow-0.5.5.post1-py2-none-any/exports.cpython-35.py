# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/exports.py
# Compiled at: 2019-04-18 17:27:00
# Size of source mod 2**32: 15836 bytes
"""
Created on Fri May 15 16:48:01 2015

@author: hugo
"""
from beampy.commands import document
from beampy.functions import render_texts
import json
try:
    from cStringIO import StringIO
except:
    from io import StringIO

import sys, os, time, io
curdir = os.path.dirname(__file__) + '/'

def save_layout():
    for islide in range(document._global_counter['slide'] + 1):
        slide = document._slides[('slide_%i' % islide)]
        slide.build_layout()


def reset_module_rendered_flag():
    for slide in document._slides:
        document._slides[slide].reset_rendered()
        for ct in document._slides[slide].contents:
            document._slides[slide].contents[ct].reset_outputs()


def save(output_file=None, format=None):
    """
        Function to render the document to html

    """
    if document._quiet:
        sys.stdout = open(os.devnull, 'w')
    texp = time.time()
    bname = os.path.basename(output_file)
    bdir = output_file.replace(bname, '')
    if document._rendered:
        document._rendered = False
        reset_module_rendered_flag()
    file_ext = os.path.splitext(output_file)[(-1)]
    if 'html' in file_ext or format == 'html5':
        document._output_format = 'html5'
        render_texts()
        save_layout()
        output = html5_export()
    else:
        if 'svg' in file_ext or format == 'svg':
            document._output_format = 'svg'
            render_texts()
            save_layout()
            output = svg_export(bdir + '/tmp')
            output_file = None
        elif 'pdf' in file_ext or format == 'pdf':
            document._output_format = 'pdf'
            render_texts()
            save_layout()
            output = pdf_export(output_file)
            output_file = None
    if output_file is not None:
        with open(output_file, 'w') as (f):
            f.write(output.encode('utf8'))
    if document._cache is not None:
        document._cache.write_cache()
    document._rendered = True
    print('====================' + ' BEAMPY END (%0.3f seconds) ' % (time.time() - texp) + '====================')


def pdf_export(name_out):
    inkscapecmd = document._external_cmd['inkscape']
    pdfjoincmd = document._external_cmd['pdfjoin']
    svgcmd = inkscapecmd + " --without-gui  --file='%s' --export-pdf='%s' -d=300"
    bdir = os.path.dirname(name_out)
    print('Render svg slides')
    aa = svg_export(bdir + '/tmp')
    print('Convert svg to pdf with inkscape')
    output_svg_names = []
    for islide in range(document._global_counter['slide'] + 1):
        print('slide %i' % islide)
        for layer in range(max(document._slides[('slide_%i' % islide)].svglayers) + 1):
            print('layer %i' % layer)
            res = os.popen(svgcmd % (bdir + '/tmp/slide_%i-%i.svg' % (islide, layer),
             bdir + '/tmp/slide_%i-%i.pdf' % (islide, layer)))
            res.close()
            output_svg_names += ['slide_%i-%i' % (islide, layer)]

    res = os.popen(pdfjoincmd + ' %s -o %s' % (' '.join(['"' + bdir + '/tmp/%s.pdf"' % sname for sname in output_svg_names]), name_out))
    output = res.read()
    res.close()
    msg = 'Saved to %s' % name_out
    return msg


def svg_export(dir_name, quiet=False):
    if quiet:
        sys.stdout = open(os.devnull, 'w')
    try:
        os.mkdir(dir_name)
    except:
        pass

    if dir_name[(-1)] != '/':
        dir_name += '/'
    for islide in range(document._global_counter['slide'] + 1):
        print('Export slide %i' % islide)
        slide = document._slides[('slide_%i' % islide)]
        slide.newrender()
        if 'glyphs' in document._global_store:
            glyphs_svg = '<defs>%s</defs>' % ''.join([glyph['svg'] for glyph in document._global_store['glyphs'].values()])
        else:
            glyphs_svg = ''
        def_svg = '<defs>%s</defs>' % ''.join(slide.svgdefout)
        for layer in range(max(slide.svglayers) + 1):
            tmp = slide.svgheader + glyphs_svg + def_svg
            tmp += slide.svglayers[layer]
            tmp += slide.svgfooter
            with io.open(dir_name + 'slide_%i-%i.svg' % (islide, layer), 'w', encoding='utf8') as (f):
                f.write(tmp)

    return 'saved to ' + dir_name


def html5_export():
    with open(curdir + 'statics/jquery.js', 'r') as (f):
        jquery = f.read()
    with open(curdir + 'statics/header_V2.html', 'r') as (f):
        output = f.read() % jquery
    htmltheme = document._theme['document']['html']
    output += '\n    <!-- Default Style -->\n    <style>\n      * { margin: 0; padding: 0;\n        -moz-box-sizing: border-box; -webkit-box-sizing: border-box;\n        box-sizing: border-box; outline: none; border: none;\n        }\n\n      body {\n        width: ' + str(document._width) + 'px;\n        height: ' + str(document._height) + 'px;\n        margin-left: -' + str(int(document._width / 2)) + 'px; margin-top: -' + str(int(document._height / 2)) + 'px;\n        position: absolute; top: 50%; left: 50%;\n        overflow: hidden;\n        display: none;\n        background-color: #ffffff;\n\n      }\n\n      section {\n        position: absolute;\n        width: 100%; height: 100%;\n      }\n\n\n      html { background-color: ' + str(htmltheme['background_color']) + ';\n        height: 100%;\n        width: 100%;\n      }\n\n      video {\n        visibility: hidden;\n      }\n\n\n      body.loaded { display: block;}\n    </style>\n\n    '
    tmpout = {}
    tmpscript = {}
    global_store = ''
    for islide in range(document._global_counter['slide'] + 1):
        tnow = time.time()
        slide_id = 'slide_%i' % islide
        tmpout[slide_id] = {}
        slide = document._slides[slide_id]
        slide.newrender()
        tmpout[slide_id]['svg'] = []
        tmpout[slide_id]['layers_nums'] = slide.num_layers
        tmpout[slide_id]['svg_header'] = slide.svgheader
        tmpout[slide_id]['svg_footer'] = slide.svgfooter
        modulessvgdefs = ''.join(slide.svgdefout)
        global_store += '<svg><defs>' + modulessvgdefs
        for layer in range(slide.num_layers + 1):
            print('write layer %i' % layer)
            if layer in slide.svglayers:
                layer_content = slide.svglayers[layer]
            else:
                layer_content = ''
            global_store += "<g id='slide_{i}-{layer}'>{content}</g>".format(i=islide, layer=layer, content=layer_content)
            tmpout[slide_id]['svg'] += ['<use xlink:href="#slide_{i}-{layer}"/>'.format(i=islide, layer=layer)]

        global_store += '</defs></svg>'
        if slide.animout is not None:
            tmpout[slide_id]['svganimates'] = {}
            headers = []
            for ianim, data in enumerate(slide.animout):
                headers += [data['header']]
                data.pop('header')
                tmpout[slide_id]['svganimates'][data['anim_num']] = data

            if headers:
                tmp = ''.join(headers)
                global_store += '<svg>%s</svg>' % tmp
            if slide.scriptout is not None:
                tmpscript['slide_%i' % islide] = ''.join(slide.scriptout)
            if slide.htmlout is not None:
                for layer in slide.htmlout:
                    global_store += '<div id="html_store_slide_%i-%i">%s</div>' % (islide, layer,
                     ''.join(slide.htmlout[layer]))

            print('Done in %0.3f seconds' % (time.time() - tnow))

    jsonfile = StringIO()
    json.dump(tmpout, jsonfile, indent=None)
    jsonfile.seek(0)
    if 'glyphs' in document._global_store:
        glyphs_svg = '<svg id="glyph_store"><defs>%s</defs></svg>' % ''.join([glyph['svg'] for glyph in document._global_store['glyphs'].values()])
        output += glyphs_svg
    output += ''.join(global_store)
    output += '<script> slides = eval( ( %s ) );</script>' % jsonfile.read()
    if tmpscript != {}:
        bokeh_required = False
        output += '\n <script> scripts_slide = {}; //dict with scrip function for slides \n'
        for slide in tmpscript:
            output += '\nscripts_slide["%s"] = {};\n scripts_slide["%s"]%s; \n' % (slide, slide, tmpscript[slide])
            if 'bokeh' in tmpscript[slide].lower():
                bokeh_required = True

        output += '</script>\n'
        if bokeh_required:
            cssbk, jsbk = get_bokeh_includes()
            output += cssbk + jsbk
            output
    with open(curdir + 'statics/footer_V2.html', 'r') as (f):
        output += f.read()
    return output


def check_content_type_change(slide, nothtml=True):
    """
        Function to change type of some slide contents (like for video html -> svg ) when render is changer from html5 to another
    """
    for ct in slide['contents']:
        if nothtml:
            if 'type_nohtml' in ct:
                print('done')
                ct['original_type'] = copy(ct['type'])
                ct['type'] = ct['type_nohtml']
            else:
                if 'original_type' in ct:
                    ct['type'] = ct['original_type']


def display_matplotlib(slide_id, show=False):
    """
        Display the given slide in a matplotlib figure
    """
    from matplotlib import pyplot
    from PIL import Image
    from numpy import asarray
    if document._quiet:
        sys.stdout = open(os.devnull, 'w')
    oldformat = document._output_format
    document._output_format = 'svg'
    slide = document._slides[slide_id]
    render_texts([slide.contents[eid] for eid in slide.element_keys if slide.contents[eid].type == 'text'])
    slide.build_layout()
    slide.newrender()
    svgout = slide.svgheader
    if 'glyphs' in document._global_store:
        glyphs_svg = '<defs>%s</defs>' % ''.join([glyph['svg'] for glyph in document._global_store['glyphs'].values()])
        svgout += glyphs_svg
    svgout += '<defs>%s</defs>' % ''.join(slide.svgdefout)
    for layer in range(max(slide.svglayers) + 1):
        svgout += slide.svglayers[layer]

    svgout += slide.svgfooter
    tmpname = './.%s' % slide_id
    with io.open(tmpname + '.svg', 'w', encoding='utf8') as (f):
        f.write(svgout)
    reset_module_rendered_flag()
    document._output_format = oldformat
    inkscapecmd = document._external_cmd['inkscape']
    svgcmd = inkscapecmd + " --without-gui  --file='%s' --export-png='%s' -b='white' -d=300"
    os.popen(svgcmd % (tmpname + '.svg', tmpname + '.png'))
    img = asarray(Image.open(tmpname + '.png'))
    os.unlink(tmpname + '.svg')
    os.unlink(tmpname + '.png')
    pyplot.figure(dpi=300)
    pyplot.imshow(img)
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.tight_layout()
    if show:
        pyplot.show()


def get_bokeh_includes():
    """
    Function to get bokeh dependencies (style and javascript) from their CDN
    
    Return string with <style>bokeh_css</style><script>bokeh js</script>
    """
    from bokeh.resources import CDN
    try:
        from urllib2 import URLError
        from urllib2 import urlopen
    except:
        from urllib.error import URLError
        from urllib.request import urlopen

    css_out = '<style>'
    for cssurl in CDN.css_files:
        cssname = cssurl[cssurl.rfind('/') + 1:]
        if document._cache is not None and document._cache.is_file_cached(cssname):
            csst = document._cache.get_cached_file(cssname)
            css_out += csst.decode('utf8') + '\n'
        else:
            try:
                print('Download %s' % cssurl)
                response = urlopen(cssurl, timeout=5)
                csst = response.read()
                if document._cache is not None:
                    document._cache.add_file(cssname, csst)
                css_out += csst.decode('utf8') + '\n'
            except URLError as e:
                print('Error in download: %s' % e)

    css_out += '</style>'
    js_out = '<script>'
    for jsurl in CDN.js_files:
        jsname = jsurl[jsurl.rfind('/') + 1:]
        if document._cache is not None and document._cache.is_file_cached(jsname):
            jst = document._cache.get_cached_file(jsname)
            js_out += jst.decode('utf8') + '\n'
        else:
            try:
                print('Download %s' % jsurl)
                response = urlopen(jsurl, timeout=5)
                jst = response.read()
                if document._cache is not None:
                    document._cache.add_file(jsname, jst)
                js_out += jst.decode('utf8') + '\n'
            except URLError as e:
                print('Error in download: %s' % e)

    js_out += '</script>'
    return (
     css_out, js_out)