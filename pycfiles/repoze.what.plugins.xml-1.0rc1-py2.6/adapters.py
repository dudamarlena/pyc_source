# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/repoze/what/plugins/xml/adapters.py
# Compiled at: 2009-01-27 15:57:21
"""The repoze.what groups and permission adapters for XML sources"""
from xml.dom.minidom import parse
from repoze.what.adapters import BaseSourceAdapter, SourceError
__all__ = [
 'XMLGroupsAdapter', 'XMLPermissionsAdapter']

class _BaseXMLAdapter(BaseSourceAdapter):
    """The base class for XML source adapters"""

    def __init__(self, file, **kwargs):
        """
        Create an XML source adapter for ``file``.
        
        :param file: The path to the XML file or a :class:`file` object.
        :type file: ``str`` or ``file``
        
        """
        self.file = file
        self.document = parse(file)
        self.is_writable = True
        super(_BaseXMLAdapter, self).__init__(**kwargs)
        self.section_tag = self.elements['section']
        self.item_tag = self.elements['item']

    def _get_all_sections(self):
        sections = {}
        for section in self.document.getElementsByTagName(self.section_tag):
            section_name = section.getAttribute('name')
            items = set()
            for item in section.getElementsByTagName(self.item_tag):
                items.add(item.getAttribute('name'))

            sections[section_name] = items

        return sections

    def _get_section_items(self, section):
        section_as_element = self._get_section_as_element(section)
        items = set()
        for item in section_as_element.getElementsByTagName(self.item_tag):
            items.add(item.getAttribute('name'))

        return items

    def _include_items(self, section, items):
        section_as_element = self._get_section_as_element(section)
        for item in items:
            item_element = self.document.createElement(self.item_tag)
            item_element.setAttribute('name', item)
            section_as_element.appendChild(item_element)

        self._save()

    def _exclude_items(self, section, items):
        section_as_element = self._get_section_as_element(section)
        for item in section_as_element.getElementsByTagName(self.item_tag):
            if item.getAttribute('name') in items:
                section_as_element.removeChild(item)

        self._save()

    def _item_is_included(self, section, item_name):
        section_as_element = self._get_section_as_element(section)
        for item in section_as_element.getElementsByTagName(self.item_tag):
            if item.getAttribute('name') == item_name:
                return True

        return False

    def _create_section(self, section):
        section_element = self.document.createElement(self.section_tag)
        section_element.setAttribute('name', section)
        self.document.documentElement.appendChild(section_element)
        self._save()

    def _edit_section(self, section, new_section):
        section_as_element = self._get_section_as_element(section)
        section_as_element.setAttribute('name', new_section)
        self._save()

    def _delete_section(self, section):
        section_as_element = self._get_section_as_element(section)
        self.document.documentElement.removeChild(section_as_element)
        self._save()

    def _section_exists(self, section):
        section_as_element = self._get_section_as_element(section)
        return section_as_element is not None

    def _get_sections_of_item(self, item_name):
        sections = set()
        for section in self.document.getElementsByTagName(self.section_tag):
            for item in section.getElementsByTagName(self.item_tag):
                if item_name == item.getAttribute('name'):
                    sections.add(section.getAttribute('name'))

        return sections

    def _get_section_as_element(self, section_name):
        for section in self.document.getElementsByTagName(self.section_tag):
            if section.getAttribute('name') == section_name:
                return section

    def _save(self):
        if hasattr(self.file, 'write'):
            writer = self.file
        else:
            writer = open(self.file, 'w')
        writer.write(self.document.toprettyxml(encoding='utf-8'))


class XMLGroupsAdapter(_BaseXMLAdapter):
    """
    The XML group source adapter.
    
    The ``file`` is the path to the XML-based group source or the :class:`file`
    object for such a file.
    
    Additional arguments will be passed to 
    :class:`repoze.what.adapters.BaseSourceAdapter`.
    
    For example, if we have the following XML-based group source:
    
    .. code-block:: xml
    
        <?xml version="1.0" encoding="UTF-8"?>
        <groups>
            <group name="admins">
                <member name="rms" />
            </group>
            <group name="developers">
                <member name="rms" />
                <member name="linus" />
            </group>
            <group name="trolls">
                <member name="sballmer" />
            </group>
            <group name="python">
                <!-- An empty group -->
            </group>
            <group name="php">
                <!-- An empty group -->
            </group>
        </groups>
    
    Then we can use its adapter like this::
    
        >>> from repoze.what.plugins.xml.adapters import XMLGroupsAdapter
        >>> groups = XMLGroupsAdapter('tests/fixture/groups.xml')
        >>> groups.get_section_items('developers')
        set([u'rms', u'linus'])
    
    """
    elements = {'section': 'group', 
       'item': 'member'}

    def _find_sections(self, credentials):
        userid = credentials['repoze.what.userid']
        return self._get_sections_of_item(userid)


class XMLPermissionsAdapter(_BaseXMLAdapter):
    """
    The XML permission source adapter.
    
    The ``file`` is the path to the XML-based permission source or the 
    :class:`file` object for such a file.
    
    Additional arguments will be passed to 
    :class:`repoze.what.adapters.BaseSourceAdapter`.
    
    For example, if we have the following XML-based permission source:

        .. code-block:: xml
        
            <?xml version="1.0" encoding="UTF-8"?>
            <permissions>
                <permission name="edit-site">
                    <group name="admins" />
                    <group name="developers" />
                </permission>
                <permission name="commit">
                    <group name="developers" />
                </permission>
                <permission name="see-site">
                    <group name="trolls" />
                </permission>
            </permissions>
    
    Then we can use its adapter like this:
    
        >>> from repoze.what.plugins.xml.adapters import XMLPermissionsAdapter
        >>> permissions = XMLPermissionsAdapter('tests/fixture/permissions.xml')
        >>> permissions.get_section_items('edit-site')
        set([u'admins', u'developers'])
    
    """
    elements = {'section': 'permission', 
       'item': 'group'}

    def _find_sections(self, group):
        return self._get_sections_of_item(group)