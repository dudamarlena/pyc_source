# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/zope/Extensions/Method.py
# Compiled at: 2011-04-12 15:57:23
from linkexchange.zope import support as lx_support

def get_block(self, request, num):
    """
    Returns links block #num for specified request. Use this function as Zope
    External Method with following parameters:

        Id: LinkExchangeBlock
        Module Name: linkexchange.zope.Method
        Function Name: get_block

    Then you can use in in templates:

        <div tal:content="structure python: context.LinkExchangeBlock(request,0)"></div>
    """
    return lx_support.get_blocks(request)[num]


def get_links(self, request):
    """
    Returns raw links for specified request.
    """
    return lx_support.get_links(request)


def content_filter(self, request, content):
    """
    Filters content through clients content_filter().
    """
    return lx_support.content_filter(request, content)