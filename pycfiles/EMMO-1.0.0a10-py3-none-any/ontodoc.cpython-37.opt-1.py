# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/ontodoc.py
# Compiled at: 2020-04-10 04:40:37
# Size of source mod 2**32: 41723 bytes
"""
A module for documenting ontologies.
"""
import os, re, time, warnings, shlex, shutil, subprocess
from textwrap import dedent
from tempfile import NamedTemporaryFile, TemporaryDirectory
import yaml, owlready2
from .utils import asstring, camelsplit
from .graph import OntoGraph

class OntoDoc:
    __doc__ = 'A class for helping documentating ontologies.\n\n    Parameters\n    ----------\n    onto : Ontology instance\n        The ontology that should be documented.\n    style : dict | "html" | "markdown" | "markdown_tex"\n        A dict defining the following template strings (and substitutions):\n\n        :header: Formats an header.\n            Substitutions: {level}, {label}\n        :link: Formats a link.\n           Substitutions: {name}\n        :point: Formats a point (list item).\n           Substitutions: {point}, {ontology}\n        :points: Formats a list of points.  Used within annotations.\n           Substitutions: {points}, {ontology}\n        :annotation: Formats an annotation.\n            Substitutions: {key}, {value}, {ontology}\n        :substitutions: list of ``(regex, sub)`` pairs for substituting\n            annotation values.\n    '
    _markdown_style = dict(sep='\n',
      figwidth='{{ width={width:.0f}px }}',
      figure='![{caption}]({path}){figwidth}\n',
      header='\n{:#<{level}} {label}',
      link='[{name}]({lowerurl})',
      point='  - {point}\n',
      points='\n\n{points}\n',
      annotation='**{key}:** {value}\n',
      substitutions=[])
    _markdown_tex_extra_style = dict(substitutions=[
     ('∀', '$\\\\forall$'),
     ('∃', '$\\\\exists$'),
     ('∆', '$\\\\nabla$'),
     ('∧', '$\\\\land$'),
     ('∨', '$\\\\lor$'),
     ('∇', '$\\\\nabla$'),
     ('−', '-'),
     ('->', '$\\\\rightarrow$'),
     ('Α', '$\\\\Upalpha$'),
     ('Β', '$\\\\Upbeta$'),
     ('Γ', '$\\\\Upgamma$'),
     ('Δ', '$\\\\Updelta$'),
     ('Ε', '$\\\\Upepsilon$'),
     ('Ζ', '$\\\\Upzeta$'),
     ('Η', '$\\\\Upeta$'),
     ('Θ', '$\\\\Uptheta$'),
     ('Ι', '$\\\\Upiota$'),
     ('Κ', '$\\\\Upkappa$'),
     ('Λ', '$\\\\Uplambda$'),
     ('Μ', '$\\\\Upmu$'),
     ('Ν', '$\\\\Upnu$'),
     ('Ξ', '$\\\\Upxi$'),
     ('Ο', '$\\\\Upomekron$'),
     ('Π', '$\\\\Uppi$'),
     ('Ρ', '$\\\\Uprho$'),
     ('Σ', '$\\\\Upsigma$'),
     ('Τ', '$\\\\Uptau$'),
     ('Υ', '$\\\\Upupsilon$'),
     ('Φ', '$\\\\Upvarphi$'),
     ('Χ', '$\\\\Upchi$'),
     ('Ψ', '$\\\\Uppsi$'),
     ('Ω', '$\\\\Upomega$'),
     ('α', '$\\\\upalpha$'),
     ('β', '$\\\\upbeta$'),
     ('γ', '$\\\\upgamma$'),
     ('δ', '$\\\\updelta$'),
     ('ε', '$\\\\upepsilon$'),
     ('ζ', '$\\\\upzeta$'),
     ('η', '$\\\\upeta$'),
     ('θ', '$\\\\uptheta$'),
     ('ι', '$\\\\upiota$'),
     ('κ', '$\\\\upkappa$'),
     ('λ', '$\\\\uplambda$'),
     ('μ', '$\\\\upmu$'),
     ('ν', '$\\\\upnu$'),
     ('ξ', '$\\\\upxi$'),
     ('ο', 'o'),
     ('π', '$\\\\uppi$'),
     ('ρ', '$\\\\uprho$'),
     ('ς', '$\\\\upvarsigma$'),
     ('σ', '$\\\\upsigma$'),
     ('τ', '$\\\\uptau$'),
     ('υ', '$\\\\upupsilon$'),
     ('φ', '$\\\\upvarphi$'),
     ('χ', '$\\\\upchi$'),
     ('ψ', '$\\\\uppsi$'),
     ('ω', '$\\\\upomega$'),
     ('ή', '$\\\\acute{\\\\upeta}$'),
     ('ḗ', '$\\\\acute{\\\\bar{\\\\mathrm{e}}}$'),
     ('ά', '$\\\\acute{\\\\upalpha}$'),
     ('á', '$\\\\acute{\\\\mathrm{a}}$'),
     ('ό', '$\\\\acute{o}$'),
     ('ō', '$\\\\bar{\\\\mathrm{o}}$'),
     ('ὅ', '$\\\\acute{o}$')])
    _html_style = dict(sep='<p>\n',
      figwidth='width="{width:.0f}"',
      figure='<img src="{path}" alt="{caption}"{figwidth}>',
      header='<h{level} id="{lowerlabel}">{label}</h{level}>',
      link='<a href="{lowerurl}">{name}</a>',
      point='      <li>{point}</li>\n',
      points='    <ul>\n      {points}\n    </ul>\n',
      annotation='  <dd><strong>{key}:</strong>\n{value}  </dd>\n',
      substitutions=[
     ('\\n\\n', '<p>'),
     ('\\n', '<br>\\n'),
     ('&', '&#8210;'),
     ('<p>', '<p>\\n\\n'),
     ('\\u2018([^\\u2019]*)\\u2019', '<q>\\1</q>'),
     ('\\u2019', "'"),
     ('\\u2260', '&ne;'),
     ('\\u2264', '&le;'),
     ('\\u2265', '&ge;'),
     ('\\u226A', '&x226A;'),
     ('\\u226B', '&x226B;'),
     ('"Y$', '')])

    def __init__(self, onto, style='markdown'):
        if isinstance(style, str):
            if style == 'markdown_tex':
                style = self._markdown_style.copy()
                style.update(self._markdown_tex_extra_style)
            else:
                style = getattr(self, '_%s_style' % style)
        self.onto = onto
        self.style = style
        self.url_regex = re.compile('https?:\\/\\/[^\\s ]+')

    def get_default_template(self):
        """Returns default template."""
        title = os.path.splitext(os.path.basename(self.onto.base_iri.rstrip('/#')))[0]
        irilink = self.style.get('link', '{name}').format(name=(self.onto.base_iri),
          url=(self.onto.base_iri),
          lowerurl=(self.onto.base_iri))
        s = dedent('        %HEADER {title}\n        Documentation of {irilink}\n\n        %HEADER Relations level=2\n        %ALL object_properties\n\n        %HEADER Classes level=2\n        %ALL classes\n\n        %HEADER Individuals level=2\n        %ALL individuals\n\n        %HEADER Appendix               level=1\n        %HEADER "Relation taxonomies"  level=2\n        %ALLFIG object_properties\n\n        %HEADER "Class taxonomies"     level=2\n        %ALLFIG classes\n        ').format(ontology=(self.onto), title=title, irilink=irilink)
        return s

    def get_header(self, label, header_level=1):
        """Returns `label` formatted as a header of given level."""
        header_style = self.style.get('header', '{label}\n')
        return header_style.format('',
          level=header_level, label=label, lowerlabel=(label.lower()))

    def get_figure(self, path, caption='', width=None):
        """Returns a formatted insert-figure-directive."""
        figwidth_style = self.style.get('figwidth', '')
        figure_style = self.style.get('figure', '')
        figwidth = figwidth_style.format(width=width) if width else ''
        return figure_style.format(path=path, caption=caption, figwidth=figwidth)

    def itemdoc(self, item, header_level=3, show_disjoints=False):
        """Returns documentation of `item`.

        Parameters
        ----------
        item : obj | label
            The class, individual or relation to document.
        header_level : int
            Header level. Defaults to 3.
        show_disjoints : Bool
            Whether to show `disjoint_with` relations.
        """
        onto = self.onto
        if isinstance(item, str):
            item = self.onto.get_by_label(item)
        else:
            header_style = self.style.get('header', '{label}\n')
            link_style = self.style.get('link', '{name}')
            point_style = self.style.get('point', '{point}')
            points_style = self.style.get('points', '{points}')
            annotation_style = self.style.get('annotation', '{key}: {value}\n')
            substitutions = self.style.get('substitutions', [])
            order = dict(definition='00', axiom='01', theorem='02', elucidation='03',
              domain='04',
              range='05',
              example='06')
            doc = []
            label = item.label.first()
            doc.append(header_style.format('',
              level=header_level, label=label, lowerlabel=(label.lower())))
            doc.append(annotation_style.format(key='IRI',
              value=(asstring(item.iri, link_style)),
              ontology=onto))
            if isinstance(item, owlready2.Thing):
                annotations = item.get_individual_annotations()
            else:
                annotations = item.get_annotations()
        for key in sorted((annotations.keys()), key=(lambda key: order.get(key, key))):
            for value in annotations[key]:
                if self.url_regex.match(value):
                    doc.append(annotation_style.format(key=(key.capitalize()),
                      value=(asstring(value, link_style))))
                else:
                    for reg, sub in substitutions:
                        value = re.sub(reg, sub, value)

                    doc.append(annotation_style.format(key=(key.capitalize()),
                      value=value))

        points = []
        nonProp = (
         owlready2.ThingClass,
         owlready2.And, owlready2.Or, owlready2.Not)
        for p in item.is_a:
            if not isinstance(p, nonProp):
                if isinstance(item, owlready2.PropertyClass):
                    if isinstance(p, owlready2.PropertyClass):
                        points.append(point_style.format(point=('is_a ' + asstring(p, link_style)),
                          ontology=onto))
                points.append(point_style.format(point=(asstring(p, link_style)),
                  ontology=onto))

        for e in item.equivalent_to:
            points.append(point_style.format(point=('equivalent_to ' + asstring(e, link_style))))

        if show_disjoints:
            if hasattr(item, 'disjoint_with'):
                s = set(item.disjoint_with(reduce=True))
                points.append(point_style.format(point=('disjoint_with ' + ', '.join((asstring(e, link_style) for e in s))),
                  ontology=onto))
        if hasattr(item, 'disjoint_unions'):
            for u in item.disjoint_unions:
                s = ', '.join((asstring(e, link_style) for e in u))
                points.append(point_style.format(point=('disjoint_union_of ' + s),
                  ontology=onto))

        if hasattr(item, 'inverse_property'):
            if item.inverse_property:
                points.append(point_style.format(point=('inverse_of ' + asstring(item.inverse_property, link_style))))
        for d in getattr(item, 'domain', ()):
            points.append(point_style.format(point=('domain ' + asstring(d, link_style))))

        for d in getattr(item, 'range', ()):
            points.append(point_style.format(point=('range ' + asstring(d, link_style))))

        if points:
            value = points_style.format(points=(''.join(points)),
              ontology=onto)
            doc.append(annotation_style.format(key='Relations',
              value=value,
              ontology=onto))
        if hasattr(item, 'instances'):
            points = []
            for e in [i for i in item.instances() if item in i.is_instance_of]:
                points.append(point_style.format(point=(asstring(e, link_style)),
                  ontology=onto))

            if points:
                value = points_style.format(points=(''.join(points)),
                  ontology=onto)
                doc.append(annotation_style.format(key='Individuals',
                  value=value,
                  ontology=onto))
        return '\n'.join(doc)

    def itemsdoc(self, items, header_level=3):
        """Returns documentation of `items`."""
        sep_style = self.style.get('sep', '\n')
        doc = []
        for item in items:
            doc.append(self.itemdoc(item, header_level))
            doc.append(sep_style.format(ontology=(self.onto)))

        return '\n'.join(doc)


