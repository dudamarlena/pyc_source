# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/mythe_micros/utils.py
# Compiled at: 2019-12-22 13:02:48
# Size of source mod 2**32: 2394 bytes


def cprint(s, pc=-1, show=True, end='\n'):
    if pc == 'help':
        print('\n        # 显示格式: \x1b[显示方式;前景色;背景色m\n        # ------------------------------------------------\n        # 显示方式             说明\n        #   0                 终端默认设置\n        #   1                 高亮显示\n        #   4                 使用下划线\n        #   5                 闪烁\n        #   7                 反白显示\n        #   8                 不可见\n        #   22                非粗体\n        #   24                非下划线\n        #   25                非闪烁\n        #\n        #   前景色             背景色            颜色\n        #     30                40              黑色\n        #     31                41              红色\n        #     32                42              绿色\n        #     33                43              黃色\n        #     34                44              蓝色\n        #     35                45              紫红色\n        #     36                46              青蓝色\n        #     37                47              白色\n        # ------------------------------------------------\n        ')
        return
        if pc == 'show':
            for i in (0, 1, 4, 5, 7, 8, 22, 24, 25, 30, 31, 32, 33, 34, 35, 36, 37,
                      40, 41, 42, 43, 44, 45, 46, 47):
                cprint(s, i)

            return
        else:
            dct = dict({'default':0,  'highlight':1,  'underline':4,  'blink':5,  'reverse':7,  'invisible':8,  'nbold':22,  'nunderline':24, 
             'nblink':25,  'black':30,  'red':31,  'green':32,  'yellow':33,  'blue':34,  'purple':35,  'sky':36, 
             'white':37,  'bblack':40,  'bred':41,  'bgreen':42,  'byellow':43,  'bblue':44,  'bpurple':45,  'bsky':46,  'bwhite':47})
            reset = '\x1b[0m'
            if type(pc) == int:
                style = '\x1b[%dm' % pc
            else:
                if type(pc) == str:
                    if pc.lower() in dct:
                        style = '\x1b[%sm' % dct[pc.lower()]
                    else:
                        style = reset
                else:
                    style = reset
        res = '%s%s%s' % (style, s, reset)
        if show == True:
            print(res, end=end)
    else:
        return res


def cprints(arg):
    for s, pc in arg:
        cprint(s, pc, end=' ')


if __name__ == '__main__':
    cprint('Hello,world!', 'bred')
    cprints([('a', 'red'), ('b', 'yellow')])
    print('\n')