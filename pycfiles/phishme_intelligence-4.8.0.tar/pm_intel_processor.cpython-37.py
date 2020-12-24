# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.mcmahon@phishme.com/newdev/phishme_intelligence_tc/lib_3.7.3/phishme_intelligence/output/product/threatconnect/pm_intel_processor.py
# Compiled at: 2019-06-05 11:26:12
# Size of source mod 2**32: 18673 bytes
from __future__ import unicode_literals, absolute_import
import datetime

class IntelligenceProcessor(object):
    __doc__ = "\n    Helper class for storing PhishMe Intelligence before sending to ThreatConnect. It builds out the Batch API dictionary\n    for those ThreatConnect types that support it and helps with direct creation of those ThreatConnect types that don't\n    "

    def __init__(self, owner, logger, tcex):
        """
        Initialize the PhishMeIntelligenceProcessor object

        :param str owner:  ThreatConnect owner/group for PhishMe Intelligence
        :param logger: The logging object to use for logging
        :type logger: :class:`logging.logger`
        :param tcex: The TcEx object used for interaction with the Batch API
        :type tcex: :class:`tcex.TcEx`
        :param tc: The ThreatConnect object used for communication with ThreatConnect
        :type tc: :class:`threatconnect.ThreatConnect`
        """
        self.logger = logger
        self.logger.debug('__init__ of PhishMeIntelligenceProcessor')
        self.owner = owner
        self.indicator_list = []
        self.current_indicator = {}
        self.malware_family_ids = []
        self.current_group = None
        self.current_document = None
        self.current_group_id = None
        self.current_document_id = None
        self.batch = tcex.batch(owner=(self.owner), halt_on_error=False)
        self._initialize_indicator()
        self._initialize_group()
        self._initialize_document()

    def add_malware_family--- This code section failed: ---

 L.  51         0  LOAD_CONST               None
                2  RETURN_VALUE     

 L.  61         4  DUP_TOP          
                6  LOAD_GLOBAL              RuntimeError
                8  COMPARE_OP               exception-match
               10  POP_JUMP_IF_FALSE    60  'to 60'
               12  POP_TOP          
               14  STORE_FAST               'e'
               16  POP_TOP          
               18  SETUP_FINALLY        48  'to 48'

 L.  62        20  LOAD_FAST                'self'
               22  LOAD_ATTR                logger
               24  LOAD_METHOD              error
               26  LOAD_STR                 'Error getting the malware family '
               28  LOAD_FAST                'malware_family'
               30  BINARY_ADD       
               32  LOAD_GLOBAL              str
               34  LOAD_FAST                'e'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  BINARY_ADD       
               40  CALL_METHOD_1         1  '1 positional argument'
               42  POP_TOP          
               44  POP_BLOCK        
               46  LOAD_CONST               None
             48_0  COME_FROM_FINALLY    18  '18'
               48  LOAD_CONST               None
               50  STORE_FAST               'e'
               52  DELETE_FAST              'e'
               54  END_FINALLY      
               56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
             60_0  COME_FROM            10  '10'
               60  END_FINALLY      
             62_0  COME_FROM            58  '58'

 L.  66        62  LOAD_CONST               False
               64  STORE_FAST               'found_threat'

 L.  68        66  SETUP_LOOP          222  'to 222'
               68  LOAD_FAST                'threats'
               70  GET_ITER         
               72  FOR_ITER            220  'to 220'
               74  STORE_FAST               'threat'

 L.  69        76  LOAD_FAST                'self'
               78  LOAD_ATTR                logger
               80  LOAD_METHOD              debug
               82  LOAD_STR                 'Found threat for '
               84  LOAD_FAST                'malware_family'
               86  BINARY_ADD       
               88  CALL_METHOD_1         1  '1 positional argument'
               90  POP_TOP          

 L.  70        92  LOAD_FAST                'self'
               94  LOAD_ATTR                logger
               96  LOAD_METHOD              debug
               98  LOAD_STR                 'Adding family_id '
              100  LOAD_GLOBAL              str
              102  LOAD_FAST                'threat'
              104  LOAD_ATTR                id
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  BINARY_ADD       
              110  CALL_METHOD_1         1  '1 positional argument'
              112  POP_TOP          

 L.  71       114  LOAD_CONST               True
              116  STORE_FAST               'found_threat'

 L.  72       118  LOAD_FAST                'self'
              120  LOAD_ATTR                logger
              122  LOAD_METHOD              debug
              124  LOAD_STR                 'Associating with current group'
              126  CALL_METHOD_1         1  '1 positional argument'
              128  POP_TOP          

 L.  73       130  LOAD_FAST                'threat'
              132  LOAD_METHOD              associate_group
              134  LOAD_GLOBAL              ResourceType
              136  LOAD_ATTR                THREATS
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                current_group_id
              142  CALL_METHOD_2         2  '2 positional arguments'
              144  POP_TOP          

 L.  74       146  SETUP_EXCEPT        160  'to 160'

 L.  75       148  LOAD_FAST                'threat'
              150  LOAD_METHOD              commit
              152  CALL_METHOD_0         0  '0 positional arguments'
              154  POP_TOP          
              156  POP_BLOCK        
              158  JUMP_BACK            72  'to 72'
            160_0  COME_FROM_EXCEPT    146  '146'

 L.  76       160  DUP_TOP          
              162  LOAD_GLOBAL              RuntimeError
              164  COMPARE_OP               exception-match
          166_168  POP_JUMP_IF_FALSE   216  'to 216'
              170  POP_TOP          
              172  STORE_FAST               'e'
              174  POP_TOP          
              176  SETUP_FINALLY       204  'to 204'

 L.  77       178  LOAD_FAST                'self'
              180  LOAD_ATTR                logger
              182  LOAD_METHOD              error
              184  LOAD_STR                 'Error associating {0} with {1}'
              186  LOAD_METHOD              format
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                current_group_id
              192  LOAD_FAST                'malware_family'
              194  CALL_METHOD_2         2  '2 positional arguments'
              196  CALL_METHOD_1         1  '1 positional argument'
              198  POP_TOP          
              200  POP_BLOCK        
              202  LOAD_CONST               None
            204_0  COME_FROM_FINALLY   176  '176'
              204  LOAD_CONST               None
              206  STORE_FAST               'e'
              208  DELETE_FAST              'e'
              210  END_FINALLY      
              212  POP_EXCEPT       
              214  JUMP_BACK            72  'to 72'
            216_0  COME_FROM           166  '166'
              216  END_FINALLY      
              218  JUMP_BACK            72  'to 72'
              220  POP_BLOCK        
            222_0  COME_FROM_LOOP       66  '66'

 L.  78       222  LOAD_FAST                'found_threat'
          224_226  POP_JUMP_IF_FALSE   232  'to 232'

 L.  79       228  LOAD_CONST               None
              230  RETURN_VALUE     
            232_0  COME_FROM           224  '224'

 L.  81       232  LOAD_FAST                'self'
              234  LOAD_ATTR                logger
              236  LOAD_METHOD              debug
              238  LOAD_STR                 'No threat found, adding new threat'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          

 L.  82       244  LOAD_FAST                'self'
              246  LOAD_ATTR                logger
              248  LOAD_METHOD              debug
              250  LOAD_STR                 'Adding family '
              252  LOAD_FAST                'malware_family'
              254  BINARY_ADD       
              256  CALL_METHOD_1         1  '1 positional argument'
              258  POP_TOP          

 L.  83       260  LOAD_FAST                'self'
              262  LOAD_ATTR                threatconnect
              264  LOAD_METHOD              threats
              266  CALL_METHOD_0         0  '0 positional arguments'
              268  LOAD_METHOD              add
              270  LOAD_FAST                'malware_family'
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                owner
              276  CALL_METHOD_2         2  '2 positional arguments'
              278  STORE_FAST               'new_family'

 L.  84       280  LOAD_FAST                'new_family'
              282  LOAD_METHOD              add_tag
              284  LOAD_FAST                'malware_family'
              286  CALL_METHOD_1         1  '1 positional argument'
              288  POP_TOP          

 L.  85       290  LOAD_FAST                'new_family'
              292  LOAD_METHOD              add_attribute
              294  LOAD_STR                 'Description'
              296  LOAD_FAST                'description'
              298  CALL_METHOD_2         2  '2 positional arguments'
              300  POP_TOP          

 L.  86       302  LOAD_FAST                'new_family'
              304  LOAD_METHOD              associate_group
              306  LOAD_GLOBAL              ResourceType
              308  LOAD_ATTR                THREATS
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                current_group_id
              314  CALL_METHOD_2         2  '2 positional arguments'
              316  POP_TOP          

 L.  87       318  SETUP_EXCEPT        332  'to 332'

 L.  88       320  LOAD_FAST                'new_family'
              322  LOAD_METHOD              commit
              324  CALL_METHOD_0         0  '0 positional arguments'
              326  POP_TOP          
              328  POP_BLOCK        
              330  JUMP_FORWARD        392  'to 392'
            332_0  COME_FROM_EXCEPT    318  '318'

 L.  90       332  DUP_TOP          
              334  LOAD_GLOBAL              RuntimeError
              336  COMPARE_OP               exception-match
          338_340  POP_JUMP_IF_FALSE   390  'to 390'
              342  POP_TOP          
              344  STORE_FAST               'e'
              346  POP_TOP          
              348  SETUP_FINALLY       378  'to 378'

 L.  91       350  LOAD_FAST                'self'
              352  LOAD_ATTR                logger
              354  LOAD_METHOD              error
              356  LOAD_STR                 'Error creating the group for the malware family named '
              358  LOAD_FAST                'malware_family'
              360  BINARY_ADD       
              362  LOAD_GLOBAL              str
              364  LOAD_FAST                'e'
              366  CALL_FUNCTION_1       1  '1 positional argument'
              368  BINARY_ADD       
              370  CALL_METHOD_1         1  '1 positional argument'
              372  POP_TOP          

 L.  92       374  LOAD_CONST               None
              376  RETURN_VALUE     
            378_0  COME_FROM_FINALLY   348  '348'
              378  LOAD_CONST               None
              380  STORE_FAST               'e'
              382  DELETE_FAST              'e'
              384  END_FINALLY      
              386  POP_EXCEPT       
              388  JUMP_FORWARD        392  'to 392'
            390_0  COME_FROM           338  '338'
              390  END_FINALLY      
            392_0  COME_FROM           388  '388'
            392_1  COME_FROM           330  '330'

