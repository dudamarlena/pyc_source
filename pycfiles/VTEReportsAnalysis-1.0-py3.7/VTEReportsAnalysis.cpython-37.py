# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\VTEReportsAnalysis\VTEReportsAnalysis.py
# Compiled at: 2020-05-05 06:16:32
# Size of source mod 2**32: 1225 bytes
from .extractor import *
import pkg_resources
resource_package = 'VTEReportsAnalysis'
resource_path = '/'.join(('config', 'config.txt'))
path = pkg_resources.resource_filename(resource_package, resource_path)
target = []
skip = []
absolute_negative = []
absolute_positive = []
start = []
active_section = 0
with open(path, 'r') as (config):
    lines = config.readlines()
    lines.remove('\n')
    for line in lines:
        if line == '':
            continue
        elif '#target_phrases' in line:
            active_section = target
        else:
            if '#skip_phrases' in line:
                active_section = skip
            else:
                if '#absolute_negative' in line:
                    active_section = absolute_negative
                else:
                    if '#absolute_positive' in line:
                        active_section = absolute_negative
                    else:
                        if 'start' in line:
                            active_section = start
        if '#' not in line:
            active_section.append(line.strip())

config.close()
phrases = [
 target, skip, absolute_negative, absolute_positive, start]
for phrase in phrases:
    while '' in phrase:
        phrase.remove('')

extractors = reExtractor(target, skip, absolute_negative, absolute_positive, start)

def extraction(text):
    return extractors.processing(text)