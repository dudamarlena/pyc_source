# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xmind2Excel\ui3.py
# Compiled at: 2019-07-02 07:46:05
# Size of source mod 2**32: 4186 bytes
__author__ = '8034.com'
__date__ = '2018-11-08'
import sys, os
from tkinter import *
from tkinter import messagebox, filedialog
FILE_PATH = os.path.dirname(os.path.realpath(__file__))

def file_extension(path):
    return os.path.splitext(path)[1]


def file_name(path):
    return os.path.splitext(path)[0]


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets(master)

    def selectXmindFile(self):
        string_filename = ''
        print(os.path.join(FILE_PATH, 'templet'))
        filenames = filedialog.askopenfilename(initialdir=(os.path.join(FILE_PATH, 'templet')))
        print(filenames)
        if len(filenames) != 0:
            string_filename = filenames
            text = '您选择的文件是：' + string_filename
        else:
            text = '您没有选择任何文件'
        print(text)
        self.xmind_Text.delete(0.0, END)
        self.xmind_Text.insert(1.0, string_filename if string_filename else text)
        src_path = os.path.dirname(string_filename)
        excel_file = os.path.join(src_path, 'to.xls')
        excel_file = excel_file.replace('\\', '/')
        self.excel_file_Text.delete(0.0, END)
        self.excel_file_Text.insert(1.0, excel_file)
        return string_filename

    def doxmind2xls(self):
        xmind_Text_content = self.xmind_Text.get('1.0', END).strip()
        excel_file_Text_content = self.excel_file_Text.get('1.0', END).strip()
        result = 'running...'
        from xmind2Excel.libs.genexcel import GenerateExcel
        xmindParse = GenerateExcel(excel_file_Text_content)
        result = xmindParse.main(xmind_Text_content)
        self.sp05_Label.config(text=result)
        print('********************')
        return 'ok'

    def createWidgets(self, master=None):
        self.frame_1 = Frame(master)
        self.xmind_Text = Text((self.frame_1), height='1', width='60')
        self.xmind_Text.pack(side=LEFT, expand=YES)
        self.xmind_Text.insert(INSERT, 'xmind Path')
        self.sp01_Label = Label((self.frame_1), text='<==', height='1', width='5')
        self.sp01_Label.pack(side=LEFT, expand=YES)
        self.select_file_button = Button((self.frame_1), text='选择文件', command=(self.selectXmindFile))
        self.select_file_button.pack()
        self.frame_1.pack(side=TOP)
        self.frame_2 = Frame(master)
        self.excel_file_Text = Text((self.frame_2), height='1', width='60')
        self.excel_file_Text.pack(side=LEFT, expand=YES)
        self.excel_file_Text.insert(INSERT, '目标路径')
        self.sp02_Label = Label((self.frame_2), text='<==', height='1', width='5')
        self.sp02_Label.pack(side=LEFT, expand=YES)
        self.excel_file_Label = Label((self.frame_2), text='生成xls ', height='1')
        self.excel_file_Label.pack()
        self.frame_2.pack(side=TOP)
        self.frame_4 = Frame(master)
        self.change_toxlsx_Button = Button((self.frame_4), text='Xmind转为xlsx', state='normal', command=(self.doxmind2xls))
        self.change_toxlsx_Button.pack(side=LEFT, expand=YES)
        self.sp04_Label = Label((self.frame_4), text=' ', height='1', width='5')
        self.sp04_Label.pack(side=LEFT, expand=YES)
        self.change_Button = Button((self.frame_4), text='Xmind转为xls', state='normal', command=(self.doxmind2xls))
        self.change_Button.pack(side=LEFT, expand=YES)
        self.sp05_Label = Label((self.frame_4), text=' ', height='1', width='5')
        self.sp05_Label.pack(side=LEFT, expand=YES)
        self.quitButton = Button((self.frame_4), text='Quit', command=(self.quit))
        self.quitButton.pack(side=LEFT)
        self.frame_4.pack(side=TOP)
        self.frame_5 = Frame(master)
        self.sp05_Label = Label((self.frame_5), text=' ', height='1', width='80')
        self.sp05_Label.pack(side=LEFT, expand=YES)
        self.frame_5.pack(side=TOP)