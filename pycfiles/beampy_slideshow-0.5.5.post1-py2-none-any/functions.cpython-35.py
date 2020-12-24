# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/functions.py
# Compiled at: 2019-04-18 03:17:03
# Size of source mod 2**32: 23371 bytes
"""
Created on Fri May 15 16:45:51 2015

@author: hugo
"""
from beampy.document import document
from bs4 import BeautifulSoup
import re
from beampy.scour import scour
import glob, os, sys
from subprocess import check_call, check_output
import tempfile, time, hashlib, logging
_log = logging.getLogger(__name__)
import inspect
find_svg_tags = re.compile('id="(.*)"')
remove_tabnewline = re.compile('\\s+')

def unit_operation(value, to=0):
    """
        realise operation on values and return the result in px

        expl: value = 3px+4cm -> the sum

              value = +5cm, to=450 -> 450px+5cm
    """
    if '+' in value:
        vsplited = value.split('+')
        for v in vsplited:
            to += float(convert_unit(v))

    elif '-' in value:
        vsplited = value.split('-')
        for v in vsplited:
            to -= float(convert_unit(v))

    return '%0.1f' % to


def convert_unit(value, ppi=72):
    """
    Function to convert size given in some unit to pixels, following the
    https://www.w3.org/TR/2008/REC-CSS2-20080411/syndata.html#length-units

    Parameters:
    -----------

    value, str or int:
        The given size followed by it's unit. Fixed units are (in, cm,
        mm, pt, pc). Relative units are (em, ex, %)

    ppi, int, optional:
        The number of pixel per inch (Latex use 72)
    """
    value = str(value)
    if 'px' in value:
        value = '%0.1f' % float(value.replace('px', ''))
    if 'mm' in value:
        value = '%fcm' % (float(value.replace('mm', '')) * 0.1)
    if 'cm' in value:
        value = '%fin' % (float(value.replace('cm', '')) * 0.39370078740157477)
    if 'pc' in value:
        value = '%fin' % float(value.replace('pc', '') * 12)
    if 'pt' in value:
        value = '%fin' % (float(value.replace('pt', '')) * 0.013888888888888888)
    if 'in' in value:
        out = float(value.replace('in', '')) * ppi
    else:
        out = float(value)
    return out


def pre_cache_svg_image(svg_frames):
    """
        Function to extract raster image from svg to define them only
        once on the slide.
    """
    all_images = []
    out_svg_frames = []
    findimage = re.compile('<image.*?>')
    for frame in svg_frames:
        svgimages = findimage.findall(frame)
        all_images += svgimages
        out_svg_frames += [findimage.sub('\n', frame)]

    return (out_svg_frames, all_images)


def make_global_svg_defs_new_but_buggy(svg_soup):
    """
        Function to change svg refs and id to a global counter 
        to avoid miss-called elements in slides

        Input -> svg_soup: beautifulsoup object of the svg
    """
    if 'svg_id' not in document._global_counter:
        document._global_counter['svg_id'] = 0
    for defs in svg_soup.find_all('defs'):
        tags_to_replace = find_svg_tags.findall(str(defs))
        base_name = 'beampy'
        for cpt, tag in enumerate(tags_to_replace):
            new_tag = '%s_%i' % (base_name, document._global_counter['svg_id'])
            for elem in svg_soup.find_all(attrs={'xlink:href': '#%s' % tag}):
                elem['xlink:href'] = '#%s' % new_tag

            for elem in svg_soup.find_all(attrs={'id': tag}):
                elem['id'] = new_tag

            document._global_counter['svg_id'] += 1

    return svg_soup


def make_global_svg_defs(svg_soup):
    """
        Function to use global counter for id in svg defs and use

        svg_soup a BeautifulSoup object of the svg file
    """
    if 'svg_id' not in document._global_counter:
        document._global_counter['svg_id'] = 0
    strsvg = str(svg_soup)
    svgdefs = svg_soup.find('defs')
    text_id = ('%0.4f' % time.time()).split('.')[(-1)]
    if svgdefs != None:
        for tag in svgdefs.findAll(lambda x: x != None and x.has_attr('id')):
            oldid = tag['id']
            newid = '%s_%i' % (text_id, document._global_counter['svg_id'])
            strsvg = re.sub(oldid + '"', newid + '"', strsvg)
            if tag.name in ('clipPath', 'linearGradient'):
                strsvg = re.sub('(#' + oldid + ')', '#' + newid, strsvg)
            document._global_counter['svg_id'] += 1

    soup = BeautifulSoup(strsvg, 'xml')
    return soup


