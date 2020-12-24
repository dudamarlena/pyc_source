# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/html_doc/page_setup.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 3324 bytes
from xml.etree.ElementTree import Element, SubElement
from exactly_lib import program_info
from exactly_lib.definitions import formatting
from exactly_lib.definitions.entity import all_entity_types
from exactly_lib.help import std_tags
from exactly_lib.util.textformat.rendering.html.utils import ElementPopulator, ComplexElementPopulator
PAGE_TITLE = 'Reference Manual for %s' % formatting.program_name(program_info.PROGRAM_NAME)
TOC_TITLE = 'Table of Contents'
_CSS_CLASSES = {'toc': std_tags.TOC_SECTION, 
 'entity': std_tags.ENTITY, 
 'section': std_tags.SECTION, 
 'syntax_text': std_tags.SYNTAX_TEXT, 
 'enum_constant': std_tags.ENUM_CONSTANT, 
 'text_as_header': std_tags.TEXT_AS_HEADER, 
 'actor_entity': all_entity_types.ACTOR_ENTITY_TYPE_NAMES.identifier, 
 'concept_entity': all_entity_types.CONCEPT_ENTITY_TYPE_NAMES.identifier, 
 'type_entity': all_entity_types.TYPE_ENTITY_TYPE_NAMES.identifier}
ELEMENT_STYLES_ = 'pre {{\n  background-color : #EEFFCC;\n  padding: 7px;\n  border: 1px solid #cEdFaC;\n}}\n\n.{syntax_text} {{\n  font-family: monospace;\n}}\n\n\n.{enum_constant} {{\n  font-weight: bold;\n}}\n\n\n.{text_as_header} {{\n  font-weight: bold;\n}}\n\n\nsection.{toc} > header > h1 {{\n  padding: 5px;\n  border-bottom: thick solid black;\n}}\n\nsection.{toc} > header > h2 {{\n  padding: 2px;\n  border-bottom: medium solid black;\n}}\n\nsection.{toc} > header > h3 {{\n  padding: 2px;\n  border-bottom: thin solid black;\n}}\n\n\narticle > header > h1 {{\n  padding: 3px;\n  font-size: x-large;\n  background-color: #c0c0c0;\n}}\n\narticle > header > p {{\n  font-style: italic;\n  font-size: 110%;\n}}\n\narticle section > header > h1 {{\n    font-size: large;\n}}\n\narticle section > header > h2 {{\n    font-size: medium;\n}}\n\narticle.{section} > header > h1 {{\n  font-size: xx-large;\n  background-color: LightGoldenRodYellow;\n}}\n\n\ntable {{\n  border-collapse: collapse;\n}}\n\nth {{\n  font-weight: normal;\n  background-color: #f4f4f4;\n  text-align: left;\n  padding-right: 5px;\n  vertical-align: top;\n}}\n\ntd {{\n  vertical-align: top;\n}}\n\n\na:link {{\n  text-decoration: none;\n}}\n\n\na:hover {{\n  text-decoration: underline;\n}}\n\n'
ELEMENT_STYLES = ELEMENT_STYLES_.format_map(_CSS_CLASSES)
TITLE_STYLE = 'font-size: 250%;\nfont-weight: bold;\n'
TOC_TITLE_STYLE = 'font-size: 200%;\nfont-weight: bold;\n'

class StylePopulator(ElementPopulator):

    def __init__(self, style: str):
        self.style = style

    def apply(self, parent: Element):
        SubElement(parent, 'style').text = self.style


class DivWithTextAndStylePopulator(ElementPopulator):

    def __init__(self, contents: str, style: str):
        self.contents = contents
        self.style = style

    def apply(self, parent: Element):
        div = SubElement(parent, 'div')
        div.text = self.contents
        div.set('style', self.style)


class VersionPopulator(ElementPopulator):

    def apply(self, parent: Element):
        version = SubElement(parent, 'p')
        version.text = formatting.program_name(program_info.PROGRAM_NAME) + ' version ' + program_info.VERSION
        SubElement(parent, 'hr')


HEADER_POPULATOR = ComplexElementPopulator([
 DivWithTextAndStylePopulator(PAGE_TITLE, TITLE_STYLE),
 VersionPopulator(),
 DivWithTextAndStylePopulator(TOC_TITLE, TOC_TITLE_STYLE)])