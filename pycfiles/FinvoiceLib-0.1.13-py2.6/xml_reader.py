# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/reader/xml_reader.py
# Compiled at: 2010-03-24 05:47:13


class Block(object):
    block_type = None
    start = None
    end = None
    env_data = None
    data = None

    def __init__(self, block_type):
        self.block_type = block_type
        self.start = None
        self.end = None
        self.soap = ''
        self.payload = ''
        return


class FinvoiceXmlReader(object):
    filename = None

    def __init__(self, file_object):
        self.file_object = file_object

    def __iter__(self):
        soap_env_open = False
        finvoice_open = False
        msg = Block('SOAP-ENV')
        blocks = []
        for line in self.file_object:
            if not line.strip().startswith('<?xml '):
                if line.strip().startswith('<SOAP-ENV:Envelope'):
                    if finvoice_open:
                        blocks.append(msg)
                        finvoice_open = False
                        soap_env_open = True
                        yield msg
                    soap_env_open = True
                    msg = Block('SOAP-ENV')
                elif line.strip().startswith('</SOAP-ENV:Envelope>'):
                    soap_env_open = False
                    finvoice_open = False
                    msg.soap += line
                    continue
                elif line.strip().startswith('</Finvoice'):
                    finvoice_open = False
                    soap_env_open = False
                    msg.payload += line
                    return_msg = msg
                    msg = Block('SOAP-ENV')
                    blocks.append(return_msg)
                    yield return_msg
            elif not finvoice_open:
                finvoice_open = True
            elif not soap_env_open:
                finvoice_open = True
            if soap_env_open:
                msg.soap += line
            elif finvoice_open:
                msg.payload += line

        yield msg