# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wmpy_util/print_util.py
# Compiled at: 2019-12-17 02:47:17
# Size of source mod 2**32: 10585 bytes
blank = [chr(183)]
blank = [chr(12288)]
blank = [chr(32)]
tabs = ['']

class TreeNode:
    __all_dict__ = dict()
    count = 0

    def __new__(cls, id, *args, **kwargs):
        if id in TreeNode.__all_dict__:
            return TreeNode.__all_dict__[id]
        else:
            obj = super(TreeNode, cls).__new__(cls)
            obj.id = id
            obj.children = []
            obj.father = None
            obj.number_id = TreeNode.count
            TreeNode.count += 1
            TreeNode.__all_dict__[id] = obj
            return obj

    def __init__(self, id):
        """
        树节点类，继承该类可以轻松实现树状图的绘制
        需要手动往children list中插入节点
        或者调用set_parent设置父节点，可以自动实现关联
        重写__str__方法，以便打印节点的详情
        :param id 节点的唯一id
        """
        pass

    def get_children(self):
        """
        获得所有子节点
        :return:
        """
        return self.children

    def get_parent(self):
        """
        获得父节点
        :return:
        """
        return self.father

    def set_father_by_id(self, fid):
        """
        通过id设置父节点
        :param fid:
        :return:
        """
        f_node = TreeNode.get_node_by_id(fid)
        f_node.add_child(self)

    def __set_father(self, father):
        """

        :param father:
        :return:
        """
        if self.father is not None:
            if not self.father == father:
                raise ValueError('TreeNode cannot have two diff fathers f1=%s  f2=%s' % (str(self.father), str(father)))
        else:
            self.father = father

    def add_child(self, child):
        """
        添加一个子节点
        :param child:
        :return:
        """
        if child not in self.children:
            self.children.append(child)
            child._TreeNode__set_father(self)

    def add_child_by_id(self, cid):
        """
        通过id设置子节点
        :param cid:
        :return:
        """
        child = TreeNode.get_node_by_id(cid)
        self.add_child(child)

    @staticmethod
    def get_node_by_id(tid):
        """
        通过唯一id获得树节点，如果id不存在则返回null
        :param tid:
        :return:
        """
        if tid in TreeNode.__all_dict__:
            node = TreeNode.__all_dict__[tid]
        else:
            node = None
        return node

    def get_tree_structure(self):
        """
        得到指定的树形结构表示
        :return:
        """
        _result = list()
        _info = str(self)
        _children = self.get_children()
        if len(_info) > 20:
            _info = _info[0:10] + '...'
        _result.append(_info)
        if _children is not None:
            if len(_children) > 0:
                _child_infos = list()
                for child in _children:
                    _child_infos += child.get_tree_structure()

                _result.append(_child_infos)
        return _result

    def plot_tree(self):
        """
        绘制树形图
        :return:
        """
        print('--------------------')
        structure = self.get_tree_structure()
        print('-----')
        plot_tree(structure)

    def plot_tree2(self, tab=''):
        """
        绘制树形图方法2, better!
        :return:
        """
        size = 2
        child_len = len(self.children)
        s = '─' * size
        if child_len > 0:
            s += '┬'
        else:
            s += '─'
        s += '─' * size
        print(s, end='')
        print(str(self))
        tab = tab + blank[0] * size
        for index, child in enumerate(self.children):
            if index + 1 == child_len:
                pre = '└'
            else:
                pre = '├'
            print((tab + pre), end='')
            if index + 1 == child_len:
                tab += blank[0]
            else:
                tab += '│'
            child.plot_tree2(tab=tab)
            tab = tab[:-1]

    def delete(self):
        """
        删除该节点
        :return:
        """
        if self.id in TreeNode.__all_dict__:
            TreeNode.__all_dict__.pop(self.id)

    def __str__(self):
        return str(self.id)


def plot_tree(lst):
    lst_len = len(lst)
    if lst_len == 0:
        print('───')
    else:
        for i, j in enumerate(lst):
            if i != 0:
                print((tabs[0]), end='')
            else:
                if lst_len == 1:
                    s = '───'
                else:
                    if i == 0:
                        s = '┬──'
                    else:
                        if i + 1 == lst_len:
                            s = '└──'
                        else:
                            s = '├──'
            print(s, end='')
            if isinstance(j, list) or isinstance(j, tuple):
                if i + 1 == lst_len:
                    tabs[0] += blank[0] * 3
                else:
                    tabs[0] += '│' + blank[0] * 2
                plot_tree(j)
            else:
                print(j)

    tabs[0] = tabs[0][:-3]


