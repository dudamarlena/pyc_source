# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/config/ros_config.py
# Compiled at: 2020-05-11 18:43:50
# Size of source mod 2**32: 5267 bytes
import re

class RosConfiguration:
    __doc__ = '\n    Configuration of auto-generated ROS package\n    '

    def __init__(self):
        """
        Constructor of an instance of RosConfiguration
        """
        self._RosConfiguration__package_name = 'open_ros'
        self._RosConfiguration__node_name = 'ros_node_optimizer'
        self._RosConfiguration__description = 'parametric optimization with OpEn'
        self._RosConfiguration__rate = 10.0
        self._RosConfiguration__result_topic_queue_size = 100
        self._RosConfiguration__params_topic_queue_size = 100
        self._RosConfiguration__publisher_subtopic = 'result'
        self._RosConfiguration__subscriber_subtopic = 'parameters'

    @property
    def package_name(self):
        """
        Package name
        :return: package name (default: 'open_ros')
        """
        return self._RosConfiguration__package_name

    @property
    def node_name(self):
        """
        Node name (default: ros_node_optimizer)
        :return:
        """
        return self._RosConfiguration__node_name

    @property
    def publisher_subtopic(self):
        """
        Name of publisher sub-topic (default: "result")
        :return:
        """
        return self._RosConfiguration__publisher_subtopic

    @property
    def subscriber_subtopic(self):
        """
        Name of subscriber sub-topic (default: "parameters")
        :return:
        """
        return self._RosConfiguration__subscriber_subtopic

    @property
    def description(self):
        """
        Description of ROS package (in package.xml)
        :return: description
        """
        return self._RosConfiguration__description

    @property
    def rate(self):
        """
        ROS node rate in Hz (default: 10)
        :return: rate
        """
        return self._RosConfiguration__rate

    @property
    def result_topic_queue_size(self):
        """
        Size of "result" topic (default: 100)
        :return: result topic name
        """
        return self._RosConfiguration__result_topic_queue_size

    @property
    def params_topic_queue_size(self):
        """
        Size of "parameter" topic queue (default: 100)
        :return: parameter topic name
        """
        return self._RosConfiguration__params_topic_queue_size

    def with_package_name(self, pkg_name):
        """
        Set the package name, which is the same as the name
        of the folder that will store the auto-generated ROS node.
        The node name can contain lowercase and uppercase
        characters and underscores, but not spaces or other symbols
        :param pkg_name: package name
        :return: current object
        :raises: ValueError if pkg_name is not a legal package name
        """
        if re.match('^[a-zA-Z_]+[\\w]*$', pkg_name):
            self._RosConfiguration__package_name = pkg_name
            return self
        raise ValueError('invalid package name')

    def with_node_name(self, node_name):
        """
        Set the node name. The node name can contain lowercase
        and uppercase characters and underscores, but not spaces
        or other symbols
        :param node_name:
        :return: current object
        :raises: ValueError if node_name is not a legal node name
        """
        if re.match('^[a-zA-Z_]+[\\w]*$', node_name):
            self._RosConfiguration__node_name = node_name
            return self
        raise ValueError('invalid node name')

    def with_rate(self, rate):
        """
        Set the rate of the ROS node
        :param rate: rate in Hz
        :return: current object
        """
        self._RosConfiguration__rate = rate
        return self

    def with_description(self, description):
        """
        Set the description of the ROS package
        :param description: description (string)
        :return: current object
        """
        self._RosConfiguration__description = description
        return self

    def with_queue_sizes(self, result_topic_queue_size=100, parameter_topic_queue_size=100):
        """
        Set queue sizes for ROS node
        :param result_topic_queue_size:
        :param parameter_topic_queue_size:
        :return: current object
        """
        self._RosConfiguration__result_topic_queue_size = result_topic_queue_size
        self._RosConfiguration__params_topic_queue_size = parameter_topic_queue_size
        return self

    def with_publisher_subtopic(self, publisher_subtopic):
        """
        The auto-generated node will output its results to the topic
        `~/{publisher_subtopic}`. The subtopic (publisher_subtopic)
        can be specified using this method. The default subtopic name
        is 'result'. This can be configured after the package is
        generated, in `config/open_params.yaml`.

        :param publisher_subtopic: publisher sub-topic name
        :return: current object
        """
        self._RosConfiguration__publisher_subtopic = publisher_subtopic
        return self

    def with_subscriber_subtopic(self, subscriber_subtopic):
        """
        The auto-generated node will listen for input at
        `~/{subscriber_subtopic}`. The subtopic (subscriber_subtopic)
        can be specified using this method. The default subtopic name
        is 'parameters'. This can be configured after the package is
        generated, in `config/open_params.yaml`.

        :param subscriber_subtopic: subscriber sub-topic name
        :return: :return: current object
        """
        self._RosConfiguration__subscriber_subtopic = subscriber_subtopic
        return self