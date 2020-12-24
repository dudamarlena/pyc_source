# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/core.py
# Compiled at: 2019-07-06 08:09:17
# Size of source mod 2**32: 57605 bytes
"""
Created on Sun Oct 25 20:33:18 2015

@author: hugo
"""
from beampy import document
from beampy.functions import gcs, create_element_id, check_function_args, get_command_line, convert_unit, pre_cache_svg_image, print_function_args, set_curentslide, set_lastslide
from beampy.geometry import positionner, distribute
import sys, time, inspect, logging
_log = logging.getLogger(__name__)

class slide(object):
    __doc__ = '\n    Add a slide to the presentation.\n\n    Parameters\n    ----------\n\n    title : str or None, optional\n        Set the title of the slide (the default value is None)\n\n    background : str, optional\n        Background color of the slide (the default value is "white"). Accept svg color name or HTML hex value.\n\n    layout: function or None, optional\n        Function containing beampy modules that will be displayed as slide background.\n\n        >>> slide(layout=my_function)\n\n    '

    def __init__(self, title=None, **kwargs):
        if 'slide' in document._global_counter:
            document._global_counter['slide'] += 1
        else:
            document._global_counter['slide'] = 0
        document._global_counter['group'] = 0
        self.args = check_function_args(slide, kwargs)
        self.slide_num = document._global_counter['slide']
        self.id = 'slide_%i' % self.slide_num
        document._curentslide = self.id
        self.tmpout = ''
        self.contents = {}
        self.element_keys = []
        self.cpt_anim = 0
        self.num = document._global_counter['slide'] + 1
        self.title = title
        self.curwidth = document._width
        self.curheight = document._height
        self.num_layers = 0
        self.svgout = []
        self.svgdefout = []
        self.htmlout = {}
        self.scriptout = []
        self.animout = []
        self.svgheader = ''
        self.svgfooter = '\n</svg>\n'
        self.svglayers = {}
        self.render_layout = True
        document._slides[self.id] = self
        if len(document._TOC) > 0:
            self.TOCposition = document._TOC[(-1)]
        else:
            self.TOCposition = 0
        self.groupsid = {}
        self.cur_group_level = -1
        g0 = group(x=0, y=0, width=(document._width), height=(document._height))
        self.cur_group_id = g0.id
        self.groupsid[0] = [g0.id]
        if title is not None:
            import beampy.modules.title as bptitle
            self.title_element = bptitle(title)
            self.ytop = float(convert_unit(self.title.reserved_y))
        else:
            self.ytop = 0
            self.title_element = None
        g0.yoffset = self.ytop

    def add_module(self, module_id, module_content):
        self.element_keys += [module_id]
        self.contents[module_id] = module_content
        if module_content.type != 'group':
            _log.debug('Module %s added to group %s' % (str(module_content.name), self.cur_group_id))
            self.contents[self.cur_group_id].add_elements_to_group(module_id, module_content)
            self.contents[module_id].group_id = self.cur_group_id
        else:
            if module_content.grouplevel > 0:
                if module_content.parentid is not None:
                    _log.debug('Add parent (id=%s) for %s(%s)' % (module_content.parentid, module_content.name, module_id))
                    self.contents[module_content.parentid].add_elements_to_group(module_id, module_content)
                elif module_content.grouplevel not in self.groupsid:
                    self.groupsid[module_content.grouplevel] = [
                     module_id]
                else:
                    self.groupsid[module_content.grouplevel] += [module_id]
            logging.debug('Element %s added to slide' % str(module_content.name))

    def remove_module(self, module_id):
        self.element_keys.pop(self.element_keys.index(module_id))
        gid = self.contents[module_id].group_id
        self.contents[gid].remove_element_in_group(module_id)
        self.contents.pop(module_id)

    def add_rendered(self, svg=None, svgdefs=None, html=None, js=None, animate_svg=None, layer=0):
        logging.debug('Add rendered')
        if svg is not None:
            self.svgout += [svg]
        else:
            if svgdefs is not None:
                logging.debug('svgdefs')
                self.svgdefout += [svgdefs]
            if html is not None:
                if layer in self.htmlout:
                    self.htmlout[layer] += [html]
                else:
                    self.htmlout[layer] = [
                     html]
        if js is not None:
            self.scriptout += [js]
        if animate_svg is not None:
            self.animout += [animate_svg]

    def reset_rendered(self):
        self.svgout = []
        self.svgdefout = []
        self.htmlout = {}
        self.scriptout = []
        self.animout = []
        self.svgheader = ''
        self.svgfooter = '\n</svg>\n'
        self.svglayers = {}

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.check_modules_layers()

    def check_modules_layers(self):
        """
        Function to check the consistency of layers in the slide.
        To do so:

        1- Get the number of layers

        2- Resolve string layers to replace 'max' statement with the slide number of layer
           expl: 'range(0-max-1)' or '[0,max]'

        3- Check that layers are consecutive numbers from 0 -> max
        """
        for mid in self.element_keys:
            module = self.contents[mid]
            if isinstance(module.layers, str):
                start = int(module.layers.split(',')[0].replace('range(', ''))
                maxmodulelayers = start
            else:
                maxmodulelayers = max(module.layers)
            if maxmodulelayers > self.num_layers:
                self.num_layers = maxmodulelayers

        layers_in_slide = []
        for mid in self.element_keys:
            module = self.contents[mid]
            if isinstance(module.layers, str):
                if 'range' in module.layers:
                    lmax = self.num_layers + 1
                else:
                    lmax = self.num_layers
                module.add_layers(eval(module.layers.replace('max', str(lmax))))
            for layer in module.layers:
                if layer not in layers_in_slide:
                    layers_in_slide += [layer]

        layers_in_slide = sorted(layers_in_slide)
        if layers_in_slide != list(range(0, self.num_layers + 1)):
            raise ValueError('Layers are not consecutive. I got %s, I should have %s' % (str(layers_in_slide),
             str(list(range(0, self.num_layers + 1)))))
        for mid in self.element_keys:
            if self.contents[mid].type == 'group':
                logging.debug('Run propagate layer for %s' % str(self.contents[mid].name))
                self.contents[mid].propagate_layers()

    def show(self):
        from beampy.exports import display_matplotlib
        display_matplotlib(self.id, True)

    def build_layout(self):
        """
            Function to build the layout of the slide,
            elements defined in bacground inside the theme file
        """
        if self.render_layout:
            if self.args['layout'] is not None:
                if 'function' in str(type(self.args['layout'])):
                    set_curentslide(self.id)
                    curgroup = self.contents[self.cur_group_id]
                    first_elem_i = len(self.element_keys)
                    first_elem_in_group = len(curgroup.elementsid)
                    self.args['layout']()
                    created_element_keys = self.element_keys[first_elem_i:]
                    self.element_keys = created_element_keys + self.element_keys[:first_elem_i]
                    curgroup.elementsid = curgroup.elementsid[first_elem_in_group:] + curgroup.elementsid[:first_elem_in_group]
                    for eid in created_element_keys:
                        self.contents[eid].add_layers(list(range(self.num_layers + 1)))

                    set_lastslide()

    def newrender(self):
        """
            Render the slide content.
            - Transform module to svg or html
            - Loop over groups
            - Place modules
            - write the final svg
        """
        print('--------------------' + ' slide_%i ' % self.num + '--------------------')
        if self.title_element is not None:
            self.title_element.add_layers(list(range(self.num_layers + 1)))
        for i, key in enumerate(self.element_keys):
            elem = self.contents[key]
            if elem.type != 'group':
                if not elem.rendered:
                    elem.pre_render()
                    elem.run_render()
                assert elem.width.value is not None
                if not elem.height.value is not None:
                    raise AssertionError
            else:
                elem.pre_render()

        print('Number of group levels %i' % max(self.groupsid))
        for level in range(max(self.groupsid), -1, -1):
            for curgroupid in self.groupsid[level]:
                curgroup = self.contents[curgroupid]
                curgroup.compute_group_size()
                curgroup.render()

            if level == 0:
                curgroup.positionner.place((document._width, document._height))
                for layer in curgroup.layers:
                    print('export layer %i' % layer)
                    try:
                        self.svglayers[layer] = curgroup.export_svg_layer(layer)
                    except Exception as e:
                        try:
                            print('no svg for layer %i' % layer)
                        finally:
                            e = None
                            del e

                if document._output_format == 'html5':
                    for eid in curgroup.htmlid:
                        elem = self.contents[eid]
                        xgroupsf = sum([self.contents[g].positionner.x['final'] for g in elem.groups_id])
                        ygroupsf = sum([self.contents[g].positionner.y['final'] for g in elem.groups_id])
                        elem.positionner.x['final'] += xgroupsf
                        elem.positionner.y['final'] += ygroupsf
                        for layer in elem.layers:
                            htmlo = elem.export_html()
                            self.add_rendered(html=htmlo, layer=layer)

                if document._guide:
                    available_height = document._height - self.ytop
                    out = ''
                    out += '<g><line x1="400" y1="0" x2="400" y2="600" style="stroke: #777"/></g>'
                    out += '<g><line x1="0" y1="%0.1f" x2="800" y2="%0.1f" style="stroke: #777"/></g>' % (
                     self.ytop + available_height / 2.0, self.ytop + available_height / 2.0)
                    out += '<g><line x1="0" y1="%0.1f" x2="800" y2="%0.1f" style="stroke: #777"/></g>' % (
                     self.ytop, self.ytop)
                    self.add_rendered(svg=out)

        svg_template = '<?xml version="1.0" encoding="utf-8" standalone="no"?>\n        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n        <svg width=\'{width}px\' height=\'{height}px\' style=\'background-color: {bgcolor};\'\n        xmlns="http://www.w3.org/2000/svg" version="1.2" baseProfile="full"\n        xmlns:xlink="http://www.w3.org/1999/xlink"\n        xmlns:dc="http://purl.org/dc/elements/1.1/"\n        xmlns:cc="http://creativecommons.org/ns#"\n        xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n        shape-rendering="geometricPrecision"\n        >'
        header_template = svg_template.format(width=(document._width), height=(document._height),
          bgcolor=(self.args['background']))
        self.svgheader = header_template


