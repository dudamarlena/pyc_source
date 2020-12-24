# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/jupyter_images/__init__.py
# Compiled at: 2019-09-05 11:47:24
# Size of source mod 2**32: 4713 bytes
import re
html_pdf_links_str = '<p>Open: <a href="https://drive.google.com/open?id=IDSTR" target="_blank">https://drive.google.com/open?id=IDSTR</a></p>\n<p>Download: <a href="https://drive.google.com/uc?export=download&id=IDSTR" target="_blank">https://drive.google.com/uc?export=download&id=IDSTR</a></p>'
download_only_str = '<p>Download: <a href="https://drive.google.com/uc?export=download&id=IDSTR" target="_blank">https://drive.google.com/uc?export=download&id=IDSTR</a></p>'
open_only_str = '<p>Open: <a href="https://drive.google.com/open?id=IDSTR" target="_blank">https://drive.google.com/open?id=IDSTR</a></p>'
pure_open_only_str = '<p><a href="https://drive.google.com/open?id=IDSTR" target="_blank">https://drive.google.com/open?id=IDSTR</a></p>'
pure_link_str = '<p><a href="MYPATH" target="_blank">MYPATH</a></p>'
chop_list = [
 '/view', '/edit']

def chop_from_end(linkin):
    linkout = linkin
    for item in chop_list:
        if item in linkout:
            linkout, rest = linkout.split(item, 1)

    return linkout


d_file_types = [
 'file', 'presentation', 'document', 'spreadsheets']

def break_file_d_link(linkin, filetype='file'):
    splitstr = filetype + '/d/'
    base, linkid = linkin.split(splitstr, 1)
    linkid = chop_from_end(linkid)
    return linkid


def break_folder_link(linkin):
    splitstr = '/folders/'
    base, linkid = linkin.split(splitstr, 1)
    linkid = chop_from_end(linkid)
    return linkid


def get_file_id(linkin):
    match = False
    if 'id=' in linkin:
        base, linkid = linkin.split('id=', 1)
        match = True
    else:
        for item in d_file_types:
            search_str = '/' + item + '/'
            if search_str in linkin:
                match = True
                linkid = break_file_d_link(linkin, filetype=item)
                break

    if not match:
        folder_str = '/folders/'
        if folder_str in linkin:
            match = True
            linkid = break_folder_link(linkin)
        else:
            raise ValueError('Cannot work with this link: %s' % linkin)
    return linkid


def jupyter_notebook_gdrive_img_link(linkin, width=700):
    pat = '<img src="https://drive.google.com/uc?id=%s" width=%ipx>'
    my_id = get_file_id(linkin)
    out_str = pat % (my_id, width)
    return out_str


def gdrive_url_builder(linkin):
    my_id = get_file_id(linkin)
    url = 'https://drive.google.com/uc?id=%s' % my_id
    return url


def relative_path_to_link(relpath, width=700):
    pat = '<img src="%s" width=%ipx>'
    img_code = pat % (relpath, width)
    return img_code


def markdown_jupyter_download_link(linkin):
    my_id = get_file_id(linkin)
    download_str = 'https://drive.google.com/uc?export=download&id=%s' % my_id
    out_str = '[%s](%s)' % (download_str, download_str)
    return out_str


def markdown_pdf_open_link(linkin):
    my_id = get_file_id(linkin)
    open_str = 'https://drive.google.com/open?id=%s' % my_id
    out_str = '[%s](%s){target="_blank"}' % (open_str, open_str)
    return out_str


def pdf_link_download_maker(linkin):
    linkid = get_file_id(linkin)
    out_str = html_pdf_links_str.replace('IDSTR', linkid)
    print(out_str)


def pdf_link_download_maker_no_print(linkin):
    linkid = get_file_id(linkin)
    out_str = html_pdf_links_str.replace('IDSTR', linkid)
    return out_str


def pdf_link_download_only_no_print(linkin):
    linkid = get_file_id(linkin)
    out_str = download_only_str.replace('IDSTR', linkid)
    return out_str


def link_open_only_no_print(linkin):
    linkid = get_file_id(linkin)
    out_str = open_only_str.replace('IDSTR', linkid)
    return out_str


def link_pure_open_no_print(linkin):
    linkid = get_file_id(linkin)
    out_str = pure_open_only_str.replace('IDSTR', linkid)
    return out_str


def youtube_link(linkin):
    out_str = pure_link_str.replace('MYPATH', linkin)
    return out_str