# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/browser/ksscommands.py
# Compiled at: 2009-04-26 22:17:24
from kss.core.kssview import CommandSet
from Acquisition import aq_inner, aq_parent
from zope.app.component.interfaces import ISite
from zope.component import getUtility
from Products.DigestoContentTypes.content.interfaces import IArea
from Products.DigestoContentTypes.utilities.interfaces import INormativaTypes

class DigestoContentTypesCommands(CommandSet):
    __module__ = __name__
    __allow_access_to_unprotected_subobjects__ = 1

    def modifyFields(self, fieldname, source, kind):
        """Modifies the html code of the normativa source and kind dropdowns"""
        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')
        if fieldname == 'source':
            area = aq_parent(aq_inner(context))
            while not IArea.providedBy(area) and not ISite.providedBy(area):
                area = aq_parent(aq_inner(area))

            if ISite.providedBy(area):
                return
            area_sources = area.sources
            types = []
            if source:
                for items in area_sources:
                    if items['source'] == source:
                        types = items['kinds']
                        break

            else:
                nt = getUtility(INormativaTypes)
                types = nt.get_types()
            selector = ksscore.getHtmlIdSelector('kind')
            kind_html = '<select name="kind" id="kind" class="sourceorkind">                         <option value=""></option>'
            if source:
                for item in types:
                    if item == kind:
                        kind_html += '<option selected="selected" value="%s">%s</option>' % (item.decode('utf-8'), item.decode('utf-8'))
                    else:
                        kind_html += '<option value="%s">%s</option>' % (item.decode('utf-8'), item.decode('utf-8'))

            for item in types:
                if item == kind:
                    kind_html += '<option selected="selected" value="%s">%s</option>' % (item.decode('utf-8'), item.decode('utf-8'))
                else:
                    kind_html += '<option value="%s">%s</option>' % (item.decode('utf-8'), item.decode('utf-8'))

            kind_html += '</select>'
            ksscore.replaceHTML(selector, kind_html)
            selector = ksscore.getHtmlIdSelector('deletedsource')
            ksscore.replaceInnerHTML(selector, '')
            selector = ksscore.getHtmlIdSelector('disallowedkind')
            ksscore.replaceInnerHTML(selector, '')
        elif fieldname == 'kind':
            area = aq_parent(aq_inner(context))
            while not IArea.providedBy(area) and not ISite.providedBy(area):
                area = aq_parent(aq_inner(area))

            if ISite.providedBy(area):
                return
            area_sources = area.sources
            sources = []
            for items in area_sources:
                if not kind or kind in items['kinds']:
                    sources.append(items['source'])

            source_html = '<select name="source" id="source" class="sourceorkind">                           <option value=""></option>'
            for item in sources:
                if item == source:
                    source_html += '<option value="%s" selected="selected">%s</option>' % (item.decode('utf-8'), item.decode('utf-8'))
                else:
                    source_html += '<option value="%s">%s</option>' % (item.decode('utf-8'), item.decode('utf-8'))

            source_html += '</select>'
            selector = ksscore.getHtmlIdSelector('source')
            ksscore.replaceHTML(selector, source_html)
            selector = ksscore.getHtmlIdSelector('disallowedkind')
            ksscore.replaceInnerHTML(selector, '')
            selector = ksscore.getHtmlIdSelector('deletedsource')
            ksscore.replaceInnerHTML(selector, '')