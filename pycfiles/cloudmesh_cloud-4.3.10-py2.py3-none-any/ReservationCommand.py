# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/ReservationCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.cloud.reservation import Reservation
from cloudmesh_client.shell.console import Console
import json, pyaml
from timestring import Date
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.common.Error import Error

class ReservationCommand(PluginCommand, CloudPluginCommand):
    topics = {'reservation': 'todo'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command reservation')

    @command
    def do_reservation(self, args, arguments):
        """
        ::

            Usage:
                reservation info --user=USER --project=PROJECT
                reservation list [--name=NAME]
                                 [--user=USER]
                                 [--project=PROJECT]
                                 [--hosts=HOSTS]
                                 [--start=TIME_START]
                                 [--end=TIME_END]
                                 [--format=FORMAT]
                reservation delete [all]
                                   [--user=USER]
                                   [--project=PROJECT]
                                   [--name=NAME]
                                   [--start=TIME_START]
                                   [--end=TIME_END]
                                   [--hosts=HOSTS]
                reservation delete --file=FILE
                reservation update --name=NAME
                                  [--start=TIME_START]
                                  [--end=TIME_END]
                                  [--user=USER]
                                  [--project=PROJECT]
                                  [--hosts=HOSTS]
                                  [--description=DESCRIPTION]
                reservation add --name=NAME
                                [--start=TIME_START]
                                [--end=TIME_END]
                                [--user=USER]
                                [--project=PROJECT]
                                [--hosts=HOSTS]
                                [--description=DESCRIPTION]
                reservation add --file=FILE

            Arguments:

                NAME            Name of the reservation
                USER            Registration will be done for this user
                PROJECT         Project to be used
                HOSTS           Hosts to reserve
                TIME_START      Start time of reservation
                TIME_END        End time of reservation
                FORMAT          Format of output
                DESCRIPTION     Description for reservation
                FILE            File that contains reservation data to be added/ deleted

            Options:

                --name=NAME           Names of the reservation
                --user=USER           user name
                --project=PROJECT     project id
                --start=TIME_START    Start time of the reservation, in
                                      MM/DD/YYYY at hh:mm aa format. (default value: 01/01/1901 at 12:00 am])
                --end=TIME_END        End time of the reservation, in
                                      MM/DD/YYYY at hh:mm aa format. (default value: 12/31/2100 at 11:59 pm])
                --host=HOSTS          host name
                --description=DESCRIPTION  description summary of the reservation
                --file=FILE           Adding multiple reservations from one file
                --format=FORMAT       Format is either table, json, yaml or csv
                                      [default: table]

            Description:

                reservation info
                    lists the resources that support reservation for
                    a given user or project.
        """

        def _print_dict(d, header=None, format='table'):
            if format == 'json':
                return json.dumps(d, indent=4)
            if format == 'yaml':
                return pyaml.dump(d)
            if format == 'table':
                return Printer.write(d, order=[
                 'id',
                 'name',
                 'start_time',
                 'end_time',
                 'user',
                 'project',
                 'hosts',
                 'description',
                 'cloud'], output='table', sort_keys=True)
            if format == 'csv':
                TODO.implement()
            else:
                return d

        def _get_db_date_format(date):
            """
            Utility Function that accepts instance of Date object and returns a string with Datetime for DB.
            :param date: Date object
            :return: Date as string with format expected in DB.
            """
            db_date = ('{:}-{:}-{:} {:}:{:}').format(str(date.month).zfill(2), str(date.day).zfill(2), str(date.year).zfill(4), str(date.hour).zfill(2), str(date.minute).zfill(2))
            return db_date

        if arguments['info']:
            TODO.implement()
        elif arguments['list']:
            try:
                _name = arguments['--name']
                _user = arguments['--user']
                _project = arguments['--project']
                _format = arguments['--format']
                _hosts = arguments['--hosts']
                _start = arguments['--start']
                _end = arguments['--end']
                _format = arguments['--format']
                reserve = Reservation()
                dictionary = reserve.list(_name, _start, _end, _user, _project, _hosts)
                print(_print_dict(dictionary, format=_format))
                msg = 'info. OK.'
                Console.ok(msg)
            except Exception as e:
                Error.traceback(e)
                Console.error('Problem listing reservations')

        elif arguments['delete']:
            if arguments['all']:
                try:
                    reserve = Reservation()
                    reserve.delete()
                    msg = 'info. OK.'
                    Console.ok(msg)
                except Exception as e:
                    Error.traceback(e)
                    Console.error('Problem deleting all reservations')

            else:
                try:
                    _name = arguments['--name']
                    _user = arguments['--user']
                    _project = arguments['--project']
                    _format = arguments['--format']
                    _hosts = arguments['--hosts']
                    _start = arguments['--start']
                    _end = arguments['--end']
                    _format = arguments['--format']
                    reserve = Reservation()
                    reserve.delete(_name, _start, _end, _user, _project, _hosts)
                    msg = 'info. OK.'
                    Console.ok(msg)
                except Exception as e:
                    Error.traceback(e)
                    Console.error('Problem deleting reservations')

        elif arguments['add']:
            if arguments['--file'] is None:
                name = None
                try:
                    name = arguments['--name']
                    hosts = arguments['--hosts']
                    user = arguments['--user']
                    project = arguments['--project']
                    description = arguments['--description']
                    start_time = arguments['--start'] or '01/01/1901 at 07:30 pm'
                    end_time = arguments['--end'] or '12/31/2100 at 11:59 pm'
                    stime = Date(start_time)
                    etime = Date(end_time)
                    reserve = Reservation()
                    reserve.add(name, _get_db_date_format(stime), _get_db_date_format(etime), hosts=hosts, user=user, project=project, description=description)
                    print(('Reservation {:} added successfully').format(name))
                    msg = 'info. OK.'
                    Console.ok(msg)
                except Exception as e:
                    Error.traceback(e)
                    Console.error(('Problem adding reservation {:}').format(name))

            else:
                try:
                    TODO.implement()
                except Exception as e:
                    print('Error in adding from file. ', e)

        elif arguments['update']:
            name = None
            try:
                name = arguments['--name']
                hosts = arguments['--hosts']
                user = arguments['--user']
                project = arguments['--project']
                description = arguments['--description']
                start_time = arguments['--start'] or '01/01/1901 at 07:30 pm'
                end_time = arguments['--end'] or '12/31/2100 at 11:59 pm'
                stime = Date(start_time)
                etime = Date(end_time)
                reserve = Reservation()
                reserve.update(name, _get_db_date_format(stime), _get_db_date_format(etime), hosts=hosts, user=user, project=project, description=description)
                print(('Reservation {:} updated successfully').format(name))
                msg = 'info. OK.'
                Console.ok(msg)
            except Exception as e:
                Error.traceback(e)
                Console.error(('Problem updating reservation {:}').format(name))

        return ''