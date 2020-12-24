# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\core\ssl.py
# Compiled at: 2019-06-20 05:39:07
# Size of source mod 2**32: 9399 bytes
import os, ssl
from ssl import VerifyMode
import tempfile
from pathlib import Path

class SSLContextBuilder:
    doc_sslsettings = {'protocols':'', 
     'options':'', 
     'verify_mode':'', 
     'ciphers':'', 
     'server_side':'', 
     'certfile':'', 
     'keyfile':'', 
     'certdata':'', 
     'keydata':''}

    def __init__(self):
        """
                Parses the user-supplied setting and create an ssl.SSLContext class
                """
        pass

    @staticmethod
    def load_certificates(context, sslsettings):
        if 'certfile' in sslsettings:
            print('loading certfile!')
            context.load_cert_chain(certfile=(sslsettings['certfile']),
              keyfile=(sslsettings['keyfile']))
        if 'certdata' in sslsettings:
            with tempfile.TemporaryDirectory() as (td):
                random_suffix = os.urandom(8).hex()
                certfile = '%s%s%s' % ('cert', random_suffix, '.crt')
                certfile_path = str(Path(td, certfile))
                keyfile = '%s%s%s' % ('key', random_suffix, '.crt')
                keyfile_path = str(Path(td, keyfile))
                with open(certfile_path, 'w') as (f):
                    f.write(sslsettings['certdata'])
                    f.flush()
                    os.fsync(f.fileno())
                with open(keyfile_path, 'w') as (f):
                    f.write(sslsettings['keydata'])
                    f.flush()
                    os.fsync(f.fileno())
                context.load_cert_chain(certfile=certfile_path,
                  keyfile=keyfile_path)

    @staticmethod
    def load_ca_certs(context, sslsettings):
        if 'cafile' in sslsettings:
            context.load_verify_locations(sslsettings['cafile'])
        else:
            if 'cadata' in sslsettings:
                with tempfile.TemporaryDirectory() as (td):
                    random_suffix = os.urandom(8).hex()
                    cafile = '%s%s%s' % ('cert', random_suffix, '.crt')
                    cafile_path = str(Path(td, cafile))
                    with open(certfile_path, 'w') as (f):
                        f.write(sslsettings['cadata'])
                        f.flush()
                        os.fsync(f.fileno())
                    context.load_verify_locations(certfile_path)
            else:
                raise Exception('Verify mode of %s needs "cafile " or "cadata" to be set in the settings!' % verify_mode)

    @staticmethod
    def from_dict(sslsettings, server_side=False):
        """
                Creates SSL context from dictionary-based configuration
                :param sslsettings: configuration dictionary
                :param server_side: decides that the context will be created as a server or client
                :return: ssl.SSLContext

                :TODO: if python devs come up with a way to load certificates/key from string rather than from a file then rewrite the certdata part
                """
        protocol = ssl.PROTOCOL_SSLv23
        options = []
        verify_mode = ssl.CERT_NONE
        ciphers = 'ALL'
        check_hostname = None
        if 'protocol' in sslsettings:
            protocol = getattr(ssl, sslsettings['protocol'])
        elif 'options' in sslsettings:
            options = []
            if isinstance(sslsettings['options'], list):
                for option in sslsettings['options']:
                    options.append(getattr(ssl, proto, 0))

        else:
            options.append(getattr(ssl, sslsettings['options'], 0))
        if 'verify_mode' in sslsettings:
            verify_mode = getattr(ssl, sslsettings['verify_mode'], 0)
        if 'ciphers' in sslsettings:
            ciphers = sslsettings['ciphers']
        if 'server_side' in sslsettings:
            server_side = sslsettings['server_side']
        elif server_side == False:
            check_hostname = True
            if 'check_hostname' in sslsettings:
                check_hostname = sslsettings['check_hostname']
        else:
            context = ssl.SSLContext(protocol)
            context.verify_mode = verify_mode
            if check_hostname:
                context.check_hostname = check_hostname
            elif server_side == True:
                SSLContextBuilder.load_certificates(context, sslsettings)
                if verify_mode != VerifyMode.CERT_NONE:
                    SSLContextBuilder.load_ca_certs(context, sslsettings)
            elif verify_mode != VerifyMode.CERT_NONE:
                SSLContextBuilder.load_certificates(context, sslsettings)
                SSLContextBuilder.load_ca_certs(context, sslsettings)
            else:
                SSLContextBuilder.load_ca_certs(context, sslsettings)
        context.options = 0
        for o in options:
            context.options |= o

        context.set_ciphers(ciphers)
        return context