class attrdict(dict):
    __doc__ = 'A dict with attribute access.\n\n    Note that methods like key() and update() may be overridden.'

    def __init__(self, *args, **kwargs):
        (super(attrdict, self).__init__)(*args, **kwargs)
        self.__dict__ = self


class InvalidTemplateError(NameError):
    __doc__ = 'Raised on errors in template files.'


def get_options(opts, **kw):
    """Returns a dict with options from the sequence `opts` with
    "name=value" pairs. Valid option names and default values are
    provided with the keyword arguments."""
    d = attrdict(kw)
    for opt in opts:
        if '=' not in opt:
            raise InvalidTemplateError('Missing "=" in template option: %r' % opt)
        name, value = opt.split('=', 1)
        if name not in d:
            raise InvalidTemplateError('Invalid template option: %r' % name)
        t = type(d[name])
        d[name] = t(value)

    return d


class DocPP:
    __doc__ = 'Documentation pre-processor.\n\n    It supports the following features:\n\n      * Comment lines\n\n            %% Comment line...\n\n      * Insert header with given level\n\n            %HEADER label [level=1]\n\n      * Insert figure with optional caption and width. `filepath`\n        should be relative to `basedir`.  If width is 0, no width will\n        be specified.\n\n            %FIGURE filepath [caption=\'\' width=0px]\n\n      * Include other markdown files.  Header levels may be up or down with\n        `shift`\n\n            %INCLUDE filepath [shift=0]\n\n      * Insert generated documentation for ontology entity.  The header\n        level may be set with `header_level`.\n\n            %ENTITY name [header_level=3]\n\n      * Insert generated documentation for ontology branch `name`.  Options:\n          - header_level: Header level.\n          - terminated: Whether to branch should be terminated at all branch\n            names in the final document.\n          - include_leafs: Whether to include leaf.\n\n            %BRANCH name [header_level=3 terminated=1 include_leafs=0]\n\n      * Insert generated figure of ontology branch `name`.  The figure\n        is written to `path`.  The default path is `figdir`/`name`,\n        where `figdir` is given at class initiation. It is recommended\n        to exclude the file extension from `path`.  In this case, the\n        default figformat will be used (and easily adjusted to the\n        correct format required by the backend). `leafs` may be a comma-\n        separated list of leaf node names.\n\n            %BRANCHFIG name [path=\'\' caption=\'\' terminated=1 include_leafs=1\n                             strict_leafs=1, width=0px leafs=\'\' relations=all\n                             edgelabels=0]\n\n      * This is a combination of the %HEADER and %BRANCHFIG directives.\n\n            %BRANCHHEAD name [level=2  path=\'\' caption=\'\' terminated=1\n                              include_leafs=1 width=0px leafs=\'\']\n\n      * This is a combination of the %HEADER, %BRANCHFIG and %BRANCH\n        directives. It inserts documentation of branch `name`, with a\n        header followed by a figure and then documentation of each\n        element.\n\n            %BRANCHDOC name [level=2  path=\'\' caption=\'\' terminated=1\n                             width=0px leafs=\'\']\n\n      * Insert generated documentation for all entities of the given type.\n        Valid values of `type` are: "classes", "individuals",\n        "object_properties", "data_properties", "annotations_properties"\n\n            %ALL type [header_level=3]\n\n      * Insert generated figure of all entities of the given type.\n        Valid values of `type` are: "classes", "object_properties" and\n        "data_properties".\n\n            %ALLFIG type\n\n    Parameters\n    ----------\n    template : str\n        Input template.\n    ontodoc : OntoDoc instance\n        Instance of OntoDoc\n    basedir : str\n        Base directory for including relative file paths.\n    figdir : str\n        Default directory to store generated figures.\n    figformat : str\n        Default format for generated figures.\n    figscale : float\n        Default scaling of generated figures.\n    maxwidth : float\n        Maximum figure width.  Figures larger than this will be rescaled.\n\n    '

    def __init__(self, template, ontodoc, basedir='.', figdir='genfigs', figformat='png', figscale=1.0, maxwidth=None):
        self.lines = template.split('\n')
        self.ontodoc = ontodoc
        self.basedir = basedir
        self.figdir = os.path.join(basedir, figdir)
        self.figformat = figformat
        self.figscale = figscale
        self.maxwidth = maxwidth
        self._branch_cache = None
        self._processed = False

    def __str__(self):
        return self.get_buffer()

    def get_buffer(self):
        """Returns the current buffer."""
        return '\n'.join(self.lines)

    def copy(self):
        """Returns a copy of self."""
        docpp = DocPP('', (self.ontodoc), (self.basedir), figformat=(self.figformat), figscale=(self.figscale),
          maxwidth=(self.maxwidth))
        docpp.lines[:] = self.lines
        docpp.figdir = self.figdir
        return docpp

    def get_branches(self):
        """Returns a list with all branch names as specified with %BRANCH
        (in current and all included documents).  The returned value is
        cached for efficiency purposes and so that it is not lost after
        processing branches."""
        if self._branch_cache is None:
            names = []
            docpp = self.copy()
            docpp.process_includes()
            for line in docpp.lines:
                if line.startswith('%BRANCH'):
                    names.append(shlex.split(line)[1])

            self._branch_cache = names
        return self._branch_cache

    def shift_header_levels(self, shift):
        """Shift header level of all hashtag-headers in buffer.  Underline
        headers are ignored."""
        if not shift:
            return
        pat = re.compile('^#+ ')
        for i, line in enumerate(self.lines):
            m = pat.match(line)
            if m:
                if shift > 0:
                    self.lines[i] = '#' * shift + line
                elif shift < 0:
                    n = m.end()
                    if shift > n:
                        self.lines[i] = line.lstrip('# ')
                    else:
                        self.lines[i] = line[n:]

    def process_comments(self):
        """Strips out comment lines starting with "%%"."""
        self.lines = [line for line in self.lines if not line.startswith('%%')]

    def process_headers(self):
        """Expand all %HEADER specifications."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%HEADER '):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options((tokens[2:]), level=1)
                del self.lines[i]
                self.lines[i:i] = self.ontodoc.get_header(name, int(opts.level)).split('\n')

    def process_figures(self):
        """Expand all %FIGURE specifications."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%FIGURE '):
                tokens = shlex.split(line)
                path = tokens[1]
                opts = get_options((tokens[2:]), caption='', width=0)
                del self.lines[i]
                self.lines[i:i] = self.ontodoc.get_figure((os.path.join(self.basedir, path)),
                  caption=(opts.caption),
                  width=(opts.width)).split('\n')

    def process_entities(self):
        """Expand all %ENTITY specifications."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%ENTITY '):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options((tokens[2:]), header_level=3)
                del self.lines[i]
                self.lines[i:i] = self.ontodoc.itemdoc(name, int(opts.header_level)).split('\n')

    def process_branches(self):
        """Expand all %BRANCH specifications."""
        names = self.get_branches()
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%BRANCH '):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options((tokens[2:]), header_level=3, terminated=1, include_leafs=0)
                leafs = names if opts.terminated else ()
                branch = self.ontodoc.onto.get_branch(name, leafs, opts.include_leafs)
                del self.lines[i]
                self.lines[i:i] = self.ontodoc.itemsdoc(branch, int(opts.header_level)).split('\n')

    def _make_branchfig(self, name, path, terminated, include_leafs, strict_leafs, width, leafs, relations, edgelabels, rankdir, legend):
        """Help method for process_branchfig().

        Args:
            name: name of branch root
            path: optional figure path name
            include_leafs: whether to include leafs
            strict_leafs: whether strictly exclude leafs descendants
            terminated: whether the graph should be terminated at leaf nodes
            width: optional figure width
            leafs: optional leafs node names for graph termination
            relations: comma-separated list of relations to include
            edgelabels: whether to include edgelabels
            rankdir: graph direction (BT, TB, RL, LR)
            legend: whether to add legend

        Returns:
            filepath: path to generated figure
            leafs: used list of leaf node names
            width: actual figure width
        """
        onto = self.ontodoc.onto
        if leafs:
            if isinstance(leafs, str):
                leafs = leafs.split(',')
        elif terminated:
            leafs = set(self.get_branches())
            leafs.discard(name)
        else:
            leafs = None
        if path:
            figdir = os.path.dirname(path)
            formatext = os.path.splitext(path)[1]
            if formatext:
                format = formatext.lstrip('.')
            else:
                format = self.figformat
                path += '.' + format
        else:
            figdir = self.figdir
            format = self.figformat
            term = 'T' if terminated else ''
            path = os.path.join(figdir, name + term) + '.' + format
        graph = OntoGraph(onto, graph_attr={'rankdir': rankdir})
        graph.add_branch(root=name, leafs=leafs, include_leafs=include_leafs, strict_leafs=strict_leafs,
          relations=relations,
          edgelabels=edgelabels)
        if legend:
            graph.add_legend()
        figwidth, figheight = width or graph.get_figsize()
        width = self.figscale * figwidth
        if self.maxwidth:
            if width > self.maxwidth:
                width = self.maxwidth
        filepath = os.path.join(self.basedir, path)
        destdir = os.path.dirname(filepath)
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        graph.save(filepath, format=format)
        return (filepath, leafs, width)

    def process_branchfigs(self):
        """Process all %BRANCHFIG directives."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%BRANCHFIG '):
                tokens = shlex.split(line)
                name = tokens[1]
                opts = get_options((tokens[2:]),
                  path='', caption='', terminated=1, include_leafs=1,
                  strict_leafs=1,
                  width=0,
                  leafs='',
                  relations='all',
                  edgelabels=0,
                  rankdir='BT',
                  legend=1)
                filepath, leafs, width = self._make_branchfig(name, opts.path, opts.terminated, opts.include_leafs, opts.strict_leafs, opts.width, opts.leafs, opts.relations, opts.edgelabels, opts.rankdir, opts.legend)
                del self.lines[i]
                self.lines[i:i] = self.ontodoc.get_figure(filepath,
                  caption=(opts.caption), width=width).split('\n')

    def process_branchdocs(self):
        """Process all %BRANCHDOC and  %BRANCHEAD directives."""
        onto = self.ontodoc.onto
        for i, line in reversed(list(enumerate(self.lines))):
            if not line.startswith('%BRANCHDOC '):
                if line.startswith('%BRANCHHEAD '):
                    with_branch = True if line.startswith('%BRANCHDOC ') else False
                    tokens = shlex.split(line)
                    name = tokens[1]
                    title = camelsplit(name)
                    title = title[0].upper() + title[1:] + ' branch'
                    opts = get_options((tokens[2:]), level=2, path='', title=title, caption=(title + '.'),
                      terminated=1,
                      strict_leafs=1,
                      width=0,
                      leafs='',
                      relations='all',
                      edgelabels=0,
                      rankdir='BT',
                      legend=1)
                    include_leafs = 1
                    filepath, leafs, width = self._make_branchfig(name, opts.path, opts.terminated, include_leafs, opts.strict_leafs, opts.width, opts.leafs, opts.relations, opts.edgelabels, opts.rankdir, opts.legend)
                    sec = []
                    sec.append(self.ontodoc.get_header(opts.title, int(opts.level)))
                    sec.append(self.ontodoc.get_figure(filepath, caption=(opts.caption), width=width))
                    if with_branch:
                        include_leafs = 0
                        branch = onto.get_branch(name, leafs, include_leafs)
                        sec.append(self.ontodoc.itemsdoc(branch, int(opts.level + 1)))
                del self.lines[i]
                self.lines[i:i] = sec

    def process_alls(self):
        """Expand all %ALL specifications."""
        onto = self.ontodoc.onto
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%ALL '):
                tokens = shlex.split(line)
                type = tokens[1]
                opts = get_options((tokens[2:]), header_level=3)
                if type == 'classes':
                    items = onto.classes()
                else:
                    if type in ('object_properties', 'relations'):
                        items = onto.object_properties()
                    else:
                        if type == 'data_properties':
                            items = onto.data_properties()
                        else:
                            if type == 'annotation_properties':
                                items = onto.annotation_properties()
                            else:
                                if type == 'individuals':
                                    items = onto.individuals()
                                else:
                                    raise InvalidTemplateError('Invalid argument to %%ALL: %s' % type)
                items = sorted(items, key=(lambda x: asstring(x)))
                del self.lines[i]
                self.lines[i:i] = self.ontodoc.itemsdoc(items, int(opts.header_level)).split('\n')

    def process_allfig(self):
        """Process all %ALLFIG directives."""
        onto = self.ontodoc.onto
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%ALLFIG '):
                tokens = shlex.split(line)
                type = tokens[1]
                opts = get_options((tokens[2:]), path='', level=3, terminated=0, include_leafs=1,
                  strict_leafs=1,
                  width=0,
                  leafs='',
                  relations='isA',
                  edgelabels=0,
                  rankdir='BT',
                  legend=1)
                if type == 'classes':
                    roots = onto.get_root_classes()
                else:
                    if type in ('object_properties', 'relations'):
                        roots = onto.get_root_object_properties()
                    else:
                        if type == 'data_properties':
                            roots = onto.get_root_data_properties()
                        else:
                            raise InvalidTemplateError('Invalid argument to %%ALL: %s' % type)
                sec = []
                for root in roots:
                    name = asstring(root)
                    filepath, leafs, width = self._make_branchfig(name, opts.path, opts.terminated, opts.include_leafs, opts.strict_leafs, opts.width, opts.leafs, opts.relations, opts.edgelabels, opts.rankdir, opts.legend)
                    title = 'Taxonomy of %s.' % name
                    sec.append(self.ontodoc.get_header(title, int(opts.level)))
                    caption = 'Taxonomy of %s.' % name
                    sec.extend(self.ontodoc.get_figure(filepath,
                      caption=caption, width=width).split('\n'))

                del self.lines[i]
                self.lines[i:i] = sec

    def process_includes(self):
        """Process all %INCLUDE directives."""
        for i, line in reversed(list(enumerate(self.lines))):
            if line.startswith('%INCLUDE '):
                tokens = shlex.split(line)
                filepath = tokens[1]
                opts = get_options((tokens[2:]), shift=0)
                with open(os.path.join(self.basedir, filepath), 'rt') as (f):
                    docpp = DocPP((f.read()),
                      (self.ontodoc), basedir=(os.path.dirname(filepath)),
                      figformat=(self.figformat),
                      figscale=(self.figscale),
                      maxwidth=(self.maxwidth))
                    docpp.figdir = self.figdir
                if opts.shift:
                    docpp.shift_header_levels(int(opts.shift))
                docpp.process()
                del self.lines[i]
                self.lines[i:i] = docpp.lines

    def process(self):
        """Perform all pre-processing steps."""
        if not self._processed:
            self.process_comments()
            self.process_headers()
            self.process_figures()
            self.process_entities()
            self.process_branches()
            self.process_branchfigs()
            self.process_branchdocs()
            self.process_alls()
            self.process_allfig()
            self.process_includes()
            self._processed = True

    def write(self, outfile, format=None, pandoc_option_files=(), pandoc_options=(), genfile=None, verbose=True):
        """Writes documentation to `outfile`.

        Parameters
        ----------
        outfile : str
            File that the documentation is written to.
        format : str
            Output format.  If it is "md" or "simple-html",
            the built-in template generator is used.  Otherwise
            pandoc is used.  If not given, the format is inferred
            from the `outfile` name extension.
        pandoc_option_files : sequence
            Sequence with command line arguments provided to pandoc.
        pandoc_options : sequence
            Additional pandoc options overriding options read from
        `pandoc_option_files`.
        genfile : str
            Store temporary generated markdown input file to pandoc
            to this file (for debugging).
        verbose : bool
            Whether to show some messages when running pandoc.
        """
        self.process()
        content = self.get_buffer()
        substitutions = self.ontodoc.style.get('substitutions', [])
        for reg, sub in substitutions:
            content = re.sub(reg, sub, content)

        format = get_format(outfile, format)
        if format not in ('simple-html', 'markdown', 'md'):
            if not genfile:
                f = NamedTemporaryFile(mode='w+t', suffix='.md')
                f.write(content)
                f.flush()
                genfile = f.name
            else:
                with open(genfile, 'wt') as (f):
                    f.write(content)
            run_pandoc(genfile, outfile, format, pandoc_option_files=pandoc_option_files,
              pandoc_options=pandoc_options,
              verbose=verbose)
        else:
            if verbose:
                print('Writing:', outfile)
            with open(outfile, 'wt') as (f):
                f.write(content)


