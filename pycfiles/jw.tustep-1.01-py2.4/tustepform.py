# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jw/tustep/browser/tustepform.py
# Compiled at: 2010-07-21 02:03:28
from zope import interface, schema
from zope.formlib import form
from Products.Five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from Products.CMFCore import utils as cmfutils
from Products.Five.browser import pagetemplatefile
from collective.plone.gsxml.context import TarballExportContext
from collective.plone.gsxml.content import XMLContentFSExporter
from jw.tustep import tustepMessageFactory as _
from zope.component import getMultiAdapter
import urllib, xml.dom.minidom as dom, os, shutil, re, webbrowser, xmlrpclib, codecs

class ITustepFormSchema(interface.Interface):
    __module__ = __name__

    @interface.invariant
    def invariant_url(input):
        pass


class TustepForm(formbase.PageForm):
    __module__ = __name__
    form_fields = form.FormFields(ITustepFormSchema)
    label = _('TUSTEP Ausgabe')
    description = _('Es wird ein PDF-Dokument mithilfe von TUSTEP erzeugt.')
    result_template = pagetemplatefile.ZopeTwoPageTemplateFile('ergebnis.pt')

    @form.action('pdf')
    def actionpdf(self, action, data):
        pfad = '/home/wagner/'
        pstate = getMultiAdapter((self.context, self.request), name='plone_context_state')
        url = pstate.current_base_url()
        url = re.sub('/tustepform', '', url)
        export_context = TarballExportContext()
        exporter = XMLContentFSExporter(self.context)
        exporter.export(export_context, 'structure', True)
        file = export_context.getArchiveStream()
        name = export_context.getArchiveFilename()
        size = export_context.getArchiveSize()
        ausgabe = open(pfad + 'archiv', 'w')
        ausgabe.write(file.getvalue())
        ausgabe.close()
        shutil.rmtree(pfad + 'structure')
        os.system('tar xf ' + pfad + 'archiv --directory=' + pfad)
        eigenname = re.sub('.*/', '', url)
        string_text = ''
        ausgabe = codecs.open(pfad + 'ymir.xml', 'w', 'utf8')
        ausgabe.write('Vor der Verarbeitung der XML-Datei')
        ausgabe.close()
        xml_datei = open(pfad + 'structure/' + eigenname + '.xml', 'r')
        xml_text = ''
        for line in xml_datei:
            xml_text += line

        baum = dom.parseString(xml_text)
        eintraege = [
         'shorttitle', 'histdatum', 'stddatum', 'histort']
        divs = baum.lastChild.getElementsByTagName('cmf:type')
        for di in divs:
            text = re.sub('\\A\\s*', '', str(di.firstChild.data))
            text = re.sub('\\s*\\Z', '', text)
            string_text += '<type>' + text + '</type>\n'

        divs = baum.lastChild.getElementsByTagName('dc:creator')
        for di in divs:
            text = re.sub('\\A\\s*', '', str(di.firstChild.data))
            text = re.sub('\\s*\\Z', '', text)
            string_text += '<ersteller>' + text + '</ersteller>\n'

        divs = baum.lastChild.getElementsByTagName('field')
        for di in divs:
            for eintrag in eintraege:
                if di.getAttribute('name') == eintrag:
                    str_eintrag = '<' + eintrag + '>' + str(di.firstChild.data) + '</' + eintrag + '>' + '\n'
                    str_eintrag = re.sub('\n', '', str_eintrag)
                    str_eintrag = re.sub('\r', '', str_eintrag)
                    str_eintrag = re.sub('\t', '', str_eintrag)
                    str_eintrag = re.sub('\\A\\s*', '', str_eintrag)
                    str_eintrag = re.sub('\\s*\\Z', '', str_eintrag)
                    string_text += str(str_eintrag) + '\n'

        ausgabe = codecs.open(pfad + 'ymir.xml', 'w', 'utf8')
        ausgabe.write(string_text)
        ausgabe.close()
        texttypen = [
         'untertitel', 'fabstract', 'description', 'regest', 'fundort', 'druckort', 'fachartikeltext', 'originaltext', 'text', 'erlauterung', 'uebetragung', 'aboutauthors']
        for i in texttypen:
            text_name = eigenname + '.' + i + '.data'
            try:
                datei = codecs.open(pfad + 'structure/' + text_name, encoding='utf8')
                text = datei.read()
                if re.search('\\w', text):
                    text = re.sub('<!-- start content -->', '', text)
                    text = re.sub('\r', '', text, re.S | re.U)
                    text = re.sub('<p>', '', text)
                    text = re.sub('<p .*?>', '', text)
                    text = re.sub('</p>', '', text)
                    text = re.sub('\\A\\W*?', '', text, re.DOTALL)
                    text = re.sub('\\W*?\\Z', '', text, re.DOTALL)
                    text = re.sub('&nbsp;?', ' ', text)
                    text = re.sub('<script.*?>', '', text, re.DOTALL)
                    text = re.sub('<a.*?>', '', text, re.DOTALL)
                    loe = [
                     '\n', '\r', '<a.*?>']
                    for j in loe:
                        text = re.sub(i, '', text, re.DOTALL)

                    text = re.sub('&hellip;', '<...>', text)
                    text = re.sub('&mdash;', '-', text)
                    string_text += '\n' + '<' + i + '>' + '\n'
                    string_text += text
                    string_text += '\n' + '</' + i + '>' + '\n'
                text.close()
            except:
                pass

        string_text = '<bttitel>' + str(pstate.object_title()) + '</bttitel>' + '\n' + string_text
        string_text = '<dokument>\n' + string_text + '\n</dokument>'
        ausgabe = codecs.open(pfad + 'ymir.xml', 'w', 'utf8')
        ausgabe.write(string_text)
        ausgabe.close()
        baum = dom.parse(pfad + 'ymir.xml')
        ausgabe = codecs.open(pfad + 'ymir.xml', 'w', 'utf8')
        ausgabe.write('geparsed')
        ausgabe.close()
        typ = baum.lastChild.getElementsByTagName('type')[0].firstChild.data
        ausgabe = codecs.open(pfad + 'type.xml', 'w', 'utf8')
        ausgabe.write(typ)
        ausgabe.close()
        felder = [
         'bttitel', 'description', 'text']
        if typ == 'Quellentext':
            felder = [
             'bttitel', 'histort', 'stddatum', 'regest', 'fundort', 'druckort', 'originaltext', 'uebetragung', 'erlauterung', 'aboutauthors', 'ersteller']
        if typ == 'Fachartikel':
            felder = [
             'bttitel', 'untertitel', 'ersteller', 'fachartikeltext', 'fabstract', 'aboutauthors']
        text = ''
        for i in felder:
            try:
                text += baum.lastChild.getElementsByTagName(i)[0].toxml()
            except:
                pass

        ausgabe = codecs.open(pfad + 'ymir.xml', 'w', 'utf8')
        ausgabe.write(text)
        ausgabe.close()
        os.system('tcsh -c "tustep 1"')
        os.system('ps2pdf ' + pfad + 'buri.ps ' + pfad + 'buri.pdf')
        shutil.copy(pfad + 'buri.pdf', '/var/www/tustep_pdf/buri.pdf')
        pstate = getMultiAdapter((self.context, self.request), name='plone_context_state')
        obj = pstate.object_title()
        self.ergebnisse = obj
        return self.result_template()

    @form.action('einstellungen')
    def actioneinstellungen(self, action, data):
        pstate = getMultiAdapter((self.context, self.request), name='plone_context_state')
        url = pstate.current_base_url()
        url = re.sub('/tustepform', '', url)
        obj = pstate.object_title()
        self.ergebnisse = obj
        return self.result_template()