# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/toolbox/tags.py
# Compiled at: 2018-04-20 03:19:42
""" Handle details of tool tagging - perhaps a deprecated feature.
"""
import logging
from abc import ABCMeta, abstractmethod
import six
log = logging.getLogger(__name__)

def tool_tag_manager(app):
    """ Build a tool tag manager according to app's configuration
    and return it.
    """
    if hasattr(app.config, 'get_bool') and app.config.get_bool('enable_tool_tags', False):
        return PersistentToolTagManager(app)
    else:
        return NullToolTagManager()


@six.add_metaclass(ABCMeta)
class AbstractToolTagManager(object):

    @abstractmethod
    def reset_tags(self):
        """ Starting to load tool panels, reset all tags.
        """
        pass

    @abstractmethod
    def handle_tags(self, tool_id, tool_definition_source):
        """ Parse out tags and persist them.
        """
        pass


class NullToolTagManager(AbstractToolTagManager):

    def reset_tags(self):
        return

    def handle_tags(self, tool_id, tool_definition_source):
        return


class PersistentToolTagManager(AbstractToolTagManager):

    def __init__(self, app):
        self.app = app
        self.sa_session = app.model.context

    def reset_tags(self):
        log.info('removing all tool tag associations (' + str(self.sa_session.query(self.app.model.ToolTagAssociation).count()) + ')')
        self.sa_session.query(self.app.model.ToolTagAssociation).delete()
        self.sa_session.flush()

    def handle_tags(self, tool_id, tool_definition_source):
        elem = tool_definition_source
        if self.app.config.get_bool('enable_tool_tags', False):
            tag_names = elem.get('tags', '').split(',')
            for tag_name in tag_names:
                if tag_name == '':
                    continue
                tag = self.sa_session.query(self.app.model.Tag).filter_by(name=tag_name).first()
                if not tag:
                    tag = self.app.model.Tag(name=tag_name)
                    self.sa_session.add(tag)
                    self.sa_session.flush()
                    tta = self.app.model.ToolTagAssociation(tool_id=tool_id, tag_id=tag.id)
                    self.sa_session.add(tta)
                    self.sa_session.flush()
                else:
                    for tagged_tool in tag.tagged_tools:
                        if tagged_tool.tool_id == tool_id:
                            break
                    else:
                        tta = self.app.model.ToolTagAssociation(tool_id=tool_id, tag_id=tag.id)
                        self.sa_session.add(tta)
                        self.sa_session.flush()