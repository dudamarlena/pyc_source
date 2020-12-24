# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nsfw_dl/__main__.py
# Compiled at: 2017-09-19 09:41:52
# Size of source mod 2**32: 1620 bytes
"""
Read the license at:
https://github.com/IzunaDevs/nsfw_dl/blob/master/LICENSE
"""
import argparse, sys, nsfw_dl

def download(downloader, args, file, download_file):
    with nsfw_dl.NSFWDL() as (dl):
        img = dl.download(downloader, args=args)
        if callable(file):
            file = file(img)
        else:
            if download_file:
                with open(file, 'wb') as (f):
                    f.write(dl.get(img))
                    print(file)
            else:
                print(img)


def main(argv=sys.argv[1:]):
    """
    Main entrypoint to nsfw_dl commandline.
    """
    parser = argparse.ArgumentParser()
    image = argparse.ArgumentParser()
    parser.add_argument('action', choices=['image', 'sources'])
    image.add_argument('-d', '--download', help='Download the result to a file.',
      default=False,
      action='store_true')
    image.add_argument('-f', '--file', help='Filename to download to.',
      default=(lambda x: x.split('/')[(-1)]))
    image.add_argument('source', help='Image source to use.')
    image.add_argument('query', help='Tags to use during search.', default='',
      nargs='*')
    args = parser.parse_args(argv)
    if args.action == 'sources':
        sources = '\n'.join('\n'.join(v for v in source) for source in nsfw_dl.SOURCES.values())
        print(sources)
    else:
        args = image.parse_args(argv[1:])
        download(args.source, args.query, args.file, args.download)


if __name__ == '__main__':
    main()