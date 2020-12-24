# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\grodriguez\Downloads\gitchangelog\src\gitchangelog\parameters_to_use.py
# Compiled at: 2020-02-10 10:38:49
# Size of source mod 2**32: 1804 bytes


def parameter_to_clean(opts):
    if opts.clean:
        cleaner = opts.clean
        return cleaner
    else:
        return


def change_title(opts):
    try:
        if opts.title:
            new_title = opts.title
            return ' '.join(new_title)
        else:
            if opts.title is []:
                return 'Changelog'
            return 'Changelog'
    except TypeError:
        return 'Changelog'


def parameter_to_show(opts):
    try:
        if opts.show:
            to_show = opts.show
            return to_show
        else:
            return
    except TypeError:
        return


def change_jira_url(opts, jira_url):
    try:
        if opts.url:
            new_url = opts.url
            return ' '.join(new_url)
        else:
            return jira_url
    except TypeError:
        return


def give_file_name(opts):
    try:
        if opts.file:
            new_file = opts.file
            return ' '.join(new_file)
        else:
            return
    except TypeError:
        return


def change_template(opts, config):
    if opts.template:
        try:
            from gitchangelog import mustache
        except Exception:
            from gitchangelog.gitchangelog import mustache

        new_route = ' '.join(opts.template)
        config['output_engine'] = mustache(new_route)
        return config['output_engine']


def module_implementation(opts):
    if opts.module:
        module_to_show = ' '.join(opts.module)
        return module_to_show