class beampy_module(object):
    __doc__ = '\n        Base class for creating a module\n\n        Each module need a render method and need to return a register\n    '
    rendered = False
    positionner = None
    content = None
    type = None
    name = None
    args = {}
    svgout = None
    htmlout = None
    jsout = None
    animout = None
    call_cmd = ''
    call_lines = ''
    id = None
    uid = None
    group_id = None
    start_line = 0
    stop_line = 0
    x = 0
    y = 0
    width = None
    height = None
    svg_decoration = ''
    args_for_cache_id = None
    special_kwargs = {'parent_slide_id': None}
    cache = True
    slide_id = None
    svgdefs = []
    svgdefsargs = []

    def __init__(self, **kargs):
        self.check_args_from_theme(kargs)
        self.register()
        print('Base class for a new module')

    def register(self, auto_render=False):
        self.load_special_kwargs()
        if self.parent_slide_id is None:
            self.slide_id = gcs()
        else:
            self.slide_id = self.parent_slide_id
        self.groups_id = []
        self.name = self.get_name()
        self.id = create_element_id(self)
        _log.debug('%s(id=%s) store the slide id: %s' % (self.name, self.id, self.slide_id))
        self.layers = [
         0]
        self.exported = False
        self.svgdefs = []
        self.out_svgdefs = None
        self.svgdefsargs = []
        document._slides[self.slide_id].add_module(self.id, self)
        self.positionner = positionner(self.x, self.y, self.width, self.height, self.id, self.slide_id)
        self.top = self.positionner.top
        self.bottom = self.positionner.bottom
        self.left = self.positionner.left
        self.right = self.positionner.right
        self.center = self.positionner.center
        self.update_size(self.width, self.height)
        try:
            start, stop, source = get_command_line(self.name)
        except:
            start = 0
            stop = 0
            source = 'None'

        self.call_cmd = source
        self.call_lines = (start, stop)
        if auto_render:
            self.rendered or self.pre_render()
            self.run_render()
            assert self.width.value is not None
            assert self.height.value is not None

    def delete(self):
        document._slides[self.slide_id].remove_module(self.id)
        del self

    def reset_outputs(self):
        self.svgout = None
        self.htmlout = None
        self.jsout = None
        self.animout = None
        self.rendered = False
        self.exported = False

    def pre_render(self):
        """
        A method that is called at the begining of the slide.newrender method 
        """
        pass

    def render(self):
        self.svgout = None
        self.htmlout = None
        self.jsout = None
        self.animout = None
        self.rendered = True

    def run_render(self):
        """
            Run the function self.render if the module is not in cache
        """
        slide = document._slides[self.slide_id]
        _log.debug('Render %s(id=%s): with height: %s and width: %s on slide: %s' % (self.name, self.id, self.height, self.width, slide.num))
        if self.cache:
            if document._cache is not None:
                ct_cache = document._cache.is_cached('slide_%i' % slide.num, self)
                if ct_cache:
                    self.rendered = True
                    try:
                        print('Elem [%s ...] from cache' % self.call_cmd.strip()[:20])
                    except:
                        print('Elem %s from cache' % self.name)

            else:
                self.rendered or self.render()
                _log.debug('Add %s(id=%s) cache for slide_id: %s' % (self.name, self.id, slide.num))
                document._cache.add_to_cache('slide_%i' % slide.num, self)
                try:
                    print('Elem [%s ...] rendered' % self.call_cmd.strip()[:20])
                except:
                    print('Elem %s rendered' % self.name)

        else:
            self.rendered or self.render()
            try:
                print('Elem [%s ...] rendered' % self.call_cmd.strip()[:20])
            except:
                print('Elem %s rendered' % self.name)

            self.render_svgdefs()

    def get_name(self):
        name = str(self.__init__.__self__.__class__).split('.')[(-1)]
        if "'>" in name:
            name = name.replace("'>", '')
        return name

    def check_args_from_theme(self, arg_values_dict, parent=None):
        """
            Function to check input function keyword args.

            Functions args are defined in the default_theme.py or if a
            theme is added the new value is taken rather than the
            default one

        Parameters
        ----------
        arg_values_dict: dictionary,
            The key-value dictionary containing function arguments.

        parent: string optional
            The name of the parent beampy_module to also load args 

        """
        self.args = arg_values_dict
        function_name = self.get_name()
        default_dict = document._theme[function_name]
        if parent is not None:
            default_dict = dict(default_dict, **document._theme[parent])
        outdict = {}
        for key, value in arg_values_dict.items():
            if key in default_dict or key in self.special_kwargs:
                outdict[key] = value
                setattr(self, key, value)
            else:
                print('Error the key %s is not defined for %s module' % (key, function_name))
                print_function_args(function_name)
                sys.exit(1)

        for key, value in default_dict.items():
            if key not in outdict:
                setattr(self, key, value)

    def load_special_kwargs(self):
        """

        Load all attributes contained in self.sepcial_kwargs
        dictionnary as attributes of the beampy_module with the
        setattr function.

        """
        for key, value in self.special_kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    def load_extra_args(self, theme_key):
        """
        Function to load default args from the theme for the given theme_key
        and add them to the module
        """
        for key, value in document._theme[theme_key].items():
            if not hasattr(self, key):
                setattr(self, key, value)
                self.args[key] = value

    def load_args(self, kwargs_dict):
        """
            Function to transform input kwargs dict into attribute of the module
        """
        for key, value in kwargs_dict.items():
            setattr(self, key, value)

    def update_size(self, width, height):
        """
            Update the size (width, height) of the current module
        """
        self.positionner.update_size(width, height)
        self.width = self.positionner.width
        self.height = self.positionner.height

    def add_svgdef(self, svgdef, svgdefsargs=None):
        """
        Function to add svg clipPath or filter.

        Parameters:
        -----------

        svgdef: string,
            The svg syntax to add to <defs> environnement. This svg
            syntax could include arguments as python string format
            replacement (like '{width}') that will be replaced by
            their value (store as instance of the class, like
            self.width for '{width}') when render is executed.

        svgdefargs: list of string optional
            The list of arguments as string to format in the svgdef.
        """
        if svgdefsargs is None:
            svgdefsargs = []
        assert isinstance(svgdefsargs, list)
        self.svgdefs += [svgdef]
        self.svgdefsargs += [svgdefsargs]

    def render_svgdefs(self):
        """
        Function to render the svgdefs 
        """
        out_svgdefs = ''
        if len(self.svgdefs) > 0:
            logging.debug('Export svg defs added to module %s' % str(self.name))
            for i, svgdef in enumerate(self.svgdefs):
                out_args = {}
                for args in self.svgdefsargs[i]:
                    out_args[args] = getattr(self, args)

                if out_args != {}:
                    svgdef = (svgdef.format)(**out_args)
                out_svgdefs += svgdef

            logging.debug(out_svgdefs)
        if out_svgdefs != '':
            document._slides[self.slide_id].svgdefout += [out_svgdefs]
        self.out_svgdefs = out_svgdefs

    def __repr__(self):
        out = 'module: %s\n' % self.name
        try:
            out += 'source (lines %i->%i):\n%s\n' % (self.call_lines[0], self.call_lines[1],
             self.call_cmd)
        except:
            out += 'source : fail\n'

        out += 'width: %s, height: %s\n' % (str(self.width.value), str(self.height.value))
        return out

    def export_svg(self):
        """
            function to export rendered svg in a group positionned in the slide
        """
        out = '<g transform="translate(%s,%s)" class="%s">' % (self.positionner.x['final'],
         self.positionner.y['final'], self.name)
        out += self.svgout
        if document._text_box:
            out += '<rect x="0"  y="0" width="%s" height="%s"\n            style="stroke:#009900;stroke-width: 1;stroke-dasharray: 10 5;\n            fill: none;" />' % (self.positionner.width.value,
             self.positionner.height.value)
        if self.svg_decoration != '':
            out += self.svg_decoration.format(width=(self.positionner.width.value), height=(self.positionner.height.value))
        out += '</g>'
        return out

    def export_svg_def(self):
        """
            function to export rendered svg in a group positionned in the slide
        """
        out = '<g id="%s" transform="translate(%s,%s)" class="%s" >' % (self.id,
         self.positionner.x['final'],
         self.positionner.y['final'],
         self.name)
        out += self.svgout
        if document._text_box:
            out += '<rect x="0"  y="0" width="%s" height="%s"\n            style="stroke:#009900;stroke-width: 1;stroke-dasharray: 10 5;\n            fill: none;" />' % (self.positionner.width.value,
             self.positionner.height.value)
        if self.svg_decoration != '':
            out += self.svg_decoration.format(width=(self.positionner.width.value), height=(self.positionner.height.value))
        out += '</g>'
        logging.debug(str(self.name), type(out))
        return out

    def export_html(self):
        out = '<div style="visibility: hidden; position: absolute; left: %spx; top: %spx;"> %s </div></br>'
        out = out % (self.positionner.x['final'], self.positionner.y['final'], self.htmlout)
        return out

    def export_animation(self):
        if isinstance(self.animout, list):
            frames_svg_cleaned, all_images = pre_cache_svg_image(self.animout)
            animout = {}
            animout['header'] = '%s' % ''.join(all_images)
            animout['config'] = {'autoplay':self.autoplay,  'fps':self.fps}
            animout['anim_num'] = self.anim_num
            animout['frames'] = frames_svg_cleaned
            return animout

    def export_animation_layer(self, layer):
        out = '<g id="svganimate_{slide}-{layer}_{id_anim}" transform="translate({x},{y})" onclick="Beampy.animatesvg({id_anim},{fps},{anim_size});" data-slide={slide} data-anim={id_anim} data-fps={fps} data-lenght={anim_size}>{frame_init}</g>'
        out = out.format(slide=(self.slide_id), layer=layer, id_anim=(self.anim_num), x=(self.positionner.x['final']), y=(self.positionner.y['final']),
          fps=(self.fps),
          anim_size=(len(self.animout)),
          frame_init=(self.animout[0]))
        return out

    def add_border(self, svg_style={'stroke':'red', 
 'fill':'none',  'stroke-width':0.5}):
        """
            function to add a border to the given element
        """
        output = '<rect x="0" y="0" width="{width}" height="{height}" '
        for key in svg_style:
            output += '%s="%s" ' % (key, svg_style[key])

        output += ' />'
        self.svg_decoration = output

    def add_layers(self, layerslist):
        """
        Function to add this elements to given layers
        :param layerslist: list of layers where the module should be printed
        :return:
        """
        logging.debug('layer list %s' % str(layerslist))
        self.layers = layerslist

    def __call__(self, *args, **kwargs):
        print('Not implemented')

    def __getitem__(self, item):
        """
        Manage layer of a given module using the python getitem syntax
        with slicing

        self()[0] -> layer(0)
        self()[:1] -> layer(0,1)
        self()[1:3] -> layer(1,2,3)
        self()[2:] -> layer(2,..,max(layer))
        """
        if isinstance(item, slice):
            if item.step is None:
                step = 1
            else:
                step = item.step
            if item.start is None:
                start = 0
            else:
                start = item.start
                if start < 0:
                    start = 'max%i' % start
                elif item.stop is None or item.stop > 100000:
                    stop = 'max'
                else:
                    stop = item.stop
                    if stop < 0:
                        stop = 'max%i' % stop
                    elif isinstance(stop, str):
                        if isinstance(start, str):
                            self.add_layers('range(%s,max,%i)' % (start, step))
                        else:
                            self.add_layers('range(%i,max,%i)' % (start, step))
                    elif isinstance(start, str):
                        self.add_layers('range(%s,%i,%i)' % (start, stop + 1, step))
                    else:
                        self.add_layers(list(range(start, item.stop + 1, step)))
        else:
            if isinstance(item, list) or isinstance(item, tuple):
                string_layers = False
                item = list(item)
                for i, it in enumerate(item):
                    if it < 0:
                        item[i] = 'max%i+1' % it
                        string_layers = True
                    if isinstance(it, str):
                        string_layers = True

                if string_layers:
                    self.add_layers(str(item).replace("'", ''))
                else:
                    self.add_layers(item)
            else:
                if item < 0:
                    item = 'max%i+1' % item
                elif isinstance(item, str):
                    self.add_layers('[%s]' % item)
                else:
                    self.add_layers([item])
        return self

    def __len__(self):
        return 0

    def __enter__(self):
        """
        Implement __enter__ __exit__ to pass the string input of
        the function as comment inside a "with" statement to an input
        of the function via the "process_with" method

        with beampy_module():
            '''
            This text will be stored in the self.input 
            '''

            "this one also"
        """
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.start_line = traceback.lineno
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        previous_frame = inspect.currentframe().f_back
        traceback = inspect.getframeinfo(previous_frame)
        self.stop_line = traceback.lineno
        self.process_with()

    def process_with(self):
        """
        Function called by the __exit__ function

        Need to be redefined by each module to adjust the behaviours
        of "with :"
        """
        print('With statement not implemented for this module')

    def above(self, other_element):
        """
        Set the current module to appears above the other_element_id.
        """
        if not isinstance(other_element, beampy_module):
            raise AssertionError
        elif self.type == 'group':
            pid = self.parentid
        else:
            pid = self.group_id
        curgroup = document._slides[self.slide_id].contents[pid]
        other_pos = curgroup.exports_id.index(other_element.id)
        self_pos = curgroup.exports_id.index(self.id)
        curgroup.exports_id.pop(self_pos)
        curgroup.exports_id.insert(other_pos + 1, self.id)

    def below(self, other_element):
        """
        Set the current module to appears beow the othe_element
        """
        if not isinstance(other_element, beampy_module):
            raise AssertionError
        elif self.type == 'group':
            pid = self.parentid
        else:
            pid = self.group_id
        curgroup = document._slides[self.slide_id].contents[pid]
        other_pos = curgroup.exports_id.index(other_element.id)
        self_pos = curgroup.exports_id.index(self.id)
        curgroup.exports_id.pop(self_pos)
        curgroup.exports_id.insert(other_pos, self.id)

    def first(self):
        """
        Set the current object in the background
        """
        if self.type == 'group':
            pid = self.parentid
        else:
            pid = self.group_id
        curgroup = document._slides[self.slide_id].contents[pid]
        self_pos = curgroup.exports_id.index(self.id)
        curgroup.exports_id.pop(self_pos)
        curgroup.exports_id.insert(0, self.id)

    def last(self):
        """
        Set the current object in the foreground
        """
        if self.type == 'group':
            pid = self.parentid
        else:
            pid = self.group_id
        curgroup = document._slides[self.slide_id].contents[pid]
        self_pos = curgroup.exports_id.index(self.id)
        curgroup.exports_id.pop(self_pos)
        curgroup.exports_id.insert(len(curgroup.exports_id), self.id)


