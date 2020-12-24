# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/statisk/PyStatisk.py
# Compiled at: 2020-01-15 09:28:43
# Size of source mod 2**32: 7881 bytes
import re
from statisk import ImageFilter, Log
import sys, os, markdown
from pathlib import Path
DITHER_PREFIX = 'p_'
post_links = list()
post_titles = list()

def bytes_label(size, precision=2):
    suffixes = [
     ' bytes', 'kb', 'mb', 'gb', 'tb']
    suffix_index = 0
    while size > 1024 and suffix_index < 4:
        suffix_index += 1
        size = size / 1024.0

    return '%.*f%s' % (precision, size, suffixes[suffix_index])


def get_value(meta_data, key, show_log):
    key_index = meta_data.find(key)
    if key_index == -1:
        if show_log:
            Log.error('Key {0} does not exist in {1}'.format(key, meta_data))
        return
    data_index = key_index + len(key) + 1
    post_data = meta_data[data_index:]
    return post_data.split(' ')[0]


def process_images(directory, config_str):
    Log.blue('post config: %s' % config_str)
    files = directory.glob('*')
    image_bytes = 0
    for file_name in files:
        file = Path(file_name)
        if not str(file.name).startswith(DITHER_PREFIX):
            if file.name.endswith('.jpeg') or file.name.endswith('.jpg') or file.name.endswith('.png'):
                Log.blue('processing:   %s' % file)
                output_filename = Path(file.parent, '%s%s' % (DITHER_PREFIX, file.name))
                filter_name = get_value(config_str, '-algorithm', False)
                threshold_arg = get_value(config_str, '-threshold', False)
                threshold_value = 255
                if threshold_arg is not None:
                    threshold_value = int(threshold_arg)
                if filter_name is not None:
                    image_foreground = get_value(config_str, '-image_foreground', False)
                    if image_foreground is not None:
                        ImageFilter.foreground = tuple((int(image_foreground.lstrip('#')[i:i + 2], 16) for i in (0,
                                                                                                                 2,
                                                                                                                 4)))
                    else:
                        ImageFilter.foreground = ImageFilter.BLACK
                    image_background = get_value(config_str, '-image_background', False)
                    if image_background is not None:
                        ImageFilter.background = tuple((int(image_background.lstrip('#')[i:i + 2], 16) for i in (0,
                                                                                                                 2,
                                                                                                                 4)))
                    else:
                        ImageFilter.background = ImageFilter.WHITE
                    ImageFilter.filter_from_name(file, threshold_value, output_filename, filter_name)
                else:
                    ImageFilter.filter_dummy(file, 0, output_filename)
            stat_info = os.stat(output_filename)
            size = stat_info.st_size
            image_bytes = image_bytes + size

    return image_bytes


def extract_title(content):
    meta_data_index = content.find('-->')
    if meta_data_index is not -1:
        title = content[meta_data_index + 3:].strip()
    else:
        title = content
    key_index = title.find('#')
    title = title[key_index + 2:]
    return title.split('\n')[0]


def process_markdown(html_template, markdown_file):
    Log.line_break()
    Log.green('processing:  %s' % markdown_file)
    output_filename = markdown_file.name.replace('.md', '.html')
    output_file = Path(markdown_file.parent, output_filename)
    if 'posts/' in str(output_file):
        post_link = str(output_file)
        post_segment_index = post_link.index('posts/')
        post_link = post_link[post_segment_index:]
        post_links.append(post_link)
    Log.blue('output file: %s' % output_file)
    md_stream = open(markdown_file)
    md_content = md_stream.read()
    config_str = md_content.split('\n', 1)[0]
    md_stream.close()
    html = markdown.markdown(md_content)
    output_html = html_template.replace('{{ content }}', html)
    title = extract_title(md_content)
    if 'posts/' in str(output_file):
        post_titles.append(title)
    output_html = output_html.replace('{{ title }}', title)
    if config_str.__contains__('-bg') or config_str.__contains__('-background'):
        background_color = get_value(config_str, '-bg', False)
        if background_color is None:
            background_color = get_value(config_str, '-background', False)
        Log.blue('override page background: %s' % background_color)
        output_html = output_html.replace('<body', str('<body style="background-color:%s"' % background_color))
    images = re.findall('([-\\w]+\\.(?:jpg|gif|png|jpeg))', output_html, re.IGNORECASE)
    if len(images) > 0:
        for image_ref in images:
            processed_filename = '%s%s' % (DITHER_PREFIX, image_ref)
            output_html = output_html.replace(image_ref, processed_filename)

    page_bytes = len(output_html.encode('utf-8'))
    image_bytes = process_images(markdown_file.parent, config_str)
    output_html = output_html.replace('{{ page_size }}', str('Page size including images: ' + bytes_label(image_bytes + page_bytes, 0)))
    output_file.write_text(output_html)


def process_posts(template, posts_directory):
    markdown_files = Path(posts_directory).glob('**/*/*.md')
    for md in markdown_files:
        process_markdown(template, md)


