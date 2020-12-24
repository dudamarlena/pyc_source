# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/gnomikologikon_fortune/gnomikologikon_fortune.py
# Compiled at: 2018-12-02 09:18:03
# Size of source mod 2**32: 7659 bytes
import requests, bs4
from bs4 import BeautifulSoup
import os, re, argparse
from pathlib import Path

def get_cat_info():
    """
    Gets category names from the website

    :return: 2 lists containing the category names and URL suffixes for the categories,respectively.
    :rtype: list
    """
    categ = requests.get('https://www.gnomikologikon.gr/categ.php')
    soup = BeautifulSoup(categ.content, 'html.parser')
    test = soup.find_all('table', {'class': 'authrst'})
    broadcateg = []
    for tag in test:
        broadcateg.append(str(tag.find('td', {'class': 'authrsh'}).contents[0]))

    gencateg = dict.fromkeys(broadcateg)
    del broadcateg
    for key in gencateg.keys():
        gencateg[key] = [[], []]

    for tag in test:
        catname = str(tag.find('td', {'class': 'authrsh'}).contents[0])
        for item in list(tag.find('div', {'class': 'cgs'}).find_all('a')):
            gencateg[catname][0].append(str(item.contents))
            gencateg[catname][1].append(item.attrs['href'])

    for key in gencateg.keys():
        for i in range(len(gencateg[key][0])):
            gencateg[key][0][i] = re.search('([\\w\\s]+)', str(gencateg[key][0][i]), re.UNICODE).group(0)

    return gencateg


def choose_cat(categories):
    """
    This function asks the user to choose a category and then returns its URL

    :param categories: Dictionary of categories
    :type categories: dict
    :rtype: list
    """
    catlist = []
    for i, key in enumerate(categories.keys()):
        print(i + 1, key)
        catlist.append(key)

    while True:
        sel = input('Select a category: ')
        try:
            if catlist[(int(sel) - 1)] in categories.keys():
                key = catlist[(int(sel) - 1)]
                break
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print('You must enter a valid number!')
            continue

    del catlist
    for i, catname in enumerate(categories[key][0]):
        print(i + 1, catname)

    while True:
        print('You can select a single category, a range of categories(by using -) or multiple categories by seperating numbers with a whitespace')
        sel = input('Please select: ')
        catsel = []
        urlsel = []
        try:
            selections = sel.split(' ')
            for item in selections:
                if '-' in item:
                    rang = sel.split('-')
                    rang[0] = int(rang[0]) - 1
                    rang[1] = int(rang[1])
                    for category in range(*rang):
                        catsel.append(categories[key][0][category])
                        urlsel.append(categories[key][1][category])

                else:
                    catsel.append(categories[key][0][(int(item) - 1)])
                    urlsel.append(categories[key][1][(int(item) - 1)])

            break
        except (KeyboardInterrupt, SystemExit):
            raise
        except (ValueError, IndexError):
            print('You must enter a valid number!')
            continue

    return (
     catsel, urlsel)


def get_cat_quotes(url, file, append=False, filepath=None):
    if filepath is not None:
        filepath = filepath.rstrip(' ')
    page = requests.get('https://www.gnomikologikon.gr/' + url)
    souppage = BeautifulSoup(page.content, 'html.parser')
    del page
    test = souppage.find_all('table', {'class': 'quotes'})
    results = list()
    for result in test:
        results.append(result.find_all('td', {'class': 'quote'}))

    for set in results:
        for quote in set:
            try:
                author = quote.find('a', {'class': 'author'}).text
            except AttributeError:
                try:
                    author = quote.find('p', {'class': 'auth2'}).text
                except AttributeError:
                    author = 'Άγνωστος'

            string = ''
            for item in quote.contents:
                if isinstance(item, bs4.element.NavigableString):
                    string += item + ' '

            string = string.replace('\r', '')
            file.write('{0}\n  - {1}\n%\n'.format(string, author))

    if not append:
        file.close()
        command = 'strfile "{}"'.format(filepath)
        os.system(command)


def get_quote_all(categs, urls, path, args):
    if len(categs) != len(urls):
        raise ValueError('You must input two lists of the same length!')
    else:
        path.mkdir(exist_ok=True)
        if args.single_file:
            if args.single_file is 'default':
                filepath = str(path) + '/' + str(categs[0]) + ' and ' + str(len(categs) - 1) + ' more'
            else:
                filepath = args.single_file
            if Path(filepath).is_file():
                sel = input('File already exists. Do you want to replace it? [yes/No]')
                if 'y' not in sel.lower():
                    raise FileExistsError
            file = open(filepath.rstrip(' '), 'a')
            file.truncate(0)
            for url in urls:
                get_cat_quotes(url, file, True)

            command = 'strfile "{}"'.format(filepath)
            os.system(command)
        else:
            for i, url in enumerate(urls):
                filepath = str(path) + '/' + categs[i]
                if Path(filepath).is_file():
                    sel = input('File already exists. Do you want to replace it? [yes/No]')
                    if 'y' not in sel.lower():
                        raise FileExistsError
                file = open(filepath.rstrip(' '), 'w')
                get_cat_quotes(url, file, filepath=filepath)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-dir', help='Output directory', type=str)
    parser.add_argument('-s', '--single-file', help='output all categories to a single file',
      nargs='?',
      const='default',
      type=str)
    args = parser.parse_args()
    if args.output_dir:
        if '/' not in args.output_dir:
            path = str(args.output_dir)
        else:
            if re.match('(.*/.*)*', str(args.output_dir)):
                path = str(args.output_dir)
            else:
                raise ValueError('You must specify a valid path')
        if re.match('.*/$', args.output_dir) is None:
            args.output_dir = args.output_dir + '/'
    if not re.match('\\w*', str(args.single_file)):
        raise ValueError('File name must only contain letters, numbers and underscores!')
    elif args.output_dir is not None:
        path = Path(args.output_dir)
    else:
        path = Path(os.getcwd())
    allcategories = get_cat_info()
    categories, urls = choose_cat(dict(allcategories))
    for i, item in enumerate(categories):
        categories[i] = re.search('(\\w*\\s\\w*)*', item).string

    get_quote_all(categories, urls, path, args)


if __name__ == '__main__':
    main()