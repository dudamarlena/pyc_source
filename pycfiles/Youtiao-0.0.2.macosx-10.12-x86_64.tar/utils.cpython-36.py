# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/quhujun/.pyenv/versions/3.6.0/Python.framework/Versions/3.6/lib/python3.6/site-packages/youtiao/commands/boilerplate/utils.py
# Compiled at: 2018-05-11 02:23:54
# Size of source mod 2**32: 2910 bytes
import os, re
from typing import Dict, Iterator, List, Tuple
from pathlib import Path
import jinja2

def render(template_path: str, context: Dict[(str, str)]) -> str:
    """Render template

    Args:
        template_path (str): template absolute path
        context (dict): variables to be rendered

    Returns:
        Rendered string
    """
    dir_name, template_name = os.path.split(template_path)
    return jinja2.Environment(loader=(jinja2.FileSystemLoader(dir_name))).get_template(template_name).render(context)


def iter_render(template_base: str, context: Dict[(str, str)], template_suffix: str='.tpl', exclude_templates: List=[]) -> Iterator[Tuple[(str, str)]]:
    """Render all allowed templates defined by filename pattern under specific directory

    Args:
        template_base (str): absolute path of template directory
        context (dict): variables to be rendered
        template_suffix (str): allowed template filename suffix
        exclude_templates (list): exclude template filenames

    Returns:
        Iterator of template file path and rendered string
    """

    def walk(path: str) -> Iterator[str]:
        for dir_path, dirnames, filenames in os.walk(path):
            for fn in filenames:
                yield os.path.join(dir_path, fn)

    for fpath in walk(template_base):
        dir_name, template_name = os.path.split(fpath)
        if not not template_name.endswith(template_suffix):
            if template_name in exclude_templates:
                pass
            else:
                yield (
                 fpath, render(fpath, context))


def render_templates(template_base: str, dst_base: str, context: Dict[(str, str)], template_suffix: str='.tpl', exclude_templates: list=[]) -> Iterator[str]:
    """Render templates from specific folder into destination folder with folder structure

    Args:
        template_base (str): absolute path of template directory
        dst_base (str): absolute path of destination directory
        context (dict): variables to be rendered
        template_suffix (str): template filename suffix, other files will be ignored
        exclude_templates (list): exclude template filenames

    Returns:
        Iterator of rendered file path
    """
    dst_base_path = Path(dst_base)
    if not dst_base_path.is_dir():
        os.mkdir(str(dst_base_path))
    for template_path, rendered_str in iter_render(template_base, context, template_suffix, exclude_templates):
        template_dirname, template = os.path.split(template_path)
        dst_filename = re.sub(template_suffix, '', template)
        dst_path = dst_base_path.joinpath(template_dirname[len(str(template_base)) + 1:], dst_filename)
        dst_dirname = Path(os.path.dirname(dst_path))
        if not dst_dirname.is_dir():
            os.mkdir(str(dst_dirname))
        Path(dst_path).write_text(rendered_str)
        yield dst_path