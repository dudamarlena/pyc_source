# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flawless/server/webapp.py
# Compiled at: 2018-03-24 18:10:25
from __future__ import absolute_import
import __main__, cgi, copy, collections, inspect, logging
try:
    import urlparse, urllib
    urlencode = urllib.urlencode
except ImportError:
    import urllib.parse as urlparse
    urlencode = urlparse.urlencode

from future.utils import iteritems
from thrift.Thrift import TType
import flawless.lib.config
from flawless.lib.utils import dump_json
import flawless.server.api.ttypes as api_ttypes
from flawless.server.service import FlawlessServiceBaseClass
log = logging.getLogger(__name__)
config = flawless.lib.config.get()

class FlawlessWebServiceHandler(FlawlessServiceBaseClass):
    """Handler for HTTP server to show state of the Flawless service"""

    def __init__(self, *args, **kwargs):
        super(FlawlessWebServiceHandler, self).__init__(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.get_weekly_error_report(*args, **kwargs)

    def _get_errors_seen_for_ts(self, timestamp):
        prefix = self._partition_for_ms(int(timestamp) * 1000 if timestamp else None)
        errors_seen = self.storage_factory(prefix)
        errors_seen.open()
        return errors_seen

    def _add_new_entry_to_config(self, key, entry, attr='identifiers'):
        class_map = dict(known_errors=api_ttypes.KnownErrorList, building_blocks=api_ttypes.CodeIdentifierList, third_party_whitelist=api_ttypes.CodeIdentifierList, watch_list=api_ttypes.WatchList, disownership_list=api_ttypes.FileDisownershipList)
        config_storage = self.storage_factory(partition=None)
        config_storage.open()
        current_value = config_storage[key] or class_map[key]()
        getattr(current_value, attr).append(entry)
        current_value.last_update_ts = self._epoch_ms()
        config_storage[key] = current_value
        config_storage.sync()
        config_storage.close()
        return

    def _construct_instance(self, params, cls):
        THRIFT_SPEC_NAME_FIELD = 2
        THRIFT_SPEC_TYPE_FIELD = 1
        THRIFT_SPEC_SUBTYPE_FIELD = 3
        init_args = inspect.getargspec(cls.__init__).args
        whitelist_attrs = [ s for s in init_args if s != 'self' ]
        args = dict((k, params.get(k)) for k in whitelist_attrs)
        arg_type_map = dict()
        for spec in cls.thrift_spec:
            if not spec or len(spec) < 3:
                continue
            if spec[THRIFT_SPEC_TYPE_FIELD] == TType.BOOL:
                arg_type_map[spec[THRIFT_SPEC_NAME_FIELD]] = bool
            elif spec[THRIFT_SPEC_TYPE_FIELD] == TType.I64 or spec[THRIFT_SPEC_TYPE_FIELD] == TType.I32:
                arg_type_map[spec[THRIFT_SPEC_NAME_FIELD]] = int
            elif spec[THRIFT_SPEC_TYPE_FIELD] == TType.LIST and spec[THRIFT_SPEC_SUBTYPE_FIELD][0] == TType.STRING:
                arg_type_map[spec[THRIFT_SPEC_NAME_FIELD]] = lambda v: [ s.strip() for s in v.split(',') ]

        for field, value in args.items():
            if value and field in arg_type_map:
                args[field] = arg_type_map[field](value)

        new_entry = cls(**args)
        return new_entry

    def get_weekly_error_report(self, timestamp=None, include_known_errors=False, include_modified_before_min_date=False):
        errors_seen = self._get_errors_seen_for_ts(timestamp)
        html_parts = ['<html><head><title>Error Report</title></head><body>']
        grouped_errors = collections.defaultdict(list)
        developer_score = collections.defaultdict(int)
        for key, value in iteritems(errors_seen):
            if (not value.is_known_error or include_known_errors) and (value.date >= config.report_only_after_minimum_date or include_modified_before_min_date):
                grouped_errors[value.developer_email].append((key, value))
                developer_score[value.developer_email] += value.error_count

        for developer, score in sorted(developer_score.items(), key=lambda t: t[1], reverse=True):
            html_parts.append('<strong id="%s">%s (score: %d)</strong>' % (developer.replace('"', "'"), developer, score))
            for err_key, err_info in sorted(grouped_errors[developer], key=lambda t: t[1].error_count, reverse=True):
                html_parts.append(('Number of Occurrences: {:,}').format(err_info.error_count))
                html_parts.append('Last Occurred: ' + err_info.last_occurrence)
                html_parts.append('Filename: ' + err_key.filename)
                html_parts.append('Function Name: ' + err_key.function_name)
                html_parts.append('Line Number: ' + str(err_key.line_number))
                html_parts.append('Date Committed: ' + err_info.date)
                html_parts.append('Email Sent: ' + str(err_info.email_sent))
                params = copy.copy(err_key.__dict__)
                if timestamp:
                    params['timestamp'] = timestamp
                view_url = '%s/view_traceback?%s' % (config.hostname, urlencode(params))
                html_parts.append("<a href='%s'>view traceback</a>" % view_url)
                html_parts.append('<br />')

            html_parts.append('<br />')

        if not grouped_errors:
            html_parts.append('Wow, no errors. Great job!')
        return ('<br />').join(html_parts)

    def view_traceback(self, filename='', function_name='', text='', line_number='', timestamp=None):
        errors_seen = self._get_errors_seen_for_ts(timestamp)

        def convert(s):
            if hasattr(s, 'decode'):
                return s.decode()

        err_key = api_ttypes.ErrorKey(filename=convert(filename), function_name=convert(function_name), text=convert(text), line_number=int(line_number))
        err_info = errors_seen[err_key]
        if err_info:
            datastr = self._format_traceback(err_info, include_err_info=True)
        else:
            datastr = 'Not Found'
        return ("\n            <html>\n                <head>\n                    <title>Flawless Traceback</title>\n                </head>\n                <body style='font-family: courier; font-size: 10pt'>\n                    {data}\n                </body>\n            </html>\n        ").format(data=datastr)

    def admin(self):
        return '\n            <html>\n                <head>\n                    <title>Flawless Admin Panel</title>\n                </head>\n                <body>\n                <div>\n                    <b>Change Configuration</b><br />\n                    <a href="add_known_error">Add Known Error</a><br />\n                    <a href="add_watch">Add File Watcher</a><br />\n                    <a href="remap_email">Remap Invalid Email Address</a><br />\n                    <a href="disown_file">Disown a File</a><br />\n                    <a href="add_ignored_exception">Add Ignored Exception Type</a><br />\n                    <br /><br />\n                    <b>View Configuration</b><br />\n                    <a href="view_config?key=building_blocks">View Building Blocks</a><br />\n                    <a href="view_config?key=third_party_whitelist">View Thirdparty Whitelist</a><br />\n                    <a href="view_config?key=known_errors">View Whitelisted Errors</a><br />\n                    <a href="view_config?key=ignored_exceptions">View Ignored Exception Types</a><br />\n                    <a href="view_config?key=watch_list">View File Watch List</a><br />\n                    <a href="view_config?key=disownership_list">View File Disownership List</a><br />\n                    <a href="view_config?key=email_remapping">View Email Remapping</a><br />\n                </div>\n             </body>\n            </html>\n        '

    def add_known_error(self, filename='', function_name='', code_fragment=''):
        code_fragment = cgi.escape(code_fragment)
        return ("\n            <html>\n                <head>\n                    <title>Add Known Error</title>\n                </head>\n                <body>\n                <div>\n                    Instructions: Fill out the file path, function name and code fragment for the known error.\n                    If function name or code fragment are left empty, then they are treated as wildcards.<br />\n                    Just entering file path, function name and code fragment will whitelist the error and stop\n                    all emails about it. If you want to continue emails, but at a lower (or higher)\n                    frequency or threshold you can use the optional fields.\n                </div><br /><br />\n                <form action='save_known_error' method='POST'>\n                    <table>\n                        <tr><td>* = Required</td></tr>\n                        <tr>\n                            <td>* File Path:</td>\n                            <td><input name='filename' type='text' value='{filename}' size='50'/></td>\n                        </tr>\n                        <tr>\n                            <td>* Function Name:</td>\n                            <td><input name='function_name' type='text'value='{function_name}' size='50'/></td>\n                        </tr>\n                        <tr>\n                            <td>* Code Fragment:</td>\n                            <td><textarea name='code_fragment' rows='1' cols='50'/>{code_fragment}</textarea></td>\n                        </tr>\n                        <tr>\n                            <td>* Error Type:</td>\n                            <td>\n                                <select name='type'>\n                                    <option value='known_errors' selected>Add to Known Errors</option>\n                                    <option value='building_blocks'>Mark as Library Code</option>\n                                    <option value='third_party_whitelist'>Add to Ignored Thirdparty Errors</option>\n                                </select>\n                            </td>\n                        </tr>\n                        <tr><td>&nbsp</td></tr>\n                        <tr><td><strong>Following section is only for known errors</strong></td></tr>\n                        <tr><td>Must set one of the following **</td></tr>\n                        <tr>\n                            <td>** Minimum Alert Threshold:</td>\n                            <td><input name='min_alert_threshold' type='text' /></td>\n                        </tr>\n                        <tr>\n                            <td>** Maximum Alert Threshold:</td>\n                            <td><input name='max_alert_threshold' type='text' /></td>\n                        </tr>\n                        <tr>\n                            <td>** Alert Every N Occurrences:</td>\n                            <td><input name='alert_every_n_occurrences' type='text' /></td>\n                        </tr>\n                        <tr>\n                            <td>Email Recipients CSV:</td>\n                            <td><input name='email_recipients' type='text' size='50'/></td>\n                        </tr>\n                        <tr>\n                            <td>Email Header:</td>\n                            <td><textarea name='email_header' rows='5' cols='50'></textarea></td>\n                        </tr>\n                    </table>\n                    <input type='submit'></input>\n                </form>\n             </body>\n            </html>\n        ").format(**dict(locals().items()))

    def save_known_error(self, request):
        params = dict(urlparse.parse_qsl(request))
        class_map = dict(known_errors=api_ttypes.KnownError, building_blocks=api_ttypes.CodeIdentifier, third_party_whitelist=api_ttypes.CodeIdentifier)
        new_entry = self._construct_instance(params, class_map[params['type']])
        self._add_new_entry_to_config(params['type'], new_entry)
        return '<html><body>SUCCESS</body></html>'

    def add_watch(self):
        return "\n            <html>\n                <head>\n                    <title>Add Watch</title>\n                </head>\n                <body>\n                <div>\n                    Instructions: Fill out the file path & email to send reports to.\n                </div><br /><br />\n                <form action='save_watch' method='POST'>\n                    <table>\n                        <tr><td>* = Required</td></tr>\n                        <tr>\n                            <td>* File Path:</td>\n                            <td><input name='filepath' type='text' size='50'/></td>\n                        </tr>\n                        <tr>\n                            <td>* Email:</td>\n                            <td><input name='email' type='text' size='50'/></td>\n                        </tr>\n                        <tr>\n                            <td>* Watch Type:</td>\n                            <td>\n                                <select name='watch_all_errors'>\n                                    <option value='true' selected>Any Error</option>\n                                    <option value='false'>Only Blamed Errors</option>\n                                </select>\n                            </td>\n                        </tr>\n                    </table>\n                    <input type='submit'></input>\n                </form>\n             </body>\n            </html>\n        "

    def save_watch(self, request):
        params = dict(urlparse.parse_qsl(request))
        params['watch_all_errors'] = params['watch_all_errors'] == 'true'
        new_entry = self._construct_instance(params, api_ttypes.WatchFileEntry)
        self._add_new_entry_to_config('watch_list', new_entry, attr='watches')
        return '<html><body>SUCCESS</body></html>'

    def remap_email(self):
        return "\n            <html>\n                <head>\n                    <title>Remap Email</title>\n                </head>\n                <body>\n                <div>\n                    Instructions: Fill out the old email & the new email to send reports to.\n                </div><br /><br />\n                <form action='save_remap_email' method='POST'>\n                    <table>\n                        <tr><td>* = Required</td></tr>\n                        <tr>\n                            <td>* Old Email:</td>\n                            <td><input name='old_email' type='text' size='50'/></td>\n                        </tr>\n                        <tr>\n                            <td>* New Email:</td>\n                            <td><input name='new_email' type='text' size='50'/></td>\n                        </tr>\n                    </table>\n                    <input type='submit'></input>\n                </form>\n             </body>\n            </html>\n        "

    def save_remap_email(self, request):
        params = dict(urlparse.parse_qsl(request))
        config_storage = self.storage_factory(partition=None)
        config_storage.open()
        current_value = config_storage['email_remapping'] or api_ttypes.EmailRemapping()
        current_value.remap[params['old_email']] = params['new_email']
        current_value.last_update_ts = self._epoch_ms()
        config_storage['email_remapping'] = current_value
        config_storage.sync()
        config_storage.close()
        return '<html><body>SUCCESS</body></html>'

    def disown_file(self):
        return "\n            <html>\n                <head>\n                    <title>Disown File</title>\n                </head>\n                <body>\n                <div>\n                    Instructions: Fill out filepath, your email & the new email to send reports to.\n                </div><br /><br />\n                <form action='save_disown_file' method='POST'>\n                    <table>\n                        <tr><td>* = Required</td></tr>\n                        <tr>\n                            <td>* Filepath:</td>\n                            <td><input name='filepath' type='text' size='50'/></td>\n                        </tr>\n                        <tr>\n                            <td>* Your Email:</td>\n                            <td><input name='email' type='text' size='50'/></td>\n                        </tr>\n                        <tr>\n                            <td>* New Email:</td>\n                            <td><input name='designated_email' type='text' size='50'/></td>\n                        </tr>\n                    </table>\n                    <input type='submit'></input>\n                </form>\n             </body>\n            </html>\n        "

    def save_disown_file(self, request):
        params = dict(urlparse.parse_qsl(request))
        new_entry = self._construct_instance(params, api_ttypes.FileDisownershipEntry)
        self._add_new_entry_to_config('disownership_list', new_entry, attr='disownerships')
        return '<html><body>SUCCESS</body></html>'

    def add_ignored_exception(self):
        return "\n            <html>\n                <head>\n                    <title>Add Ignored Exception</title>\n                </head>\n                <body>\n                <div>\n                    Instructions: Enter the full module path for the exception (ex: exceptions.ValueError)\n                </div><br /><br />\n                <form action='save_ignored_exceptions' method='POST'>\n                    <table>\n                        <tr><td>* = Required</td></tr>\n                        <tr>\n                            <td>* Exception Path:</td>\n                            <td><input name='exc_name' type='text' size='50'/></td>\n                        </tr>\n                    </table>\n                    <input type='submit'></input>\n                </form>\n             </body>\n            </html>\n        "

    def save_ignored_exceptions(self, request):
        params = dict(urlparse.parse_qsl(request))
        config_storage = self.storage_factory(partition=None)
        config_storage.open()
        current_value = config_storage['ignored_exceptions'] or api_ttypes.IgnoredExceptionList()
        if params['exc_name'] not in current_value.exceptions:
            current_value.exceptions.append(params['exc_name'])
        current_value.last_update_ts = self._epoch_ms()
        config_storage['ignored_exceptions'] = current_value
        config_storage.sync()
        config_storage.close()
        return '<html><body>SUCCESS</body></html>'

    def view_config(self, key):
        config_storage = self.storage_factory(partition=None)
        config_storage.open()
        current_value = config_storage[key]
        config_storage.close()
        data = dump_json(current_value)
        data = data.replace('\n', '<br />')
        return ("\n            <html>\n                <head>\n                    <title>Flawless Config</title>\n                </head>\n                <body style='font-family: courier; font-size: 10pt'>\n                    <pre>\n                        {data}\n                    </pre>\n                </body>\n            </html>\n        ").format(data=data)

    def check_health(self):
        parts = [
         '<html><body>OK<br/>']
        for option in flawless.lib.config.OPTIONS:
            parts.append('%s: %s' % (option.name, str(getattr(config, option.name))))

        parts.append('</body></html>')
        return ('<br />').join(parts)