# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sixfoh/cli.py
# Compiled at: 2012-06-28 10:46:20
"""
Generates base sixfoh-encoded images for yer websites.
"""
import os, sys, getopt, mimetypes
options = {'files': None, 
   'mimetypes': [
               'image/jpeg', 'image/png', 'image/gif'], 
   'encoding': 'base64', 
   'output_format': 'image/png', 
   'scheme': 'data:{output_format};{encoding},{content}'}
css_formats = {'less': '@{filename}: "{content}";\n', 
   'scss': '${filename}: "{content}";\n'}
NO_IMAGES_MESSAGE = 'No valid images found'
IMAGE_NOT_FOUND_MESSAGE = "'{0}' not found\n"
FILE_SIZE_WARNING = 'Warning: {0} is larger than 32KB and will not display in IE 8.\n\nPress Enter to continue. Use --force to stifle this warning.'

def print_usage(exit_code=0):
    print '\nUsage: %(cmd)s [-LSf] files\n    %(cmd)s [-h]\n\nOptions\n    --less  Writes images into a group of LessCSS variables, to included in a stylesheet\n            or written to a .less file to be imported. See README.md for examples.\n    --scss  Writes images into a group of Sass variables, to included in a stylesheet\n            or written to a .scss file to be imported. See README.md for examples.\n    -f      Force output and ignore warnings.\n    ' % {'cmd': os.path.basename(sys.argv[0])}
    sys.exit(exit_code)


def parse_opts(args):
    try:
        opts, args = getopt.getopt(args, 'hfLS', [
         'help', 'files', 'less', 'scss', 'force'])
    except getopt.GetoptError:
        print_usage(1)

    if args:
        options['files'] = args
    for opt, optarg in opts:
        if opt in ('-h', '--help'):
            print_usage()
        elif opt in ('-L', '--less'):
            options['less'] = True
        elif opt in ('-S', '--scss'):
            options['scss'] = True
        elif opt in ('-f', '--force'):
            options['force'] = True


def parse_file_mimetypes(images):
    file_list = []
    for file in images:
        if not os.path.isfile(file):
            print IMAGE_NOT_FOUND_MESSAGE.format(file)
            continue
        mimetype = mimetypes.guess_type(file)[0]
        if mimetype in options['mimetypes']:
            file_list.append([file, mimetype])

    if file_list:
        return file_list
    print NO_IMAGES_MESSAGE
    sys.exit()


def encode_image(image, mimetype):
    image_size = os.path.getsize(image)
    content = open(image, 'r').read().encode(options['encoding']).replace('\n', '')
    output = options['scheme'].format(output_format=mimetype, encoding=options['encoding'], content=content)
    if image_size > 32000:
        if not options.get('force'):
            raw_input(FILE_SIZE_WARNING.format(image))
            return output
        else:
            return output

    else:
        return output


def output_css(image, mimetype, format):
    print css_formats[format].format(filename=os.path.splitext(image)[0].replace(' ', '_'), content=encode_image(image, mimetype))


def main():
    parse_opts(sys.argv[1:])
    if options.get('files'):
        files = options['files']
    else:
        files = sorted([ f for f in os.listdir('.') if os.path.isfile(f) ])
    images = parse_file_mimetypes(files)
    for image, mimetype in images:
        if options.get('less'):
            output_css(image, mimetype, 'less')
        elif options.get('scss'):
            output_css(image, mimetype, 'scss')
        else:
            print encode_image(image, mimetype) + '\n'