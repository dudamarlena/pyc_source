# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jsick/.virtualenvs/paperweight/lib/python2.7/site-packages/paperweight/texutils.py
# Compiled at: 2015-01-12 15:24:15
"""
Utilities for maniuplating latex documents.
"""
import os, re, codecs, fnmatch, logging
from .gitio import read_git_blob
__all__ = [
 'find_root_tex_document', 'iter_tex_documents', 'inline',
 'inline_blob', 'inline_bbl', 'remove_comments']
cite_pattern = re.compile('\\\\cite((.*?)((\\[.*?\\])*)){(.*?)}', re.UNICODE)
section_pattern = re.compile('\\\\section{(.*?)}', re.UNICODE)
bib_pattern = re.compile('\\\\bibliography{(.*?)}', re.UNICODE)
input_pattern = re.compile('\\\\input{(.*?)}', re.UNICODE)
input_ifexists_pattern = re.compile('\\\\InputIfFileExists{(.*)}{(.*)}{(.*)}', re.UNICODE)
docclass_pattern = re.compile('\\\\documentclass(.*?){(.*?)}', re.UNICODE)

def find_root_tex_document(base_dir='.'):
    r"""Find the tex article in the current directory that can be considered
    a root. We do this by searching contents for ``'\documentclass'``.

    Parameters
    ----------
    base_dir : str
        Directory to search for LaTeX documents, relative to the current
        working directory.

    Returns
    -------
    tex_path : str
        Path to the root tex document relative to the current
        working directory.
    """
    log = logging.getLogger(__name__)
    for tex_path in iter_tex_documents(base_dir=base_dir):
        with codecs.open(tex_path, 'r', encoding='utf-8') as (f):
            text = f.read()
            if len(docclass_pattern.findall(text)) > 0:
                log.debug(('Found root tex {0}').format(tex_path))
                return tex_path

    log.warning('Could not find a root .tex file')
    raise RootNotFound


def iter_tex_documents(base_dir='.'):
    """Iterate through all .tex documents in the current directory."""
    for path, dirlist, filelist in os.walk(base_dir):
        for name in fnmatch.filter(filelist, '*.tex'):
            yield os.path.join(path, name)


class RootNotFound(BaseException):
    pass


def inline_bbl(root_tex, bbl_tex):
    """Inline a compiled bibliography (.bbl) in place of a bibliography
    environment.

    Parameters
    ----------
    root_tex : unicode
        Text to process.
    bbl_tex : unicode
        Text of bibliography file.

    Returns
    -------
    txt : unicode
        Text with bibliography included.
    """
    bbl_tex = bbl_tex.replace('\\', '\\\\')
    result = bib_pattern.sub(bbl_tex, root_tex)
    return result


def inline(root_text, base_dir='', replacer=None, ifexists_replacer=None):
    r"""Inline all input latex files.

    The inlining is accomplished recursively. All files are opened as UTF-8
    unicode files.

    Parameters
    ----------
    root_txt : unicode
        Text to process (and include in-lined files).
    base_dir : str
        Base directory of file containing ``root_text``. Defaults to the
        current working directory.
    replacer : function
        Function called by :func:`re.sub` to replace ``\input`` expressions
        with a latex document. Changeable only for testing purposes.
    ifexists_replacer : function
        Function called by :func:`re.sub` to replace ``\InputIfExists``
        expressions with a latex document. Changeable only for
        testing purposes.

    Returns
    -------
    txt : unicode
        Text with referenced files included.
    """

    def _sub_line(match):
        """Function to be used with re.sub to inline files for each match."""
        fname = match.group(1)
        if not fname.endswith('.tex'):
            full_fname = ('.').join((fname, 'tex'))
        else:
            full_fname = fname
        full_path = os.path.abspath(os.path.join(base_dir, full_fname))
        try:
            with codecs.open(full_path, 'r', encoding='utf-8') as (f):
                included_text = f.read()
        except IOError:
            print ('Cannot open {0} for in-lining').format(full_path)
            return ''

        new_base_dir = os.path.dirname(full_path)
        included_text = inline(included_text, new_base_dir)
        return included_text

    def _sub_line_ifexists(match):
        """Function to be used with re.sub for the input_ifexists_pattern."""
        fname = match.group(1)
        if not fname.endswith('.tex'):
            full_fname = ('.').join((fname, 'tex'))
        else:
            full_fname = fname
        full_path = os.path.abspath(os.path.join(base_dir, full_fname))
        new_base_dir = os.path.dirname(full_path)
        if os.path.exists(full_path):
            with codecs.open(full_path, 'r', encoding='utf-8') as (f):
                included_text = f.read()
            included_text = ('\n').join((included_text, match.group(2)))
        else:
            included_text = match.group(3)
        included_text = inline(included_text, new_base_dir)
        return included_text

    result = input_pattern.sub(_sub_line, root_text)
    result = input_ifexists_pattern.sub(_sub_line_ifexists, result)
    return result


def inline_blob(commit_ref, root_text, root_path, repo_dir=''):
    """Inline all input latex files that exist as git blobs in a tree object.

    The inlining is accomplished recursively. All files are opened as UTF-8
    unicode files.

    Parameters
    ----------
    commit_ref : str
        String identifying a git commit/tag.
    root_text : unicode
        Text of tex document where referenced files will be inlined.
    root_path : str
        Path of file containing root_text relative to the git directory.
    repo_dir : str
        Directory of the containing git repository.

    Returns
    -------
    txt : unicode
        Text with referenced files included.
    """

    def _sub_blob(match):
        """Function to be used with re.sub to inline files for each match."""
        fname = match.group(1)
        if not fname.endswith('.tex'):
            full_fname = ('.').join((fname, 'tex'))
        else:
            full_fname = fname
        git_rel_path = os.path.relpath(os.path.join(repo_dir, root_path, full_fname), repo_dir)
        included_text = read_git_blob(commit_ref, git_rel_path, repo_dir=repo_dir)
        if included_text is None:
            with codecs.open(full_fname, 'r', encoding='utf-8') as (f):
                included_text = f.read()
        included_text = inline_blob(commit_ref, included_text, git_rel_path, repo_dir=repo_dir)
        return included_text

    def _sub_blob_ifexists(match):
        """Function to be used with re.sub for the input_ifexists_pattern."""
        fname = match.group(1)
        if not fname.endswith('.tex'):
            full_fname = ('.').join((fname, 'tex'))
        else:
            full_fname = fname
        git_rel_path = os.path.relpath(os.path.join(repo_dir, root_path, full_fname), repo_dir)
        included_text = read_git_blob(commit_ref, git_rel_path, repo_dir=repo_dir)
        if included_text is not None:
            included_text = ('\n').join((included_text, match.group(2)))
        if included_text is None:
            included_text = match.group(3)
        included_text = inline_blob(commit_ref, included_text, git_rel_path, repo_dir=repo_dir)
        return included_text

    result = input_pattern.sub(_sub_blob, root_text)
    result = input_ifexists_pattern.sub(_sub_blob_ifexists, result)
    return result


def remove_comments(tex):
    """Delete latex comments from a manuscript.

    Parameters
    ----------
    tex : unicode
        The latex manuscript

    Returns
    -------
    tex : unicode
        The manuscript without comments.
    """
    return re.sub('(?<!\\\\)%.*', '', tex)