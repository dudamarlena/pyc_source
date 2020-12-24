# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/interfaces/content.py
# Compiled at: 2014-05-12 04:24:12
__docformat__ = 'restructuredtext'
from ztfy.base.interfaces import IBaseContent
from ztfy.i18n.interfaces import II18nAttributesAware
from ztfy.i18n.schema import I18nTextLine, I18nText, I18nImage, I18nCthumbImage
from ztfy.i18n import _

class II18nBaseContent(IBaseContent, II18nAttributesAware):
    """Base content interface"""
    title = I18nTextLine(title=_('Title'), description=_('Content title'), required=True)
    shortname = I18nTextLine(title=_('Short name'), description=_('Short name of the content can be displayed by several templates'), required=True)
    description = I18nText(title=_('Description'), description=_("Internal description included in HTML 'meta' headers"), required=False)
    keywords = I18nTextLine(title=_('Keywords'), description=_('A list of keywords matching content, separated by commas'), required=False)
    header = I18nImage(title=_('Header image'), description=_('This banner can be displayed by skins on page headers'), required=False)
    heading = I18nText(title=_('Heading'), description=_('Short header description of the content'), required=False)
    illustration = I18nCthumbImage(title=_('Illustration'), description=_('This illustration can be displayed by several presentation templates'), required=False)
    illustration_title = I18nTextLine(title=_('Illustration alternate title'), description=_('This text will be used as an alternate title for the illustration'), required=False)