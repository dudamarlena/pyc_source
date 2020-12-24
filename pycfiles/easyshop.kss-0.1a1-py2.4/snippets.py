# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/kss/snippets.py
# Compiled at: 2008-06-20 09:36:23
PRODUCT_DETAILS = '\n<table class="shop-default">\n    <tr>\n        <td width="210px"\n            class="image">\n            <img src="%(url)s/image_mini" />\n        </td>\n        \n        <td class="information">\n            <a href="%(url)s">\n                %(title)s\n                (%(short_title)s)\n            </a>    \n            <div>%(article_id)s</div>        \n            <p>\n                %(short_text)s\n        \n                <span class="label">\n                    Price\n                </span>                                \n                <span>\n                    %(price)s\n                </span>\n            </p>\n'
RELATED_PRODUCTS_HEADER = '\n    <div class="label">\n        Related Products\n    </div>\n    <ul>\n'
RELATED_PRODUCTS_BODY = '\n    <li>\n        <a href="%(url)s">\n            <span>%(title)s</span>\n            <span>%(article_id)s</span>\n        </a>    \n    </li>\n'
RELATED_PRODUCTS_FOOTER = '\n    </ul>\n'
CATEGORIES_HEADER = '\n    <div class="label">\n        Categories\n    </div>\n    <ul>\n'
CATEGORIES_BODY = '\n    <li>\n        <a href="%(url)s">\n            <span>%(title)s</span>\n        </a>    \n    </li>\n'
CATEGORIES_FOOTER = '\n    </ul>\n'
GROUPS_HEADER = '\n    <div class="label">\n        Groups\n    </div>\n    <ul>\n'
GROUPS_BODY = '\n    <li>\n        <a href="%(url)s">\n            <span>%(title)s</span>\n        </a>    \n    </li>\n'
GROUPS_FOOTER = '\n    </ul><td></tr></table>\n'