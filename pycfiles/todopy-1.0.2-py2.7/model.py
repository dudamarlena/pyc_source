# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\todopy\model.py
# Compiled at: 2011-12-15 09:18:38
import re

class Todo(object):
    """Class representing single todo.

    >>> t = Todo(1, "My todo")
    >>> t.id
    1
    >>> t.todo
    'My todo'
    """
    PRIORITY_REGEX = '^\\(([A-Z])\\)\\s+'
    DONE_REGEX = '^x\\s+'

    def __init__(self, id, todo):
        self.id = id
        self.todo = todo

    def append(self, text):
        """Append string to todo text, separated by a space.

        >>> t = Todo(2, "My")
        >>> t.append('todo')
        >>> t.todo
        'My todo'
        """
        self.todo += ' ' + text.strip()

    def prepend(self, text):
        """Prepend string to todo text, separated by a space.

        Takes care to keep priority in correct place

        >>> t = Todo(2, "(A) todo")
        >>> t.prepend('My')
        >>> t.todo
        '(A) My todo'
        """
        if self.priority():
            self.todo = '(' + self.priority() + ') ' + text.strip() + ' ' + re.sub(Todo.PRIORITY_REGEX, '', self.todo)
        else:
            self.todo = text.strip() + ' ' + self.todo

    def set_priority(self, priority):
        """Set priority, or remove if None.

        >>> t = Todo(1, "My todo")
        >>> t.set_priority('A')
        >>> t.todo
        '(A) My todo'
        >>> t.set_priority(None)
        >>> t.todo
        'My todo'
        """
        if priority:
            if re.match(Todo.PRIORITY_REGEX, self.todo):
                self.todo = re.sub(Todo.PRIORITY_REGEX, '(' + priority + ') ', self.todo)
            else:
                self.todo = '(' + priority + ') ' + self.todo
        else:
            self.todo = re.sub(Todo.PRIORITY_REGEX, '', self.todo)

    def priority(self):
        """Get priority.

        >>> t = Todo(1, "My todo")
        >>> t.priority()
        >>> t.set_priority('A')
        >>> t.priority()
        'A'
        """
        match = re.match(Todo.PRIORITY_REGEX, self.todo)
        if match:
            return match.group(1)
        else:
            return

    def set_done(self, done=True):
        """Change 'done' state of this todo.

        >>> t = Todo(1, "(A) My todo")
        >>> t.set_done()
        >>> t.todo
        'x My todo'
        """
        if done:
            if not self.done():
                self.set_priority(None)
                self.todo = 'x ' + self.todo
        elif self.done():
            self.todo = re.sub(Todo.DONE_REGEX, '', self.todo)
        return

    def done(self):
        """Check done state of todo.

        >>> t = Todo(1, "My todo")
        >>> t.done()
        False
        """
        m = re.match(Todo.DONE_REGEX, self.todo)
        return m != None


