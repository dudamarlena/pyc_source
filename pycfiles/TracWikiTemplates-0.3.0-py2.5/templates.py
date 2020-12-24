# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/WikiTemplates/macros/templates.py
# Compiled at: 2007-11-10 06:34:56
import re, inspect
from trac.core import *
from trac.env import IEnvironmentSetupParticipant
from trac.wiki.api import IWikiMacroProvider
from trac.wiki.formatter import wiki_to_html, wiki_to_oneliner
from trac.util.text import to_unicode
from WikiTemplates.model import WikiTemplate
from WikiTemplates.errors import TemplatesError
from WikiTemplates.db_schema import version as templates_version
ARGS_RE = re.compile('\\{\\{\\d+\\}\\}')
STRIP_RE = re.compile('^<p>|^</p>|<p>$|</p>$')
templates_version_db = 0

class TemplatesMacro(Component):
    """ Grab a wiki page and include it inside another with
pre-formated text replacing the vars '''`{{n}}`''' by the args passed,
'''`n`''' being a number.

All templates are stored on a diferent DB table than the wiki one.[[BR]]
To create them click the ''Wiki Templates'' button shown on the menu bar,
there's a box on the topmost right side that allows you to do just that; or go
to ''`http://domain.com/templates/TheNameOfTemplate`'', !TheNameOfTemplate
being the name of the template you want to create.

Arguments are separated by '''`|`'''(pipe), and the first one passed is the
name of the template to be used.

So, for example, if you have a template(!RedTemplate) with the pre-formated
text inside, like for example:
    {{{
    {{{
    #!html
    <span style="color: red; font-family: monospace;">{{1}}</span>
    }}}
    }}}

You would use it like:
    {{{
    [[T(RedTemplate|Arg1)]]
    }}}
[[BR]]
For more information go to:
http://wikitemplates.ufsoft.org """
    implements(IWikiMacroProvider, IEnvironmentSetupParticipant)

    def environment_created(self):
        pass

    def environment_needs_upgrade(self, db):
        cursor = db.cursor()
        try:
            QUERY = "SELECT value FROM system WHERE name='templates_version'"
            cursor.execute(QUERY)
            version = int(cursor.fetchone()[0])
            if not version:
                return True
            if version < templates_version:
                templates_version_db = version
                return True
            elif version == templates_version:
                return False
        except:
            db.rollback()
            return True

    def upgrade_environment(self, db):
        cursor = db.cursor()
        for i in range(templates_version_db + 1, templates_version + 1):
            name = 'db%i' % i
            try:
                upgrades = __import__('WikiTemplates.upgrades', globals(), locals(), [name])
                script = getattr(upgrades, name)
            except AttributeError:
                err = 'No upgrade module for version %i (%s.py)' % (i, name)
                raise TracError, err

            script.do_upgrade(self.env, i, db)

    def get_macros(self):
        yield 'T'

    def get_macro_description(self, name):
        return inspect.getdoc(TemplatesMacro)

    def render_macro(self, req, name, content):
        if not content:
            raise Exception('No template name passed')
        if content:
            if content.find('\\|') > 0:
                temp_args = content.replace('\\|', '~!#~')
                striped_args = [ arg.strip() for arg in temp_args.split('|') ]
                args = [ striped_args[x].replace('~!#~', '|') for x in range(len(striped_args))
                       ]
            else:
                args = [ arg.strip() for arg in content.split('|') ]
        template = WikiTemplate(self.env, args.pop(0))
        self.log.debug("Template Wiki: '%r'", to_unicode(template))
        if template.version < 1:
            self.log.debug("Template Wiki '%r' does not exist.", template.name)
            return_message = TemplatesError("Template '%r' does not exist." % template.name)
            self.log.debug('%r', return_message)
            return return_message
        self.log.debug("Template Wiki '%r' exists.", template.name)
        contents = template.text
        tmp_args = len(ARGS_RE.findall(contents))
        tpl_args = 0
        for i in range(tmp_args):
            if contents.find('{{%d}}' % (i + 1)) != -1:
                tpl_args += 1

        self.log.debug('Template asks for %d arguments', tpl_args)
        nr_args = len(args)
        self.log.debug('User is passing %d arguments', nr_args)
        if nr_args != tpl_args:
            self.log.debug("Passed args and asked args don't match.")
        if nr_args < tpl_args:
            return TemplatesError("You're passing less arguments(%d) than those the template asks for(%d).\nClick your browser's back button and correct the error, or check the edit box below if present." % (
             nr_args, tpl_args))
        elif nr_args > tpl_args:
            return TemplatesError("You're passing more arguments(%d) that those the template supports(%d).\nClick your browser's back button and correct the error, or check theedit box below if present." % (
             nr_args, tpl_args))
        for i in range(tpl_args):
            if contents.find('Include({{%d}})' % (i + 1)) != -1:
                contents = contents.replace('{{%d}}' % (i + 1), args[i])
            else:
                args[i] = wiki_to_oneliner(args[i], self.env, shorten=False, absurls=True)
                args[i] = args[i].replace('\\n', '<br>')
                contents = contents.replace('{{%d}}' % (i + 1), args[i])

        wiki2html = wiki_to_html(contents, self.env, req)
        wiki2html = re.sub(STRIP_RE, '', wiki2html)
        return wiki2html.strip()