def load_pandoc_option_file(yamlfile):
    """Loads pandoc options from `yamlfile` and return a list with
    corresponding pandoc command line arguments."""
    with open(yamlfile) as (f):
        d = yaml.safe_load(f)
    options = d.pop('input-files', [])
    variables = d.pop('variables', {})
    for k, v in d.items():
        if isinstance(v, bool):
            if v:
                options.append('--%s' % k)
        else:
            options.append('--%s=%s' % (k, v))

    for k, v in variables.items():
        if k == 'date':
            if v == 'now':
                v = time.strftime('%B %d, %Y')
        options.append('--variable=%s:%s' % (k, v))

    return options


def append_pandoc_options(options, updates):
    """Append `updates` to pandoc options `options`.

    Parameters
    ----------
    options : sequence
        Sequence with initial Pandoc options.
    updates : sequence of str
        Sequence of strings of the form "--longoption=value", where
        ``longoption`` is a valid pandoc long option and ``value`` is the
        new value.  The "=value" part is optional.

        Strings of the form "no-longoption" will filter out "--longoption"
        from `options`.

    Returns
    -------
    new_options : list
        Updated pandoc options.
    """
    no_options = set('no-highlight')
    if not updates:
        return list(options)
    u = {}
    for s in updates:
        k, sep, v = s.partition('=')
        u[k.lstrip('-')] = v if sep else None
        filter_out = set((k for k, v in u.items() if k.startswith('no-') if k not in no_options))
        _filter_out = set(('--' + k[3:] for k in filter_out))
        new_options = [opt for opt in options if opt.partition('=')[0] not in _filter_out]
        new_options.extend(['--%s' % k if v is None else '--%s=%s' % (k, v) for k, v in u.items() if k not in filter_out])

    return new_options


