# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/docs/autogen.py
# Compiled at: 2020-03-20 20:49:57
# Size of source mod 2**32: 16721 bytes
from __future__ import print_function
from __future__ import unicode_literals
import re, inspect, os, shutil, six
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

import sciann
from docs.structure import EXCLUDE
from docs.structure import PAGES
from docs.structure import template_np_implementation
from docs.structure import template_hidden_np_implementation
import sys
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding('utf8')
docs_dir = pathlib.Path(__file__).resolve().parents[0]
sciann_dir = pathlib.Path(__file__).resolve().parents[1]

def get_function_signature(function, method=True):
    wrapped = getattr(function, '_original_function', None)
    if wrapped is None:
        signature = inspect.getargspec(function)
    else:
        signature = inspect.getargspec(wrapped)
    defaults = signature.defaults
    if method:
        args = signature.args[1:]
    else:
        args = signature.args
    if defaults:
        kwargs = zip(args[-len(defaults):], defaults)
        args = args[:-len(defaults)]
    else:
        kwargs = []
    st = '%s.%s(' % (clean_module_name(function.__module__), function.__name__)
    for a in args:
        st += str(a) + ', '

    for a, v in kwargs:
        if isinstance(v, str):
            v = "'" + v + "'"
        st += str(a) + '=' + str(v) + ', '

    if kwargs or args:
        signature = st[:-2] + ')'
    else:
        signature = st + ')'
    return post_process_signature(signature)


def get_class_signature(cls):
    try:
        class_signature = get_function_signature(cls.__init__)
        class_signature = class_signature.replace('__init__', cls.__name__)
    except (TypeError, AttributeError):
        class_signature = '{clean_module_name}.{cls_name}()'.format(clean_module_name=(cls.__module__),
          cls_name=(cls.__name__))

    return post_process_signature(class_signature)


def post_process_signature(signature):
    parts = re.split('\\.(?!\\d)', signature)
    if len(parts) >= 4:
        if parts[1] == 'layers':
            signature = 'sciann.layers.' + '.'.join(parts[3:])
        if parts[1] == 'utils':
            signature = 'sciann.utils.' + '.'.join(parts[3:])
        if parts[1] == 'backend':
            signature = 'sciann.backend.' + '.'.join(parts[3:])
    return signature


def clean_module_name(name):
    if name.startswith('sciann_applications'):
        name = name.replace('sciann_applications', 'sciann.applications')
    if name.startswith('sciann_preprocessing'):
        name = name.replace('sciann_preprocessing', 'sciann.preprocessing')
    return name


def class_to_source_link(cls):
    module_name = clean_module_name(cls.__module__)
    path = module_name.replace('.', '/')
    path += '.py'
    line = inspect.getsourcelines(cls)[(-1)]
    link = 'https://github.com/sciann/sciann/tree/master/' + path + '#L' + str(line)
    return '[[source]](' + link + ')'


def code_snippet(snippet):
    result = '```python\n'
    result += snippet.encode('unicode_escape').decode('utf8') + '\n'
    result += '```\n'
    return result


def count_leading_spaces(s):
    ws = re.search('\\S', s)
    if ws:
        return ws.start()
    return 0


