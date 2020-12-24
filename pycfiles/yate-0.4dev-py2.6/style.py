# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yate/style.py
# Compiled at: 2012-01-19 20:54:27


class Style:

    def __init__(self, name, fore, back, fontStyle):
        self.name = name
        self.fore = fore
        self.back = back
        self.fontStyle = fontStyle

    def GetStyleString(self):
        styles = []
        if self.fore:
            styles.append('fore:%s' % self.fore)
        if self.back:
            styles.append('back:%s' % self.back)
        if self.fontStyle:
            styles.append('%s' % self.fontStyle)
        return (',').join(styles)

    def __repr__(self):
        return self.GetStyleString()


if __name__ == '__main__':
    s = Style('algo', 'black', 'blue', 'italic')
    print s.GetStyleString()