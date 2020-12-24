# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/processes/sub.py
# Compiled at: 2013-03-18 06:45:19
from __future__ import unicode_literals
import re, time, os
from lxml import etree
from copy import deepcopy
from anolislib import utils
latest_version = re.compile(b'latest[%s]+version' % utils.spaceCharacters, re.IGNORECASE)
w3c_tr_url_status = b'http://www\\.w3\\.org/TR/[^/]*/(MO|WD|CR|PR|REC|PER|NOTE)-'
w3c_tr_url_status = re.compile(w3c_tr_url_status)
title = re.compile(b'\\[TITLE[^\\]]*\\]')
title_identifier = b'[TITLE'
status = re.compile(b'\\[STATUS[^\\]]*\\]')
status_identifier = b'[STATUS'
longstatus = re.compile(b'\\[LONGSTATUS[^\\]]*\\]')
longstatus_identifier = b'[LONGSTATUS'
longstatus_map = {b'MO': b'W3C Member-only Draft', 
   b'ED': b"Editor's Draft", 
   b'WD': b'W3C Working Draft', 
   b'CR': b'W3C Candidate Recommendation', 
   b'PR': b'W3C Proposed Recommendation', 
   b'REC': b'W3C Recommendation', 
   b'PER': b'W3C Proposed Edited Recommendation', 
   b'NOTE': b'W3C Working Group Note'}
shortname = re.compile(b'\\[SHORTNAME[^\\]]*\\]')
shortname_identifier = b'[SHORTNAME'
latest = re.compile(b'\\[LATEST[^\\]]*\\]')
latest_identifier = b'[LATEST'
version = re.compile(b'\\[VERSION[^\\]]*\\]')
version_identifier = b'[VERSION'
w3c_stylesheet = re.compile(b'http://www\\.w3\\.org/StyleSheets/TR/W3C-[A-Z]+')
w3c_stylesheet_identifier = b'http://www.w3.org/StyleSheets/TR/W3C-'
basic_comment_subs = ()