def process_list_block--- This code section failed: ---

 L. 123         0  LOAD_FAST                'docstring'
                2  LOAD_METHOD              find
                4  LOAD_STR                 '\n\n'
                6  LOAD_FAST                'starting_point'
                8  CALL_METHOD_2         2  '2 positional arguments'
               10  STORE_FAST               'ending_point'

 L. 124        12  LOAD_FAST                'docstring'
               14  LOAD_FAST                'starting_point'

 L. 125        16  LOAD_FAST                'ending_point'
               18  LOAD_CONST               -1
               20  COMPARE_OP               >
               22  POP_JUMP_IF_FALSE    32  'to 32'
               24  LOAD_FAST                'ending_point'
               26  LOAD_CONST               1
               28  BINARY_SUBTRACT  
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            22  '22'

 L. 126        32  LOAD_FAST                'section_end'
             34_0  COME_FROM            30  '30'
               34  BUILD_SLICE_2         2 
               36  BINARY_SUBSCR    
               38  STORE_FAST               'block'

 L. 128        40  LOAD_FAST                'docstring'

 L. 129        42  LOAD_FAST                'starting_point'
               44  LOAD_FAST                'section_end'
               46  BUILD_SLICE_2         2 
               48  BINARY_SUBSCR    
               50  LOAD_METHOD              replace
               52  LOAD_FAST                'block'
               54  LOAD_FAST                'marker'
               56  CALL_METHOD_2         2  '2 positional arguments'
               58  STORE_FAST               'docstring_slice'

 L. 131        60  LOAD_FAST                'docstring'
               62  LOAD_CONST               None
               64  LOAD_FAST                'starting_point'
               66  BUILD_SLICE_2         2 
               68  BINARY_SUBSCR    
               70  LOAD_FAST                'docstring_slice'
               72  BINARY_ADD       

 L. 132        74  LOAD_FAST                'docstring'
               76  LOAD_FAST                'section_end'
               78  LOAD_CONST               None
               80  BUILD_SLICE_2         2 
               82  BINARY_SUBSCR    
               84  BINARY_ADD       
               86  STORE_FAST               'docstring'

 L. 133        88  LOAD_FAST                'block'
               90  LOAD_METHOD              split
               92  LOAD_STR                 '\n'
               94  CALL_METHOD_1         1  '1 positional argument'
               96  STORE_FAST               'lines'

 L. 135        98  LOAD_CLOSURE             'leading_spaces'
              100  BUILD_TUPLE_1         1 
              102  LOAD_LISTCOMP            '<code_object <listcomp>>'
              104  LOAD_STR                 'process_list_block.<locals>.<listcomp>'
              106  MAKE_FUNCTION_8          'closure'
              108  LOAD_FAST                'lines'
              110  GET_ITER         
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  STORE_FAST               'lines'

 L. 138       116  LOAD_STR                 '^    ([^\\s\\\\\\(]+):(.*)'
              118  STORE_DEREF              'top_level_regex'

 L. 139       120  LOAD_STR                 '- __\\1__:\\2'
              122  STORE_DEREF              'top_level_replacement'

 L. 140       124  LOAD_CLOSURE             'top_level_regex'
              126  LOAD_CLOSURE             'top_level_replacement'
              128  BUILD_TUPLE_2         2 
              130  LOAD_LISTCOMP            '<code_object <listcomp>>'
              132  LOAD_STR                 'process_list_block.<locals>.<listcomp>'
              134  MAKE_FUNCTION_8          'closure'

 L. 141       136  LOAD_FAST                'lines'
              138  GET_ITER         
              140  CALL_FUNCTION_1       1  '1 positional argument'
              142  STORE_FAST               'lines'

 L. 143       144  LOAD_LISTCOMP            '<code_object <listcomp>>'
              146  LOAD_STR                 'process_list_block.<locals>.<listcomp>'
              148  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              150  LOAD_FAST                'lines'
              152  GET_ITER         
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  STORE_FAST               'lines'

 L. 145       158  LOAD_CONST               0
              160  STORE_FAST               'indent'

 L. 146       162  LOAD_CONST               False
              164  STORE_FAST               'text_block'

 L. 147       166  SETUP_LOOP          316  'to 316'
              168  LOAD_GLOBAL              range
              170  LOAD_GLOBAL              len
              172  LOAD_FAST                'lines'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  GET_ITER         
              180  FOR_ITER            314  'to 314'
              182  STORE_FAST               'i'

 L. 148       184  LOAD_FAST                'lines'
              186  LOAD_FAST                'i'
              188  BINARY_SUBSCR    
              190  STORE_FAST               'line'

 L. 149       192  LOAD_GLOBAL              re
              194  LOAD_METHOD              search
              196  LOAD_STR                 '\\S'
              198  LOAD_FAST                'line'
              200  CALL_METHOD_2         2  '2 positional arguments'
              202  STORE_FAST               'spaces'

 L. 150       204  LOAD_FAST                'spaces'
          206_208  POP_JUMP_IF_FALSE   304  'to 304'

 L. 152       210  LOAD_FAST                'line'
              212  LOAD_FAST                'spaces'
              214  LOAD_METHOD              start
              216  CALL_METHOD_0         0  '0 positional arguments'
              218  BINARY_SUBSCR    
              220  LOAD_STR                 '-'
              222  COMPARE_OP               ==
          224_226  POP_JUMP_IF_FALSE   264  'to 264'

 L. 153       228  LOAD_FAST                'spaces'
              230  LOAD_METHOD              start
              232  CALL_METHOD_0         0  '0 positional arguments'
              234  LOAD_CONST               1
              236  BINARY_ADD       
              238  STORE_FAST               'indent'

 L. 154       240  LOAD_FAST                'text_block'
          242_244  POP_JUMP_IF_FALSE   302  'to 302'

 L. 155       246  LOAD_CONST               False
              248  STORE_FAST               'text_block'

 L. 156       250  LOAD_STR                 '\n'
              252  LOAD_FAST                'line'
              254  BINARY_ADD       
              256  LOAD_FAST                'lines'
              258  LOAD_FAST                'i'
              260  STORE_SUBSCR     
              262  JUMP_FORWARD        302  'to 302'
            264_0  COME_FROM           224  '224'

 L. 157       264  LOAD_FAST                'spaces'
              266  LOAD_METHOD              start
              268  CALL_METHOD_0         0  '0 positional arguments'
              270  LOAD_FAST                'indent'
              272  COMPARE_OP               <
          274_276  POP_JUMP_IF_FALSE   312  'to 312'

 L. 158       278  LOAD_CONST               True
              280  STORE_FAST               'text_block'

 L. 159       282  LOAD_FAST                'spaces'
              284  LOAD_METHOD              start
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  STORE_FAST               'indent'

 L. 160       290  LOAD_STR                 '\n'
              292  LOAD_FAST                'line'
              294  BINARY_ADD       
              296  LOAD_FAST                'lines'
              298  LOAD_FAST                'i'
              300  STORE_SUBSCR     
            302_0  COME_FROM           262  '262'
            302_1  COME_FROM           242  '242'
              302  JUMP_BACK           180  'to 180'
            304_0  COME_FROM           206  '206'

 L. 162       304  LOAD_CONST               False
              306  STORE_FAST               'text_block'

 L. 163       308  LOAD_CONST               0
              310  STORE_FAST               'indent'
            312_0  COME_FROM           274  '274'
              312  JUMP_BACK           180  'to 180'
              314  POP_BLOCK        
            316_0  COME_FROM_LOOP      166  '166'

 L. 164       316  LOAD_STR                 '\n'
              318  LOAD_METHOD              join
              320  LOAD_FAST                'lines'
              322  CALL_METHOD_1         1  '1 positional argument'
              324  STORE_FAST               'block'

 L. 165       326  LOAD_FAST                'docstring'
              328  LOAD_FAST                'block'
              330  BUILD_TUPLE_2         2 
              332  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 312_0


