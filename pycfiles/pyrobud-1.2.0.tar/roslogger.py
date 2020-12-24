# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/robots/roslogger.py
# Compiled at: 2015-01-26 11:58:05
import logging
try:
    import rospy
    from rosgraph_msgs.msg import Log
except ImportError:
    logging.warning('ROS not available: no ROS logging')

roslevel = {'DEBUG': 1, 'INFO': 2, 'WARNING': 4, 'ERROR': 8, 'CRITICAL': 16}

class RXConsoleHandler(logging.Handler):

    def __init__(self, topic='/rosout'):
        logging.Handler.__init__(self)
        rospy.sleep(0.5)
        self.pub = rospy.Publisher(topic, Log)
        self.log = Log()
        self.level = logging.DEBUG
        self.log.level = 2
        self.log.name = 'pyrobots logger'
        self.log.msg = 'Welcome in pyRobots'
        self.log.file = ''
        self.log.function = ''
        self.log.line = 0
        self.log.header.stamp = rospy.rostime.Time.now()
        self.pub.publish(self.log)

    def emit(self, record):
        if record.levelname in roslevel:
            level = roslevel[record.levelname]
        else:
            level = 2
        log = Log(level=level, name=record.name, msg=record.msg, file=record.filename, function=record.funcName, line=record.lineno)
        log.header.stamp = rospy.rostime.Time.now()
        self.pub.publish(log)


if __name__ == '__main__':
    logger = logging.getLogger('test')
    logger.addHandler(RXConsoleHandler())
    logger.setLevel(logging.DEBUG)
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Fatal message')