# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/g/projects/superhelp/build/lib/superhelp/displayers/cli_displayer.py
# Compiled at: 2020-04-15 03:58:31
# Size of source mod 2**32: 2575 bytes
from textwrap import dedent
from superhelp import mdv_fixed as mdv
from .. import conf
TERMINAL_WIDTH = 220
SHORT_LINE = '--'
LONG_LINE = '------------------------------------------------------------------------------------------------------------------------'
MDV_CODE_BOUNDARY = '```'

def get_message(message_dets, message_level):
    message = dedent(message_dets.message[message_level])
    if message_level == conf.EXTRA:
        message = dedent(message_dets.message[conf.MAIN]) + message
    warning_str = 'WARNING:\n' if message_dets.warning else ''
    message = dedent(warning_str + message)
    message = message.replace(f"    {conf.PYTHON_CODE_START}", MDV_CODE_BOUNDARY).replace(f"\n    {conf.PYTHON_CODE_END}", MDV_CODE_BOUNDARY)
    message = mdv.main(md=message)
    return message


def display(snippet, messages_dets, *, message_level=conf.BRIEF, in_notebook=False):
    """
    Show by code blocks.
    """
    mdv.term_columns = TERMINAL_WIDTH
    text = [mdv.main(f"{LONG_LINE}\n# SuperHELP - Help for Humans!\n"),
     mdv.main(f"\n{SHORT_LINE}\n"),
     'Help is provided for your overall snippet and for each line as appropriate.\n',
     f"Currently showing {message_level} content as requested"]
    text.append(mdv.main(dedent(f"## Overall Snippet\n{MDV_CODE_BOUNDARY}\n" + snippet + f"\n{MDV_CODE_BOUNDARY}")))
    overall_messages_dets, block_messages_dets = messages_dets
    for message_dets in overall_messages_dets:
        message = get_message(message_dets, message_level)
        text.append(message)

    block_messages_dets.sort(key=(lambda nt: nt.first_line_no))
    prev_line_no = None
    for message_dets in block_messages_dets:
        line_no = message_dets.first_line_no
        if line_no != prev_line_no:
            text.append(mdv.main(f"{LONG_LINE}\n## Code block starting line {line_no:,}"))
            text.append(mdv.main(dedent(f"{MDV_CODE_BOUNDARY}\n" + message_dets.code_str + f"\n{MDV_CODE_BOUNDARY}")))
            prev_line_no = line_no
        message = get_message(message_dets, message_level)
        text.append(message)

    content = '\n'.join(text)
    print(content)