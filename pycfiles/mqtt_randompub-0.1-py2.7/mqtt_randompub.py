# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mqtt_randompub/mqtt_randompub.py
# Compiled at: 2013-09-10 11:19:06
import random, time, sys, os, signal, itertools, mosquitto, opthandling

def send(broker, port, qos, number, interval, topic, subtopic1, subtopic2, payload):
    count = 1
    mqttclient = mosquitto.Mosquitto('mqtt-randompub')
    mqttclient.connect(broker, port=int(port))
    if number == 0:
        print 'Messages are published on topic %s/#... -> CTRL + C to shutdown' % topic
        while True:
            complete_topic = generate_topic(topic, subtopic1, subtopic2)
            mqttclient.publish(complete_topic, payload)
            time.sleep(interval)

    elif number == 1:
        complete_topic = generate_topic(topic, subtopic1, subtopic2)
        mqttclient.publish(complete_topic, payload)
    else:
        for x in range(1, number + 1):
            complete_topic = generate_topic(topic, subtopic1, subtopic2)
            mqttclient.publish(complete_topic, str(count) + payload)
            count = count + 1
            time.sleep(interval)

    mqttclient.disconnect()


def generate_topic(topic, subtopic1, subtopic2):
    if type(subtopic1) != list:
        stopic1_lst = str2list(subtopic1)
        stopic1 = random_subtopic(stopic1_lst)
    else:
        stopic1 = random_subtopic(subtopic1)
    if type(subtopic2) != list:
        stopic2_lst = str2list(subtopic2)
        stopic2 = random_subtopic(stopic2_lst)
    else:
        stopic2 = random_subtopic(subtopic2)
    generated_topic = topic + '/' + str(stopic1) + '/' + str(stopic2)
    return generated_topic


def random_subtopic(list):
    return random.choice(list)


def str2list(string):
    str_lst = string.split(',')
    for i, s in enumerate(str_lst):
        str_lst[i] = s.strip()

    return str_lst


def main():
    args = opthandling.argparsing()
    if args.number:
        send(args.broker, args.port, args.qos, int(args.number), float(args.interval), args.topic, args.subtopic1, args.subtopic2, args.load)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print 'Interrupted, exiting...'
        sys.exit(1)