# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ln/prueba.py
# Compiled at: 2007-09-07 13:49:52
import ln

class Content(ln.Thing):
    __module__ = __name__


doc1 = Content('doc1')
ln.KB.tell(doc1)

class WfState(ln.Thing):
    __module__ = __name__


deleted = WfState('deleted')
ln.KB.tell(deleted)
private = WfState('private')
ln.KB.tell(private)
public = WfState('public')
ln.KB.tell(public)

class HasState(ln.State):
    __module__ = __name__
    subject = Content
    advs = {'state': WfState}


class ChangeOfState(ln.State):
    __module__ = __name__
    subject = Content
    advs = {'init_state': WfState, 'end_state': WfState}


class User(ln.Thing):
    __module__ = __name__


john = User('john')
ln.KB.tell(john)

class Action(ln.Thing):
    __module__ = __name__


view = Action('view')
ln.KB.tell(view)
edit = Action('edit')
ln.KB.tell(edit)
remove = Action('remove')
ln.KB.tell(remove)
change_state = Action('change_state')
ln.KB.tell(change_state)

class HasPermission(ln.State):
    __module__ = __name__
    subject = User
    advs = {'action': Action, 'content': Content}


class Do(ln.State):
    __module__ = __name__
    subject = User
    advs = {'action': Action, 'content': Content}


class Ask(ln.State):
    __module__ = __name__
    subject = User
    advs = {'action': Action, 'content': Content}


class IsNotifed(ln.State):
    __module__ = __name__
    subject = User
    advs = {'expr': ln.Prop}


class RelationToContent(ln.Thing):
    __module__ = __name__


owner = RelationToContent('owner')
ln.KB.tell(owner)
not_owner = RelationToContent('not_owner')
ln.KB.tell(not_owner)

class HasRelation(ln.State):
    __module__ = __name__
    subject = User
    advs = {'relation_to_content': RelationToContent, 'content': Content}


prop1 = ln.Prop(doc1, HasState(state=public), 0)
ln.KB.tell(prop1)
u1 = User('X1')
c1 = Content('X2')
p1 = ln.Prop(c1, HasState(state=public), ln.Number('X3'))
p2 = ln.Prop(u1, HasPermission(action=view, content=c1), ln.Number('X3'))
ln.KB.tell(ln.Rule((u1, c1, p1), (p2,)))
ln.KB.extend()
ln.KB.ask(remove)
remove.name = 'delete'
ln.KB.ask(remove)
q1 = ln.Prop(s=john, v=HasPermission(action=view, content=doc1), t=0)
ln.KB.ask(q1)