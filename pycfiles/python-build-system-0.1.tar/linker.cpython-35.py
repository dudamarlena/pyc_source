# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kiv/projects/python-build-system/python_build_system/modules/platform/tools/linker.py
# Compiled at: 2016-10-24 12:35:02
# Size of source mod 2**32: 865 bytes
import os

def link_executable(ctx, sources):
    if not isinstance(sources, list) or len(sources) == 0:
        return
    output_file_name = os.path.join(ctx.build_dir, ctx.get_param('PROJECT_NAME') + ctx.get_param('EXECUTABLE_SUFFIX'))
    linker = ctx.get_param('LINKER')
    assert linker, 'LINKER not defined'
    flags = ctx.get_param('LINK_FLAGS[]')
    sources_str = ''
    for source in sources:
        if source.endswith('.ld'):
            flags += ' -T "%s"' % source
        else:
            sources_str += '"' + source + '" '

    command = '"%s" %s -o "%s" %s' % (linker, sources_str, output_file_name, flags)
    ctx.run_command(command, sources, output_file_name)
    ctx.add_param('EXECUTABLE_NAME', output_file_name)
    return output_file_name


def load_to_context(ctx, config):
    ctx.add_rule('.*\\.(o|ld)$', link_executable)