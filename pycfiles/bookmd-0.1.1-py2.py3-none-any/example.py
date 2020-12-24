# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/example.py
# Compiled at: 2015-06-28 04:05:05
from six import print_
bookmark_dir = '.'
import bookmark_pyparser as bpp, os
htmlfiles = []
for root, dirs, files in os.walk(bookmark_dir):
    print_(root)
    htmlfiles_tmp = [ os.path.join(root, fils) for fils in files if fils.split('.')[(-1)].lower() == 'html' ]
    htmlfiles.extend(htmlfiles_tmp)

print_()
result = {}
numhref = 0
for bookmarkfile in htmlfiles:
    print_('############################## parsing ', bookmarkfile)
    parsedfile = bpp.bookmarkshtml.parseFile(open(bookmarkfile))
    numhref += len(bpp.hyperlinks(parsedfile))
    print_('############################## creating a bookmarkDict ')
    bmDict = bpp.bookmarkDict(parsedfile)
    print_('############################## merging latest file into result')
    result = bpp.merge_bookmarkDict(result, bmDict)

finalfile = open('merged bookmarks.html', 'w')
finalstr = bpp.serialize_bookmarkDict(result)
finalfile.write(finalstr)
finalfile.close()
print_('total nunber of hyperlinks found = ', numhref)
print_('number of hyperlinks in final file=', len(bpp.hyperlinks_bookmarkDict(result)))
print_('number of unique hyperlinks =', len(set(bpp.hyperlinks_bookmarkDict(result))))
print_('number of folders =', bpp.count_folders(result))