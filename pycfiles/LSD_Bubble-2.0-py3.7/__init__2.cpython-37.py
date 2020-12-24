# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/LSD/all_in_one/__init__2.py
# Compiled at: 2018-12-03 05:45:48
# Size of source mod 2**32: 15250 bytes
from math import inf
from LSD.filter import Filter
WHITE = 0
GREY = 1
BLACK = 2
GREEN = 3
YELLOW = 4
PURPLE = 5
ORANGE = 6
RED = 7

def abitarry_graph_detect(graph, rep):
    g = ColordGraph(graph)
    for v in g.nodes:
        g.set_color(v, WHITE)

    for v, alt in generate_starts(g):
        order, pos = create_dfs_order(v, g, alt)
        superbubble(g, order, SCCFilter(rep), alt, pos)


def generate_starts(g):
    for v in g.nodes:
        if g.in_degree(v) == 0:
            yield (
             v, None)

    for cycle in find_cycles2(g):
        paths = find_paths2(g, cycle)
        cut = cycle[find_cover_cut(paths)]
        yield (cut, cut)


def find_cycles--- This code section failed: ---

 L.  44       0_2  SETUP_LOOP          292  'to 292'
                4  LOAD_FAST                'g'
                6  LOAD_ATTR                nodes
                8  GET_ITER         
             10_0  COME_FROM            28  '28'
            10_12  FOR_ITER            290  'to 290'
               14  STORE_FAST               'v'

 L.  45        16  LOAD_FAST                'g'
               18  LOAD_METHOD              get_color
               20  LOAD_FAST                'v'
               22  CALL_METHOD_1         1  '1 positional argument'
               24  LOAD_GLOBAL              WHITE
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    10  'to 10'

 L.  46        30  LOAD_FAST                'g'
               32  LOAD_METHOD              set_color
               34  LOAD_FAST                'v'
               36  LOAD_GLOBAL              GREEN
               38  CALL_METHOD_2         2  '2 positional arguments'
               40  POP_TOP          

 L.  47        42  LOAD_FAST                'v'
               44  BUILD_LIST_1          1 
               46  STORE_FAST               'stack'

 L.  48        48  SETUP_LOOP          288  'to 288'
             50_0  COME_FROM           262  '262'
               50  LOAD_FAST                'stack'
            52_54  POP_JUMP_IF_FALSE   286  'to 286'

 L.  49        56  LOAD_FAST                'stack'
               58  LOAD_CONST               -1
               60  BINARY_SUBSCR    
               62  STORE_FAST               'u'

 L.  50        64  LOAD_FAST                'g'
               66  LOAD_METHOD              get_color
               68  LOAD_FAST                'u'
               70  CALL_METHOD_1         1  '1 positional argument'
               72  STORE_FAST               'c'

 L.  51        74  LOAD_FAST                'c'
               76  LOAD_GLOBAL              WHITE
               78  COMPARE_OP               ==
            80_82  POP_JUMP_IF_FALSE   256  'to 256'

 L.  52        84  LOAD_FAST                'g'
               86  LOAD_METHOD              set_color
               88  LOAD_FAST                'u'
               90  LOAD_GLOBAL              GREEN
               92  CALL_METHOD_2         2  '2 positional arguments'
               94  POP_TOP          

 L.  53        96  SETUP_LOOP          284  'to 284'
               98  LOAD_FAST                'g'
              100  LOAD_METHOD              successors
              102  LOAD_FAST                'u'
              104  CALL_METHOD_1         1  '1 positional argument'
              106  GET_ITER         
            108_0  COME_FROM           148  '148'
              108  FOR_ITER            252  'to 252'
              110  STORE_FAST               'w'

 L.  54       112  LOAD_FAST                'g'
              114  LOAD_METHOD              get_color
              116  LOAD_FAST                'w'
              118  CALL_METHOD_1         1  '1 positional argument'
              120  STORE_FAST               'wc'

 L.  55       122  LOAD_FAST                'wc'
              124  LOAD_GLOBAL              WHITE
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   142  'to 142'

 L.  56       130  LOAD_FAST                'stack'
              132  LOAD_METHOD              append
              134  LOAD_FAST                'w'
              136  CALL_METHOD_1         1  '1 positional argument'
              138  POP_TOP          
              140  JUMP_BACK           108  'to 108'
            142_0  COME_FROM           128  '128'

 L.  57       142  LOAD_FAST                'wc'
              144  LOAD_GLOBAL              GREEN
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   108  'to 108'

 L.  58       150  LOAD_FAST                'stack'
              152  LOAD_METHOD              pop
              154  CALL_METHOD_0         0  '0 positional arguments'
              156  BUILD_LIST_1          1 
              158  STORE_FAST               'cycle'

 L.  59       160  LOAD_FAST                'g'
              162  LOAD_METHOD              set_color
              164  LOAD_FAST                'w'
              166  LOAD_GLOBAL              PURPLE
              168  CALL_METHOD_2         2  '2 positional arguments'
              170  POP_TOP          

 L.  60       172  SETUP_LOOP          234  'to 234'
            174_0  COME_FROM           206  '206'
              174  LOAD_FAST                'stack'
              176  LOAD_CONST               -1
              178  BINARY_SUBSCR    
              180  LOAD_FAST                'w'
              182  COMPARE_OP               !=
              184  POP_JUMP_IF_FALSE   232  'to 232'

 L.  61       186  LOAD_FAST                'stack'
              188  LOAD_METHOD              pop
              190  CALL_METHOD_0         0  '0 positional arguments'
              192  STORE_FAST               'x'

 L.  62       194  LOAD_FAST                'g'
              196  LOAD_METHOD              get_color
              198  LOAD_FAST                'x'
              200  CALL_METHOD_1         1  '1 positional argument'
              202  LOAD_GLOBAL              GREEN
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   174  'to 174'

 L.  63       208  LOAD_FAST                'g'
              210  LOAD_METHOD              set_color
              212  LOAD_FAST                'x'
              214  LOAD_GLOBAL              PURPLE
              216  CALL_METHOD_2         2  '2 positional arguments'
              218  POP_TOP          

 L.  64       220  LOAD_FAST                'cycle'
              222  LOAD_METHOD              append
              224  LOAD_FAST                'x'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  POP_TOP          
              230  JUMP_BACK           174  'to 174'
            232_0  COME_FROM           184  '184'
              232  POP_BLOCK        
            234_0  COME_FROM_LOOP      172  '172'

 L.  65       234  LOAD_GLOBAL              list
              236  LOAD_GLOBAL              reversed
              238  LOAD_FAST                'cycle'
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  CALL_FUNCTION_1       1  '1 positional argument'
              244  YIELD_VALUE      
              246  POP_TOP          

 L.  66       248  BREAK_LOOP       
              250  JUMP_BACK           108  'to 108'
              252  POP_BLOCK        
              254  JUMP_BACK            50  'to 50'
            256_0  COME_FROM            80  '80'

 L.  67       256  LOAD_FAST                'c'
              258  LOAD_GLOBAL              GREEN
              260  COMPARE_OP               ==
              262  POP_JUMP_IF_FALSE    50  'to 50'

 L.  68       264  LOAD_FAST                'g'
              266  LOAD_METHOD              set_color
              268  LOAD_FAST                'u'
              270  LOAD_GLOBAL              YELLOW
              272  CALL_METHOD_2         2  '2 positional arguments'
              274  POP_TOP          

 L.  69       276  LOAD_FAST                'stack'
              278  LOAD_METHOD              pop
              280  CALL_METHOD_0         0  '0 positional arguments'
              282  POP_TOP          
            284_0  COME_FROM_LOOP       96  '96'
              284  JUMP_BACK            50  'to 50'
            286_0  COME_FROM            52  '52'
              286  POP_BLOCK        
            288_0  COME_FROM_LOOP       48  '48'
              288  JUMP_BACK            10  'to 10'
              290  POP_BLOCK        
            292_0  COME_FROM_LOOP        0  '0'