class group(beampy_module):
    __doc__ = "Group Beampy modules together and manipulate them as a group\n\n    Parameters\n    ----------\n\n    elements_to_group : None or list of beampy.base_module, optional\n        List of Beampy module to put inside the group (the default is None).\n        This argument allows to group Beampy modules, when `group` is not used\n        with the python :py:mod:`with` expression.\n\n    x : int or float or {'center', 'auto'} or str, optional\n        Horizontal position for the group (the default is 'center'). See\n        positioning system of Beampy.\n\n    y : int or float or {'center', 'auto'} or str, optional\n        Vertical position for the group (the default is 'auto'). See\n        positioning system of Beampy.\n\n    width : int or float or None, optional\n       Width of the group (the default is None, which implies that the width\n       is computed to fit the group contents width).\n\n    height : int or float or None, optional\n       Height of the group (the default is None). When height is None the\n       height is computed to fit the group contents height.\n\n    background : str or None, optional\n       Svg color name of the background color for the group (the default is None).\n\n    perentid : str or None, optional\n        Beampy id of the parent group (the default is None). This parentid is\n        given automatically by Beampy render.\n\n\n    .. note::\n\n       When the position of a group (`x`, `y`) are relative to a parent group\n       and that the parent group has `width`=None or `height`=None and\n       positions `x` or `y` equal to 'auto' or 'center', the render will use\n       the `slide.curwidth` as `width` and the `document._height` as height.\n       This will produce unexpected positioning of child group.\n\n\n    "

    def __init__(self, elements_to_group=None, x='center', y='auto', width=None, height=None, background=None, parentid=None, parent_slide_id=None, opengroup=True):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.background = background
        self.type = 'group'
        self.content = []
        self.xoffset = 0
        self.yoffset = 0
        self.parentid = parentid
        self.grouplevel = 0
        self.elementsid = []
        self.exports_id = []
        self.element_keys = []
        self.autoxid = []
        self.autoyid = []
        self.manualid = []
        self.htmlid = []
        self.content_layer = {}
        if parent_slide_id is None:
            slide = document._slides[gcs()]
        else:
            self.parent_slide_id = parent_slide_id
            slide = document._slides[self.parent_slide_id]
        if elements_to_group is not None:
            opengroup = False
        if slide.cur_group_level >= 0:
            self.parentid = slide.contents[slide.groupsid[slide.cur_group_level][(-1)]].id
        self.grouplevel = slide.cur_group_level + 1
        if opengroup:
            slide.cur_group_level = self.grouplevel
        self.register(auto_render=False)
        self.group_id = self.id
        self.init_width = self.positionner.width.value
        self.init_height = self.positionner.height.value
        if elements_to_group is not None:
            for e in elements_to_group:
                self.add_elements_to_group(e.id, e)
                if e.group_id is not None:
                    slide.contents[e.group_id].remove_element_in_group(e.id)
                e.group_id = self.id

    def reset_outputs(self):
        """
        Rewrite the reset_outputs function of beampy_module to add content_layer.
        """
        self.svgout = None
        self.htmlout = None
        self.jsout = None
        self.animout = None
        self.rendered = False
        self.exported = False
        self.content_layer = {}

    def __enter__(self):
        if document._slides[self.slide_id].cur_group_level != self.grouplevel:
            document._slides[self.slide_id].cur_group_level = self.grouplevel
        else:
            logging.debug('Enter a new group %s with level: %i' % (self.id,
             self.grouplevel))
            document._slides[self.slide_id].cur_group_id = self.id
            if self.width.value is not None:
                document._slides[self.slide_id].curwidth = self.width.value
            else:
                self.width.value = document._slides[self.slide_id].curwidth
        if self.height.value is not None:
            document._slides[self.slide_id].curheight = self.height.value
        return self

    def __exit__(self, type, value, traceback):
        logging.debug('Exit group %s' % self.id)
        if self.grouplevel >= 1:
            document._slides[self.slide_id].cur_group_level = self.grouplevel - 1
        if self.parentid is not None:
            if document._slides[self.slide_id].contents[self.parentid].width.value is not None:
                document._slides[self.slide_id].curwidth = document._slides[self.slide_id].contents[self.parentid].width.value
        if self.parentid is not None:
            if document._slides[self.slide_id].contents[self.parentid].height.value is not None:
                document._slides[self.slide_id].curheight = document._slides[self.slide_id].contents[self.parentid].height.value
        document._slides[self.slide_id].cur_group_id = self.parentid
        logging.debug('Set current group level to %i' % document._slides[self.slide_id].cur_group_level)

    def add_layers(self, layerslist):
        self.layers = layerslist

    def propagate_layers(self):
        """
        Function to recusivly propagate the layers to group elements
        :return:
        """
        slide = document._slides[self.slide_id]
        for eid in self.elementsid:
            for layer in self.layers:
                if layer not in slide.contents[eid].layers and layer > min(slide.contents[eid].layers):
                    logging.debug('add layer %i to %s' % (layer, slide.contents[eid].name))
                    slide.contents[eid].layers += [layer]

            for elayer in slide.contents[eid].layers:
                if elayer < min(self.layers):
                    slide.contents[eid].layers.pop(slide.contents[eid].layers.index(elayer))

            if slide.contents[eid].type == 'group':
                slide.contents[eid].propagate_layers()

    def add_elements_to_group(self, eid, element):
        is_auto = False
        self.elementsid += [eid]
        self.exports_id += [eid]
        if element.x == 'auto':
            self.autoxid += [eid]
            is_auto = True
        if element.y == 'auto':
            self.autoyid += [eid]
            is_auto = True
        if not is_auto:
            self.manualid += [eid]
        if element.type == 'html':
            self.htmlid += [eid]

    def remove_element_in_group(self, elementid):
        """
        Function to remove element from the group key stores

        :param elementid: The id of the module to remove
        """
        for store in (self.autoxid, self.autoyid, self.manualid, self.htmlid, self.elementsid, self.exports_id):
            if elementid in store:
                store.pop(store.index(elementid))

    def add_svg_content(self, layer, svg):
        if layer in self.content_layer:
            self.content_layer[layer] += [svg]
        else:
            self.content_layer[layer] = [
             svg]
        if layer not in self.layers:
            self.layers += [layer]

    def compute_group_size(self):
        """
        Function to compute the size of a given group 

        Update the size with self.update_size(width, height) at the end
        """
        if self.init_width is None:
            auto_width = document._width
        else:
            auto_width = self.width.value
        if self.init_height is None:
            auto_height = document._height
        else:
            auto_height = self.height.value
        if len(self.autoxid) > 0:
            distribute((self.autoxid), 'hspace', auto_width, offset=(self.xoffset),
              curslide=(document._slides[self.slide_id]))
        if len(self.autoyid) > 0:
            distribute((self.autoyid), 'vspace', auto_height, offset=(self.yoffset),
              curslide=(document._slides[self.slide_id]))
        for elem in self.autoxid + self.autoyid + self.manualid:
            if 'final' not in document._slides[self.slide_id].contents[elem].positionner.x:
                document._slides[self.slide_id].contents[elem].positionner.place((auto_width, auto_height), self.yoffset)

        if self.init_width is None:
            allxw = []
            for eid in self.elementsid:
                ewidth = document._slides[self.slide_id].contents[eid].positionner.width
                ewidth = ewidth.value
                if ewidth is None:
                    print('Width not known for:')
                    print(document._slides[self.slide_id].contents[eid])
                    sys.exit(0)
                allxw += [
                 (document._slides[self.slide_id].contents[eid].positionner.x['final'],
                  ewidth)]

            minx = min([i[0] for i in allxw])
            maxx = max([i[0] + i[1] for i in allxw])
            width = maxx - minx
            self.width.value = width
            for eid in self.elementsid:
                document._slides[self.slide_id].contents[eid].positionner.x['final'] -= minx

        if self.init_height is None:
            allyh = []
            for eid in self.elementsid:
                eheight = document._slides[self.slide_id].contents[eid].height
                eheight = eheight.value
                if eheight is None:
                    print('Height not known for:')
                    print(document._slides[self.slide_id].contents[eid])
                    sys.exit(0)
                allyh += [
                 (document._slides[self.slide_id].contents[eid].positionner.y['final'],
                  eheight)]

            miny = min([i[0] for i in allyh])
            maxy = max([i[0] + i[1] for i in allyh])
            height = maxy - miny
            self.height.value = height
            for eid in self.elementsid:
                document._slides[self.slide_id].contents[eid].positionner.y['final'] -= miny

        self.update_size(self.width, self.height)

    def render(self):
        """
            group render
        """
        slide = document._slides[self.slide_id]
        self.content = []
        for eid in self.exports_id:
            elem = slide.contents[eid]
            if elem.type == 'group':
                for layer in elem.layers:
                    if layer in elem.content_layer:
                        self.add_svg_content(layer, elem.export_svg_layer(layer))

            else:
                if elem.svgout is not None:
                    if not elem.exported:
                        if elem.type == 'html':
                            if document._output_format != 'html5':
                                slide.add_rendered(svgdefs=(elem.export_svg_def()))
                                elem.exported = True
                        else:
                            slide.add_rendered(svgdefs=(elem.export_svg_def()))
                            elem.exported = True
                    for layer in elem.layers:
                        if elem.type == 'html':
                            if document._output_format != 'html5':
                                self.add_svg_content(layer, '<use xlink:href="#{id}"></use>'.format(id=(elem.id)))
                        else:
                            self.add_svg_content(layer, '<use xlink:href="#{id}"></use>'.format(id=(elem.id)))

            if elem.jsout is not None:
                slide.add_rendered(js=(elem.jsout))
            if elem.animout is not None:
                if document._output_format == 'html5':
                    if not elem.exported:
                        tmpanim = elem.export_animation()
                        slide.add_rendered(animate_svg=tmpanim)
                        elem.exported = True
                    for layer in elem.layers:
                        self.add_svg_content(layer, elem.export_animation_layer(layer))

                if elem.type == 'html' and elem.htmlout is not None and self.grouplevel > 0:
                    elem.groups_id += [self.id]
                    elem.x = '%ipx' % elem.positionner.x['final']
                    elem.y = '%ipx' % elem.positionner.y['final']
                    slide.contents[self.parentid].add_elements_to_group(elem.id, elem)

        self.rendered = True

    def export_svg_content_layer(self, layer):
        """
        Function to export group content for a given layer to svg
        :param layer:
        :return:
        """
        if self.background is not None:
            pre_rect = '<rect width="%s" height="%s" style="fill:%s;" />' % (self.width.value,
             self.height.value, self.background)
        else:
            pre_rect = ''
        output = pre_rect + ''.join(self.content_layer[layer])
        return output

    def export_svg_layer(self, layer):
        out = '<g transform="translate(%s,%s)" class="%s" data-layer="%i">' % (self.positionner.x['final'],
         self.positionner.y['final'],
         self.name, layer)
        out += self.export_svg_content_layer(layer)
        if document._text_box:
            out += '<rect x="0"  y="0" width="%s" height="%s"\n              style="stroke:#009900;stroke-width: 1;stroke-dasharray: 10 5;\n              fill: none;" />' % (self.positionner.width.value,
             self.positionner.height.value)
        if self.svg_decoration != '':
            out += self.svg_decoration.format(width=(self.positionner.width.value), height=(self.positionner.height.value))
        out += '</g>'
        return out