Parse error at or near `DUP_TOP' instruction at offset 4

    def _add_indicator(self, indicator_type, indicator):
        indicator_xid = self.batch.generate_xid([self.owner, indicator, indicator_type])
        current_indicator = self.batch.indicators[indicator_xid] if indicator_xid in self.batch.indicators else None
        if not current_indicator:
            current_indicator = {'xid':indicator_xid, 
             'summary':indicator,  'type':indicator_type}
        else:
            self.duplicate_indicator = True
            self.logger.debug("Indicator already exists so we're just associating the group")
        if 'associatedGroups' not in current_indicator:
            current_indicator['associatedGroups'] = []
        if self.current_group_xid not in current_indicator['associatedGroups']:
            current_indicator['associatedGroups'].append({'groupXid': self.current_group_xid})
        self.current_indicator = current_indicator

    def add_ip_indicator(self, ip):
        """
        Create ThreatConnect indicator of type Address (and group association) for Batch API list

        :param str ip: The Ip Address to add
        """
        self.logger.debug('add_ip_indicator of PhishMeIntelligenceProcessor')
        self._add_indicator'Address'ip

    def add_email_indicator(self, email):
        """
        Create ThreatConnect indicator of type EmailAddress (and group association) for Batch API list

        :param str email: The email address to add
        """
        self.logger.debug('add_email_indicator of PhishMeIntelligenceProcessor')
        self._add_indicator'EmailAddress'email

    def add_host_indicator(self, host):
        """
        Create ThreatConnect indicator of type Host (and group association) for Batch API list

        :param str host: The hostname to add
        """
        self.logger.debug('add_host_indicator of PhishMeIntelligenceProcessor')
        self._add_indicator'Host'host

    def add_domain_indicator(self, domain):
        self.logger.debug('add_domain_indicator of PhishMeIntelligenceProcessor')
        self._add_indicator'Domain'domain

    def add_url_indicator(self, url):
        """
        Create ThreatConnect indicator of type URL (and group association) for Batch API list

        :param str url: The URL to add
        """
        self.logger.debug('add_url_indicator of PhishMeIntelligenceProcessor')
        self._add_indicator'URL'url

    def add_file_indicator(self, md5, sha1=None, sha256=None):
        """
        Create ThreatConnect indicator of type File (and group association) for Batch API list

        :param str md5: MD5 of file indicator
        :param sha1: SHA-1 of file indicator
        :param sha256: SHA-256 of file indicator
        """
        self.logger.debug('add_file_indicator of PhishMeIntelligenceProcessor')
        hashes = '{} : {} : {}'.format(md5, sha1, sha256)
        self._add_indicator'File'hashes
        self.add_indicator_rating(3)

    def _add_indicator_group_association(self, indicator):
        """
        Sets up group association for indicator being processed

        :param dict indicator: indicator to add association to
        """
        self.logger.debug('_add_indicator_group_association of PhishMeIntelligenceProcessor')
        indicator['associatedGroups'] = []
        if self.current_group_xid is not None:
            self.logger.debug('{0} is associated to group_xid {1}'.formatindicator['summary']self.current_group_xid)
            indicator['associatedGroups'].append({'groupXid': str(self.current_group_xid)})
        if self.current_document_id is not None:
            indicator['associatedGroups'].append({'groupXid': str(self.current_document_id)})

    def add_indicator_attribute(self, attribute_type, value):
        """
        Add ThreatConnect attribute for current indicator being processed

        :param str attribute_type:  Type of attribute
        :param str value: Value of attribute
        """
        self.logger.debug('add_indicator_attribute of PhishMeIntelligenceProcessor')
        if 'attribute' not in self.current_indicator:
            self.current_indicator['attribute'] = []
        new_indicator_attribute = {'type':attribute_type, 
         'value':value}
        if new_indicator_attribute not in self.current_indicator['attribute']:
            self.current_indicator['attribute'].append(new_indicator_attribute)

    def add_group_attribute(self, attribute_type, value):
        """
        Add ThreatConnect attribute to current group being processed

        :param str attribute_type:  Type of attribute
        :param str value: Value of attribute
        """
        self.logger.debug('add_group_attribute of PhishMeIntelligenceProcessor')
        self.current_group.attributeattribute_typevalue

    def add_indicator_tag(self, name):
        """
        add tag to current indicator being processed

        :param str name: tag to add
        """
        self.logger.debug('add_indicator_tag of PhishMeIntelligenceProcessor')
        if 'tag' not in self.current_indicator:
            self.current_indicator['tag'] = []
        self.logger.debug('Adding tag {0} to {1}'.formatnameself.current_indicator['summary'])
        new_tag = {'name': name}
        if new_tag not in self.current_indicator['tag']:
            self.current_indicator['tag'].append(new_tag)

    def add_group_tag(self, name):
        """
        add tag to current group being processed

        :param str name: tag to add
        """
        self.logger.debug('add_group_tag of PhishMeIntelligenceProcessor')
        self.current_group.tag(name)

    def add_indicator_rating(self, rating):
        """
        add rating value to current indicator being processed

        :param str rating: tag to add
        """
        self.logger.debug('add_indicator_rating of PhishMeIntelligenceProcessor')
        if 'rating' in self.current_indicator:
            if self.current_indicator['rating'] >= rating:
                return
        self.current_indicator['rating'] = rating

    def _generate_group_xid(self, threat_id, group_type, owner):
        return self.batch.generate_xid([str(threat_id), group_type, owner])

    def add_group(self, group_type, group_name, published_date, threat_id):
        """
        Create group stub (this is not the commit to ThreatConnect)

        :param str group_type:  Type of group
        :param str group_name:  Name of group
        :param int published_date: published date (epoch timestamp)
        """
        self.logger.debug('add_group of PhishMeIntelligenceProcessor')
        self.logger.debug('Calling add_group in pm_intel_processor. group_type: {}, group_name: {}, published_date: {}'.format(group_type, group_name, published_date))
        group_xid = self._generate_group_xid(threat_id, group_type, self.owner)
        group_type = 'Threat' if group_type.lower().strip() == 'threat' else 'Incident'
        self.current_group = self.batch.group(group_type, group_name, xid=group_xid, date_added=(published_date / 1000))
        self.current_group_xid = group_xid
        if group_type == 'Incident':
            self.current_group.add_key_value'eventDate'datetime.datetime.fromtimestamp(published_date / 1000).strftime('%Y-%m-%dT%X')

    def add_document(self, document_name, file_name, active_threat_report, group_type, threat_id):
        """
        Create document stub (this is not the commit to ThreatConnect)

        :param str document_name: Name to give Document type
        :param str file_name:  Name of document
        :param str active_threat_report:
        :param str group_type: Type of group this document will be associated wit
        """
        self.logger.debug('add_document of PhishMeIntelligenceProcessor')
        self.current_document_xid = self._generate_group_xid('Document', document_name, str(threat_id))
        self.current_document = self.batch.group('Document', document_name, xid=(self.current_document_xid), associatedGroupXid=[self.current_group_xid])
        self.current_document.add_key_value'fileName'file_name
        self.current_document.add_filefile_nameactive_threat_report

    def add_document_attribute(self, attribute_type, value):
        """
        Add ThreatConnect attribute to current document being processed

        :param str attribute_type:  Type of attribute
        :param str value: Value of attribute
        """
        self.logger.debug('add_document_attribute of PhishMeIntelligenceProcessor')
        self.current_document.attributeattribute_typevalue

    def add_document_tag(self, tag):
        """
        add tag to current document being processed

        :param str name: tag to add
        """
        self.logger.debug('add_document_tag of PhishMeIntelligenceProcessor')
        self.current_document.tag(tag)

    def group_ready(self):
        """
        Call this method to indicate that group is ready to be "processed" (sent to ThreatConnect instance)

        :return: None
        """
        self.logger.debug('group_ready of PhishMeIntelligenceProcessor')
        self._process_group(self.current_group)

    def document_ready(self):
        """
        Call this method to indicate that document is ready to be "processed" (sent to ThreatConnect instance)

        :return: None
        """
        self.logger.debug('document_ready of PhishMeIntelligenceProcessor')
        self._process_document(self.current_document)

    def indicator_ready(self, source, threat_id):
        """
        Call this method to indicate that indicator is ready to be processed. This method also handles the situation
        where duplicate indicators exist in the current batch.

        :param str source: source of intelligence (always PhishMe Intelligence at this point)
        :param int threat_id:  Current Phishme Intelligence threat id being processed
        :return: None
        """
        self._process_indicator()

    def _process_group(self, group):
        """
        Commit group to ThreatConnect and prepare for next group

        :param group: ThreatConnect group object
        :type group: :class:`threatconnect-python.threatconnect.GroupObject`
        """
        self.logger.debug('process_group of PhishMeIntelligenceProcessor')
        self.current_group_xid = group.xid
        self._initialize_group()

    def _process_document(self, document):
        """
        Commit document to ThreatConnect and prepare for next group

        :param document: ThreatConnect document object
        :type doucment: :class:`threatconnect-python.threatconnect.DocumentObject`
        """
        self.logger.debug('process_document of PhishMeIntelligenceProcessor')
        self.current_document_xid = document.xid
        self._initialize_document()

    def _process_indicator(self):
        """
        Add ThreatConnect indicator to batch processing queue

        :param dict indicator: ThreatConnect Indicator is is ready for batch processing
        """
        self.logger.debug('_process_indicator of PhishMeIntelligenceProcessor')
        self.logger.debug(str(self.current_indicator))
        self.logger.debug('Adding indicator with xid: {}'.format(self.current_indicator['xid']))
        self.batch.add_indicator(self.current_indicator)
        self._initialize_indicator()

    def _check_for_duplicate_indicator(self, indicator):
        """
        Helper method to search for a duplicate indicator; if it exists return it and remove it from current list

        :param indicator: indicator that we are looking for a duplicate of
        :return: Duplicate indicator (if one exists)
        :rtype: dict or None
        """
        self.logger.debug('_check_for_duplicate_indicator of PhishMeIntelligenceProcessor')
        try:
            existing_indicators = self.batch.indicators
            self.logger.debug(type(existing_indicators))
            self.logger.debug(dir(existing_indicators))
            self.logger.debug(str(existing_indicators))
            matched_indicator = next((i for i in existing_indicators if i['xid'] == indicator['xid']))
            existing_indicators[:] = [i for i in existing_indicators if i['xid'] != indicator['xid']]
            self.batch.unprocessed_indicators = existing_indicators
            self.logger.debug('Indicator ' + indicator['summary'].split(' :')[0] + ' Is already in processing list...')
            return matched_indicator
        except StopIteration:
            return

    def commit(self):
        """
        Kick off batch processing of indicators to push into ThreatConnect

        :return: None
        """
        self.logger.debug('commit of PhishMeIntelligenceProcessor')
        try:
            self.logger.debug('processing jobs')
            self.batch.submit_all(halt_on_error=False)
        except Exception as e:
            try:
                self.logger.error('Failure Batch Processing Indicators: ' + str(e))
            finally:
                e = None
                del e

    def _initialize_indicator(self):
        """
        Preparation for processing new Indicator to add to ThreatConnect batch processing queue
        """
        self.logger.debug('_initialize_indicator of PhishMeIntelligenceProcessor')
        self.current_indicator = {'confidence': 100}
        self.duplicate_indicator = False

    def _initialize_group(self):
        """
        Preparation for processing new group to push into ThreatConnect
        """
        self.logger.debug('_initialize_group of PhishMeIntelligenceProcessor')
        self.current_group = None
        self.current_document = None
        self.current_document_id = None

    def _initialize_document(self):
        """
        Prepartion for processing new document to push into ThreatConnect
        """
        self.logger.debug('_initialize_document of PhishMeIntelligenceProcessor')
        self.current_document = None