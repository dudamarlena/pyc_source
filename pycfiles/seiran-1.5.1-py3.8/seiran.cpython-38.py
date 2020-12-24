# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seiran/seiran.py
# Compiled at: 2020-02-03 04:39:14
# Size of source mod 2**32: 19787 bytes
name = 'seiran'
author = 'gargargarrick'
__author__ = 'gargargarrick'
__version__ = '1.5.1'
__copyright__ = 'Copyright 2015-2019 Matthew Ellison'
__license__ = 'GPL'
__maintainer__ = 'gargargarrick'
__status__ = 'Development'
import datetime, os, sys, argparse, sqlite3
from appdirs import *
import seiran.ff_bkm_import, seiran.onetab_bkm_import

def initBookmarks():
    """Check if a bookmarks database already exists."""
    try:
        c.execute('CREATE TABLE bookmarks\n            (title text,url text NOT NULL,date text,folder text,PRIMARY KEY(url))')
        print('Database created.')
    except sqlite3.OperationalError:
        pass


def addBKM(title, url, folder):
    """
    Add a new bookmark to the database.

    Parameters
    ----------

    title : str
        The name of the new bookmark.
    url : str
        The new bookmark's Uniform Resource Locator. Must be unique.
    folder : str
        A category or folder for the new bookmark.
    """
    if title == None:
        title = input('Title? > ')
    elif url == None:
        url = input('URL? > ')
        while not url == '':
            if url[0:4] != 'http':
                print("Sorry, that is empty or doesn't seem to be a URL. (Make sure your URL uses the HTTP or HTTPS protocol.)")
                url = input('URL? > ')

        date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        if folder == None:
            folder = input('Folder/Category? (can be left blank) > ')
    else:
        bkm = (
         title, url, date, folder)
        try:
            c.execute('INSERT INTO bookmarks VALUES (?,?,?,?)', bkm)
            print('Inserted.')
            conn.commit()
        except sqlite3.IntegrityError:
            print('Already exists.')
        except sqlite3.OperationalError:
            print('Operational error')


def delBKM(url):
    """
    Remove a bookmark from the database.

    Parameters
    ----------
    url : str
        The U.R.L. of the bookmark to be deleted.
    """
    if url == None:
        url = input('URL to delete? (Deleted bookmarks cannot be recovered!) > ')
    else:
        sq_url = (
         url,)
        c.execute('SELECT url FROM bookmarks WHERE url=?', sq_url)
        conn.commit()
        if len(c.fetchall()) >= 1:
            try:
                c.execute('DELETE FROM bookmarks WHERE url=?', sq_url)
                conn.commit()
                print('DELETED!')
            except:
                print('Unable to delete for unknown reasons.')

        else:
            print('No bookmark of {url} exists.'.format(url=url))


def listBKMs():
    """
    List all bookmarks in the database. Spaces are included at the ends
    of lines such that the output can be interpreted as Markdown.
    """
    c.execute('SELECT * from bookmarks')
    print('# Seiran Bookmarks')
    template = '\nTitle: {title}  \n  URL: {url}  \n  Date: {date}  \n  Folder: {folder}'
    for i in c.fetchall():
        print(template.format(title=(i[0]), url=(i[1]), date=(i[2]), folder=(i[3])))


def oneSearch(search_term, column):
    """
    Search a single field in the bookmark database.

    Parameters
    ----------
    search_term : str
        The phrase for which to search.
    column : str
        The field to search. Can be title, url, folder, or date.
    """
    sq_search_term = '%{search_term}%'.format(search_term=search_term)
    t = (sq_search_term,)
    if column == 'title':
        c.execute('SELECT * from bookmarks WHERE title LIKE ?', t)
    else:
        if column == 'url':
            c.execute('SELECT * from bookmarks WHERE url LIKE ?', t)
        else:
            if column == 'folder':
                c.execute('SELECT * from bookmarks WHERE folder LIKE ?', t)
            else:
                if column == 'date':
                    c.execute('SELECT * from bookmarks WHERE date LIKE ?', t)
                else:
                    result_list = c.fetchall()
                    if result_list == []:
                        print('No results.')
                    else:
                        print('\n# Seiran - Results for {column}: {search_term}'.format(search_term=search_term, column=column))
                    template = '\nTitle: {title}  \n  URL: {url}  \n  Date: {date}  \n  Folder: {folder}'
                    for i in result_list:
                        print(template.format(title=(i[0]), url=(i[1]), date=(i[2]), folder=(i[3])))