def process_docstring(docstring):
    code_blocks = []
    if '```' in docstring:
        tmp = docstring[:]
        while '```' in tmp:
            tmp = tmp[tmp.find('```'):]
            index = tmp[3:].find('```') + 6
            snippet = tmp[:index]
            docstring = docstring.replace(snippet, '$CODE_BLOCK_%d' % len(code_blocks))
            snippet_lines = snippet.split('\n')
            num_leading_spaces = snippet_lines[(-1)].find('`')
            snippet_lines = [snippet_lines[0]] + [line[num_leading_spaces:] for line in snippet_lines[1:]]
            inner_lines = snippet_lines[1:-1]
            leading_spaces = None
            for line in inner_lines:
                if line:
                    if line[0] == '\n':
                        continue
                    spaces = count_leading_spaces(line)
                    if leading_spaces is None:
                        leading_spaces = spaces
                    if spaces < leading_spaces:
                        leading_spaces = spaces

            if leading_spaces:
                snippet_lines = [
                 snippet_lines[0]] + [line[leading_spaces:] for line in snippet_lines[1:-1]] + [
                 snippet_lines[(-1)]]
            snippet = '\n'.join(snippet_lines)
            code_blocks.append(snippet)
            tmp = tmp[index:]

    section_regex = '\\n( +)# (.*)\\n'
    section_idx = re.search(section_regex, docstring)
    shift = 0
    sections = {}
    while section_idx and section_idx.group(2):
        anchor = section_idx.group(2)
        leading_spaces = len(section_idx.group(1))
        shift += section_idx.end()
        next_section_idx = re.search(section_regex, docstring[shift:])
        if next_section_idx is None:
            section_end = -1
        else:
            section_end = shift + next_section_idx.start()
        marker = '$' + anchor.replace(' ', '_') + '$'
        docstring, content = process_list_block(docstring, shift, section_end, leading_spaces, marker)
        sections[marker] = content
        section_idx = re.search(section_regex, docstring[shift:])

    docstring = re.sub('\\n(\\s+)# (.*)\\n', '\\n\\1__\\2__\\n\\n', docstring)
    lines = docstring.split('\n')
    docstring = '\n'.join([line.lstrip(' ') for line in lines])
    for marker, content in sections.items():
        docstring = docstring.replace(marker, content)

    for i, code_block in enumerate(code_blocks):
        docstring = docstring.replace('$CODE_BLOCK_%d' % i, code_block)

    return docstring


