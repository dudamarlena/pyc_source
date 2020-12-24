# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/toc.py
# Compiled at: 2019-01-11 12:09:13
# Size of source mod 2**32: 17449 bytes
from beampy.document import document
from beampy.modules.core import beampy_module, group
from beampy.modules.text import text
from beampy.modules.svg import circle, rectangle
from beampy.geometry import center
from beampy.functions import set_curentslide, set_lastslide, render_texts

class tableofcontents(group):
    __doc__ = "Create the table of content for your presentation.\n    This function print the TOC tree as defined in your presentation by\n    the functions: section(), subsection(), subsubsection()\n\n    Parameters\n    ----------\n    \n    sections : list of section number or int, optional\n        List of sections to be displayed (the default is an empty list\n        which displays all the section in the TOC). If an integer is\n        given, only the given section is displayed.\n\n    subsection : boolean, optional\n        Display subsections (the default is True). \n    \n    subsubsection : boolean, optional\n        Display the subsubsections (the default is True).\n\n    currentsection : boolean, optional\n        Highlight the current section (the default is False). When\n        True, all other section (and their subsections/subsubsections)\n        are shaded with the *hidden_opacity* value, except for the\n        subsections/subsubsections of the current section.\n    \n    currentsubsection : boolean, optional\n        Highlight the current subsection (the default is False). Same\n        as *currentsection* except that the subsection/subsubsection\n        not already presented are also shaded.\n\n    hideothersubsection : boolean, optional\n        Hide all the subsections/subsubsections of the section other\n        than the current one (the default is False).\n\n    x : int or float or {'center', 'auto'} or str, optional\n        Horizontal position for the TOC (the default theme sets this\n        to '25px').  See positioning system of Beampy.\n\n    y : int or float or {'center', 'auto'} or str, optional\n        Vertical position for the TOC (the default theme\n        set this to 'center'). See positioning system of Beampy.\n\n    width : int or float or None, optional\n       Width of the TOC (the default is None, which implies that the\n       width is the parent group with).\n\n    height : int or float or None, optional\n       Height of the TOC (the default is None, which implies that the\n       heihgt is the parent group height)\n\n    section_yoffset : int or float, option\n       The vertical offset in pixel between two sections (the default theme\n       sets this value to 50).\n\n    subsection_xoffset : int or float, optional\n       The horizontal offset in pixel between the section and its subsections\n       (the default theme sets this to 20). For subsubsections the\n       xoffset = 2 * subsection_xoffset.\n\n    subsection_yoffset : int or float, optional\n       The vertical offset in pixel between subsections. (the default\n       theme sets this to 10).\n\n    section_style : {'round','square','number'} or None, optional\n       The decoration displayed in front of the sections. (the default\n       theme sets this to 'round').\n       \n       Possible decorcations are:\n       - 'round', display a circle of radius *section_decoration_size*\n         filled with *section_decoration_color* color.\n       - 'square', display a circle of length *2 x section_decoration_size*\n         filled with *section_decoration_color* color.\n       - 'number', display section number with the color *section_number_color*\n       - None, display nothing.\n\n    subsection_style : {'round','square','number'} or None, optional\n       The decoration displayed in front of the subsections. (the default\n       theme sets this to None).\n       \n       Possible decorcations are:\n       - 'round', display a circle of radius *subsection_decoration_size*\n         filled with *subsection_decoration_color* color.\n       - 'square', display a circle of length *2 x subsection_decoration_size*\n         filled with *subsection_decoration_color* color.\n       - 'number', display section number with the color\n         *subsection_text_color*\n       - None, display nothing.\n\n    section_decoration_color : string, option\n       Section decoration color (the default theme sets this to\n       THEME['title']['color']).\n\n    section_decoration_size : int or float, optional\n       Section decoration size in pixel (the default theme sets this to 13).\n\n    section_number_color : string, optional\n       Section number color (the default theme sets this to 'white').\n\n    section_text_color : string, optional\n       Section text color (the default theme sets this to\n       THEME['title']['color']).\n\n    subsection_text_color : string, optional\n       Subsection text color (the default theme sets this to\n       THEME['text']['color']).\n\n    subsection_decoration_color : string, optional\n       Subsection decoration color (the default theme sets this to 'gray').\n\n    subsection_decoration_size : int or float, optional\n       Subsection decoration size in pixel (the default theme sets\n       this to 13/2).\n\n    hidden_opacity : float, optional\n       Hidden element opacity (the default theme sets this to\n       0.2). Opacity is between 0 (fully hidden) to 1.\n\n    "

    def __init__(self, sections=[], subsection=True, subsubsection=True, currentsection=False, currentsubsection=False, hideothersubsection=False, **kwargs):
        self.check_args_from_theme(kwargs)
        super(tableofcontents, self).__init__(x=self.x, y=self.y, width=self.width, height=self.height, opengroup=False)
        self.show_subsection = subsection
        self.currentsection = currentsection
        self.currentsubsection = currentsubsection
        self.hideothersubsection = hideothersubsection
        self.sections = sections
        if not isinstance(self.sections, list):
            self.sections = [
             self.sections]
        if not subsection:
            self.show_subsubsection = False
        else:
            self.show_subsubsection = subsubsection
        self.default_show_subsubsection = self.show_subsubsection
        self.default_show_subsection = self.show_subsection
        self.show_section = True

    def build_toc_tree(self):
        set_curentslide(self.slide_id)
        oldtheme = document._theme['link']
        document._theme['link']['fill'] = 'black'
        secyoffset = self.section_yoffset
        xoffset = self.subsection_xoffset
        yoffset = self.subsection_yoffset
        if self.currentsection or self.currentsubsection:
            vispos = get_visibles_indices(self.slide_id, self.currentsection)
            hidden_opacity = self.hidden_opacity
        else:
            vispos = []
            hidden_opacity = 1
        opacity = 1
        text_elements = []
        with self:
            cpt_section = 1
            prev = None
            section = None
            for i, node in enumerate(document._TOC):
                if node['slide'] <= document._global_counter['slide']:
                    slidelink = '#%i-0' % node['slide']
                else:
                    slidelink = '#%i-0' % document._global_counter['slide']
                if i in vispos:
                    opacity = 1
                else:
                    opacity = hidden_opacity
                if node['level'] == 0 and len(self.sections) > 0:
                    if cpt_section in self.sections:
                        self.show_section = True
                    else:
                        self.show_section = False
                        cpt_section += 1
                    if self.show_section and node['level'] == 0:
                        cpt_subsection = 1
                        if prev is not None:
                            y = prev.bottom + secyoffset
                        else:
                            y = 0
                        if self.hideothersubsection:
                            if i in vispos:
                                self.show_subsection = self.default_show_subsection
                                self.show_subsubsection = self.default_show_subsubsection
                            else:
                                self.show_subsection = False
                                self.show_subsubsection = False
                            deco_x = 0
                            deco_y = y
                            if self.section_style in ('round', 'square'):
                                if self.section_style == 'round':
                                    c = circle(r=self.section_decoration_size, x=0, y=y, opacity=opacity, color=self.section_decoration_color, edgecolor=self.section_decoration_color)
                                else:
                                    c = rectangle(width=self.section_decoration_size * 2, height=self.section_decoration_size * 2, x=0, y=y, opacity=opacity, color=self.section_decoration_color, edgecolor=self.section_decoration_color)
                                tt = text('\\textbf{%i}' % cpt_section, x=c.center + center(0), y=c.center + center(0), color=self.section_number_color, size=self.section_decoration_size)
                                text_elements += [tt]
                                deco_x = c.right + 5
                                deco_y = c.center + center(0)
                            if self.section_style == 'number':
                                c = text('\\textbf{%i}' % cpt_section, x=0, y=y, color=self.section_number_color, size=self.section_decoration_size)
                                text_elements += [c]
                                deco_x = c.right + 5
                                deco_y = c.center + center(0)
                            prev = text('\\href{%s}{%s}' % (slidelink, node['title']), x=deco_x, y=deco_y, color=self.section_text_color, opacity=opacity, width=document._slides[self.slide_id].curwidth - (self.section_decoration_size * 2 + 5))
                            text_elements += [prev]
                            section = prev
                            cpt_section += 1
                        if self.show_subsection and self.show_section and node['level'] == 1:
                            cpt_subsubsection = 1
                            x = node['level'] * xoffset
                            if section is not None:
                                x = section.left + x
                            if prev is not None:
                                y = prev.bottom + yoffset
                            else:
                                y = 0
                            deco_x = x
                            deco_y = y
                            if self.subsection_style == 'number':
                                c = text('%i-%i' % (cpt_section - 1, cpt_subsection), x=x, y=y, color=self.subsection_text_color)
                                text_elements += [c]
                                deco_x = c.right + 5
                                deco_y = c.center + center(0)
                            if self.subsection_style in ('round', 'square'):
                                if self.subsection_style == 'round':
                                    c = circle(r=self.subsection_decoration_size, x=x, y=y, opacity=opacity, color=self.subsection_decoration_color, edgecolor=self.subsection_decoration_color)
                                else:
                                    c = rectangle(width=self.subsection_decoration_size * 2, height=self.subsection_decoration_size * 2, x=x, y=y, opacity=opacity, color=self.subsection_decoration_color, edgecolor=self.subsection_decoration_color)
                                deco_x = c.right + 5
                                deco_y = c.center + center(0)
                            prev = text('\\href{%s}{%s}' % (slidelink, node['title']), x=deco_x, y=deco_y, opacity=opacity, color=self.subsection_text_color)
                            text_elements += [prev]
                            cpt_subsection += 1
                        if self.show_subsubsection and self.show_section and node['level'] == 2:
                            x = node['level'] * xoffset
                            if section is not None:
                                x = section.left + x
                            if prev is not None:
                                y = prev.bottom + yoffset
                            else:
                                y = 0
                            deco_x = x
                            deco_y = y
                            if self.subsection_style == 'number':
                                c = text('%i-%i-%i' % (cpt_section - 1, cpt_subsection - 1,
                                 cpt_subsubsection), x=x, y=y, color=self.subsection_text_color)
                                text_elements += [c]
                                deco_x = c.right + 5
                                deco_y = c.center + center(0)
                            if self.subsection_style in ('round', 'square'):
                                if self.subsection_style == 'round':
                                    c = circle(r=self.subsection_decoration_size, x=x, y=y, opacity=opacity, color=self.subsection_decoration_color, edgecolor=self.subsection_decoration_color)
                                else:
                                    c = rectangle(width=self.subsection_decoration_size * 2, height=self.subsection_decoration_size * 2, x=x, y=y, opacity=opacity, color=self.subsection_decoration_color, edgecolor=self.subsection_decoration_color)
                                deco_x = c.right + 5
                                deco_y = c.center + center(0)
                            prev = text('\\href{%s}{%s}' % (slidelink, node['title']), x=deco_x, y=deco_y, opacity=opacity, color=self.subsection_text_color)
                            text_elements += [prev]
                            cpt_subsubsection += 1

        set_lastslide()
        document._theme['link'] = oldtheme
        return text_elements

    def pre_render(self):
        text_elements = self.build_toc_tree()
        render_texts(text_elements)
        self.propagate_layers()


def get_visibles_indices(slide_id, currentsection=False):
    currenttoc = document._slides[slide_id].TOCposition
    tocposition = document._TOC.index(currenttoc)
    currentlevel = currenttoc['level']
    visiblespos = [
     tocposition]
    while currentlevel != 0 and tocposition > 0:
        tocposition -= 1
        currentlevel = document._TOC[tocposition]['level']
        visiblespos += [tocposition]

    if currentsection:
        max_visiblepos = max(visiblespos)
        maxlevel = document._TOC[max_visiblepos]['level']
        while maxlevel != 0 and max_visiblepos < len(document._TOC) - 1:
            max_visiblepos += 1
            maxlevel = document._TOC[max_visiblepos]['level']
            if maxlevel != 0:
                visiblespos += [max_visiblepos]

    return visiblespos