class sub(object):
    """Perform substitutions."""

    def __init__(self, ElementTree, w3c_compat=False, w3c_compat_substitutions=False, w3c_compat_crazy_substitutions=False, w3c_status=b'', publication_date=b'', **kwargs):
        if w3c_status:
            self.w3c_status = w3c_status
        elif w3c_compat or w3c_compat_substitutions or w3c_compat_crazy_substitutions:
            self.w3c_status = self.getW3CStatus(ElementTree, **kwargs)
        else:
            self.w3c_status = b''
        self.pubdate = publication_date and time.strptime(publication_date, b'%d %b %Y') or time.gmtime()
        self.stringSubstitutions(ElementTree, w3c_compat, w3c_compat_substitutions, w3c_compat_crazy_substitutions, **kwargs)
        self.commentSubstitutions(ElementTree, w3c_compat, w3c_compat_substitutions, w3c_compat_crazy_substitutions, **kwargs)

    def stringSubstitutions(self, ElementTree, w3c_compat=False, w3c_compat_substitutions=False, w3c_compat_crazy_substitutions=False, w3c_shortname=b'', **kwargs):
        try:
            doc_title = utils.textContent(ElementTree.getroot().find(b'head').find(b'title'))
        except (AttributeError, TypeError):
            doc_title = b''

        year = re.compile(b'\\[YEAR[^\\]]*\\]')
        year_sub = time.strftime(b'%Y', self.pubdate)
        year_identifier = b'[YEAR'
        date = re.compile(b'\\[DATE[^\\]]*\\]')
        date_sub = time.strftime(b'%d %B %Y', self.pubdate).lstrip(b'0')
        date_identifier = b'[DATE'
        cdate = re.compile(b'\\[CDATE[^\\]]*\\]')
        cdate_sub = time.strftime(b'%Y%m%d', self.pubdate)
        cdate_identifier = b'[CDATE'
        udate = re.compile(b'\\[UDATE[^\\]]*\\]')
        udate_sub = time.strftime(b'%Y-%m-%d', self.pubdate)
        udate_identifier = b'[UDATE'
        string_subs = (
         (
          year, year_sub, year_identifier),
         (
          date, date_sub, date_identifier),
         (
          cdate, cdate_sub, cdate_identifier),
         (
          udate, udate_sub, udate_identifier))
        if w3c_compat or w3c_compat_substitutions:
            doc_longstatus = longstatus_map[self.w3c_status]
        if w3c_compat_crazy_substitutions:
            doc_w3c_stylesheet = b'http://www.w3.org/StyleSheets/TR/W3C-%s' % (self.w3c_status,)
        string_subs += ((title, doc_title, title_identifier),)
        if w3c_compat or w3c_compat_substitutions:
            try:
                shortname_sub = w3c_shortname or os.path.basename(os.getcwd())
            except OSError:
                shortname_sub = b''

            latest_sub = b'http://www.w3.org/TR/%s/' % (shortname_sub,)
            version_sub = b'http://www.w3.org/TR/%s/%s-%s-%s/' % (year_sub, self.w3c_status, shortname_sub, cdate_sub)
            string_subs += ((status, self.w3c_status, status_identifier),
             (
              longstatus, doc_longstatus, longstatus_identifier),
             (
              shortname, shortname_sub, shortname_identifier),
             (
              latest, latest_sub, latest_identifier),
             (
              version, version_sub, version_identifier))
        if w3c_compat_crazy_substitutions:
            string_subs += ((w3c_stylesheet, doc_w3c_stylesheet, w3c_stylesheet_identifier),)
        for node in ElementTree.iter():
            for regex, sub, identifier in string_subs:
                if node.text is not None and identifier in node.text:
                    node.text = regex.sub(sub, node.text)
                if node.tail is not None and identifier in node.tail:
                    node.tail = regex.sub(sub, node.tail)
                for name, value in node.attrib.items():
                    if identifier in value:
                        node.attrib[name] = regex.sub(sub, value)

        return

    def commentSubstitutions(self, ElementTree, w3c_compat=False, w3c_compat_substitutions=False, w3c_compat_crazy_substitutions=False, enable_woolly=False, **kwargs):
        instance_basic_comment_subs = basic_comment_subs
        if w3c_compat or w3c_compat_substitutions:
            copyright = b'copyright'
            copyright_sub = etree.fromstring(b'<p class="copyright"><a href="http://www.w3.org/Consortium/Legal/ipr-notice#Copyright">Copyright</a> &#xA9; %s <a href="http://www.w3.org/"><abbr title="World Wide Web Consortium">W3C</abbr></a><sup>&#xAE;</sup> (<a href="http://www.csail.mit.edu/"><abbr title="Massachusetts Institute of Technology">MIT</abbr></a>, <a href="http://www.ercim.eu/"><abbr title="European Research Consortium for Informatics and Mathematics">ERCIM</abbr></a>, <a href="http://www.keio.ac.jp/">Keio</a>, <a href="http://ev.buaa.edu.cn/">Beihang</a>), All Rights Reserved. W3C <a href="http://www.w3.org/Consortium/Legal/ipr-notice#Legal_Disclaimer">liability</a>, <a href="http://www.w3.org/Consortium/Legal/ipr-notice#W3C_Trademarks">trademark</a> and <a href="http://www.w3.org/Consortium/Legal/copyright-documents">document use</a> rules apply.</p>' % time.strftime(b'%Y', self.pubdate))
            logo = b'logo'
            logo_str = b'<a href="http://www.w3.org/"><img height="48" width="72" alt="W3C" src="https://www.w3.org/Icons/w3c_home"/></a>'
            if enable_woolly:
                logo_str += b'<a class="logo" href="https://www.w3.org/Style/Group/" rel="in-activity"><img alt="CSS WG" src="https://www.w3.org/Style/Woolly/woolly-icon"/></a>'
            logo_sub = etree.fromstring(b'<p>%s</p>' % logo_str)
            instance_basic_comment_subs += ((logo, logo_sub),
             (
              copyright, copyright_sub))
        to_remove = set()
        link_parent = None
        link = None
        for node in ElementTree.iter():
            if link_parent is not None:
                if node.tag is etree.Comment and node.text.strip(utils.spaceCharacters) == b'end-link':
                    if node.getparent() is not link_parent:
                        raise utils.DifferentParentException(b'begin-link and end-link have different parents')
                    utils.removeInteractiveContentChildren(link)
                    link.set(b'href', utils.textContent(link))
                    link_parent = None
                else:
                    if node.getparent() is link_parent:
                        link.append(deepcopy(node))
                    to_remove.add(node)
            elif node.tag is etree.Comment and node.text.strip(utils.spaceCharacters) == b'begin-link':
                link_parent = node.getparent()
                link = etree.Element(b'a')
                link.text = node.tail
                node.tail = None
                node.addnext(link)

        for comment, sub in instance_basic_comment_subs:
            utils.replaceComment(ElementTree, comment, sub, **kwargs)

        for node in to_remove:
            node.getparent().remove(node)

        return

    def getW3CStatus(self, ElementTree, **kwargs):
        for text in ElementTree.xpath(b"//text()[contains(translate(., 'LATEST', 'latest'), 'latest') and contains(translate(., 'VERSION', 'version'), 'version') or contains(., 'http://www.w3.org/TR/')]"):
            if latest_version.search(text):
                return b'ED'
            if w3c_tr_url_status.search(text):
                return w3c_tr_url_status.search(text).group(1)
        else:
            return b'ED'


class DifferentParentException(utils.AnolisException):
    """begin-link and end-link do not have the same parent."""