Parse error at or near `COME_FROM' instruction at offset 286_0


def find_cycles2(g):
    for v in g.nodes:
        if g.get_color(v) == WHITE:
            g.set_color(v, GREEN)
            stack = [(v, iter(g.successors(v)))]
            while stack:
                parent, children = stack[(-1)]
                if g.get_color(parent) == BLACK:
                    stack.pop
                else:
                    try:
                        child = next(children)
                        color = g.get_color(child)
                        if color == WHITE:
                            g.set_color(child, GREEN)
                            stack.append((child, iter(g.successors(child))))
                        else:
                            if color == GREEN:
                                k = 0
                                for k in range(len(stack)):
                                    if stack[k][0] == child:
                                        break

                                yield [x[0] for x in stack[k:]]
                                stack = stack[:k]
                    except StopIteration:
                        g.set_color(parent, YELLOW)
                        stack.pop


def cycle_distance(k, i, end):
    if end > i:
        return end - i - 1
    return end + k - i - 1


def find_paths(g, cycle):
    revers = {}
    for i in range(len(cycle)):
        revers[cycle[i]] = i

    k = len(cycle)

    def cycle_min(*args):
        min_value = inf
        ret = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value < min_value:
                min_value = new_value
                ret = x

        return ret

    def cycle_max(*args):
        max_value = -1
        ret = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value > max_value:
                max_value = new_value
                ret = x

        return ret

    ret = []
    for v in cycle:
        stack = []
        for w in g.successors(v):
            if g.get_color(w) != PURPLE:
                stack.append(w)

        inorder = []
        while stack:
            u = stack[(-1)]
            c = g.get_color(u)
            if c != ORANGE:
                g.set_color(u, ORANGE)
                g.property(u, 'in', len(inorder))
                inorder.append(u)
                for w in g.successors(u):
                    wc = g.get_color(w)
                    if wc == PURPLE:
                        new = revers[w]
                        g.update_property(u, 'min', cycle_min, new)
                        g.update_property(u, 'max', cycle_max, new)
                    elif wc == ORANGE:
                        g.update_property(u, 'link', min, g.property(w, 'in'))
                    elif wc != BLACK and wc != RED:
                        stack.append(w)

            else:
                g.set_color(u, RED)
                stack.pop
                for w in g.successors(u):
                    g.update_property(u, 'min', cycle_min, g.property(w, 'min'), g.property(w, 'max'))
                    g.update_property(u, 'max', cycle_max, g.property(w, 'min'), g.property(w, 'max'))
                    g.update_property(u, 'link', min, g.property(w, 'link'))

        for w in inorder:
            if g.property(w, 'link'):
                other = inorder[g.property(w, 'link')]
                g.update_property(w, 'min', cycle_min, g.property(other, 'min'))
                g.update_property(w, 'max', cycle_max, g.property(other, 'max'))
                g.property(w, 'link', inf)

        maxlist = []
        for w in g.successors(v):
            if g.get_color(w) != PURPLE:
                maxlist.append(g.property(w, 'min'))
                maxlist.append(g.property(w, 'max'))
            else:
                maxlist.append(revers[w])

        ret.append(cycle_max(maxlist))

    return ret


def find_paths2(g, cycle):
    revers = {}
    for i in range(len(cycle)):
        revers[cycle[i]] = i

    k = len(cycle)

    def cycle_min(*args):
        min_value = inf
        ret = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value < min_value:
                min_value = new_value
                ret = x

        return ret

    def cycle_max(*args):
        max_value = -1
        ret = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value > max_value:
                max_value = new_value
                ret = x

        return ret

    for i in range(len(cycle)):
        r = cycle[i]
        stack = [(r, iter(g.successors(r)))]
        inorder = []
        while stack:
            parent, children = stack[(-1)]
            try:
                child = next(children)
                color = g.get_color(child)
                if color == PURPLE:
                    new = revers[child]
                    g.update_property(parent, 'min', cycle_min, new)
                    g.update_property(parent, 'max', cycle_max, new)
                else:
                    if color == ORANGE:
                        g.update_property(parent, 'link', min, g.property(child, 'in'))
                    else:
                        if color != BLACK:
                            if color != RED:
                                g.set_color(child, ORANGE)
                                g.property(child, 'in', len(inorder))
                                inorder.append(child)
                                stack.append((child, iter(g.successors(child))))
            except StopIteration:
                for suc in g.successors(parent):
                    color = g.get_color(suc)
                    if color != PURPLE and color != BLACK:
                        g.update_property(parent, 'min', cycle_min, g.property(suc, 'min'), g.property(suc, 'max'))
                        g.update_property(parent, 'max', cycle_max, g.property(suc, 'min'), g.property(suc, 'max'))
                        g.update_property(parent, 'link', min, g.property(suc, 'link'))

                if g.get_color(parent) == ORANGE:
                    g.set_color(parent, RED)
                stack.pop

        for v in inorder:
            if g.property(v, 'link'):
                other = inorder[g.property(v, 'link')]
                g.update_property(v, 'min', cycle_min, g.property(other, 'min'))
                g.update_property(v, 'max', cycle_max, g.property(other, 'max'))
                g.property(v, 'link', inf)

    return [g.property(v, 'max') for v in cycle]


def max_distance(paths, k, l, pos):
    end = paths[pos]
    max_dis = (0, None)
    for i in l:
        dis = cycle_distance(k, i, paths[i]) - cycle_distance(k, i, end)
        if dis > max_dis[0]:
            max_dis = (
             dis, i)

    return max_dis


def generate_cycle_range(k, pos, end):
    i = pos
    if end < pos:
        while i < end or i >= pos:
            yield i
            i = (i + 1) % k

    else:
        while i < end:
            yield i
            i += 1


def find_cover_cut(paths):
    k = len(paths)
    m = max(((cycle_distance(k, i, paths[i]), i) for i in range(k)))
    if m[0] == k:
        return m[1]
    j = m[1]
    outset = set(generate_cycle_range(k, j, paths[j]))
    outset.add(paths[j])
    while 1:
        n = max_distance(paths, k, generate_cycle_range(k, j, paths[j]), j)
        if n[0] == 0:
            return paths[j]
        j = n[1]
        if paths[j] in outset:
            return m[1]


def create_dfs_order(v, g, alt=None):
    """Do a topological ordering of the graph.
    It does a linear version of a deep first search.
    """
    order = Order()
    stack = [(v, iter(g.successors(v)))]
    g.set_color(v, GREY)
    first = alt is not None
    pos = None
    while stack:
        parent, children = stack[(-1)]
        try:
            child = next(children)
            if first:
                if child == alt:
                    first = False
                    pos = order.pos
                    order.add(child)
            color = g.get_color(child)
            if color != GREY:
                if color != BLACK:
                    stack.append((child, iter(g.successors(child))))
                    g.set_color(child, GREY)
        except StopIteration:
            stack.pop
            order.add(parent)
            g.set_color(parent, BLACK)

    return (
     order, pos)


class Order:
    __doc__ = 'A order representation.\n    Get a vertex on an arbitrary position in O(1).\n    Get the position of an arbitrary vertex in O(1).'

    def __init__(self):
        """Init the order set source position -1 and sink and None position to infinity """
        self.order = []
        self.revers = {None: inf}
        self.pos = 0

    def add(self, v):
        """Add an element to the end of the order"""
        self.order.append(v)
        self.revers[v] = self.pos
        self.pos += 1

    def __len__(self):
        return len(self.order)

    @property
    def n(self):
        """Get the length of the order."""
        return len(self.order)

    def __getitem__(self, item):
        """Get element at position item"""
        return self.order[item]

    def get_position(self, v):
        """Get position of element v. If v not contained return -2"""
        try:
            return self.revers[v]
        except KeyError:
            return -2


def out_parent3(k, g, order):
    v = order[k]
    if g.in_degree(v) == 0:
        return inf
    maximum = -1
    for v2 in g.predecessors(v):
        pos = order.get_position(v2)
        if pos <= k:
            return inf
        maximum = max(maximum, pos)

    return maximum


def out_child3(k, g, order, alt, altpos):
    v = order[k]
    if g.out_degree(v) == 0:
        return -2
    minimum = inf
    for v2 in g.successors(v):
        if v2 == alt:
            pos = altpos
        else:
            pos = order.get_position(v2)
        if pos >= k:
            return -2
        minimum = min(minimum, pos)

    return minimum


def superbubble(g, order, reporter, alt=None, pos=0):
    """Detect all superbubbles in a DAG."""

    def report(i, o):
        reporter.rep(order[o:i + 1][::-1])

    stack = []
    out_parent_map = []
    t = None
    for k in range(len(order)):
        child = out_child3(k, g, order, alt, pos)
        if child == k - 1:
            stack.append(t)
            t = k - 1
        else:
            while t is not None and t > child:
                t2 = stack.pop
                if t2 is not None:
                    out_parent_map[t2] = max(out_parent_map[t], out_parent_map[t2])
                t = t2

        if t is not None:
            if out_parent_map[t] == k:
                report(k, t)
                t2 = stack.pop
                if t2 is not None:
                    out_parent_map[t2] = max(out_parent_map[t], out_parent_map[t2])
                t = t2
        out_parent_map.append(out_parent3(k, g, order))
        if t is not None:
            out_parent_map[t] = max(out_parent_map[t], out_parent_map[k])


class SCCFilter(Filter):
    __doc__ = 'The filter that correct the artifical vertex and discards false added superbubble.'

    def rep(self, dag):
        if dag[0] != dag[(-1)]:
            self.report(dag)


class ColordGraph:
    __doc__ = 'The auxiliary graph representation.\n    It is in the core a subgraph of the complete NetworkX graph.\n    However, it have an other initialisation, some extra features and depend slightly different.'

    def __init__(self, g):
        """Save the the graph."""
        self.g = g

    def in_degree(self, v):
        """Get the in degree of a vertex."""
        return self.g.in_degree(v)

    def out_degree(self, v):
        """Get the out degree of a vertex"""
        return self.g.out_degree(v)

    def successors(self, v):
        """Get all successors of a vertex."""
        return list(self.g.successors(v))

    def predecessors(self, v):
        """Get all predeccessors of a vertex."""
        return list(self.g.predecessors(v))

    @property
    def nodes(self):
        """Get all vertices of a graph (including a and b)."""
        return self.g.nodes

    def set_color(self, v, c):
        """Set the color of v to c."""
        self.g.node[v]['c'] = c

    def get_color(self, v):
        """Get the color of v."""
        return self.g.node[v]['c']

    def property(self, v, key, value=None):
        if value is not None:
            self.g.node[v][key] = value
        else:
            try:
                return self.g.node[v][key]
            except KeyError:
                return

    def update_property(self, v, key, func, *values):
        values = list(filter(lambda x: x is not None, values))
        if values:
            node = self.g.node[v]
            if key in node:
                node[key] = func(node[key], *values)
            else:
                if len(values) > 1:
                    node[key] = func(*values)
                else:
                    node[key] = values[0]

    def __iter__(self):
        """Iterate over the vertices of the graph (excluding a and b)."""
        return iter(self.nodes)

    def __str__(self):
        s = ', '.join(('{v} {color}'.format(v=v, color=(self.get_color(v))) for v in self.nodes))
        s += '\n'
        s += ', '.join((str(s) for s in self.g.edges))
        s += '\n'
        return s