def run_pandoc(genfile, outfile, format, pandoc_option_files=(), pandoc_options=(), verbose=True):
    """Runs pandoc.

    Parameters
    ----------
    genfile : str
        Name of markdown input file.
    outfile : str
        Output file name.
    format : str
        Output format.
    pandoc_option_files : sequence
        List of files with additional pandoc options.  Default is to read
        "pandoc-options.yaml" and "pandoc-FORMAT-options.yml", where
        `FORMAT` is the output format.
    pandoc_options : sequence
        Additional pandoc options overriding options read from
        `pandoc_option_files`.
    verbose : bool
        Whether to print the pandoc command before execution.

    Raises
    ------
    subprocess.CalledProcessError
        If the pandoc process returns with non-zero status.  The `returncode`
        attribute will hold the exit code.
    """
    args = [
     genfile]
    files = ['pandoc-options.yaml', 'pandoc-%s-options.yaml' % format]
    if pandoc_option_files:
        files = pandoc_option_files
    for fname in files:
        if os.path.exists(fname):
            args.extend(load_pandoc_option_file(fname))
        else:
            warnings.warn('missing pandoc option file: %s' % fname)

    args = append_pandoc_options(args, pandoc_options)
    if format == 'pdf':
        pdf_engine = 'pdflatex'
        for arg in args:
            if arg.startswith('--pdf-engine'):
                pdf_engine = arg.split('=', 1)[1]
                break

        with TemporaryDirectory() as (tmpdir):
            run_pandoc_pdf(tmpdir, pdf_engine, outfile, args, verbose=verbose)
    else:
        args.append('--output=%s' % outfile)
        cmd = ['pandoc'] + args
        if verbose:
            print()
            print('* Executing command:')
            print(' '.join((shlex.quote(s) for s in cmd)))
        subprocess.check_call(cmd)


