# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/csstools/client/v_render_info_fetcher.py
# Compiled at: 2013-04-04 15:36:36


class VRenderInfoFetcher(object):
    ATTR_TARGET_COMPONENT = 'c'
    ATTR_PROPERTIES = 'props'
    ATTR_RENDER_INFO = 'ri'


class CssProperty(object):
    width = 'width'
    height = 'height'
    marginTop = 'marginTop'
    marginRight = 'marginRight'
    marginBottom = 'marginBottom'
    marginLeft = 'marginLeft'
    paddingTop = 'paddingTop'
    paddingRight = 'paddingRight'
    paddingBottom = 'paddingBottom'
    paddingLeft = 'paddingLeft'
    borderTopWidth = 'borderTopWidth'
    borderRightWidth = 'borderRightWidth'
    borderBottomWidth = 'borderBottomWidth'
    borderLeftWidth = 'borderLeftWidth'
    fontSize = 'fontSize'
    color = 'color'
    display = 'display'
    visibility = 'visibility'
    overflow = 'overflow'
    overflowX = 'overflowX'
    overflowY = 'overflowY'
    position = 'position'
    top = 'top'
    right = 'right'
    bottom = 'bottom'
    left = 'left'
    zIndex = 'zIndex'
    absoluteTop = 'absoluteTop'
    absoluteLeft = 'absoluteLeft'
    _values = [
     width, height, marginTop, marginRight, marginBottom,
     marginLeft, paddingTop, paddingRight, paddingBottom,
     paddingLeft, borderTopWidth, borderRightWidth,
     borderBottomWidth, borderLeftWidth, fontSize, color, display,
     visibility, overflow, overflowX, overflowY, position, top,
     right, bottom, left, zIndex, absoluteTop, absoluteLeft]

    @classmethod
    def values(cls):
        return cls._values[:]