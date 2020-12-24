# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/abl/robot/mail.py
# Compiled at: 2012-01-06 08:43:45
__docformat__ = 'restructuredtext en'
from turbomail.message import Message
from turbomail.control import interface
from genshi.template.loader import package
from genshi.template import MarkupTemplate, NewTextTemplate

class TemplateMessage(Message):
    """
    This is a genshi-based template mail renderer.
    """
    loader = staticmethod(package('abl.devtools', ''))

    def __init__(self, **kwargs):
        """
        This is a genshi-based template mail renderer.

        It derives from L{Message} and introduces three
        additional keyword-args:

         - "html" for a MarkupTemplate
         - "text" for a TextTemplate
         - "subject" for a TextTemplate to use for the subject

        The templates are currently always loaded relative
        to the package::

          abl.devtools

        """
        html = kwargs.pop('html', None)
        text = kwargs.pop('text', None)
        subject = kwargs.pop('subject', None)
        super(TemplateMessage, self).__init__(**kwargs)
        self._html_template = self._text_template = None
        if html is not None:
            _, _, inf, _ = self.loader(html)
            self._html_template = MarkupTemplate(inf)
        if text is not None:
            _, _, inf, _ = self.loader(text)
            self._text_template = NewTextTemplate(inf)
        else:
            self._text_template = None
        if subject is not None:
            _, _, inf, _ = self.loader(subject)
            self._subject_template = NewTextTemplate(inf)
        else:
            self._subject_template = None
        return

    def render(self, **values):
        if self._html_template is not None:
            self.rich = self._html_template.generate(**values).render('html', doctype='html')
        if self._text_template is not None:
            self.plain = self._text_template.generate(**values).render()
        if self._subject_template is not None:
            subject = self._subject_template.generate(**values).render()
            subject = (' ').join(subject.split('\n'))
            self.subject = subject
        return

    def send(self):
        interface.send(self)


def configure(conf):
    """
    Configures the turbomail system.
    """
    default_conf = {'manager': 'immediate', 
       'transport': 'smtp', 
       'smtp.server': 'mail.ableton.net', 
       'message.encoding': 'utf-8', 
       'utf8qp.on': True}
    default_conf.update(conf)
    for key in default_conf.keys():
        default_conf['mail.' + key] = default_conf[key]
        del default_conf[key]

    default_conf['mail.on'] = True
    interface.start(default_conf)