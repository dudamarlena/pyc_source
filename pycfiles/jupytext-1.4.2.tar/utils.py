# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Marc\Documents\GitHub\jupytext\tests\utils.py
# Compiled at: 2019-09-16 15:52:56
import os, sys, re, pytest
from jupytext.cli import system
from jupytext.cell_reader import rst2md
from jupytext.pandoc import is_pandoc_available
from jupytext.kernels import kernelspec_from_language
skip_if_dict_is_not_ordered = pytest.mark.skipif(sys.version_info < (3, 6), reason='unordered dict result in changes in chunk options')

def tool_version(tool):
    try:
        args = tool.split(' ')
        args.append('--version')
        return system(*args)
    except (OSError, SystemExit):
        return

    return


requires_jupytext_installed = pytest.mark.skipif(not tool_version('jupytext'), reason='jupytext is not installed')
requires_black = pytest.mark.skipif(not tool_version('black'), reason='black not found')
requires_flake8 = pytest.mark.skipif(not tool_version('flake8'), reason='flake8 not found')
requires_autopep8 = pytest.mark.skipif(not tool_version('autopep8'), reason='autopep8 not found')
requires_nbconvert = pytest.mark.skipif(not tool_version('jupyter nbconvert'), reason='nbconvert not found')
requires_sphinx_gallery = pytest.mark.skipif(not rst2md, reason='sphinx_gallery is not available')
requires_pandoc = pytest.mark.skipif(not is_pandoc_available(), reason='pandoc>=2.7.2 is not available')
requires_ir_kernel = pytest.mark.skipif(kernelspec_from_language('R') is None, reason='irkernel is not installed')

def list_notebooks(path='ipynb', skip='World'):
    """All notebooks in the directory notebooks/path,
    or in the package itself"""
    if path == 'ipynb':
        return list_notebooks('ipynb_julia', skip=skip) + list_notebooks('ipynb_py', skip=skip) + list_notebooks('ipynb_R', skip=skip)
    if path == 'ipynb_all':
        all_notebooks = []
        nb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'notebooks')
        for dir in os.listdir(nb_path):
            if dir.startswith('ipynb_'):
                all_notebooks.extend(list_notebooks(dir, skip=skip))

        return all_notebooks
    nb_path = os.path.dirname(os.path.abspath(__file__))
    if path.startswith('.'):
        nb_path = os.path.join(nb_path, path)
    else:
        nb_path = os.path.join(nb_path, 'notebooks', path)
    if skip:
        skip_re = re.compile('.*' + skip + '.*')
        notebooks = [ os.path.join(nb_path, nb_file) for nb_file in os.listdir(nb_path) if not skip_re.match(nb_file) ]
    else:
        notebooks = [ os.path.join(nb_path, nb_file) for nb_file in os.listdir(nb_path) ]
    return notebooks