def get_default_server_ctx():
    d = {'protocols':'PROTOCOL_SSLv23', 
     'options':'OP_CIPHER_SERVER_PREFERENCE', 
     'verify_mode':'CERT_NONE', 
     'ciphers':'ALL', 
     'server_side':True, 
     'certdata':'-----BEGIN CERTIFICATE-----\r\nMIIDEzCCAfugAwIBAgIBAjANBgkqhkiG9w0BAQsFADATMREwDwYDVQQDEwhyM3Rl\r\nc3RDQTAeFw0xODExMDEyMDM3MDBaFw0yODExMDEyMDM3MDBaMBYxFDASBgNVBAMM\r\nC3Rlc3Rfc2VydmVyMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtd1A\r\nTN7yDtJH5h1PHDOjBSZzd4PO1/EL35UyeRJ7uwUk6NyCgiwUicr+sMEVqKkiAaNN\r\nxbhGiJv9+uWtJWkSyhpBb2kDlXq/aBA1aAJ1U7y1CAK6QOTrxO9+ugLJuILsY5i/\r\nN4GERITeJgCwRdDaOCR3EzeG8mt+znQNwE3vdD3DCpNGSDMenyCF/STjBcpdXABF\r\n1CNeSnzEZUZ5enp2yg2oCTCbgN8yuTftM04gWyhojeYXitRJRYAE7INNqYGPyg73\r\nmXY4rN6mIgeVIhaWSYxpjp6g7LXOr0xNsBnt2pctf9zpYbq40HxI4SNBqB/9lwXV\r\n7PPC2cuWg2QEuCZANQIDAQABo28wbTAMBgNVHRMBAf8EAjAAMB0GA1UdDgQWBBTv\r\nWx/+SvpZgV8dyYVoGZ3norTwWzALBgNVHQ8EBAMCBeAwEQYJYIZIAYb4QgEBBAQD\r\nAgZAMB4GCWCGSAGG+EIBDQQRFg94Y2EgY2VydGlmaWNhdGUwDQYJKoZIhvcNAQEL\r\nBQADggEBAGB56E1cfRmoum67ska+3qo4xM41uU40rm+VnGQpcBhloNEZ8fGL/vB6\r\n0eJXsGe2uju49QfXccIV7JEawOauifc7cYYMNGKDCcPAXa3FXsCzRkkw+hO8l5zK\r\nqgtbcqy+ov0I2bn09iM3CdB9ZhyISPBcPTtGFQjRJSX2NXQbfOTlz5CWyqb8bR/g\r\nQqF1upvc0xzjJRjg/5VSxBdsBwqbH80vyiFBP9C919IfpUm+HDLe4Gps5NV5w+VT\r\nGVC3WHkWU5PUUbwaD0b1O32rYiihYrPLYWFLqDPzhWPTZjpBr/Ehu/WbGVtSQmFv\r\ng1T4Y9c1mGDYzyOy2/zeQWpWGZ0VnaE=\r\n-----END CERTIFICATE-----\r\n', 
     'keydata':'-----BEGIN RSA PRIVATE KEY-----\r\nMIIEowIBAAKCAQEAtd1ATN7yDtJH5h1PHDOjBSZzd4PO1/EL35UyeRJ7uwUk6NyC\r\ngiwUicr+sMEVqKkiAaNNxbhGiJv9+uWtJWkSyhpBb2kDlXq/aBA1aAJ1U7y1CAK6\r\nQOTrxO9+ugLJuILsY5i/N4GERITeJgCwRdDaOCR3EzeG8mt+znQNwE3vdD3DCpNG\r\nSDMenyCF/STjBcpdXABF1CNeSnzEZUZ5enp2yg2oCTCbgN8yuTftM04gWyhojeYX\r\nitRJRYAE7INNqYGPyg73mXY4rN6mIgeVIhaWSYxpjp6g7LXOr0xNsBnt2pctf9zp\r\nYbq40HxI4SNBqB/9lwXV7PPC2cuWg2QEuCZANQIDAQABAoIBAGLA4MCdM22u69Hd\r\nym5y76vFRF/6l+AUiTEAcCbkTYGxemhkDQ4oZ4KnUwOh5WPva4LeLUYXGV3m7tRF\r\n0W6GDujltvCLYqHRxIv6eTWgWBt/VgIikQbaB9ipf/P7vZPOrBQtBnBaiPs39vVF\r\n3HIcxdJEotAxj7qlenca97ib2VIRqGKI4xr36UdYs3XW2Ip1zatZPLTMBVroyLpY\r\nf9ytiXz7QlQH5mBE99oIksKrAz/z38zXZ18yIZJQRwnbC/nOapEeokMpRu61opEl\r\ne50K/qIKhrdGJJ+20BLIAa05W8jRC8ezZ7Hb+5XI4bl5HJF8IpVMqi1ZVLssQo3F\r\nS1N9egECgYEA6syeCP/b5hbV6z28SH4lT7fXAaakxxUt0otzt0lV2wUvsfvF3S9p\r\nWV4OYKvJrSapbzsGLseSjQE8ho9OIxpscPX4iqALhnbnY21DeSMY/zigLHPHX0mP\r\nSDInlfI+W+LapnHNU6ofZA5K+tN5WWAzskXmC5G3TPsGIv6A1YOANLUCgYEAxkkK\r\nmZIgMA5yGyv8t8jAe1B6cF40X2+77lM220ZgMTLfvFmjnQgypwPXxez4jHoAAgth\r\n/1ivxV7fvny6xl/J6IM8orKmKk8GQAganyzq50KxxxoSd8yasmqGlXoHVDsMbEoK\r\nRBFI9BtEn5OJ2impWYdE12mpt4IumkVgOw/0jYECgYEAqSr3ieBeHO7C/ZQjPc+1\r\nLjR0MnpQKie2NgXHP30U4JJiBMgzjOMF8h90GG5tBdXfKYbLM5USn4kOhJxnXZ9C\r\nFjkB807QPvcYS2iDvpls/yVbMevQ73ReSVPpdX1tNGLDyjwgBXGC4GHz37fRrHVF\r\nieIWlqtL96i8iSX4yNzP2CkCgYBca+Ev8YdlPuZ6uccCluT41WssgwxgS4FKNalF\r\nDYl6hR75+MIlSJPrewQQ8kJrn9XvHgUgcuMC2RTrAdJA8pb29GzH3QNMhyb/o4dd\r\nGB+piVG53vIqusiETtjKRWWzIg7JTr14OqJJfYg/5RIFCRQxcbZpvYtoyJoWOC4B\r\neY9ggQKBgDEMW8ZkNFgXpj+j7zxGpp/TQUtM4LL/uGa4Du3Wicz7T/Ho6lmVkLCZ\r\nGWQrsJZjqI512qFKDTVWX7nOap+oGqGBF4VnefvO9RVoB6wVqb3FpZRx8elUyPXN\r\noChY/SCgtGktqGgtcHYiFXVUqHW8cHTk9Sb0YL4T8xLMrab2j13C\r\n-----END RSA PRIVATE KEY-----\r\n'}
    return SSLContextBuilder.from_dict(d)