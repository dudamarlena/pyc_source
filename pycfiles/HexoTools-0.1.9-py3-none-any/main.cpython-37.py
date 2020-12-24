# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\projects\hexotools\hexotools\gui\main.py
# Compiled at: 2019-10-12 03:56:27
# Size of source mod 2**32: 6209 bytes
import PySimpleGUI as sg
import hexotools.imgmanage as I
from . import functions as F
from ..sh import sh as S
import pyperclip, re, os
text_setting = {}
button_setting = {}
introduction = '###---上传文件---###\n选中图片文件后即可上传,\nMarkdown源码会自动复制到粘贴板!!!\n\n\n###---删除图片---###\n删除服务器上图片则请复制图片链接到粘贴板\n'
menu = [
 [
  '设置', ['设置', 'Run_CWD', '退出']],
 [
  '关于', ['关于...', 'README']]]
tab_hexo = [
 [
  sg.Frame(title='Hexo 指令', title_color='black',
    relief=(sg.RELIEF_SUNKEN),
    layout=[
   [
    sg.Button('启动本地服务器'),
    sg.Button('部署')],
   [
    sg.B('停止本地服务器'),
    sg.B('新建')]])],
 [
  sg.Button('分类')]]
tab_img = [
 [
  (sg.Text)('选中的图片', size=(15, 1), 
   auto_size_text=False, 
   justification='right', **text_setting),
  (sg.InputText)('图片本地路径', tooltip='仅上传时使用', 
   key='_img_path_', **text_setting),
  sg.FileBrowse('浏览', file_types=[
   ('图片文件', '*.png *.jpg *.jpeg *.bmp')],
    tooltip='选择图片')],
 [
  (sg.Text)('图片描述', size=(15, 1), 
   auto_size_text=False, 
   justification='right', **text_setting),
  (sg.InputText)('这是一个图片', key='_description_', **text_setting)],
 [
  sg.Button('上传')],
 [
  sg.Multiline(introduction, key='_result_', size=(70, 18))],
 [
  sg.Button('删除服务器上图片', tooltip='请确保图片链接在剪贴板')]]
tab_output = [
 [
  sg.Frame('自己写?', layout=[
   [
    sg.InputText(focus=True, key='_sh_'),
    sg.Button('Run', bind_return_key=True)]])],
 [
  sg.T('程序运行部分信息......')], [sg.Output(size=(65, 25))]]
layout = [
 [
  sg.Menu(menu, tearoff=True)],
 [
  sg.TabGroup([
   [
    sg.Tab('图床管理', tab_img),
    sg.Tab('Hexo', tab_hexo),
    sg.Tab('Info', tab_output)]])]]
window = sg.Window('Hexo Tools',
  layout,
  icon=(F.ICON_PATH))
up_down = I.UpDownload()
if F.getConf('pop_introduction') != None:
    if F.getConf('pop_introduction'):
        sg.Popup('请在及时设置博客路径和相关信息!!!', title='初始化',
          auto_close=True,
          auto_close_duration=2,
          icon=(F.ICON_PATH))
        while not F.initConf():
            sg.Popup('(￣▽￣), 设置啊', icon=(F.ICON_PATH))
            F.initConf()

db = I.Db(F.getConf('db'))
db.creatTable()
while 1:
    event, values = window.Read()
    if not event is None:
        if event == '退出':
            break
        img = I.Img(path=(values['_img_path_']))
        if event == '上传':
            img.path = values['_img_path_']
            img.localExists()
            if img.local_exists:
                img.hash = ''
                result = db.isRepeative(hash=(img.hash))
                if result:
                    result = (F.urlFormat)(*result[0])
                    pyperclip.copy(re.search('.*#\\n(!\\[.*?\\))', result).group(1))
                    window.Element('_result_').Update('图片已经在数据库中\n\n' + result)
                else:
                    reponse = up_down.localUpload(img.path)
                code, url, delete_url = up_down.evalResult(reponse)
                if code == 'success' or code == 'exception':
                    result = F.urlFormat(url, delete_url, values['_description_'], values['_img_path_'])
                    pyperclip.copy(re.search('.*#\\n(!\\[.*?\\))', result).group(1))
                    window.Element('_result_').Update(result)
                    img.url, img.delete_url = url, delete_url
                    img.description = values['_description_']
                    db.insertData(img.data())
                else:
                    window.Element('_result_').Update('\n文件不存在ㄟ( ▔, ▔ )ㄏ')
            else:
                if event == '删除服务器上图片':
                    img.url = pyperclip.paste()
                    result = db.isRepeative(url=(img.url))
                    if result:
                        delete_url = result[0][1]
                        if up_down.imgDelete(delete_url) and db.deleteRow(url=(img.url)):
                            window.Element('_result_').Update('\n删除成功(￣y▽￣)╭ Ohohoho.....')
                        else:
                            window.Element('_result_').Update('\n删除失败(⊙o⊙)？')
                    else:
                        window.Element('_result_').Update('\n不在数据库中 (￣_￣|||)~~')
        else:
            if event == '启动本地服务器':
                popen_server = S.startServer()
        if event == '停止本地服务器':
            if S.stopNodeProcess(popen_server.pid):
                sg.Popup('成功', icon=(F.ICON_PATH))
            else:
                sg.Popup('失败', icon=(F.ICON_PATH))
        elif event == '部署':
            S.deploy()
        elif event == '新建':
            F.newPostUi()
        elif event == '分类':
            F.editCate()
        elif event == 'Run':
            S.executeCommand(values['_sh_'])
        elif event == '关于...':
            sg.Popup('关于', 'Github:https://github.com/ShoorDay/HexoTools',
              icon=(F.ICON_PATH))
        elif event == 'README':
            S.webReadme()
        elif event == '设置':
            F.confUi()
        else:
            if event == 'Run_CWD':
                cwd = sg.PopupGetFolder('选择文件夹', no_window=True)
                F.setConf('cwd', cwd)
            continue

db.closeCursor()
db.closeConn()
window.Close()