def add_np_implementation(function, docstring):
    np_implementation = getattr(numpy_backend, function.__name__)
    code = inspect.getsource(np_implementation)
    code_lines = code.split('\n')
    for i in range(len(code_lines)):
        if code_lines[i]:
            code_lines[i] = '        ' + code_lines[i]

    code = '\n'.join(code_lines[:-1])
    if len(code_lines) < 10:
        section = template_np_implementation.replace('{{code}}', code)
    else:
        section = template_hidden_np_implementation.replace('{{code}}', code)
    return docstring.replace('{{np_implementation}}', section)


def read_file(path):
    with open(path) as (f):
        return f.read()


def collect_class_methods(cls, methods):
    if isinstance(methods, (list, tuple)):
        return [getattr(cls, m) if isinstance(m, str) else m for m in methods]
    methods = []
    for _, method in inspect.getmembers(cls, predicate=(inspect.isroutine)):
        if not method.__name__[0] == '_':
            if method.__name__ in EXCLUDE:
                continue
            methods.append(method)

    return methods


def render_function(function, method=True):
    subblocks = []
    signature = get_function_signature(function, method=method)
    if method:
        signature = signature.replace(clean_module_name(function.__module__) + '.', '')
    subblocks.append('### ' + function.__name__ + '\n')
    subblocks.append(code_snippet(signature))
    docstring = function.__doc__
    if docstring:
        if 'backend' in signature:
            if '{{np_implementation}}' in docstring:
                docstring = add_np_implementation(function, docstring)
        subblocks.append(process_docstring(docstring))
    return '\n\n'.join(subblocks)


def read_page_data(page_data, type):
    assert type in ('classes', 'functions', 'methods')
    data = page_data.get(type, [])
    for module in page_data.get('all_module_{}'.format(type), []):
        module_data = []
        for name in dir(module):
            if name[0] == '_' or name in EXCLUDE:
                continue
            module_member = getattr(module, name)
            if not (inspect.isclass(module_member) and type == 'classes'):
                if not inspect.isfunction(module_member) or type == 'functions':
                    instance = module_member
                    if module.__name__ in instance.__module__ and instance not in module_data:
                        module_data.append(instance)

        module_data.sort(key=(lambda x: id(x)))
        data += module_data

    return data


def get_module_docstring(filepath):
    """Extract the module docstring.

    Also finds the line at which the docstring ends.
    """
    co = compile(open(filepath).read(), filepath, 'exec')
    if co.co_consts and isinstance(co.co_consts[0], six.string_types):
        docstring = co.co_consts[0]
    else:
        print('Could not get the docstring from ' + filepath)
        docstring = ''
    return (
     docstring, co.co_firstlineno)