def horizontal_centering(object_width, xinit=0, page_width=None):
    """
        Function to center and object on the page_width

        xinit: is the initial position

        final position:
            xinit + available_space/2
    """
    if page_width == None:
        page_width = document._width
    if page_width > object_width:
        available_space = page_width - object_width
        xnew = xinit + available_space / 2
    else:
        xnew = xinit
    return xnew


def optimize_svg(svgfile_in):
    """
        Use python scour to optimise svg gain roughtly 50% in size

        options (default):
        {'strip_ids': False,
        'shorten_ids': False,
        'simple_colors': True,
        'strip_comments': False,
        'remove_metadata': False,
        'outfilename': None,
        'group_create': False,
        'protect_ids_noninkscape': False,
        'indent_type': 'space',
        'keep_editor_data': False,
        'shorten_ids_prefix': '',
        'keep_defs': False,
        'renderer_workaround': True,
        'style_to_xml': True,
        'protect_ids_prefix': None,
        'enable_viewboxing': False,
        'digits': 5,
        'embed_rasters': True,
        'infilename': 'none',
        'strip_xml_prolog': False,
        'group_collapse': True,
        'quiet': False,
        'protect_ids_list': None}
    """
    opts = scour.generateDefaultOptions()
    options = opts.__dict__
    options['indent_type'] = None
    options['strip_comments'] = True
    t = time.time()
    svgout = scour.scourString(svgfile_in, opts)
    print('optimize svg run in %f' % (time.time() - t))
    return svgout


def latex2svg(latexstring, write_tmpsvg=False):
    """
        Command to render latex -> dvi -> svg

    Parameters
    ==========

    write_tmpsvg: true or false optional,
        Write the svg produced by dvisvgm to a file (if True)
        otherwise the output is read from stdout
    """
    _log.debug('Run latex2svg function')
    _log.debug(latexstring)
    dvisvgmcmd = document._external_cmd['dvisvgm']
    tmpfile, tmpnam = tempfile.mkstemp(prefix='beampytmp')
    tmppath = tmpnam.replace(os.path.basename(tmpnam), '')
    with open(tmpnam + '.tex', 'w') as (f):
        f.write(latexstring)
    tex = os.popen('cd ' + tmppath + ' && latex -interaction=nonstopmode ' + tmpnam + '.tex')
    output = tex.read()
    tex.close()
    if 'error' in output or '!' in output:
        print('Latex compilation error')
        print(output)
    else:
        if write_tmpsvg:
            res = os.popen(dvisvgmcmd + ' -n -a --linkmark=none -o ' + tmpnam + '.svg --verbosity=0 ' + tmpnam + '.dvi')
            res.close()
            with open(tmpnam + '.svg') as (svgf):
                outsvg = svgf.read()
        else:
            res = os.popen(dvisvgmcmd + ' -n -s -a --linkmark=none -v0 ' + tmpnam + '.dvi')
            outsvg = res.read()
            res.close()
        for f in glob.glob(tmpnam + '*'):
            os.remove(f)

    return outsvg


def getsvgwidth(svgfile):
    """
        get svgfile width using inkscape
    """
    inkscapecmd = document._external_cmd['inkscape']
    cmd = inkscapecmd + ' -z -W %s' % svgfile
    req = os.popen(cmd)
    res = req.read()
    req.close()
    return res


def getsvgheight(svgfile):
    """
        get svgfile height using inkscape
    """
    inkscapecmd = document._external_cmd['inkscape']
    cmd = inkscapecmd + ' -z -H %s' % svgfile
    req = os.popen(cmd)
    res = req.read()
    req.close()
    return res


def gcs():
    """
        Fonction get current slide of the doc
    """
    return document._curentslide


def set_curentslide(slide_id):
    """
    Set the curent slide to the given slide_id
    """
    document._curentslide = slide_id


def set_lastslide():
    """
    Set the curent slide as the last slide added in the presentation
    """
    last_slide_id = 'slide_%i' % document._global_counter['slide']
    document._curentslide = last_slide_id


def gce(doc=document):
    """
        Function to get the current element number
    """
    return doc._global_counter['element']


def pdf2svg(pdf_input_file, svg_output_file):
    """
    Runs pdf2svg in shell:
    pdf2svg pdf_input_file svg_output_file

    """
    return check_call([document._external_cmd['pdf2svg'],
     pdf_input_file, svg_output_file])


def convert_pdf_to_svg(pdf_input_file, temp_directory='local'):
    """
    Open pdf_input_file, convert to svg using pdf2svg.
    """
    local_directory, filename_pdf = os.path.split(pdf_input_file)
    filename = os.path.splitext(filename_pdf)[0]
    if temp_directory == 'local':
        temp_directory = local_directory
    if len(temp_directory) > 0:
        svg_output_file = temp_directory + '/' + filename + '.svg'
    else:
        svg_output_file = filename + '.svg'
    try:
        pdf2svg(pdf_input_file, svg_output_file)
        with open(svg_output_file, 'r') as (f):
            svg_figure = f.read()
        check_call(['rm', svg_output_file])
        return svg_figure
    except ValueError:
        return