def exp_plot_tree():
    """
    测试画树形图
    :return:
    """
    Linux = (
     'Fedora', ['Debian', ['Ubuntu', ['Kubuntu', 'Xubuntu', 'Edubuntu']], ['KNOPPIX']],
     [
      [
       'Puppy Linux']], 'Open SUSE', 'Gentoo', 'Slackware', ['abc', 'def'])
    Android = ('Android 1.5 Cupcake', 'Android 1.6  Donut ', 'Android 2.2/2.2 Froyo',
               'Android 2.3 Gingerbread', 'Android 3.0 Honeycomb', 'Android 4.0 Ice Cream Sandwich')
    OS = ([['Unix', [['Free BSD', 'Mac OS']], [Linux]], ['Dos', ['MS-DOS']], 'Windows'], [], ['iOS', Android, 'Symbian', 'BlackBerry OS', 'WebOS', []])
    print('OS')
    plot_tree(Linux)


color_black = 'black'
color_red = 'red'
color_green = 'green'
color_yellow = 'yellow'
color_blue = 'blue'
color_purple = 'purple'
color_cyan = 'cyan'
color_white = 'white'
mode_normal = 'normal'
mode_bold = 'bold'
mode_underline = 'underline'
mode_blink = 'blink'
mode_invert = 'invert'
mode_hide = 'hide'
STYLE = {'fore':{'black':30, 
  'red':31, 
  'green':32, 
  'yellow':33, 
  'blue':34, 
  'purple':35, 
  'cyan':36, 
  'white':37}, 
 'back':{'black':40, 
  'red':41, 
  'green':42, 
  'yellow':43, 
  'blue':44, 
  'purple':45, 
  'cyan':46, 
  'white':47}, 
 'mode':{'normal':0, 
  'bold':1, 
  'underline':4, 
  'blink':5, 
  'invert':7, 
  'hide':8}, 
 'default':{'end': 0}}

def UseStyle(string, mode='', font_color='', back_color=''):
    mode = '%s' % STYLE['mode'][mode] if mode in STYLE['mode'] else ''
    font_color = '%s' % STYLE['fore'][font_color] if font_color in STYLE['fore'] else ''
    back_color = '%s' % STYLE['back'][back_color] if back_color in STYLE['back'] else ''
    style = ';'.join([s for s in [mode, font_color, back_color] if s])
    style = '\x1b[%sm' % style if style else ''
    end = '\x1b[%sm' % STYLE['default']['end'] if style else ''
    return '%s%s%s' % (style, string, end)


def TestColor():
    print(UseStyle('正常显示'))
    print('')
    print('测试显示模式')
    print(UseStyle('高亮', mode='bold'))
    print(UseStyle('下划线', mode='underline'))
    print(UseStyle('闪烁', mode='blink'))
    print(UseStyle('反白', mode='invert'))
    print(UseStyle('不可见', mode='hide'))
    print('')
    print('测试前景色')
    print(UseStyle('黑色', font_color='black'))
    print(UseStyle('红色', font_color='red'))
    print(UseStyle('绿色', font_color='green'))
    print(UseStyle('黄色', font_color='yellow'))
    print(UseStyle('蓝色', font_color='blue'))
    print(UseStyle('紫红色', font_color='purple'))
    print(UseStyle('青蓝色', font_color='cyan'))
    print(UseStyle('白色', font_color='white'))
    print('')
    print('测试背景色')
    print(UseStyle('黑色', back_color=color_black))
    print(UseStyle('红色', back_color='red'))
    print(UseStyle('绿色', back_color='green'))
    print(UseStyle('黄色', back_color='yellow'))
    print(UseStyle('蓝色', back_color='blue'))
    print(UseStyle('紫红色', back_color='purple'))
    print(UseStyle('青蓝色', back_color='cyan'))
    print(UseStyle('白色', back_color='white'))
    print('')


if __name__ == '__main__':
    exp_plot_tree()
    TestColor()