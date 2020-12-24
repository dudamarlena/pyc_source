# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slow/model/preference_model.py
# Compiled at: 2006-01-10 04:15:14
PREF_NAMESPACE_URI = 'http://www.dvs1.informatik.tu-darmstadt.de/research/OverML/slow-gui-setup'
from lxml import etree
from xpathmodel import XPathModel, autoconstruct

def buildPreferences():
    prefs = etree.Element('{%s}prefs' % PREF_NAMESPACE_URI)
    prefs.optimize_xml_size = True
    prefs.auto_update_edsm_graph = True
    return prefs


def _build_bool_element(name):
    tag = '{%%(DEFAULT_NAMESPACE)s}%s' % name
    get = "./%s/@on = 'true'" % tag

    def set(self, _xpath_result, value):
        value = unicode(bool(value)).lower()
        if not _xpath_result:
            etree.SubElement(self, tag, on=value)
        else:
            _xpath_result[0].set('on', value)

    set.__doc__ = './' + tag
    return (get, autoconstruct(set))


class PreferenceModel(XPathModel):
    __module__ = __name__
    DEFAULT_NAMESPACE = PREF_NAMESPACE_URI
    (_get_optimize_xml_size, _set_optimize_xml_size) = _build_bool_element('optimize_xml_size')
    (_get_auto_update_edsm_graph, _set_auto_update_edsm_graph) = _build_bool_element('auto_update_edsm_graph')

    def _get_languages(self, _xpath_result):
        """./{%(DEFAULT_NAMESPACE)s}languages/*"""
        if _xpath_result:
            return [ l.text for l in _xpath_result ]
        else:
            return []

    def _set_languages(self, _xpath_result, languages):
        """./{%(DEFAULT_NAMESPACE)s}languages"""
        if _xpath_result:
            lang_tag = _xpath_result[0]
            lang_tag.clear()
        else:
            lang_tag = etree.SubElement(self, '{%s}languages' % PREF_NAMESPACE_URI)
        language_tagname = '{%s}language' % PREF_NAMESPACE_URI
        for language in languages:
            tag = etree.SubElement(lang_tag, language_tagname)
            tag.text = unicode(language)

    def __iter__(self):
        for (name, value) in vars(self.__class__).iteritems():
            if isinstance(value, property):
                yield (
                 name, getattr(self, name))


ns = etree.Namespace(PREF_NAMESPACE_URI)
ns['prefs'] = PreferenceModel