def load_args_from_theme(function_name, args):
    """
        Function to set args of a given element
    """
    for key in args:
        if args[key] == '' or args[key] is None:
            try:
                args[key] = document._theme[function_name][key]
            except KeyError:
                print('[Beampy] No theme propertie for %s in %s' % (key, element_id))


def check_function_args(function, arg_values_dict):
    """
        Function to check input function args.

        Functions args are defined in the default_theme.py
        or if a theme is added the new value is taken rather than the default one
    """
    function_name = function.__name__
    default_dict = document._theme[function_name]
    outdict = {}
    for key, value in arg_values_dict.items():
        if key in default_dict:
            outdict[key] = value
        else:
            print('Error the key %s is not defined for %s module' % (key, function_name))
            print_function_args(function_name)
            sys.exit(1)

    for key, value in default_dict.items():
        if key not in outdict:
            outdict[key] = value

    return outdict


def print_function_args(function_name):
    print('Allowed arguments for %s' % function_name)
    for key, value in document._theme[function_name].items():
        print('%s: [%s] %s' % (key, str(value), type(value)))


def inherit_function_args(function_name, args_dict):
    for key, value in document._theme[function_name].items():
        if key not in args_dict:
            args_dict[key] = value

    return args_dict


def color_text(textin, color):
    """
    Adds Latex color to a string.
    """
    if '#' in color:
        textin = '{\\color[HTML]{%s} %s }' % (color.replace('#', '').upper(),
         textin)
    else:
        textin = '{\\color{%s} %s }' % (color, textin)
    return textin


def dict_deep_update(original, update):
    """
    Recursively update a dict.
    Subdict's won't be overwritten but also updated.
    from http://stackoverflow.com/questions/38987/how-can-i-merge-two-python-dictionaries-in-a-single-expression/44512#44512
    """
    for key, value in original.items():
        if key not in update:
            update[key] = value
        elif isinstance(value, dict):
            dict_deep_update(value, update[key])

    return update


def create_element_id(bpmod, use_args=True, use_name=True, use_content=True, add_slide=True, slide_position=True):
    """
        create a unique id for the beampy_module using bpmod.content
        and bpmod.args.keys() and bpmod.name
    """
    ct_to_hash = ''
    if add_slide:
        ct_to_hash += bpmod.slide_id
    if use_args and bpmod.args is not None:
        ct_to_hash += ''.join(['%s:%s' % (k, v) for k, v in bpmod.args.items()])
    if use_name and bpmod.name is not None:
        ct_to_hash += bpmod.name
    if use_content and bpmod.content is not None:
        ct_to_hash += str(bpmod.content)
    if slide_position:
        ct_to_hash += str(len(document._slides[bpmod.slide_id].element_keys))
    outid = None
    if ct_to_hash != '':
        try:
            outid = hashlib.md5(ct_to_hash).hexdigest()
        except:
            outid = hashlib.md5(ct_to_hash.encode('utf8')).hexdigest()

        if outid in document._slides[bpmod.slide_id].element_keys:
            print('Id for this element already exist!')
            sys.exit(0)
            outid = None
    return outid


def get_command_line(func_name):
    """
    Function to print the line of the command in the source code file
    frame,filename,nline,function_name,lines,index = inspect.stack()[-1]
    """
    frame, filename, nline, function_name, lines, index = inspect.stack()[(-1)]
    if not isinstance(func_name, str):
        func_name = func_name.__name__
    start = None
    src = document._source_code.source(stop=nline).split('\n')
    for cpt, line in enumerate(src[::-1]):
        if func_name + '(' in line:
            start = nline - (cpt + 1)
            break

    if start is not None:
        stop = nline - 1
        source = document._source_code.source(start + 1, nline).replace('\n', '')
    else:
        start = 0
        stop = 0
        source = func_name
    source = remove_tabnewline.sub(' ', source)
    return (
     start, nline - 1, source)


def guess_file_type(file_name, file_type=None):
    """
    Guess the type of a file name
    """
    file_extensions = {'svg': ['svg'], 
     'pdf': ['pdf'], 
     'png': ['png'], 
     'jpeg': ['jpg', 'jpeg'], 
     'gif': ['gif']}
    if file_type is None:
        try:
            ext = file_name.lower().split('.')[(-1)]
            for file_type in file_extensions:
                if ext in file_extensions[file_type]:
                    break

        except TypeError:
            print('Unknown file type for file name: ' + file_name + '.')

    return file_type


