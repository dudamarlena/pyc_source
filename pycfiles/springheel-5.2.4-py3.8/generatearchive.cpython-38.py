# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/generatearchive.py
# Compiled at: 2019-12-29 19:13:58
# Size of source mod 2**32: 2654 bytes
import springheel.parseconf, os

def getLinks(i, translated_strings):
    """Generate hyperlinks for the archive page.

    Takes a Strip object and links it according to the archive link
    format for the current language from strings.json.

    Parameters
    ----------
    i : Strip
        The Strip whose link is to be formatted.
    translated_strings: dict
        The translation file contents for this site.
    Returns
    -------
    archive_link : str
        The formatted link to the page.
    """
    archive_l = translated_strings['archive_l_s'].format(title=(i.title), page=(i.page))
    link_format = '<li><a href="{html_filename}">{archive_l}</a></li>'
    archive_link = link_format.format(html_filename=(i.html_filename), archive_l=archive_l)
    return archive_link


def generateChapArchList(archive, chapter, chapter_title, translated_strings, l):
    """Generates an ordered list of pages in a chapter."""
    sep = '\n'
    link_list = sep.join(archive)
    chapter_s = translated_strings['chapter_s'].format(chapter=chapter, chapter_title=chapter_title)
    sect = '<h{l}>{chapter_s}</h{l}>\n<ol class="chapterarch">\n{link_list}\n</ol>'
    arch_list = sect.format(chapter_s=chapter_s, link_list=link_list,
      l=l)
    return arch_list


def generateSeriesArchives(category, status, archive):
    """Generates an ordered list of pages sorted by date."""
    sep = '\n'
    link_list = sep.join(archive)
    sect = '<section class="archive">\n<h2>{category}</h2>\n<p class="status">{status}</p>\n<ol class="datearch">\n{link_list}\n</ol>\n</section>'
    arch_section = sect.format(category=category, status=status,
      link_list=link_list)
    return arch_section