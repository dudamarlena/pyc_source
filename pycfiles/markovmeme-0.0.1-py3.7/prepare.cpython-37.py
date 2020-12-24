# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/markovmeme/data/corpus/office/prepare.py
# Compiled at: 2019-12-29 16:35:46
# Size of source mod 2**32: 1288 bytes
import re, json
with open('office_transcript.csv', 'r') as (filey):
    content = filey.readlines()
lines = {}
for row in content:
    for line in row.split(','):
        line = ' '.join(line.split(';')[1:]).strip()
        if line:
            if ':' in line:
                char, rest = line.split(':', 1)
                line = ''.join(rest)
                if char not in lines:
                    lines[char] = []
            line = line.replace("'", '').replace('"', '').replace('\n', '').strip()
            line = re.sub('\\[.*?\\]', ' ', line).replace('[', ' ').replace(']', '')
            lines[char].append(line.strip())

with open('office.json', 'w') as (filey):
    filey.writelines(json.dumps(lines, indent=4))
with open('../the_office.txt', 'w') as (filey):
    for char, sentences in lines.items():
        for sentence in sentences:
            filey.write('%s\n' % sentence)

for char, sentences in lines.items():
    if len(sentences) > 100:
        with open('%s.txt' % char.lower(), 'w') as (filey):
            for sentence in sentences:
                filey.write('%s\n' % sentence)