def run_pandoc_pdf(latex_dir, pdf_engine, outfile, args, verbose=True):
    """Run pandoc for pdf generation."""
    basename = os.path.join(latex_dir, os.path.splitext(os.path.basename(outfile))[0])
    texfile = basename + '.tex'
    args.append('--output=%s' % texfile)
    cmd = ['pandoc'] + args
    if verbose:
        print()
        print('* Executing commands:')
        print(' '.join((shlex.quote(s) for s in cmd)))
    else:
        subprocess.check_call(cmd)
        texfile2 = basename + '2.tex'
        with open(texfile, 'rt') as (f):
            content = f.read().replace('\\$\\Uptheta\\$', '$\\Uptheta$')
        with open(texfile2, 'wt') as (f):
            f.write(content)
        pdffile = basename + '2.pdf'
        cmd = [pdf_engine, texfile2, '-halt-on-error',
         '-output-directory=%s' % latex_dir]
        if verbose:
            print()
            print(' '.join((shlex.quote(s) for s in cmd)))
        output = subprocess.check_output(cmd, timeout=60)
        output = subprocess.check_output(cmd, timeout=60)
        if (os.path.exists(pdffile) or os.path.exists)(os.path.basename(pdffile)):
            pdffile = os.path.basename(pdffile)
            for ext in ('aux', 'out', 'toc', 'log'):
                filename = os.path.splitext(pdffile)[0] + '.' + ext
                if os.path.exists(filename):
                    os.remove(filename)

        else:
            print()
            print(output)
            print()
            raise RuntimeError('latex did not produce pdf file: ' + pdffile)
    if not (os.path.exists(outfile) and os.path.samefile(pdffile, outfile)):
        if verbose:
            print()
            print('move %s to %s' % (pdffile, outfile))
        shutil.move(pdffile, outfile)


