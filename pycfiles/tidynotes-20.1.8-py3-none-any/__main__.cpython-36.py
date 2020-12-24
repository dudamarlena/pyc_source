# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dropbox\dropbox\code\tidynotes\src\tidynotes\__main__.py
# Compiled at: 2020-01-20 03:59:12
# Size of source mod 2**32: 2299 bytes
import os
from tidynotes import notebook

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Markdown notebook manager.')
    parser.add_argument('-notedir',
      type=str, help='Notebook directory path.', default=(os.getcwd()))
    parser.add_argument('-g',
      '--generate_note', help='Make a note for today.', action='store_true')
    parser.add_argument('-d', '--make_day', help='Make notes for a specific day.')
    parser.add_argument('-s',
      '--make_series', help='Make notes for n days in the future.', type=int)
    parser.add_argument('-r',
      '--render_all', help='Render all notes.', action='store_true')
    parser.add_argument('-c',
      '--clean_headings',
      help='Clean headings in the notes.',
      action='store_true')
    parser.add_argument('-i',
      '--initialise_notebook',
      help='Create a blank notebook in the target directory.',
      action='store_true')
    parser.add_argument('-e',
      '--extract_project',
      help='Extracts all entries for a single project and renders them to HTML.')
    parser.add_argument('-a',
      '--extract_all',
      help='Extracts all entries for a each project and renders them to HTML.',
      action='store_true')
    args = parser.parse_args()
    if len(os.listdir(args.notedir)) > 0:
        if not args.initialise_notebook:
            print("Use the '-i' argument to force initialisation in a non-empty folder.")
            return
    book = notebook.Tidybook(config_path=(args.notedir),
      initialise=(args.initialise_notebook))
    if args.clean_headings:
        book.clean()
    if args.render_all:
        book.render_notebook()
    if args.generate_note:
        book.make_note()
    if args.make_day is not None:
        book.make_note_str(args.make_day)
    if args.make_series is not None:
        book.make_note_series(args.make_series)
    if args.extract_project is not None:
        book.render_project(args.extract_project)
    if args.extract_all:
        book.render_all_projects()


if __name__ == '__main__':
    main()