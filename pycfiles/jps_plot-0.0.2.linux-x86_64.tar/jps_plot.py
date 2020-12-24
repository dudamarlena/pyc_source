# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jps_plot/jps_plot.py
# Compiled at: 2016-06-25 02:36:26
import argparse, jps, json_utils, plot, time

class AddDataSubscriber(object):

    def __init__(self, plot, topic_name, element_text, host=jps.DEFAULT_HOST, subscriber_port=jps.DEFAULT_SUB_PORT):
        self._plot = plot
        self._topic_name = topic_name
        self._element_text = element_text
        self._sub = jps.Subscriber(self._topic_name, self.callback, host=host, sub_port=subscriber_port)

    def callback(self, msg):
        t = time.time()
        label_data_list = json_utils.extract_data_by_text(msg, self._element_text)
        for label, data in label_data_list:
            self._plot.add_data_with_timestamp(('{0}.{1}').format(self._topic_name, label), data, t)

    def spin(self):
        self._sub.spin(use_thread=True)


def main():
    import sys, time
    parser = jps.ArgumentParser(publisher=False, description='jps plot')
    parser.add_argument('topic_and_elements', type=str, help='topic.element_name list', nargs='+')
    args = parser.parse_args()
    p = plot.InteructivePlotter()
    topic_element_texts = args.topic_and_elements
    subscribers = []
    for topic_element_text in topic_element_texts:
        topic, _, label = topic_element_text.partition('.')
        sub = AddDataSubscriber(p, topic, label, host=args.host, subscriber_port=args.subscriber_port)
        subscribers.append(sub)
        sub.spin()

    try:
        while True:
            p.draw()
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()