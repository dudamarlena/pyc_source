# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/menuish/menu.py
# Compiled at: 2010-03-11 08:19:18
from restish import url
from breve.tags.html import tags as T
from breve.flatten import flatten

class Node(object):
    """
    A Navigation Node
    """

    def __init__(self, dottedpath, label, id, group=None, item_id=None, children=None, namespace=None):
        self.id = id
        self.path = dottedpath
        self.group = group
        self.item_id = item_id
        self.label = label
        self.item = None
        if children is not None:
            self.children = children
        else:
            self.children = []
        self.namespace = namespace
        return

    def name():

        def get(self):
            return self.path.split('.')[(-1)]

        def set(self, new_name):
            self.path = ('.').join(self.path.split('.')[:-1] + [new_name])

        return property(get, set)

    name = name()

    def descendent_by_id(self, childId):
        """
        Search all the children of this node for a child with the specified id.
        """
        for child in self.children:
            if child.id == childId:
                return child
            child = child.descendent_by_id(childId)
            if child is not None:
                return child

        return

    def child_by_name(self, name):
        """
        Find an immediate child with the specified name.
        """
        for child in self.children:
            if child.name == name:
                return child

    def descendent_by_abspath(self, child_url):
        if child_url.startswith('/'):
            child_url = child_url[1:]
        segments = [
         'root'] + child_url.split('/')
        return self.descendent_by_segments(segments)

    def descendent_by_dottedpath(self, dottedpath):
        segments = dottedpath.split('.')
        return self.descendent_by_segments(segments)

    def descendent_by_segments(self, segments):
        if len(segments) == 1:
            return self
        else:
            node = self
            for segment in segments[1:]:
                for n in node.children:
                    if n.path.split('.')[(-1)] == segment:
                        node = n
                        break
                else:
                    return

            if n != self:
                return n
            return
            return

    def add(self, child):
        self.children.append(child)

    def add_from_node_def(self, dottedpath, label, id, **kw):
        parent_dottedpath = ('.').join(dottedpath.split('.')[:-1])
        parent_node = self.descendent_by_dottedpath(parent_dottedpath)
        parent_node.add(Node(dottedpath, label, id, **kw))


def create_sitemap(node_defs):
    """
    creates a node tree from a list of args e.g. the following yaml representation
        - [root, Home, 1, {}]
        - [root.about, About, 2, {}]
        - [root.gallery, Gallery, 3, {}]
    """
    root_node_def = node_defs.pop(0)
    sitemap = Node(*root_node_def[:-1], **root_node_def[(-1)])
    for node_def in node_defs:
        sitemap.add_from_node_def(*node_def[:-1], **node_def[(-1)])

    return sitemap