def get_format(outfile, format=None):
    """Infer format from outfile and format."""
    if format is None:
        format = os.path.splitext(outfile)[1]
    if not format:
        format = 'html'
    if format.startswith('.'):
        format = format[1:]
    return format


def get_style(format):
    """Infer style from output format."""
    if format == 'simple-html':
        style = 'html'
    else:
        if format in ('tex', 'latex', 'pdf'):
            style = 'markdown_tex'
        else:
            style = 'markdown'
    return style


def get_figformat(format):
    """Infer preferred figure format from output format."""
    if format == 'pdf':
        figformat = 'pdf'
    else:
        if 'html' in format:
            figformat = 'svg'
        else:
            figformat = 'png'
    return figformat


def get_maxwidth(format):
    """Infer preferred max figure width from output format."""
    if format == 'pdf':
        maxwidth = 668
    else:
        maxwidth = 1024
    return maxwidth


def get_docpp(ontodoc, infile, figdir='genfigs', figformat='png', maxwidth=None):
    """Read `infile` and return a new docpp instance."""
    if infile:
        with open(infile, 'rt') as (f):
            template = f.read()
        basedir = os.path.dirname(infile)
    else:
        template = ontodoc.get_default_template()
        basedir = '.'
    docpp = DocPP(template, ontodoc, basedir=basedir, figdir=figdir, figformat=figformat,
      maxwidth=maxwidth)
    return docpp