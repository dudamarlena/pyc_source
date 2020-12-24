# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/galfect/cmdline.py
# Compiled at: 2016-03-16 03:53:13
import re, sys, os.path as op, argparse as ap
from galfect.initialize import GalfectInitialize
from tempfile import mkstemp
from shutil import move
from os import remove, close
res = {'comment': '//', 
   'aside': '---$', 
   'avatar': '-.*\\((.*)\\):$', 
   'scene': '#(\\d+) (.*)$', 
   'end': '\\* END(.*)$', 
   'choose': '> (.*)\\((\\d+)\\)$', 
   'url': '\\[(.*)\\]:(.*)$'}
for key in res:
    res[key] = re.compile(res[key])

empty_img = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='
title = ''

def replace_title(path, text):
    fh, abs_path = mkstemp()
    with open(abs_path, 'w') as (new_file):
        with open(path) as (old_file):
            for line in old_file:
                new_file.write(line.replace('<title>Show White</title>', text))

    close(fh)
    remove(path)
    move(abs_path, path)


def analyze(lines):
    global title
    chapter, pos, scene, avatar, url, chaps, states = (
     0, 1, '', '', {}, {}, [])
    title = '<title>' + lines[0] + '</title>'
    n = len(lines)
    while pos < n:
        l = lines[pos]
        end, dialog, choose = '', '', {}
        pos += 1
        if not l or res['comment'].match(l):
            continue
        if res['aside'].match(l):
            avatar = empty_img
        elif res['avatar'].match(l):
            avatar = res['avatar'].match(l).group(1) or empty_img
        elif res['scene'].match(l):
            m = res['scene'].match(l)
            chapter = m.group(1)
            scene = m.group(2) or empty_img
            avatar = empty_img
        elif res['end'].match(l):
            end = res['end'].match(l).group(1) or 'END'
        elif res['choose'].match(l):
            m = res['choose'].match(l)
            choose[m.group(1)] = m.group(2)
            while pos < n:
                m = res['choose'].match(lines[pos])
                if m:
                    choose[m.group(1)] = m.group(2)
                    pos += 1
                else:
                    break

        elif res['url'].match(l):
            m = res['url'].match(l)
            url[m.group(1)] = m.group(2)
        else:
            dialog = l
        if end or dialog or choose:
            if chapter not in chaps:
                chaps[chapter] = len(states)
            state = {'avatar': avatar, 'scene': scene}
            if end:
                state['end'] = end
            if dialog:
                state['dialog'] = dialog
            if choose:
                state['choose'] = choose
            states.append(state)

    for s in states:
        if s['scene'] in url:
            s['scene'] = url[s['scene']]
        if s['avatar'] in url:
            s['avatar'] = url[s['avatar']]
        if 'choose' in s:
            for key in s['choose']:
                s['choose'][key] = chaps[s['choose'][key]]

    pos = len(states) - 1
    while pos > 0:
        for key in ('avatar', 'scene'):
            if states[pos][key] == states[(pos - 1)][key]:
                states[pos].pop(key, None)

        pos -= 1

    return states


def load(f):
    fh = open(f, 'r')
    content = fh.readlines()
    fh.close()
    return map(str.strip, content)


def generate(outdir, output):
    fh = open(op.join(outdir, 'js', 'main.js'), 'w')
    fh.write('var strs=' + str(output) + ';')
    fh.close()


def execute(argv=None):
    if argv is None:
        argv = sys.argv
    parser = ap.ArgumentParser(description='tranfer drama file to html pages')
    parser.add_argument('-output', help='specify the output')
    parser.add_argument('drama_file', help='the drama file')
    args = parser.parse_args()
    drama = args.drama_file
    if not op.isfile(drama):
        print drama, 'is not a file.'
        exit(1)
    else:
        outdir = args.output or op.basename(op.splitext(drama)[0])
        if op.exists(outdir):
            prompt = outdir + ' already exists.\n  Do you want to override it?[Y]es/[N]o:'
            out = raw_input(prompt)
            while out.lower() != 'y' and out.lower() != 'n':
                out = raw_input(prompt)

            if out == 'n':
                exit(0)
        GalfectInitialize(outdir).run()
        generate(outdir, analyze(load(drama)))
        replace_title(op.join(outdir, 'index.html'), title)
    return