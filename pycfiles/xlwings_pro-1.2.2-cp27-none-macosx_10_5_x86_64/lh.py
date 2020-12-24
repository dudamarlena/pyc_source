# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <xlwings_pro-1.2.2>/xlwings/lh.py
# Compiled at: 2020-03-09 05:37:56
import sys, os, datetime as dt, json
from base64 import b64decode
try:
    import rsa
except ImportError as e:
    sys.exit(("Couldn't import 'rsa', a dependency of xlwings-pro. Please install it via 'pip install rsa'. Details: {0}.").format(str(e)))

class LicenseHandler:

    @staticmethod
    def get_license():
        if sys.platform.startswith('darwin'):
            config_file = os.path.join(os.path.expanduser('~'), 'Library', 'Containers', 'com.microsoft.Excel', 'Data', 'xlwings.conf')
        else:
            config_file = os.path.join(os.path.expanduser('~'), '.xlwings', 'xlwings.conf')
        if not os.path.exists(config_file):
            sys.exit('Could not find xlwings.conf. Run the following command first: xlwings license update -k MY_KEY')
        with open(config_file, 'r') as (f):
            config = f.readlines()
        key = None
        for line in config:
            if line.split(',')[0] == '"LICENSE_KEY"':
                key = line.split(',')[1].strip()[1:-1]

        if key:
            return key
        else:
            sys.exit('Could not find a LICENSE_KEY in xlwings.conf. Run the following command first: xlwings license update -k MY_KEY')
            return

    @staticmethod
    def validate_license(product):
        privkey_string = '-----BEGIN RSA PRIVATE KEY-----\nMIIEqAIBAAKCAQEAlYtfNQhYPCWdfgr7wktVUVGcYzdxpOtK4eWar4JNyrx4U9W9\nsE8i+56y7MUlgaF/lSo0xDfjbQBMFpCepBr/DUuHbbEKkpKEl/ooz76KbeafVtqq\nCYQhSi2kPHH8huKYhB7JcFQSA3v1fDhsh8hta64Hok7/1M6+zDOgYw8iZo4FbpIJ\n5V8jRA61XnTBI4BEE2ZMbfL7uhdFEFRe3sWasPbSgZ8FGr7uEovWzlLrYFUq74IU\n2C3ZWc8r9PPapn/O+AiZ7VPxf1baiC+yeWeK9uBXlOjm3onnihaz9utHuu5u2Glx\nSXfJmt5JSUMQpI3Drf++OmDZ3ptNBTfDREa5hQIDAQABAoIBAGBDfj76JypYoGAB\nm/x/V+Vn3n6zsxERcXumvINcIs1tsxtsTJYQ6xkEGHN3mOQwXJtdtufUfi6tcU1Z\nPPWwdxxM0VnYDFE7xeS64MiSBDQor8tOKQTFLFS+uqk6Su9dMAZkdxE63PmnMugK\nvjpN17noJfviVKbdir0VWwGe2joF5oYxvwvS8EhJFkcWBAek6/lfgzazjMliMXwt\nS7hRtiIPEP8oKx/W6nnypIyYAySE3ZG3u7jBjH6DLX2DRM6eGDQbKZzKhkskvELy\niIQKVhe17zjAh3UCG45OvKmAGOncCUAzTruuQa7Ng7gzRjwP1hOsxvl8lFGEna2m\nbWlFh6ECgYkA4gKhk5NNF16q5knqmUUqRUyI4eM5jVLlr7c0DK2kcv2gGZITRaC4\ncoB9FnShrPul7ZTI+77aTHfMh0R4D3IiLQmGc9LzN0xCayoKLpIWrGniENCuN46e\n2oOJr4WkaEj/ytHSQp1xa/KuFvgEfYStu51LEH133ghGZepmrddJb+UCVz6FSThp\nHQJ5AKljQ2wZo3ww7jl7xq80Qikn0qRqf/uM5VfYujvFqsjbSZR5BbY9C3ElyYMt\nBERVe3Rf880YCqCVebQnBSRGVJ2QwZrdWz/0LNf4qrD8djUnXSTojD49QyBcones\n99pweY+7KeFnoH3RfLbDzGCztNlVoZA+SsANiQKBiBjfCUDgON+Vf2EQSUzMm7Y8\nkeOpya+Pq88GbifnA+3Tk0a9GHnVEfcnxJwwAYqztrLKaMOrYQKBPHS2SDAK80/Z\neH5OfI1dSwHYAn7VfMFEdag8Dq/2dey+BOzX3BvNzLhZFrZV9SFX92h3qqbVbvjy\nekw6QnKgnn6gqOQAiQhTP0qyiqBgINECeGx4lIR1Jqww6V0GVoV8AaI5TjrbuHlu\nEK/gqeH9AxD83HGnznCVRu5+ND08Zq8bzqMHjyiXbLbJAdbL5g8EusrsGA8EEZsy\n0kS7iRMtmMURICSyhpyUvpfKun/I1C+eNzpDsN4Xbj8kF6kyWX7TlcxXec7VFSlH\ngQKBiGkg7oDcXfKe5HPYAnEhk3FpgW1UfqJwDwAV8QSHUoL+jyNB4hsagwSSlC7h\ncpa3/uxlpj0vsmhUZwjMTfUr/bZO4D9Z8d92FPDarpCXycFLT1pfgYKrXVDIFi/U\nLnrOUvYquXFrT/snfJrfyVHA/q5FF/3E35CRjuJKaCXdHBLlc0forMf2Qsg=\n-----END RSA PRIVATE KEY-----\n'
        privkey = rsa.PrivateKey.load_pkcs1(privkey_string)
        key = LicenseHandler.get_license()
        try:
            license_info = json.loads(rsa.decrypt(b64decode(key.encode('ascii')), privkey).decode())
        except Exception:
            sys.exit('Invalid license key.')

        if 'valid_until' not in license_info.keys() or 'products' not in license_info.keys():
            sys.exit('Invalid license key format.')
        license_valid_until = dt.datetime.strptime(license_info['valid_until'], '%Y-%m-%d').date()
        if dt.date.today() > license_valid_until:
            sys.exit(('Your license expired on {}.').format(license_valid_until.strftime('%Y-%m-%d')))
        if product not in license_info['products']:
            if product == 'pro':
                sys.exit('Invalid license key for xlwings PRO.')
            elif product == 'reports':
                sys.exit('Your license is not valid for the xlwings reports add-on.')