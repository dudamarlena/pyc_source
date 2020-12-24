# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Projects\HexoTools\hexotools\gui.py
# Compiled at: 2019-10-06 04:30:58
# Size of source mod 2**32: 5403 bytes
import PySimpleGUI as sg
import imgmanage.img as I
import functions as F
import sh.sh as S
import pyperclip, re
text_setting = {}
button_setting = {}
introduction = '###---上传文件---###\n选中图片文件后即可上传,\nMarkdown源码会自动复制到粘贴板!!!\n\n\n###---删除图片---###\n删除服务器上图片则请复制图片链接到粘贴板\n'
menu = [
 [
  '设置', ['Blog文件夹', 'Run_CWD', '退出']],
 [
  '关于', ['关于...', 'README']]]
tab_hexo = [
 [
  sg.Frame(title='Hexo 指令', title_color='black',
    relief=(sg.RELIEF_SUNKEN),
    tooltip='Use these to set flags',
    layout=[
   [
    (sg.Button)(*('本地服务器', ), **button_setting),
    (sg.Button)(*('部署', ), **button_setting)]])],
 [
  (sg.Button)(*('分类', ), **button_setting)]]
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
  (sg.Button)(*('上传', ), **button_setting)],
 [
  sg.Multiline(introduction, key='_result_', size=(70, 18))],
 [
  (sg.Button)('删除服务器上图片', tooltip='请确保图片链接在剪贴板', **button_setting)]]
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
    sg.Tab('Hexo', tab_hexo, tooltip=''),
    sg.Tab('Info', tab_output)]])]]
window = sg.Window('Hexo Tools', layout)
db = I.Db()
db.creatTable()
up_down = I.UpDownload()
while 1:
    event, values = window.Read()
    if not event is None:
        if event == '退出':
            break
        img = I.Img(path=(values['_img_path_']))
        if event == '本地服务器':
            S.startServer()
        elif event == '部署':
            S.deploy()
        elif event == '上传':
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
            elif event == '删除服务器上图片':
                img.url = pyperclip.paste()
                result = db.isRepeative(url=(img.url))
                if result:
                    delete_url = result[0][1]
                    if up_down.imgDelete(delete_url) and db.deleteRow(img.url):
                        window.Element('_result_').Update('\n删除成功(￣y▽￣)╭ Ohohoho.....')
                    else:
                        window.Element('_result_').Update('\n删除失败(⊙o⊙)？')
                else:
                    window.Element('_result_').Update('\n不在数据库中 (￣_￣|||)~~')
        elif event == '分类':
            F.editCate()
        elif event == 'Run':
            S.executeCommand(values['_sh_'])
        elif event == '关于...':
            sg.Popup('关于', '不关于')
        elif event == 'Blog文件夹':
            blog_path = sg.PopupGetFolder('选择文件夹', no_window=True)
            F.setPath(blog_path)
        else:
            if event == 'Run_CWD':
                cwd = sg.PopupGetFolder('选择文件夹', no_window=True)
                F.setCwd(cwd)
            continue

db.closeCursor()
db.closeConn()
window.Close()