# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseclient/wiki.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 5415 bytes
'''
****
Wiki
****

A Wiki page requires a title, markdown and an owner object and can
also include images.

~~~~~~~~~~~~~~~
Creating a Wiki
~~~~~~~~~~~~~~~

::

    from synapseclient import Wiki

    entity = syn.get('syn123456')

    content = """
    # My Wiki Page

    Here is a description of my **fantastic** project!

    An attached image:
    ${image?fileName=logo.png&align=none}
    """

    wiki = Wiki(title='My Wiki Page',
                owner=entity,
                markdown=content,
                attachments=['/path/to/logo.png'])

    wiki = syn.store(wiki)

~~~~~~~~~~~~~~~~
Embedding images
~~~~~~~~~~~~~~~~

Note that in the above example, we've **attached** a logo graphic and embedded it in the web page.

Figures that are more than just decoration can be stored as Synapse entities allowing versioning and provenance
information to be recorded. This is a better choice for figures with data behind them.

~~~~~~~~~~~~~~~
Updating a Wiki
~~~~~~~~~~~~~~~

::

    entity = syn.get('syn123456')
    wiki = syn.getWiki(entity)

    wiki.markdown = """
    # My Wiki Page

    Here is a description of my **fantastic** project! Let's
    *emphasize* the important stuff.

    An embedded image that is also a Synapse entity:
    ${image?synapseId=syn1824434&align=None&scale=66}

    Now we can track it's provenance and keep multiple versions.
    """

    wiki = syn.store(wiki)

~~~~~~~~~~
Wiki Class
~~~~~~~~~~

.. autoclass:: synapseclient.wiki.Wiki
   :members: __init__

~~~~~~~~~~~~
Wiki methods
~~~~~~~~~~~~

 - :py:meth:`synapseclient.Synapse.getWiki`
 - :py:meth:`synapseclient.Synapse.getWikiHeaders`
 - :py:meth:`synapseclient.Synapse.store`
 - :py:meth:`synapseclient.Synapse.delete`

'''
import os, json
from synapseclient.core.models.dict_object import DictObject
from synapseclient.core.utils import id_of

class Wiki(DictObject):
    __doc__ = '\n    Represents a wiki page in Synapse with content specified in markdown.\n\n    :param title:           Title of the Wiki\n    :param owner:           Parent Entity that the Wiki will belong to\n    :param markdown:        Content of the Wiki (cannot be defined if markdownFile is defined)\n    :param markdownFile:    Path to file which contains the Content of Wiki (cannot be defined if markdown is defined)\n    :param attachments:     List of paths to files to attach\n    :param fileHandles:     List of file handle IDs representing files to be attached\n    :param parentWikiId:    (optional) For sub-pages, specify parent wiki page\n    '
    _Wiki__PROPERTIES = ('title', 'markdown', 'attachmentFileHandleIds', 'id', 'etag',
                         'createdBy', 'createdOn', 'modifiedBy', 'modifiedOn', 'parentWikiId')

    def __init__(self, **kwargs):
        if 'owner' not in kwargs:
            raise ValueError('Wiki constructor must have an owner specified')
        else:
            if 'attachmentFileHandleIds' not in kwargs:
                kwargs['attachmentFileHandleIds'] = []
            self.update_markdown(kwargs.pop('markdown', None), kwargs.pop('markdownFile', None))
            if 'fileHandles' in kwargs:
                for handle in kwargs['fileHandles']:
                    kwargs['attachmentFileHandleIds'].append(handle)

                del kwargs['fileHandles']
        super(Wiki, self).__init__(kwargs)
        self.ownerId = id_of(self.owner)
        del self['owner']

    def json(self):
        """Returns the JSON representation of the Wiki object."""
        return json.dumps({k:v for k, v in self.items() if k in self._Wiki__PROPERTIES})

    def getURI(self):
        """For internal use."""
        return '/entity/%s/wiki/%s' % (self.ownerId, self.id)

    def postURI(self):
        """For internal use."""
        return '/entity/%s/wiki' % self.ownerId

    def putURI(self):
        """For internal use."""
        return '/entity/%s/wiki/%s' % (self.ownerId, self.id)

    def deleteURI(self):
        """For internal use."""
        return '/entity/%s/wiki/%s' % (self.ownerId, self.id)

    def update_markdown(self, markdown=None, markdown_file=None):
        """
        Updates the wiki's markdown. Specify only one of markdown or markdown_file
        :param markdown:        text that will become the markdown
        :param markdown_file:   path to a file. Its contents will be the markdown
        """
        if markdown:
            if markdown_file:
                raise ValueError('Please use only one argument: markdown or markdownFile')
        if markdown_file:
            markdown_path = os.path.expandvars(os.path.expanduser(markdown_file))
            if not os.path.isfile(markdown_path):
                raise ValueError(markdown_file + 'is not a valid file')
            with open(markdown_path, 'r') as (opened_markdown_file):
                markdown = opened_markdown_file.read()
        self['markdown'] = markdown


class WikiAttachment(DictObject):
    __doc__ = '\n    Represents a wiki page attachment\n\n    '
    _WikiAttachment__PROPERTIES = ('contentType', 'fileName', 'contentMd5', 'contentSize')

    def __init__(self, **kwargs):
        (super(WikiAttachment, self).__init__)(**kwargs)