def render_texts(elements_to_render=[], extra_packages=[]):
    r"""
    Function to merge all text in the document to run latex only once
    This function build the .tex file and then call two external programs
    .tex -> latex -> .dvi -> dvisvgm -> svgfile

    Parameters:
    -----------

    elements_to_render, list of beampy_module (optional):
        List of beampy_module object to render (the default is empty,
        which render all text module in all slides).

    extra_packages, list of string (optional):
        Give a list of extra latex packages to use in the latex
        template. Latex packages should be given as follow:
        [r'\usepackage{utf8x}{inputenc}']
    """
    print('Render texts of slides with latex')
    latex_header = '\n    \\documentclass[crop=true, multi=true]{standalone}\n    \\usepackage[utf8x]{inputenc}\n    \\usepackage{fix-cm}\n    \\usepackage[hypertex]{hyperref}\n    \\usepackage[svgnames]{xcolor}\n    \\renewcommand{\\familydefault}{\\sfdefault}\n    \\usepackage{varwidth}\n    \\usepackage{amsmath}\n    \\usepackage{amsfonts}\n    \\usepackage{amssymb}\n    %s\n    \\begin{document}\n    ' % '\n'.join(extra_packages + document._latex_packages)
    latex_pages = []
    latex_footer = '\\end{document}'
    t = time.time()
    cpt_page = 1
    elements_pages = []
    if elements_to_render == []:
        for sid in document._slides:
            for cid in document._slides[sid].element_keys:
                e = document._slides[sid].contents[cid]
                if e.type == 'text' and e.usetex and not e.rendered:
                    elements_to_render += [e]

    for e in elements_to_render:
        if e.cache and document._cache is not None:
            ct_cache = document._cache.is_cached(e.slide_id, e)
            if ct_cache is False:
                e.pre_render()
                try:
                    latex_pages += [e.latex_text]
                    elements_pages += [{'element': e, 'page': cpt_page}]
                    cpt_page += 1
                except Exception as e:
                    print(e)

        else:
            e.pre_render()
            try:
                latex_pages += [e.latex_text]
                elements_pages += [{'element': e, 'page': cpt_page}]
                cpt_page += 1
            except Exception as e:
                print(e)

    _log.debug(latex_pages)
    if len(latex_pages) > 0:
        tmpfile, tmpname = tempfile.mkstemp(prefix='beampytmp')
        tmppath = tmpname.replace(os.path.basename(tmpname), '')
        with open(tmpname + '.tex', 'w') as (f):
            f.write(latex_header)
            f.write('\\newpage'.join(latex_pages))
            f.write(latex_footer)
        print('Latex file writen in %f' % (time.time() - t))
        cmd = 'cd ' + tmppath + ' && latex -interaction=nonstopmode --halt-on-error ' + tmpname + '.tex'
        _log.debug(cmd)
        tex = os.popen(cmd)
        tex_outputs = tex.read()
        _log.debug(tex_outputs)
        if 'error' in tex_outputs or '!' in tex_outputs:
            print('Latex compilation error')
            print(tex_outputs)
        tex.close()
        dvisvgmcmd = document._external_cmd['dvisvgm']
        t = time.time()
        res = os.popen(dvisvgmcmd + ' -n -s -p1- --linkmark=none -v0 ' + tmpname + '.dvi')
        allsvgs = res.readlines()
        res.close()
        schema = allsvgs[0]
        svg_list = ''.join(allsvgs[1:]).split(schema)
        for i, ep in enumerate(elements_pages):
            cpt_page = ep['page']
            ep['element'].svgtext = schema + svg_list[i]

        print('DVI -> SVG in %f' % (time.time() - t))
        for f in glob.glob(tmpname + '*'):
            os.remove(f)


PYTHON_COMMENT_REGEX = re.compile('"{3}?|"|\'{3}?|\'', re.MULTILINE)

def small_comment_parser(src):
    """
    Find comments inside a python source code.
    return a list of parsed comments.

    Parameters
    ----------
    
    src : str
        The source code to parse.x
    """
    cur_marker_pos = 0
    cur_marker_type = ''
    marker_open = False
    text_parts = []
    for part in PYTHON_COMMENT_REGEX.finditer(src):
        start, stop = part.start(), part.end()
        if cur_marker_pos == 0:
            cur_marker_type = src[start:stop].strip()
            cur_marker_pos = stop
            marker_open = True
        elif marker_open:
            if cur_marker_type == src[start:stop].strip():
                comments = src[cur_marker_pos:stop - len(cur_marker_type)]
                text_parts += [comments]
                cur_marker_pos = stop
                cur_marker_type = ''
                marker_open = False
            else:
                cur_marker_pos = stop
                cur_marker_type = src[start:stop].strip()
                marker_open = True

    return text_parts