# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cmusselle/Mango/Workspace/masonry/package/src/masonry/postprocess.py
# Compiled at: 2017-10-24 14:50:41
# Size of source mod 2**32: 7209 bytes
import ast, fnmatch, os
from .utils import rindex
from clint.textui import puts, indent, STDOUT

def combine_file_snippets(project_dir, stream=STDOUT):
    """ Recusively search for files ending in posfix/prefix and join them to their originals """
    for dirpath, dirnames, filenames in os.walk(project_dir):
        if '.git' in dirnames:
            dirnames.remove('.git')
        postfix_files = fnmatch.filter(filenames, '*_postfix*')
        prefix_files = fnmatch.filter(filenames, '*_prefix*')
        if postfix_files or prefix_files:
            puts(f"Applying postprocessing in {dirpath} ...", stream=stream)
        with indent(4):
            for postfile in postfix_files:
                original = os.path.join(dirpath, postfile.replace('_postfix', ''))
                if os.path.exists(original):
                    postfile = os.path.join(dirpath, postfile)
                    if postfile.endswith('.py') and original.endswith('.py'):
                        all_text = insert_code(postfile, original, kind='postfix')
                        with open(original, 'w') as (f):
                            f.write(all_text)
                        os.remove(postfile)
                        puts(f"Postfixing python code to {os.path.basename(original)}",
                          stream=stream)
                    else:
                        postfix_text(postfile, original)
                        puts(f"Postfixing text to {os.path.basename(original)}", stream=stream)
                else:
                    raise ValueError(f"Original file not found for specified postfix: {postfile}")

        with indent(4):
            for prefile in prefix_files:
                original = os.path.join(dirpath, prefile.replace('_prefix', ''))
                if os.path.exists(original):
                    prefile = os.path.join(dirpath, prefile)
                    if prefile.endswith('.py'):
                        if original.endswith('.py'):
                            all_text = insert_code(prefile, original, kind='prefix')
                            with open(original, 'w') as (f):
                                f.write(all_text)
                            os.remove(prefile)
                            puts(f"Prefixing python code to {os.path.basename(original)}",
                              stream=stream)
                    else:
                        prefix_text(prefile, original)
                        puts(f"Prefixing text to {os.path.basename(original)}", stream=stream)
                else:
                    raise ValueError(f"Original file not found for specified prefix: {prefile}")


def postfix_text(src, dest):
    """ Add the content of src to the end of dest file and remove src file """
    with open(dest, 'a') as (fout):
        with open(src) as (fin):
            fout.write(fin.read())
    os.remove(fin.name)


def prefix_text(src, dest):
    """ Add the content of src file path to the begining of dest file path and remove src """
    with open(src, 'a') as (fout):
        with open(dest) as (fin):
            fout.write(fin.read())
    os.remove(fin.name)
    os.rename(fout.name, fin.name)


def insert_code(src, dest, kind):
    """Insert code in source into destination file."""
    source_text = open(src).read().strip()
    destination_text = open(dest).read()
    destination_lines = destination_text.split('\n')
    destination_tree = ast.parse(destination_text)
    if not destination_tree.body:
        idx = 0
    else:
        if kind == 'prefix':
            idx = find_prefix_insertion_idx(destination_tree)
        else:
            if kind == 'postfix':
                idx = find_postfix_insertion_idx(destination_tree)
        if idx >= len(destination_tree.body):
            if destination_lines[(-1)].strip() == '':
                del destination_lines[-1]
            destination_lines.append('\n\n' + source_text + '\n')
        else:
            line_no = destination_tree.body[idx].lineno - 1
            line_no = get_previous_blank_line_no(destination_lines, line_no)
            if destination_lines[(line_no - 1)].strip() == '':
                del destination_lines[line_no - 1]
                line_no -= 1
            destination_lines.insert(line_no, '\n\n' + source_text + '\n')
    all_text = '\n'.join(destination_lines)
    return all_text


def find_prefix_insertion_idx(module_ast):
    """Return prefix insertion point. 

    This is the point in the code after any imports and constants, but before any functions or 
    classes are defined. 
    """
    node_types = [type(x) for x in module_ast.body]
    func_class_pos = [x == ast.FunctionDef or x == ast.ClassDef for x in node_types]
    import_pos = [x == ast.Import or x == ast.ImportFrom for x in node_types]
    docstring_present = isinstance(node_types[0], ast.Expr) and isinstance(node_types[0].value, ast.Str)
    constants_pos = [isinstance(elem, ast.Assign) and elem.targets[0].id.isupper() for elem in module_ast.body]
    last_node = module_ast.body[(-1)]
    ifname_present = isinstance(last_node, ast.If) and last_node.test.left.id == '__name__'
    if any(func_class_pos):
        insert_idx = func_class_pos.index(True)
    else:
        if any(constants_pos):
            insert_idx = rindex(constants_pos, True)
            insert_idx += 1
        else:
            if any(import_pos):
                insert_idx = rindex(import_pos, True)
                insert_idx += 1
            else:
                if docstring_present:
                    insert_idx = 1
                else:
                    if ifname_present:
                        insert_idx = -1
    return insert_idx


def find_postfix_insertion_idx(module_ast):
    """Return postfix insertion point. 

    This is the point in the code after any functions or classes are defined, but before the ifname
    statement if present. 
    """
    node_types = [type(x) for x in module_ast.body]
    func_class_pos = [x == ast.FunctionDef or x == ast.ClassDef for x in node_types]
    last_node = module_ast.body[(-1)]
    ifname_present = isinstance(last_node, ast.If) and last_node.test.left.id == '__name__'
    if any(func_class_pos):
        insert_idx = rindex(func_class_pos, True)
        insert_idx += 1
    else:
        if ifname_present:
            insert_idx = -1
        else:
            insert_idx = len(module_ast.body)
    return insert_idx


def get_previous_blank_line_no(lines, idx):
    """Find a blank line before the object definition"""
    while True:
        if not lines[idx].strip():
            break
        else:
            idx -= 1

    return idx