def searchAll(search_term):
    """
    Search all fields in the bookmark database.

    Parameters
    ----------
    search_term : str
        The phrase for which to search.
    """
    sq_search_term = '%{search_term}%'.format(search_term=search_term)
    t = (sq_search_term, sq_search_term, sq_search_term, sq_search_term)
    results = []
    c.execute('SELECT DISTINCT * from bookmarks WHERE title LIKE ? OR url LIKE ? OR folder LIKE ? OR date LIKE ?', t)
    result_list = c.fetchall()
    for i in result_list:
        results.append(i)
    else:
        if results == []:
            print('No results.')
        else:
            print('\n# Seiran - {search_term}'.format(search_term=search_term))
            template = '\nTitle: {title}  \n  URL: {url}  \n  Date: {date}  \n  Folder: {folder}'
            for i in results:
                print(template.format(title=(i[0]), url=(i[1]), date=(i[2]), folder=(i[3])))


def editBKM(url, field, new):
    """
    Edit an existing bookmark.

    Parameters
    ----------
    url : str
        The U.R.L. of the target bookmark.
    field : str
        The field to be edited. Can be title or folder.
    new : str
        The new value for the edited field.
    """
    if url == None:
        url = input('Which URL do you want to edit? > ')
    sq_url = (
     url,)
    c.execute('SELECT * from bookmarks WHERE url = ?', sq_url)
    you_found_it = False
    for row in c:
        print('\nCurrent bookmark data:')
        print('\nTitle: {title}\n  URL: {url}\n  Date: {date}\n  Folder: {folder}'.format(title=(row[0]), url=(row[1]), date=(row[2]), folder=(row[3])))
        you_found_it = True
    else:
        if you_found_it == False:
            print("Sorry, that doesn't seem to be a URL in the database. Try again.")
            return False
        elif field == None:
            field = input('Which field do you wish to edit? (title/category/none)> ')
        else:
            if field == 'folder':
                field = 'category'
            if field not in ('title', 'category'):
                return
                if new == None:
                    new = input('What should the new {field} be? > '.format(field=field))
                    new = str(new)
                newBKM = (
                 new, url)
                if field == 'title':
                    c.execute('UPDATE bookmarks SET title=? WHERE url=?', newBKM)
                    conn.commit()
            elif field == 'category':
                c.execute('UPDATE bookmarks SET folder=? WHERE url=?', newBKM)
                conn.commit()
            else:
                return
        print('\nUpdated bookmark.')
        c.execute('SELECT * from bookmarks WHERE url = ?', sq_url)
        for row in c:
            print('\nTitle: {title}\n  URL: {url}\n  Date: {date}\n  Folder: {folder}'.format(title=(row[0]), url=(row[1]), date=(row[2]), folder=(row[3])))


def getFirefoxBookmarks():
    """
    Import bookmarks from Mozilla-based browsers. (This is an
    experimental feature and may cause errors. Please back up your
    bookmark database before use.)
    """
    fmarks = seiran.ff_bkm_import.importDatabase()
    for i in fmarks:
        bkm = (
         i[0], i[1], str(i[2]), i[3])
        try:
            c.execute('INSERT INTO bookmarks VALUES (?,?,?,?)', bkm)
            conn.commit()
        except sqlite3.IntegrityError:
            print('Duplicate found. Ignoring {i}.'.format(i=(i[1])))
        except sqlite3.OperationalError:
            print('Operational error')

    else:
        print('Import complete!')


def getOneTabBookmarks():
    """Import bookmarks from a OneTab text export."""
    omarks = seiran.onetab_bkm_import.importFromTxt()
    for i in omarks:
        bkm = (
         i[0], i[1], str(i[2]), i[3])
        try:
            c.execute('INSERT INTO bookmarks VALUES (?,?,?,?)', bkm)
            conn.commit()
        except sqlite3.IntegrityError:
            print('Duplicate found. Ignoring {i}.'.format(i=(i[1])))
        except sqlite3.OperationalError:
            print('Operational error')

    else:
        print('Import complete!')


def getSeiranBookmarks():
    """Import bookmarks from an existing Seiran database."""
    print('Warning! This is not well-tested and may ruin everything.')
    print('Back up your database before use!')
    seiran_file = input('Enter the path to the Seiran database you want to copy. > ')
    if seiran_file.lower() == 'q':
        print('Import cancelled.')
        return None
    sconn = sqlite3.connect(seiran_file)
    sc = sconn.cursor()
    attach_main = 'ATTACH DATABASE ? as x'
    main_db_path = installToConfig()
    main_db = (main_db_path,)
    c.execute(attach_main, main_db)
    attach_branch = 'ATTACH DATABASE ? as y'
    branch_db = (seiran_file,)
    c.execute(attach_branch, branch_db)
    c.execute('INSERT OR IGNORE INTO x.bookmarks SELECT * FROM y.bookmarks;')
    conn.commit()
    print('Import complete!')