class Navigation(object):

    def __init__(self, type=None, maxdepth=None, showroot=False, openall=False, css_class=None, openallbelow=0, startdepth=0, force_url=None, item_class=None, item_id=None, urlbase='/', urlfactory=None):
        """

        Parameters
        ----------

        type    
            If set, filters the navigation items in sitemap to be of the given
            type only. Otherwise, all navigation items (not necessarily the
            same as all sitemap items) are rendered.

        startdepth
            Depth at which to start showing navigation items. Can be an
            absolute or relative depth (see below).

        maxdepth
            Maximum depth of navigation items to show. Can be an absolute or
            relative depth (see below).

        showroot
            Flag to say whether the 'root' of the current tree should be shown
            (e.g. home for a general menu)

        openallbelow
            Open every submenu below the given depth (good for leaving top
            level closed but showing all submenus within a section).

        openall
            Flag to override the openallbelow to expand every menu.

        force_url
            render as if you are here

        item_class
            a list of what class to add. valid values are 'number' and 'firstlast'.
 
        item_id
            the node attr to use as the id. Defaults to 'name' (the only value at the moment)

        URL Depth Specification
        -----------------------

        The startdepth and maxdepth can be specified in a number of ways,
        either absolute to the root URL or relative from a symbolic location or
        a named navigation group.

            <int>   
                Absolute depth from the root of the site.

            here+<int>
                Relative to the current URL.

            startdepth+<int>
                Relative to the startdepth. (Don't use for startdepth itself!)

            <navigation>+<int>
                Relative to the deepest item in the given navigation group.
        """
        self.navigation_type = type
        self.startdepth = startdepth
        self.maxdepth = maxdepth
        self.showroot = showroot
        self.openall = openall
        self.openallbelow = openallbelow
        if urlfactory is None:
            self.urlfactory = self._urlfactory
        else:
            self.urlfactory = urlfactory
        self.urlbase = urlbase
        if force_url is not None:
            self.force_url_path = [
             'root'] + force_url.split('/')
        else:
            self.force_url_path = None
        if item_class is None:
            item_class = []
        self.item_class = item_class
        if item_id is None:
            item_id = 'name'
        self.item_id = item_id
        self.css_class = css_class
        return

    def _urlfactory(self, node):
        u = url.URL(self.urlbase)
        for segment in node.path.split('.')[1:]:
            u = u.child(segment)

        return u

    def render_navigation(self, sitemap, request):
        self.initialise_args(sitemap, request)
        n = self.build_menu(sitemap, request)
        return flatten(n)

    def initialise_args(self, sitemap, request):
        """
        Resolve the args passed to __init__ to have real meaning in the context
        of the navigation and current location in the URL.
        
        We also perform some type checking at the same time to ensure later
        comparisons work correctly.
        """
        if self.navigation_type is not None:
            self.navigation_type = int(self.navigation_type)
        if self.maxdepth is not None:
            self.maxdepth = self.calculate_depth(self.maxdepth, sitemap, request)
        self.startdepth = self.calculate_depth(self.startdepth, sitemap, request)
        self.showroot = _boolean(self.showroot)
        self.openall = _boolean(self.openall)
        self.openallbelow = int(self.openallbelow)
        return

    def calculate_depth(self, depth_spec, sitemap, request):
        """
        Resolve a depth arg.
        """
        depth_spec = str(depth_spec)
        if '+' not in depth_spec:
            return int(depth_spec)
        (relative_to, relative_offset) = depth_spec.split('+', 1)
        relative_offset = int(relative_offset)
        if relative_to == 'here':
            relative_depth = len(self.current_path_segments(request)) - 1
        elif relative_to == 'startdepth':
            relative_depth = self.calculate_depth(self.startdepth, sitemap, request)
        else:
            navigation_group = int(relative_to)
            relative_depth = len(self.current_path_segments_for_(sitemap, request, navigation_group)) - 1
        return relative_depth + relative_offset

    def current_path_segments(self, request):
        path = [
         'root'] + request.url.path_segments
        return path

    def current_path_segments_for_(self, sitemap, request, navigation_group=None):
        path = self.current_path_segments(request)
        path, rest = path[:1], path[1:]
        node = sitemap
        for segment in rest:
            node = node.child_by_name(segment)
            if node.group == navigation_group:
                path.append(segment)
            else:
                break

        return path

    def build_menu(self, sitemap, request):
        request_path = self.current_path_segments(request)
        request_path = [ r for r in request_path if r ]
        if self.force_url_path is not None:
            force_url_path = [ r for r in self.force_url_path if r ]
        else:
            force_url_path = request_path

        def _add_root_menu(tag):
            nodepath = node.path.split('.')
            nodedepth = len(nodepath)
            label = node.label
            t = T.li()[T.a(href=self.urlfactory(node))[label]]
            tag[t]
            if request_path == nodepath:
                add_class(t, 'selected')
            if self.item_id == 'name':
                t.attrs['id'] = 'nav-%s' % node.name

        def _add_child_menus(tag, node, urlpath):
            nodepath = node.path.split('.')
            nodedepth = len(nodepath)
            label = node.label
            if not self.openall:
                for (n, segment) in enumerate(urlpath[:self.openallbelow]):
                    if n + 1 >= nodedepth or segment != nodepath[(n + 1)]:
                        return

            t = T.li()[T.a(href=self.urlfactory(node))[label]]
            tag[t]
            if request_path == nodepath:
                add_class(t, 'selected')
            elif request_path[:nodedepth] == nodepath[:nodedepth]:
                add_class(t, 'selectedpath')
            if self.item_id == 'name':
                t.attrs['id'] = 'nav-%s' % node.name
            if self.maxdepth is not None and nodedepth > self.maxdepth:
                return
            else:
                if node.children and (self.openall or force_url_path[:nodedepth] == nodepath[:nodedepth]):
                    s = T.ul()
                    t[s]
                    _add_children(s, node, urlpath, is_root=False)
                return

        def _add_children(tag, node, urlpath, is_root=True):
            """ The root node is the top level segment (e.g. for an absolute url
                /a/b/c, root node is 'a'
                node is the sitemap root node (with path 'root')
            """
            if node is not None and is_root is True and self.showroot is True:
                _add_root_menu(tag)
            if node is None or node.children is None:
                return tag
            else:
                for child in node.children:
                    if self.navigation_type is not None and child.group != self.navigation_type:
                        continue
                    _add_child_menus(tag, child, urlpath)

                return tag

        def _menu_built(tag):
            if 'firstlast' in self.item_class:
                try:
                    add_class(tag.children[0], 'first-child')
                    add_class(tag.children[(-1)], 'last-child')
                except IndexError:
                    pass

            if 'number' in self.item_class:
                for (n, child) in enumerate(tag.children):
                    add_class(tag.children[n], 'item-%s' % (n + 1))

            return tag

        node = sitemap
        urlpath = request.url.path_segments
        if urlpath == ['']:
            urlpath = []
        if len(urlpath) < self.startdepth:
            node = None
        else:
            for segment in urlpath[:self.startdepth]:
                node = node.child_by_name(segment)

            tag = T.ul()
            if self.css_class is not None:
                add_class(tag, self.css_class)
            tag = _add_children(tag, node, urlpath)
            return _menu_built(tag)


def items_to_display(sitemap, current_path, navigation_group):
    items = [
     sitemap]
    current_pathDepth = len(current_path)

    def visit_children(node):
        if node is None or node.children is None:
            return
        else:
            for child in node.children:
                if child.group == navigation_group:
                    items.append(child)

            nodepath = node.path.split('.')
            nodedepth = len(nodepath)
            if nodedepth == current_pathDepth:
                return
            child = current_path[nodedepth]
            visit_children(node.child_by_name(child))
            return

    visit_children(sitemap)
    return items


def _boolean(value):
    """
    Map a boolean-like value to a Python bool instance.
    """
    try:
        return bool(int(value))
    except ValueError:
        pass

    value = value.lower()
    if value in ('true', 'yes'):
        return True
    if value in ('false', 'no'):
        return False
    raise ValueError('Unrecognised boolean-like value %r' % value)


def add_class(tag, value):
    classes = tag.attrs.get('class')
    if classes:
        classes = classes.split(' ')
    else:
        classes = []
    classes.append(value)
    tag.attrs['class'] = (' ').join(classes)