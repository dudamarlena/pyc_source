# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/core/task.py
# Compiled at: 2016-11-22 15:21:45
import fabric.tasks

class Task(fabric.tasks.Task):
    """
    A Fabric task for EC2 boxes. Use this as the base class for custom Fabric tasks to be run on
    an EC2 box, as represented by an instance of Ec2Box. Pass instances of this class to Ec2Box
    .execute(). Use this only if your intend to create a hierarchy of task classes. Otherwise,
    it is much easier to write tasks as plain methods in a concrete subclass of Ec2Box and pass
    those method to Ec2Box.execute()

    This class extends Fabric's Task by using the class name as the name of the task and
    maintaining a link to the box instance this task is executed on.
    """

    def __init__(self, box):
        """
        Initializes this task for the given box.

        :param box: the box
        :type box: Box"""
        super(Task, self).__init__(name=self.__class__.__name__)
        self.box = box