def process_path--- This code section failed: ---

 L. 161         0  LOAD_GLOBAL              Path
                2  LOAD_FAST                'root'
                4  LOAD_STR                 '_template.html'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  STORE_FAST               'template'

 L. 162        10  LOAD_FAST                'template'
               12  LOAD_METHOD              exists
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  POP_JUMP_IF_FALSE   158  'to 158'

 L. 163        18  LOAD_GLOBAL              Log
               20  LOAD_METHOD              grey
               22  LOAD_STR                 '%s exists...'
               24  LOAD_FAST                'template'
               26  BINARY_MODULO    
               28  CALL_METHOD_1         1  '1 positional argument'
               30  POP_TOP          

 L. 164        32  LOAD_GLOBAL              Path
               34  LOAD_FAST                'root'
               36  LOAD_STR                 'posts'
               38  CALL_FUNCTION_2       2  '2 positional arguments'
               40  STORE_FAST               'posts_directory'

 L. 165        42  LOAD_FAST                'posts_directory'
               44  LOAD_METHOD              exists
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  POP_JUMP_IF_FALSE   146  'to 146'

 L. 166        50  LOAD_GLOBAL              Log
               52  LOAD_METHOD              grey
               54  LOAD_STR                 '%s exists...'
               56  LOAD_FAST                'posts_directory'
               58  BINARY_MODULO    
               60  CALL_METHOD_1         1  '1 positional argument'
               62  POP_TOP          

 L. 167        64  LOAD_GLOBAL              open
               66  LOAD_FAST                'template'
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  STORE_FAST               'template_stream'

 L. 168        72  LOAD_FAST                'template_stream'
               74  LOAD_METHOD              read
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  STORE_FAST               'html_template'

 L. 169        80  LOAD_FAST                'template_stream'
               82  LOAD_METHOD              close
               84  CALL_METHOD_0         0  '0 positional arguments'
               86  POP_TOP          

 L. 171        88  LOAD_GLOBAL              process_posts
               90  LOAD_FAST                'html_template'
               92  LOAD_FAST                'posts_directory'
               94  CALL_FUNCTION_2       2  '2 positional arguments'
               96  POP_TOP          

 L. 174        98  LOAD_GLOBAL              Log
              100  LOAD_METHOD              line_break
              102  CALL_METHOD_0         0  '0 positional arguments'
              104  POP_TOP          

 L. 175       106  LOAD_GLOBAL              Log
              108  LOAD_METHOD              grey
              110  LOAD_STR                 'Building index...'
              112  CALL_METHOD_1         1  '1 positional argument'
              114  POP_TOP          

 L. 176       116  LOAD_GLOBAL              Path
              118  LOAD_FAST                'root'
              120  LOAD_STR                 'index.md'
              122  CALL_FUNCTION_2       2  '2 positional arguments'
              124  STORE_FAST               'index_md'

 L. 177       126  LOAD_FAST                'index_md'
              128  LOAD_METHOD              exists
              130  CALL_METHOD_0         0  '0 positional arguments'
              132  POP_JUMP_IF_FALSE   156  'to 156'

 L. 178       134  LOAD_GLOBAL              process_markdown
              136  LOAD_FAST                'html_template'
              138  LOAD_FAST                'index_md'
              140  CALL_FUNCTION_2       2  '2 positional arguments'
              142  POP_TOP          
              144  JUMP_ABSOLUTE       168  'to 168'
            146_0  COME_FROM            48  '48'

 L. 180       146  LOAD_GLOBAL              Log
              148  LOAD_METHOD              fatal_error
              150  LOAD_STR                 'missing posts/ directory'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  POP_TOP          
            156_0  COME_FROM           132  '132'
              156  JUMP_FORWARD        168  'to 168'
            158_0  COME_FROM            16  '16'

 L. 182       158  LOAD_GLOBAL              Log
              160  LOAD_METHOD              fatal_error
              162  LOAD_STR                 'missing _template.html'
              164  CALL_METHOD_1         1  '1 positional argument'
              166  POP_TOP          
            168_0  COME_FROM           156  '156'

Parse error at or near `POP_TOP' instruction at offset 166


def entry():
    Log.title()
    post_links.clear()
    post_titles.clear()
    argument_count = len(sys.argv)
    if argument_count == 1:
        Log.fatal_error('no path argument')
    else:
        arguments = list(sys.argv)
        path_input = arguments[1]
        website_root = Path(path_input)
        if website_root.exists():
            Log.grey('%s exists...' % website_root)
            process_path(website_root)
            posts = ''
            Log.line_break()
            for index in range(len(post_titles)):
                post_link = post_links[index]
                post_title = post_titles[index]
                posts = posts + '<a href="' + post_link + '">' + post_title + '</a><br>\n'
                Log.grey('post_link: ' + post_link + ' post_title: ' + post_title)

            index_path = Path(website_root, 'index.html')
            if index_path.exists():
                index_stream = open(index_path)
                index_template = index_stream.read()
                index_stream.close()
                index_template = index_template.replace('{{ posts }}', posts)
                index_path.write_text(index_template)
            Log.line_break()
            Log.green('Finished')
        else:
            Log.fatal_error('%s cannot be found' % website_root)


if __name__ == '__main__':
    entry()