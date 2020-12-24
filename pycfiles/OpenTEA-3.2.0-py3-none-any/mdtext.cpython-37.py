# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/src/opentea/gui_forms/mdtext.py
# Compiled at: 2020-01-23 10:55:38
# Size of source mod 2**32: 6215 bytes
""" module to show markdown test into tktest"""
import re
from tkinter import font, Tk, Text, INSERT, END

class ExpandoText(Text):

    def insert(self, *args, **kwargs):
        result = (Text.insert)(self, *args, **kwargs)
        self.reset_height()
        return result

    def reset_height(self):
        height = self.tk.call((self._w, 'count', '-update', '-displaylines', '1.0', 'end'))


def count_monkeypatch(self, index1, index2, *args):
    args = [
     self._w, 'count'] + ['-' + arg for arg in args] + [index1, index2]
    result = (self.tk.call)(*args)
    return result


Text.count = count_monkeypatch

def insert_mdline(text, line, width_char, size):
    """Add a Markdown line to a Text Widget.

    :param text: Tkinter text wiget
    :param line: string with Markdown syntax
    """
    print('>', line)
    line = line.replace(' **', ' #BEG_BOLD ')
    line = line.replace('** ', ' #END_BOLD ')
    line = line.replace('**.', ' #END_BOLD .')
    line = line.replace('**,', ' #END_BOLD ,')
    line = line.replace(' * ', ' #MULTIPLIY ')
    line = line.replace(' *', ' #BEG_ITA ')
    line = line.replace('* ', ' #END_ITA ')
    line = line.replace('*.', ' #END_ITA .')
    line = line.replace('*,', ' #END_ITA ,')
    line = line.replace(' #MULTIPLIY ', ' * ')
    count = 0
    tag = None
    subline = 0
    for word in line.split():
        if word == '#BEG_BOLD':
            tag = 'bold'
        elif word == '#BEG_ITA':
            tag = 'italic'
        elif word == '#END_BOLD':
            tag = None
        elif word == '#END_ITA':
            tag = None
        else:
            if tag is None:
                text.insert(END, word + ' ')
            else:
                print(word, tag)
                text.insert(END, word + ' ', tag)
            if subline + len(word) > width_char:
                subline = len(word)
                count += 1
            else:
                subline += len(word)
            print('>>', count, subline, width_char)

    text.insert(END, '\n')
    return int(1.2 * count)


def mdtext(root, mdcontent, background='grey', width_pix=40, height_char=None):
    """Add a Markdown content to a Text Widget.

    :param text: Tkinter text wiget
    :param mdcontent: string with Markdown syntax
    """
    family = 'Helvetica'
    size = 16
    offset = 30
    normal_font = font.Font(family=family, size=size)
    width_char = int((width_pix - 2 * offset) / (size * 0.5))
    text = Text(root,
      font=normal_font,
      bg=background,
      width=width_char)
    count_disp_line = 0
    for line in mdcontent.split('\n'):
        special = False
        regexp = re.compile('^\\s*#{1}[^#].')
        if regexp.match(line) is not None:
            special = True
            subline = line.strip()[2:]
            text.insert(END, subline + '\n', 'h1')
            count_disp_line += 1
        regexp = re.compile('^\\s*#{2}[^#].')
        if regexp.match(line) is not None:
            special = True
            subline = line.strip()[3:]
            text.insert(END, subline + '\n', 'h2')
            count_disp_line += 1
        regexp = re.compile('^\\s*#{3}[^#].')
        if regexp.match(line) is not None:
            special = True
            subline = line.strip()[4:]
            text.insert(END, subline + '\n', 'h3')
            count_disp_line += 1
        regexp = re.compile('^\\s*-{1}[^-].')
        if regexp.match(line) is not None:
            special = True
            text.insert(END, '   • ')
            count_disp_line += insert_mdline(text, line.strip()[2:], width_char, size)
        regexp = re.compile('^!\\[(?P<caption>.*)\\]\\((?P<address>.*)\\)')
        match = regexp.match(line)
        if match is not None:
            special = True
            print('... image : ', match.groupdict()['caption'])
            text.insert(END, match.groupdict()['caption'] + '\n', 'caption')
            count_disp_line += 1
        regexp = re.compile('^\\[(?P<caption>.*)\\]\\((?P<link>.*)\\)')
        match = regexp.match(line)
        if match is not None:
            special = True
            print('... link : ', match.groupdict()['caption'])
            text.insert(END, match.groupdict()['caption'] + '\n', 'hyperlink')
            count_disp_line += 1
        if not special:
            count_disp_line += insert_mdline(text, line, width_char, size)
        text.tag_add('body', 1.0, END)
        text.tag_config('body',
          lmargin1=(int(offset * 1.2)),
          lmargin2=offset,
          rmargin=offset,
          wrap='word')
        text.tag_config('h1',
          font=font.Font(family=family, size=(int(size * 2)), weight='bold'),
          justify='center')
        text.tag_config('h2',
          font=font.Font(family=family, size=(int(size * 1.6)), weight='bold'))
        text.tag_config('h3',
          font=font.Font(family=family, size=(int(size * 1.3)), weight='bold'))
        text.tag_config('caption',
          font=font.Font(family=family, size=size, weight='bold'))
        text.tag_config('hyperlink',
          foreground='blue',
          underline=True)
        text.tag_config('bold',
          font=font.Font(family=family, size=size, weight='bold'))
        text.tag_config('italic',
          font=font.Font(family=family, size=size, slant='italic'))

    text.configure(height=count_disp_line)
    return text


if __name__ == '__main__':
    mdcontent = '\nBlock 1 desc\n\n# lorem ipsum sic hamet\n\n![toto](toto.png)\n\n[totolink](https://regex101.com/)\n\n## blooo\n\n### fhezjksg\nhjhl *italique*  trap * and * totot. klhl **gras**.\n- puce1 tou **bold** geezer\n- puce2 is it *truue* .\n- puce3 kljklkl\n\n'
    root = Tk()
    text = mdtext(root, mdcontent)
    text.pack()
    root.mainloop()