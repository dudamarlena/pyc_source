# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/horde/apis/mnemo.py
# Compiled at: 2012-10-12 07:02:39
import pprint
from coils.core import *
from api import HordeAPI

def render_note(context, note):
    return {'id': note.object_id, 'uid': note.caldav_uid, 
       'desc': note.title, 
       'body': note.content, 
       'category': note.categories}


class HordeMNemoAPI(HordeAPI):

    def api_mnemo_get_notpad(self, args):
        project = self.context.run_command('project::get', name=args[0])
        if project:
            return True
        return False

    def api_mnemo_get(self, args):
        note = self.context.run_command('note::get', id=args[0])
        if note:
            return render_note(self.context, note)
        return False

    def api_mnemo_add(self, args):
        project = self.context.run_command('project::get', number=args[0])
        if project:
            note = self.context.run_command('note::new', values={'title': args[1], 'categories': args[3]}, text=args[2], context=project)
            self.context.commit()
            return render_note(self.context, note)
        return False

    def api_mnemo_modify(self, args):
        note = self.context.run_command('note::get', id=args[0])
        if note:
            note = self.context.run_command('note::set', object=note, values={'title': args[1], 'categories': args[3]}, text=args[2])
            self.context.commit()
            return render_note(self.context, note)
        return False

    def api_mnemo_move(self, args):
        project = self.context.run_command('project::get', name=args[1])
        if project:
            note = self.context.run_command('note::get', id=args[0])
            if note:
                note.project_id = project.object_id
                self.context.commit()
                return True
        return False

    def api_mnemo_delete(self, args):
        note = self.context.run_command('note::get', uid=args[1])
        if note:
            self.context.run_command('note::delete', object=note)
            return True
        return False

    def api_mnemo_retrieve(self, args):
        project = self.context.run_command('project::get', number=args[0])
        if project:
            result = []
            for note in self.context.run_command('project::get-notes', project=project):
                result.append(render_note(self.context, note))

            return result
        print ('no such project as {0}').format(args[0])
        return []