def copy_examples(examples_dir, destination_dir):
    """Copy the examples directory in the documentation.

    Prettify files by extracting the docstrings written in Markdown.
    """
    pathlib.Path(destination_dir).mkdir(exist_ok=True)
    for file in os.listdir(examples_dir):
        if not file.endswith('.py'):
            continue
        module_path = os.path.join(examples_dir, file)
        docstring, starting_line = get_module_docstring(module_path)
        destination_file = os.path.join(destination_dir, file[:-2] + 'md')
        with open(destination_file, 'w+') as (f_out):
            with open(os.path.join(examples_dir, file), 'r+') as (f_in):
                f_out.write(docstring + '\n\n')
                for _ in range(starting_line):
                    next(f_in)

                f_out.write('```python\n')
                line = next(f_in)
                if line != '\n':
                    f_out.write(line)
                for line in f_in:
                    f_out.write(line)

                f_out.write('```')


def generate(sources_dir):
    """Generates the markdown files for the documentation.

    # Arguments
        sources_dir: Where to put the markdown files.
    """
    template_dir = os.path.join(str(sciann_dir), 'docs', 'templates')
    print('Cleaning up existing sources directory.')
    if os.path.exists(sources_dir):
        shutil.rmtree(sources_dir)
    print('Populating sources directory with templates.')
    shutil.copytree(template_dir, sources_dir)
    readme = read_file(os.path.join(str(sciann_dir), 'README.md'))
    index = read_file(os.path.join(template_dir, 'index.md'))
    index = index.replace('{{autogenerated}}', readme[readme.find('##'):])
    with open(os.path.join(sources_dir, 'index.md'), 'w') as (f):
        f.write(index)
    print('Generating docs for SciANN %s.' % sciann.__version__)
    for page_data in PAGES:
        classes = read_page_data(page_data, 'classes')
        blocks = []
        for element in classes:
            if not isinstance(element, (list, tuple)):
                element = (
                 element, [])
            else:
                cls = element[0]
                subblocks = []
                signature = get_class_signature(cls)
                subblocks.append('<span style="float:right;">' + class_to_source_link(cls) + '</span>')
                if element[1]:
                    subblocks.append('## ' + cls.__name__ + ' class\n')
                else:
                    subblocks.append('### ' + cls.__name__ + '\n')
            subblocks.append(code_snippet(signature))
            docstring = cls.__doc__
            if docstring:
                subblocks.append(process_docstring(docstring))
            methods = collect_class_methods(cls, element[1])
            if methods:
                subblocks.append('\n---')
                subblocks.append('## ' + cls.__name__ + ' methods\n')
                subblocks.append('\n---\n'.join([render_function(method, method=True) for method in methods]))
            blocks.append('\n'.join(subblocks))

        methods = read_page_data(page_data, 'methods')
        for method in methods:
            blocks.append(render_function(method, method=True))

        functions = read_page_data(page_data, 'functions')
        for function in functions:
            blocks.append(render_function(function, method=False))

        if not blocks:
            raise RuntimeError('Found no content for page ' + page_data['page'])
        else:
            mkdown = '\n----\n\n'.join(blocks)
            page_name = page_data['page']
            path = os.path.join(sources_dir, page_name)
            if os.path.exists(path):
                template = read_file(path)
                if '{{autogenerated}}' not in template:
                    raise RuntimeError('Template found for ' + path + ' but missing {{autogenerated}} tag.')
                mkdown = template.replace('{{autogenerated}}', mkdown)
                print('...inserting autogenerated content into template:', path)
            else:
                print('...creating new page with autogenerated content:', path)
        subdir = os.path.dirname(path)
        if not os.path.exists(subdir):
            os.makedirs(subdir)
        with open(path, 'w') as (f):
            f.write(mkdown)

    shutil.copyfile(os.path.join(str(sciann_dir), 'CONTRIBUTING.md'), os.path.join(str(sources_dir), 'contributing.md'))
    copy_examples(os.path.join(str(sciann_dir), 'examples'), os.path.join(str(sources_dir), 'examples'))


if __name__ == '__main__':
    generate(os.path.join(str(sciann_dir), 'docs', 'sources'))