def exportBookmarks(format):
    """
    Export bookmark database to a file in the user data directory.

    Parameters
    ----------
    format : str
        The target output format. Can be txt or html.
    """
    c.execute('SELECT * from bookmarks')
    if format == 'txt':
        template = 'Title: {title}  \n  URL: {url}  \n  Date: {date}  \n  Folder: {folder}\n'
    else:
        if format == 'html':
            template = "<p><a href={url}>{title}</a> ({folder}) [<time='{date}'>{date}</a>]</p>"
        else:
            bookmarks = []
            for i in c.fetchall():
                if not i[0] == '':
                    if i[0] == None or i[0] == 'None':
                        title = i[1]
                else:
                    title = i[0]
                bookmarks.append(template.format(title=title, url=(i[1]), date=(i[2]), folder=(i[3])))
            else:
                if format == 'txt':
                    bookmarks_write = '\n'.join(bookmarks)
                else:
                    if format == 'html':
                        front_matter = [
                         '<!DOCTYPE HTML>', '<html>', '<head>',
                         '<title>Seiran Bookmarks</title>',
                         '<meta charset="utf-8">', '</head>', '<body>',
                         '<h1>Seiran Bookmarks</h1>']
                        end_matter = [
                         '</body>', '</html>']
                        bookmarks_write = '\n'.join(front_matter + bookmarks + end_matter)

        save_path = user_data_dir(name, author)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_name = 'seiran_bookmarks_export_{date}.{format}'.format(date=(datetime.datetime.now().strftime('%Y-%m-%d')), format=format)
        bookmarks_out = os.path.join(save_path, file_name)
        with open(bookmarks_out, 'w', encoding='utf-8') as (f_out):
            f_out.write(bookmarks_write)
        print('Exported to {bookmarks_out}.'.format(bookmarks_out=bookmarks_out))


def cleanBKMs():
    """
    Perform basic housekeeping features on the bookmarks database.
    It checks for bookmarks without titles, then adds their U.R.L. as a
    title. It also lists bookmarks that have the same title, which may
    indicate duplicates.
    """
    c.execute('SELECT * from bookmarks')
    for i in c.fetchall():
        if not i[0] == '':
            if i[0] == None or i[0] == 'None':
                print("Bookmark {url} doesn't have a title. Adding URL as title.".format(url=(i[1])))
                new_title = i[1]
                newBKM = (new_title, i[1])
                c.execute('UPDATE bookmarks SET title=? WHERE url=?', newBKM)
                conn.commit()
            print('# Seiran Cleanup')
            c.execute('SELECT title, COUNT(*) c FROM bookmarks GROUP BY title HAVING c > 1;')
            result_list = c.fetchall()
            if result_list == []:
                print('No results.')
        else:
            template = '\n{count} bookmarks have the title "{title}":\n'
            for i in result_list:
                print(template.format(title=(i[0]), count=(i[1])))
                t = (i[0],)
                c.execute('SELECT url from bookmarks where title is ?', t)
                url_list = c.fetchall()
                ordinal = 1
                for u in url_list:
                    print('{ordinal}. {url}'.format(ordinal=(str(ordinal)), url=(u[0])))
                    ordinal += 1


def installToConfig():
    """
    Create a Seiran folder in the user's data directory, and get the
    path to the bookmarks database within.

    Returns
    -------
    bookmarks_file : str
        The path to the active bookmarks.db file.
    """
    config_path = user_data_dir(name, author)
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    bookmarks_file = os.path.join(config_path, 'bookmarks.db')
    return bookmarks_file


