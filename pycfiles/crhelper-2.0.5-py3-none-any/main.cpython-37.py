# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mdul/main.py
# Compiled at: 2020-01-31 04:31:03
# Size of source mod 2**32: 2562 bytes
import json, requests, os, re, sys
from argparse import ArgumentParser
import configparser

def main(*argv):
    args = ArgumentParser(description='parse arguments')
    args.add_argument('--imgdir', type=str, dest='img_dir', help='image folder', default='note.assets')
    args.add_argument('--input', type=str, dest='input_file', help='file to be converted', default='note.md')
    args.add_argument('--output', type=str, dest='output_file', help='output file name', default='note_upload.md')
    args.add_argument('--key', type=str, dest='key', help='Secret Token of sm.ms', default='')
    args = args.parse_args()
    img_dir = args.img_dir
    input_file = args.input_file
    output_file = args.output_file
    if not args.key:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.environ['HOME'], '.myconfig'))
        head = {'Authorization': config['sm.ms']['key']}
    else:
        head = {'Authorization': args.key}
    for root, dirs, files in os.walk(img_dir):
        img_paths = list(map(lambda x: os.path.join(root, x), files))

    with open(input_file, 'r') as (f):
        text = f.read()
    for img_path in img_paths:
        if img_path in text:
            files = {'smfile': open(img_path, 'rb')}
            cnt = 0
            while True:
                request = requests.post('https://sm.ms/api/v2/upload', headers=head, files=files, verify=False)
                ret_dict = json.loads(request.text)
                if ret_dict['success']:
                    text = text.replace(img_path, ret_dict['data']['url'])
                    break
                elif ret_dict['code'] == 'image_repeated':
                    text = text.replace(img_path, ret_dict['images'])
                    break
                else:
                    cnt += 1
                    if cnt >= 10:
                        print(ret_dict)
                        break

    for item in set(re.findall('(?s)\\$\\$.*?\\$\\$', text)):
        rep = '```math' + item[2:-2] + '```'
        rep = rep.replace('\\begin{align}', '\\begin{aligned}')
        rep = rep.replace('\\end{align}', '\\end{aligned}')
        rep = rep.replace('\\begin{split}', '\\begin{aligned}')
        rep = rep.replace('\\end{split}', '\\end{aligned}')
        text = text.replace(item, rep)

    for item in set(re.findall('(?s)\\$.*?\\$', text)):
        rep = '`' + item + '`'
        text = text.replace(item, rep)

    with open(output_file, 'w') as (f):
        f.write(text)


if __name__ == '__main__':
    main(sys.argv)