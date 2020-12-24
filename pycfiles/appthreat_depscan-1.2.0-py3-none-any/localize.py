# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apps/command/localize.py
# Compiled at: 2010-07-26 17:09:43
import gettext, logging, os, shutil, apps.command.base, apps.config

class localize(apps.command.base.Command):
    user_options = [
     ('dir=', 'd', 'translation file directory', None),
     ('remove', 'r', 'remove .po files from original location', None)]
    option_defaults = {'dir': 'lang'}
    help = 'Generate translation directory structure from a directory of .po and .mo files.'

    def run(self):
        if not os.path.exists(os.path.join(self.project.path, self.options['dir'])):
            logging.error('The directory "%s" does not exist.' % (self.options['dir'],))
            return
        else:
            path = os.path.join(self.project.path, self.options['dir'])
            for item in os.listdir(path):
                ext = os.path.splitext(item)[1]
                lang = os.path.splitext(item)[0]
                if os.path.exists(os.path.join(path, lang)) == False and (ext == '.mo' or ext == '.po'):
                    os.makedirs(os.path.join(path, lang, 'LC_MESSAGES'))
                if ext == '.po':
                    shutil.copy(os.path.join(path, item), os.path.join(path, lang, item))
                elif ext == '.mo':
                    shutil.copy(os.path.join(path, item), os.path.join(path, lang, 'LC_MESSAGES', item))
                if self.options.get('remove', None):
                    os.remove(os.path.join(path, item))

            return