class Model(object):
    """Class representing a todo model.

    >>> m = Model()
    >>> len(m)
    0
    >>> m.add("My todo")
    >>> len(m)
    1
    >>> m[0].todo
    'My todo'
    >>> m[0].id
    1
    >>> m[1]
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    """

    def __init__(self):
        self.todos = []
        self.next_id = 1

    @staticmethod
    def sort_comparator(a, b):
        """Compare two todos and priority sort them.

        >>> t1 = Todo(1, "(B) A todo")
        >>> t2 = Todo(2, "(A) Another todo")
        >>> Model.sort_comparator(t1, t2)
        1
        >>> Model.sort_comparator(t1, t1)
        0
        >>> Model.sort_comparator(t2, t1)
        -1
        """
        p_a = a.priority() if a.priority() else 'Z'
        p_b = b.priority() if b.priority() else 'Z'
        return cmp(p_a, p_b)

    @classmethod
    def from_store(cls, store):
        """Create a Model from some iterable that yields todo strings.

        >>> s = ["(A) A todo", "(B) Another todo", "Third todo"]
        >>> m = Model.from_store(s)
        >>> len(m)
        3
        >>> m[0].todo
        '(A) A todo'
        """
        model = cls()
        model.extend(store)
        return model

    def __iter__(self):

        class Iter(object):

            def __init__(self, model):
                self.model = model
                self.index = 0

            def __iter__(self):
                return self

            def next(self):
                if self.index >= len(self.model):
                    raise StopIteration()
                data = self.model[self.index]
                self.index += 1
                return data

        return Iter(self)

    def __len__(self):
        return len(self.todos)

    def __getitem__(self, index):
        return self.todos[index]

    def add(self, item):
        """Add a todo from a string.

        >>> m = Model()
        >>> m.add("My todo")
        >>> m[0].todo
        'My todo'
        """
        todo = Todo(self.next_id, item)
        self.next_id += 1
        self.todos.append(todo)
        self.todos = sorted(self.todos, Model.sort_comparator)

    def append(self, id, text):
        """Append text to a given todo.

        >>> m = Model()
        >>> m.add("My")
        >>> m.append(1, 'todo')
        >>> m[0].todo
        'My todo'
        """
        self.get_by_id(id).append(text)

    def prepend(self, id, text):
        """prepend text to a given todo.

        >>> m = Model()
        >>> m.add("todo")
        >>> m.prepend(1, 'My')
        >>> m[0].todo
        'My todo'
        """
        self.get_by_id(id).prepend(text)

    def extend(self, iterable):
        """Extend this model with todos from some iterable.

        >>> m = Model()
        >>> m.add('My todo')
        >>> m.extend(['My other todo'])
        >>> len(m)
        2
        >>> m[1].todo
        'My other todo'
        """
        for item in iterable:
            self.add(item)

    def total(self):
        """Return the total number of items in the model.

        For plain models this is the same as len(model). Filtered models
        must return the total unfiltered item count, i.e. total() of the
        original model.
        """
        return len(self)

    def get_by_id(self, id):
        """Get todo by id.
        
        >>> m = Model()
        >>> m.add("My todo")
        >>> m.add("Other todo")
        >>> m.get_by_id(1).todo
        'My todo'
        >>> m.get_by_id(2).todo
        'Other todo'
        """
        return filter(lambda t: t.id == id, self.todos)[0]

    def set_priority(self, id, priority):
        """Set the priority of the todo with the given id.

        If priority is None, the priority gets unset.

        >>> m = Model()
        >>> m.add("My todo")
        >>> m.set_priority(1, "A")
        >>> m[0].todo
        '(A) My todo'
        >>> m.set_priority(1, 'D')
        >>> m[0].todo
        '(D) My todo'
        >>> m.set_priority(1, None)
        >>> m[0].todo
        'My todo'
        """
        self.get_by_id(id).set_priority(priority)

    def set_done(self, id, done=True):
        """Change the value of 'done' for a given todo.

        >>> m = Model()
        >>> m.add("My todo")
        >>> m.set_done(1)
        >>> m[0].done()
        True
        """
        self.get_by_id(id).set_done(done)

    def contexts(self):
        """Get all contexts defined in the todos.

        >>> m = Model()
        >>> m.add("My todo @context1")
        >>> m.contexts()
        ['@context1']
        >>> m.add("My other todo @context1 @context2")
        >>> m.contexts()
        ['@context1', '@context2']
        >>> m.add("Send email to address@example.com")
        >>> m.contexts()
        ['@context1', '@context2']
        """

        class ContextIter(object):

            def __init__(self, model):
                self.iter = iter(model)

            def __iter__(self):
                return self

            def next(self):
                todo = self.iter.next()
                return re.findall('(?<!\\w)@\\w+', todo.todo)

        return sorted(list(set([ c for ctxs in ContextIter(self) for c in ctxs ])), cmp)

    def projects(self):
        """Get all projects defined in the todos.

        >>> m = Model()
        >>> m.add("My todo +project1")
        >>> m.projects()
        ['+project1']
        >>> m.add("My other todo +project1 +project2")
        >>> m.projects()
        ['+project1', '+project2']
        >>> m.add("Solve this math problem: 1+x=2")
        >>> m.projects()
        ['+project1', '+project2']
        """

        class ProjectIter(object):

            def __init__(self, model):
                self.iter = iter(model)

            def __iter__(self):
                return self

            def next(self):
                todo = self.iter.next()
                return re.findall('(?<!\\w)\\+\\w+', todo.todo)

        return sorted(list(set([ p for projects in ProjectIter(self) for p in projects ])), cmp)


if __name__ == '__main__':
    import doctest
    doctest.testmod()