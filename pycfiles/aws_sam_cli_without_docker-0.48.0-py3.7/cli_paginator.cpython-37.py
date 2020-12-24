# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/schemas/cli_paginator.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 2334 bytes
"""
Construct one CLI page based on the input provided and returns customer choice
"""
import click

def do_paginate_cli(pages, page_to_be_rendered, items_per_page, is_last_page, cli_display_message):
    """
    Responsible for displaying a generic CLI page with available user choices for pagination/seletion
    :param pages:
    :param page_to_be_rendered:
    :param items_per_page:
    :param is_last_page:
    :param cli_display_message:
    :return: User decision on displayed page
    """
    options = pages.get(page_to_be_rendered)
    choice_num = page_to_be_rendered * items_per_page + 1
    choices = []
    for option in options:
        msg = str(choice_num) + ' - ' + option
        click.echo('\t' + msg)
        choices.append(choice_num)
        choice_num = choice_num + 1

    if len(pages) == 1 and is_last_page:
        message = str.format(cli_display_message['single_page'])
    else:
        if page_to_be_rendered == 0:
            choices = choices + ['N', 'n']
            message = cli_display_message['first_page']
        else:
            if is_last_page:
                if page_to_be_rendered == len(pages) - 1:
                    choices = choices + ['P', 'p']
                    message = cli_display_message['last_page']
                else:
                    choices = choices + ['N', 'n', 'P', 'p']
                    message = cli_display_message['middle_page']
            else:
                final_choices = list(map(str, choices))
                choice = click.prompt(message, type=(click.Choice(final_choices)), show_choices=False)
                if choice in ('N', 'n'):
                    return {'choice':None, 
                     'page_to_render':page_to_be_rendered + 1}
                    if choice in ('P', 'p'):
                        return {'choice':None, 
                         'page_to_render':page_to_be_rendered - 1}
                    index = int(choice) % items_per_page
                    if index == 0:
                        index = items_per_page - 1
                else:
                    index = index - 1
            return {'choice':options[index], 
             'page_to_render':None}