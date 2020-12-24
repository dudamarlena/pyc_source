# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/util/command.py
# Compiled at: 2019-05-16 13:41:33
import os
from functools import reduce

def path_join(path1, path2):
    return os.path.join(path1, path2 if not path2.startswith('/') else path2.lstrip('/'))


def sh_join(split_command):
    return reduce(lambda accum, arg: accum + ' ' + sh_quote(arg), split_command)


def sh_quote(arg):
    """
    will do shell style quoting for a single shell argument
      such that it can be recombined back into a single string (rather than an array of strings)
      such that shlex.split would resplit the string back into the same array.
    The characters that need quoting within an argument are: double-quote, single-quote, backslash,
      and all the whitespace characters (blank, newline, tab)
    If an arg has none of these, this function returns it as is.
    The simplest implementation of this function would simply put a backslash in front of
      any character that needs special quoting, but that would look really ugly in some cases,
      and since these modified commands end up in the uploader.json file, we try for something
      prettier.
    For the unix shell,
       single-quotes around, quotes everything, but can not contain a quote (this is different
         than Python string literals).
       double-quotes around, quotes single-quotes and whitespace, but double-quotes and backslashes
         must be escaped with a backslash.
       outside of quotes, backslash always escapes the following character

    The way we do this is to count the characters that need quoteing, and ....
    This is simpler to understand, but does at least 6 passes over the string, and can do many
      more.  This generally isn't a problem because most arguments are very short.
    A faster way to implement this would be to do one pass over the string, start building an
      output string as soon as it becomes needed, and stoping once an output string can't be used.
      If more than possible output string is left at the end, choose the best.
      For example, until you see a special character, only the unmodified output string is needed
      As soon as a space is encountered, create the single-quote output, double-quote output,
        and backslash output strings, and drop the unmodified output string.
      As soon as a single-quote is found drop the single-quote output string.
      Etc.

    But for now, do it the slower, simple way.
    """
    double_count = arg.count('"')
    single_count = arg.count("'")
    space_count = arg.count(' ') + arg.count('\t') + arg.count('\n')
    backslash_count = arg.count('\\')
    if double_count + single_count + space_count + backslash_count == 0:
        return arg
    else:
        if single_count == 0:
            return sh_single_quote(arg)
        if double_count + single_count + space_count + backslash_count < 3:
            return sh_backslash_quote(arg)
        return sh_double_quote(arg)


def sh_single_quote(arg):
    return "'" + arg + "'"


def sh_double_quote(arg):
    return '"' + arg.replace('\\', '\\\\').replace('"', '\\"') + '"'


def sh_backslash_quote(arg):
    return arg.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace(' ', '\\ ').replace('\t', '\\\t').replace('\n', '\\\n')