def main--- This code section failed: ---

 L. 392         0  LOAD_GLOBAL              installToConfig
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'bookmarks_file'

 L. 393         6  LOAD_GLOBAL              sqlite3
                8  LOAD_METHOD              connect
               10  LOAD_FAST                'bookmarks_file'
               12  CALL_METHOD_1         1  ''
               14  STORE_GLOBAL             conn

 L. 394        16  LOAD_GLOBAL              conn
               18  LOAD_METHOD              cursor
               20  CALL_METHOD_0         0  ''
               22  STORE_GLOBAL             c

 L. 395        24  LOAD_GLOBAL              initBookmarks
               26  CALL_FUNCTION_0       0  ''
               28  POP_TOP          

 L. 396        30  LOAD_GLOBAL              print
               32  LOAD_STR                 '{name} by {author}, v.{version}.'
               34  LOAD_ATTR                format
               36  LOAD_GLOBAL              name
               38  LOAD_GLOBAL              __author__
               40  LOAD_GLOBAL              __version__
               42  LOAD_CONST               ('name', 'author', 'version')
               44  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               46  CALL_FUNCTION_1       1  ''
               48  POP_TOP          

 L. 398        50  LOAD_GLOBAL              argparse
               52  LOAD_ATTR                ArgumentParser
               54  LOAD_STR                 'seiran'
               56  LOAD_CONST               ('prog',)
               58  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               60  STORE_FAST               'parser'

 L. 399        62  LOAD_FAST                'parser'
               64  LOAD_ATTR                add_subparsers
               66  LOAD_STR                 'command'
               68  LOAD_STR                 'Commands'
               70  LOAD_CONST               ('dest', 'help')
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  STORE_FAST               'subparsers'

 L. 400        76  LOAD_FAST                'subparsers'
               78  LOAD_ATTR                add_parser
               80  LOAD_STR                 'help'
               82  LOAD_STR                 'List commands'
               84  LOAD_CONST               ('help',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  STORE_FAST               'parser_help'

 L. 401        90  LOAD_FAST                'subparsers'
               92  LOAD_ATTR                add_parser
               94  LOAD_STR                 'add'
               96  LOAD_STR                 'Create a new bookmark.'
               98  LOAD_CONST               ('help',)
              100  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              102  STORE_FAST               'parser_add'

 L. 402       104  LOAD_FAST                'subparsers'
              106  LOAD_ATTR                add_parser
              108  LOAD_STR                 'del'
              110  LOAD_STR                 'Remove a bookmark.'
              112  LOAD_CONST               ('help',)
              114  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              116  STORE_FAST               'parser_del'

 L. 403       118  LOAD_FAST                'subparsers'
              120  LOAD_ATTR                add_parser
              122  LOAD_STR                 'list'
              124  LOAD_STR                 'Display all bookmarks in the database.'
              126  LOAD_CONST               ('help',)
              128  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              130  STORE_FAST               'parser_list'

 L. 404       132  LOAD_FAST                'subparsers'
              134  LOAD_ATTR                add_parser
              136  LOAD_STR                 'search'
              138  LOAD_STR                 'Find specific bookmark(s).'
              140  LOAD_CONST               ('help',)
              142  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              144  STORE_FAST               'parser_search'

 L. 405       146  LOAD_FAST                'subparsers'
              148  LOAD_ATTR                add_parser
              150  LOAD_STR                 'edit'
              152  LOAD_STR                 "Change a bookmark's metadata."
              154  LOAD_CONST               ('help',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  STORE_FAST               'parser_edit'

 L. 406       160  LOAD_FAST                'subparsers'
              162  LOAD_ATTR                add_parser
              164  LOAD_STR                 'import'
              166  LOAD_STR                 'Add bookmarks from anothe system to the database.'
              168  LOAD_CONST               ('help',)
              170  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              172  STORE_FAST               'parser_import'

 L. 407       174  LOAD_FAST                'subparsers'
              176  LOAD_ATTR                add_parser
              178  LOAD_STR                 'export'
              180  LOAD_STR                 'Save all bookmarks to a formatted file.'
              182  LOAD_CONST               ('help',)
              184  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              186  STORE_FAST               'parser_export'

 L. 408       188  LOAD_FAST                'subparsers'
              190  LOAD_ATTR                add_parser
              192  LOAD_STR                 'clean'
              194  LOAD_STR                 'Tidy up bookmark metadata.'
              196  LOAD_CONST               ('help',)
              198  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              200  STORE_FAST               'parser_clean'

 L. 409       202  LOAD_FAST                'subparsers'
              204  LOAD_ATTR                add_parser
              206  LOAD_STR                 'copyright'
              208  LOAD_STR                 'Show legal information.'
              210  LOAD_CONST               ('help',)
              212  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              214  STORE_FAST               'parser_copyright'

 L. 411       216  LOAD_FAST                'parser_add'
              218  LOAD_ATTR                add_argument
              220  LOAD_STR                 '-t'
              222  LOAD_STR                 '--title'
              224  LOAD_STR                 "A bookmark's name. Usually appears in <h1> or <title> tags on the page."
              226  LOAD_CONST               ('help',)
              228  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              230  POP_TOP          

 L. 412       232  LOAD_FAST                'parser_add'
              234  LOAD_ATTR                add_argument
              236  LOAD_STR                 '-u'
              238  LOAD_STR                 '--url'
              240  LOAD_STR                 "A bookmark's Universal Resource Locator. Must be unique."
              242  LOAD_CONST               ('help',)
              244  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              246  POP_TOP          

 L. 413       248  LOAD_FAST                'parser_edit'
              250  LOAD_ATTR                add_argument
              252  LOAD_STR                 '-u'
              254  LOAD_STR                 '--url'
              256  LOAD_STR                 "A bookmark's Universal Resource Locator. Must be unique."
              258  LOAD_CONST               ('help',)
              260  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              262  POP_TOP          

 L. 414       264  LOAD_FAST                'parser_del'
              266  LOAD_ATTR                add_argument
              268  LOAD_STR                 '-u'
              270  LOAD_STR                 '--url'
              272  LOAD_STR                 'The Universal Resource Locator of the bookmark you want to delete.'
              274  LOAD_CONST               ('help',)
              276  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              278  POP_TOP          

 L. 415       280  LOAD_FAST                'parser_add'
              282  LOAD_ATTR                add_argument
              284  LOAD_STR                 '-c'
              286  LOAD_STR                 '--category'
              288  LOAD_STR                 "A bookmark's category. This is inspired by Firefox's folders, but you can put almost anything here."
              290  LOAD_CONST               ('help',)
              292  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              294  POP_TOP          

 L. 416       296  LOAD_FAST                'parser_search'
              298  LOAD_ATTR                add_argument
              300  LOAD_STR                 '-f'
              302  LOAD_STR                 '--field'
              304  LOAD_STR                 'The column you want to search. Available arguments are title, url, category, date, or all.'
              306  LOAD_CONST               ('help',)
              308  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              310  POP_TOP          

 L. 417       312  LOAD_FAST                'parser_edit'
              314  LOAD_ATTR                add_argument
              316  LOAD_STR                 '-f'
              318  LOAD_STR                 '--field'
              320  LOAD_STR                 'The column you want to edit. Available arguments are title or category.'
              322  LOAD_CONST               ('help',)
              324  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              326  POP_TOP          

 L. 418       328  LOAD_FAST                'parser_search'
              330  LOAD_ATTR                add_argument
              332  LOAD_STR                 '-q'
              334  LOAD_STR                 '--query'
              336  LOAD_STR                 'The term you want to search for.'
              338  LOAD_CONST               ('help',)
              340  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              342  POP_TOP          

 L. 419       344  LOAD_FAST                'parser_edit'
              346  LOAD_ATTR                add_argument
              348  LOAD_STR                 '-n'
              350  LOAD_STR                 '--new'
              352  LOAD_STR                 'The new value you want an edited field to have.'
              354  LOAD_CONST               ('help',)
              356  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              358  POP_TOP          

 L. 420       360  LOAD_FAST                'parser_import'
              362  LOAD_ATTR                add_argument
              364  LOAD_STR                 '-i'
              366  LOAD_STR                 '--importformat'
              368  LOAD_STR                 'The system you want to import bookmarks from. Available arguments are firefox, onetab, or seiran.'
              370  LOAD_CONST               ('help',)
              372  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              374  POP_TOP          

 L. 421       376  LOAD_FAST                'parser_export'
              378  LOAD_ATTR                add_argument
              380  LOAD_STR                 '-x'
              382  LOAD_STR                 '--exportformat'
              384  LOAD_STR                 'The format you want to export your bookmarks to. Available options are txt or html.'
              386  LOAD_CONST               ('help',)
              388  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              390  POP_TOP          

 L. 422       392  LOAD_FAST                'parser'
              394  LOAD_METHOD              parse_args
              396  CALL_METHOD_0         0  ''
              398  STORE_FAST               'choice'

 L. 424       400  LOAD_FAST                'choice'
              402  LOAD_ATTR                command
              404  LOAD_STR                 'add'
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_FALSE   434  'to 434'

 L. 425       412  LOAD_GLOBAL              addBKM
              414  LOAD_FAST                'choice'
              416  LOAD_ATTR                title
              418  LOAD_FAST                'choice'
              420  LOAD_ATTR                url
              422  LOAD_FAST                'choice'
              424  LOAD_ATTR                category
              426  CALL_FUNCTION_3       3  ''
              428  POP_TOP          
          430_432  JUMP_FORWARD       1020  'to 1020'
            434_0  COME_FROM           408  '408'

 L. 426       434  LOAD_FAST                'choice'
              436  LOAD_ATTR                command
              438  LOAD_STR                 'del'
              440  COMPARE_OP               ==
          442_444  POP_JUMP_IF_FALSE   460  'to 460'

 L. 427       446  LOAD_GLOBAL              delBKM
              448  LOAD_FAST                'choice'
              450  LOAD_ATTR                url
              452  CALL_FUNCTION_1       1  ''
              454  POP_TOP          
          456_458  JUMP_FORWARD       1020  'to 1020'
            460_0  COME_FROM           442  '442'

 L. 428       460  LOAD_FAST                'choice'
              462  LOAD_ATTR                command
              464  LOAD_STR                 'list'
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_FALSE   490  'to 490'

 L. 429       472  LOAD_GLOBAL              print
              474  LOAD_STR                 'Listing all bookmarks...'
              476  CALL_FUNCTION_1       1  ''
              478  POP_TOP          

 L. 430       480  LOAD_GLOBAL              listBKMs
              482  CALL_FUNCTION_0       0  ''
              484  POP_TOP          

 L. 431       486  LOAD_CONST               None
              488  RETURN_VALUE     
            490_0  COME_FROM           468  '468'

 L. 432       490  LOAD_FAST                'choice'
              492  LOAD_ATTR                command
              494  LOAD_STR                 'search'
              496  COMPARE_OP               ==
          498_500  POP_JUMP_IF_FALSE   674  'to 674'

 L. 433       502  LOAD_FAST                'choice'
              504  LOAD_ATTR                field
              506  STORE_FAST               'field'

 L. 434       508  LOAD_FAST                'field'
              510  LOAD_CONST               None
              512  COMPARE_OP               ==
          514_516  POP_JUMP_IF_FALSE   526  'to 526'

 L. 435       518  LOAD_GLOBAL              input
              520  LOAD_STR                 '  Which field? (title/url/category/date/all) > '
              522  CALL_FUNCTION_1       1  ''
              524  STORE_FAST               'field'
            526_0  COME_FROM           514  '514'

 L. 436       526  LOAD_FAST                'choice'
              528  LOAD_ATTR                query
              530  STORE_FAST               'search_term'

 L. 437       532  LOAD_FAST                'search_term'
              534  LOAD_CONST               None
              536  COMPARE_OP               ==
          538_540  POP_JUMP_IF_FALSE   550  'to 550'

 L. 438       542  LOAD_GLOBAL              input
              544  LOAD_STR                 '  Search term? (case insensitive) > '
              546  CALL_FUNCTION_1       1  ''
              548  STORE_FAST               'search_term'
            550_0  COME_FROM           538  '538'

 L. 439       550  LOAD_FAST                'field'
              552  LOAD_METHOD              lower
              554  CALL_METHOD_0         0  ''
              556  LOAD_STR                 'title'
              558  COMPARE_OP               ==
          560_562  POP_JUMP_IF_FALSE   576  'to 576'

 L. 440       564  LOAD_GLOBAL              oneSearch
              566  LOAD_FAST                'search_term'
              568  LOAD_STR                 'title'
              570  CALL_FUNCTION_2       2  ''
              572  POP_TOP          
              574  JUMP_FORWARD       1020  'to 1020'
            576_0  COME_FROM           560  '560'

 L. 441       576  LOAD_FAST                'field'
              578  LOAD_METHOD              lower
              580  CALL_METHOD_0         0  ''
              582  LOAD_STR                 'url'
              584  COMPARE_OP               ==
          586_588  POP_JUMP_IF_FALSE   604  'to 604'

 L. 442       590  LOAD_GLOBAL              oneSearch
              592  LOAD_FAST                'search_term'
              594  LOAD_STR                 'url'
              596  CALL_FUNCTION_2       2  ''
              598  POP_TOP          

 L. 443       600  LOAD_CONST               None
              602  RETURN_VALUE     
            604_0  COME_FROM           586  '586'

 L. 444       604  LOAD_FAST                'field'
              606  LOAD_METHOD              lower
              608  CALL_METHOD_0         0  ''
              610  LOAD_STR                 'category'
              612  COMPARE_OP               ==
          614_616  POP_JUMP_IF_FALSE   632  'to 632'

 L. 445       618  LOAD_GLOBAL              oneSearch
              620  LOAD_FAST                'search_term'
              622  LOAD_STR                 'folder'
              624  CALL_FUNCTION_2       2  ''
              626  POP_TOP          

 L. 446       628  LOAD_CONST               None
              630  RETURN_VALUE     
            632_0  COME_FROM           614  '614'

 L. 447       632  LOAD_FAST                'field'
              634  LOAD_METHOD              lower
              636  CALL_METHOD_0         0  ''
              638  LOAD_STR                 'date'
              640  COMPARE_OP               ==
          642_644  POP_JUMP_IF_FALSE   658  'to 658'

 L. 448       646  LOAD_GLOBAL              oneSearch
              648  LOAD_FAST                'search_term'
              650  LOAD_STR                 'date'
              652  CALL_FUNCTION_2       2  ''
              654  POP_TOP          
              656  JUMP_FORWARD       1020  'to 1020'
            658_0  COME_FROM           642  '642'

 L. 450       658  LOAD_GLOBAL              searchAll
              660  LOAD_FAST                'search_term'
              662  CALL_FUNCTION_1       1  ''
              664  POP_TOP          

 L. 451       666  LOAD_CONST               None
              668  RETURN_VALUE     
          670_672  JUMP_FORWARD       1020  'to 1020'
            674_0  COME_FROM           498  '498'

 L. 452       674  LOAD_FAST                'choice'
              676  LOAD_ATTR                command
              678  LOAD_STR                 'edit'
              680  COMPARE_OP               ==
          682_684  POP_JUMP_IF_FALSE   708  'to 708'

 L. 453       686  LOAD_GLOBAL              editBKM
              688  LOAD_FAST                'choice'
              690  LOAD_ATTR                url
              692  LOAD_FAST                'choice'
              694  LOAD_ATTR                field
              696  LOAD_FAST                'choice'
              698  LOAD_ATTR                new
              700  CALL_FUNCTION_3       3  ''
              702  POP_TOP          
          704_706  JUMP_FORWARD       1020  'to 1020'
            708_0  COME_FROM           682  '682'

 L. 454       708  LOAD_FAST                'choice'
              710  LOAD_ATTR                command
              712  LOAD_STR                 'import'
              714  COMPARE_OP               ==
          716_718  POP_JUMP_IF_FALSE   852  'to 852'

 L. 457       720  LOAD_GLOBAL              input
              722  LOAD_STR                 'Are you sure you want to import bookmarks? It might take a while. Back up your database first! (y/n) > '
              724  CALL_FUNCTION_1       1  ''
              726  STORE_FAST               'ic'

 L. 458       728  LOAD_FAST                'ic'
              730  LOAD_METHOD              lower
              732  CALL_METHOD_0         0  ''
              734  LOAD_STR                 'y'
              736  COMPARE_OP               ==
          738_740  POP_JUMP_IF_TRUE    756  'to 756'
              742  LOAD_FAST                'ic'
              744  LOAD_METHOD              lower
              746  CALL_METHOD_0         0  ''
              748  LOAD_STR                 'yes'
              750  COMPARE_OP               ==
          752_754  POP_JUMP_IF_FALSE   842  'to 842'
            756_0  COME_FROM           738  '738'

 L. 459       756  LOAD_FAST                'choice'
              758  LOAD_ATTR                importformat
              760  STORE_FAST               'importer_c'

 L. 460       762  LOAD_FAST                'importer_c'
              764  LOAD_CONST               None
              766  COMPARE_OP               ==
          768_770  POP_JUMP_IF_FALSE   780  'to 780'

 L. 461       772  LOAD_GLOBAL              input
              774  LOAD_STR                 'Import from Firefox-type browser, OneTab export, or another Seiran database? (firefox/onetab/seiran) > '
              776  CALL_FUNCTION_1       1  ''
              778  STORE_FAST               'importer_c'
            780_0  COME_FROM           768  '768'

 L. 462       780  LOAD_FAST                'importer_c'
              782  LOAD_STR                 'firefox'
              784  COMPARE_OP               ==
          786_788  POP_JUMP_IF_FALSE   800  'to 800'

 L. 463       790  LOAD_GLOBAL              getFirefoxBookmarks
              792  CALL_FUNCTION_0       0  ''
              794  POP_TOP          

 L. 464       796  LOAD_CONST               None
              798  RETURN_VALUE     
            800_0  COME_FROM           786  '786'

 L. 465       800  LOAD_FAST                'importer_c'
              802  LOAD_STR                 'onetab'
              804  COMPARE_OP               ==
          806_808  POP_JUMP_IF_FALSE   820  'to 820'

 L. 466       810  LOAD_GLOBAL              getOneTabBookmarks
              812  CALL_FUNCTION_0       0  ''
              814  POP_TOP          

 L. 467       816  LOAD_CONST               None
              818  RETURN_VALUE     
            820_0  COME_FROM           806  '806'

 L. 468       820  LOAD_FAST                'importer_c'
              822  LOAD_STR                 'seiran'
              824  COMPARE_OP               ==
          826_828  POP_JUMP_IF_FALSE   850  'to 850'

 L. 469       830  LOAD_GLOBAL              getSeiranBookmarks
              832  CALL_FUNCTION_0       0  ''
              834  POP_TOP          

 L. 470       836  LOAD_CONST               None
              838  RETURN_VALUE     
              840  JUMP_FORWARD        850  'to 850'
            842_0  COME_FROM           752  '752'

 L. 472       842  LOAD_GLOBAL              print
              844  LOAD_STR                 'OK, nothing will be copied.'
              846  CALL_FUNCTION_1       1  ''
              848  POP_TOP          
            850_0  COME_FROM           840  '840'
            850_1  COME_FROM           826  '826'
              850  JUMP_FORWARD       1020  'to 1020'
            852_0  COME_FROM           716  '716'

 L. 473       852  LOAD_FAST                'choice'
              854  LOAD_ATTR                command
              856  LOAD_STR                 'export'
              858  COMPARE_OP               ==
          860_862  POP_JUMP_IF_FALSE   946  'to 946'

 L. 474       864  LOAD_FAST                'choice'
              866  LOAD_ATTR                exportformat
              868  STORE_FAST               'ex_form'

 L. 475       870  LOAD_FAST                'ex_form'
              872  LOAD_CONST               None
              874  COMPARE_OP               ==
          876_878  POP_JUMP_IF_FALSE   888  'to 888'

 L. 476       880  LOAD_GLOBAL              input
              882  LOAD_STR                 'Which format? (html,txt) > '
              884  CALL_FUNCTION_1       1  ''
              886  STORE_FAST               'ex_form'
            888_0  COME_FROM           876  '876'

 L. 477       888  LOAD_FAST                'ex_form'
              890  LOAD_STR                 'html'
              892  COMPARE_OP               ==
          894_896  POP_JUMP_IF_FALSE   910  'to 910'

 L. 478       898  LOAD_GLOBAL              exportBookmarks
              900  LOAD_STR                 'html'
              902  CALL_FUNCTION_1       1  ''
              904  POP_TOP          

 L. 479       906  LOAD_CONST               None
              908  RETURN_VALUE     
            910_0  COME_FROM           894  '894'

 L. 480       910  LOAD_FAST                'ex_form'
              912  LOAD_STR                 'txt'
              914  COMPARE_OP               ==
          916_918  POP_JUMP_IF_FALSE   932  'to 932'

 L. 481       920  LOAD_GLOBAL              exportBookmarks
            922_0  COME_FROM           574  '574'
              922  LOAD_STR                 'txt'
              924  CALL_FUNCTION_1       1  ''
              926  POP_TOP          

 L. 482       928  LOAD_CONST               None
              930  RETURN_VALUE     
            932_0  COME_FROM           916  '916'

 L. 484       932  LOAD_GLOBAL              print
              934  LOAD_STR                 'Export cancelled.'
              936  CALL_FUNCTION_1       1  ''
              938  POP_TOP          

 L. 485       940  LOAD_CONST               None
              942  RETURN_VALUE     
              944  JUMP_FORWARD       1020  'to 1020'
            946_0  COME_FROM           860  '860'

 L. 486       946  LOAD_FAST                'choice'
              948  LOAD_ATTR                command
              950  LOAD_STR                 'clean'
              952  COMPARE_OP               ==
          954_956  POP_JUMP_IF_FALSE   968  'to 968'

 L. 487       958  LOAD_GLOBAL              cleanBKMs
              960  CALL_FUNCTION_0       0  ''
              962  POP_TOP          

 L. 488       964  LOAD_CONST               None
              966  RETURN_VALUE     
            968_0  COME_FROM           954  '954'

 L. 489       968  LOAD_FAST                'choice'
              970  LOAD_ATTR                command
              972  LOAD_STR                 'copyright'
              974  COMPARE_OP               ==
          976_978  POP_JUMP_IF_FALSE   990  'to 990'

 L. 490       980  LOAD_GLOBAL              print
              982  LOAD_STR                 "Copyright 2015-2020 Matthew 'gargargarrick' Ellison. Released under the GNU GPL version 3. See LICENSE for full details."
              984  CALL_FUNCTION_1       1  ''
              986  POP_TOP          
              988  JUMP_FORWARD       1020  'to 1020'
            990_0  COME_FROM           976  '976'

 L. 491       990  LOAD_FAST                'choice'
              992  LOAD_ATTR                command
              994  LOAD_STR                 'help'
              996  COMPARE_OP               ==
         998_1000  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 492      1002  LOAD_GLOBAL              print
           1004_0  COME_FROM           656  '656'
             1004  LOAD_STR                 'Available arguments: add [a bookmark], del[ete a bookmark], list [all bookmarks], search [bookmarks], edit [a bookmark], import [bookmarks from other system], export [bookmarks to other formats], clean [bookmark metadata], copyright, help'
             1006  CALL_FUNCTION_1       1  ''
             1008  POP_TOP          
             1010  JUMP_FORWARD       1020  'to 1020'
           1012_0  COME_FROM           998  '998'

 L. 494      1012  LOAD_GLOBAL              conn
             1014  LOAD_METHOD              close
             1016  CALL_METHOD_0         0  ''
             1018  POP_TOP          
           1020_0  COME_FROM          1010  '1010'
           1020_1  COME_FROM           988  '988'
           1020_2  COME_FROM           944  '944'
           1020_3  COME_FROM           850  '850'
           1020_4  COME_FROM           704  '704'
           1020_5  COME_FROM           670  '670'
           1020_6  COME_FROM           456  '456'
           1020_7  COME_FROM           430  '430'

Parse error at or near `LOAD_STR' instruction at offset 922


if __name__ == '__main__':
    main()