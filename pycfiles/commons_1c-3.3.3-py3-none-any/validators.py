# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/commonslib/validators.py
# Compiled at: 2015-04-04 05:19:06
__doc__ = '\nCreated on 2011-6-16\nauthor: huwei\n'
import functools, re
REQUIRED = 'required'
CUSTOM = 'custom'
EMAIL = 'email'
URL = 'url'
DATE = 'date'
DATEISO = 'dateISO'
NUMBER = 'number'
DIGITS = 'digits'
CREDITCARD = 'creditcard'
EQUALTO = 'equalTo'
ACCEPT = 'accept'
MAXLENGTH = 'maxlength'
MINLENGTH = 'minlength'
RANGELENGTH = 'rangelength'
RANGE = 'range'
MAX = 'max'
MIN = 'min'
ALPHABET_DIGITS = 'alphabet_digits'

class Validators(object):
    u"""校验者类
    """
    VALID_NOT_EMPTY = '.+'
    VALID_NUMBER = '^[-+]?\\d*\\.?\\d*$'
    VALID_EMAIL = '^\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*\\.\\w+([-.]\\w+)*$'
    VALID_URL = '^(http(s)?://([a-zA-Z0-9]+.)(\\S*?\\.\\S*?))(\\s|\\|\\)|\\]|\\[|\\{|\\}|,|"|\'|:|\\<||\\.\\s)$'
    VALID_DATEISO = '^\\d{4}[\\/-]\\d{1,2}[\\/-]\\d{1,2}$'
    VALID_DIGITS = '^\\d+$'
    VALID_YEAR = '^[12][0-9]{3}$'
    VALID_ALPHABET_DIGITS = '^[0-9a-zA-Z]*[a-zA-Z]+[0-9a-zA-Z]*$'
    DEFAULT_MESSAGES = {'required': '必选字段', 
       'remote': '请修正该字段', 
       'email': '请输入正确格式的电子邮件', 
       'url': '请输入合法的网址', 
       'date': '请输入合法的日期', 
       'dateISO': '请输入合法的日期 (ISO).', 
       'number': '请输入合法的数字', 
       'digits': '只能输入整数', 
       'creditcard': '请输入合法的信用卡号', 
       'equalTo': '请再次输入相同的值', 
       'accept': '请输入拥有合法后缀名的字符串', 
       'maxlength': '请输入一个长度最多是 {0} 的字符串', 
       'minlength': '请输入一个长度最少是 {0} 的字符串', 
       'rangelength': '请输入一个长度介于 {0} 和 {1} 之间的字符串', 
       'range': '请输入一个介于 {0} 和 {1} 之间的值', 
       'max': '请输入一个最大为 {0} 的值', 
       'min': '请输入一个最小为 {0} 的值'}

    def __init__(self):
        """
        Constructor
        """
        self.rules = {}
        self.messages = {}
        self.errors = {}

    def invalidate(self, field, validate_type):
        """Sets a field as invalid.

        :param field: string field The name of the field to invalidate
        :param validate_type: validate type
        :return: void
        """
        if self.messages.get(field) and self.messages.get(field).get(validate_type):
            self.errors[field] = self.messages.get(field).get(validate_type)
        else:
            self.errors[field] = Validators.DEFAULT_MESSAGES[validate_type]

    def validates(self, data=None):
        u"""执行验证.
        ::
            validators=Validators()
            #设置验证规则
            validators.rules=dict(
                name={REQUIRED:True, MAXLENGTH:40})
            #设置验证失败的文案
            validators.messages=dict(
                name={REQUIRED:'作品名称不能为空', MAXLENGTH:'作品名称不能超过40个字符'})
            #执行验证
            if not validators.validates(shot):
                print validators.validationErrors
        :param data: 需要验证的数据
        :return: 验证通过返回True，否则返回False
        """
        if data is None:
            data = []
        return len(self.invalid_fields(data)) == 0

    def invalid_fields(self, data=None):
        """Returns an array of invalid fields.

        :param data:
        :return: return array Array of invalid fields or boolean case any error occurs
        """
        self.errors = {}
        if data is None:
            data = []
        if len(self.rules) == 0 or len(data) == 0:
            return self.errors
        else:
            for field_name, validator in self.rules.iteritems():
                for validate_type, validate_value in validator.iteritems():
                    if validate_type == REQUIRED:
                        self.required_validator(field_name, data[field_name] if data.get(field_name) else None, validate_value)
                    if data.get(field_name):
                        if validate_type == EMAIL:
                            self.email_validator(field_name, data[field_name], validate_value)
                        elif validate_type == ALPHABET_DIGITS:
                            self.alphabet_digits_validator(field_name, data[field_name], validate_value)
                        elif validate_type == URL:
                            self.url_validator(field_name, data[field_name], validate_value)
                        elif validate_type == DATEISO or validate_type == DATE:
                            self.dateiso_validator(field_name, data[field_name], validate_value)
                        elif validate_type == NUMBER:
                            self.number_validator(field_name, data[field_name], validate_value)
                        elif validate_type == DIGITS:
                            self.digits_validator(field_name, data[field_name], validate_value)
                        elif validate_type == CREDITCARD:
                            pass
                        elif validate_type == EQUALTO:
                            self.equalto_validator(field_name, data[field_name], validate_value)
                        elif validate_type == MAXLENGTH:
                            self.maxlength_validator(field_name, data[field_name], validate_value)
                        elif validate_type == MINLENGTH:
                            self.minlength_validator(field_name, data[field_name], validate_value)
                        elif validate_type == RANGELENGTH:
                            self.rangelength_validator(field_name, data[field_name], validate_value)
                        elif validate_type == RANGE:
                            self.range_validator(field_name, data[field_name], validate_value)
                        elif validate_type == MAX:
                            self.max_validator(field_name, data[field_name], validate_value)
                        elif validate_type == MIN:
                            self.min_validator(field_name, data[field_name], validate_value)
                        elif validate_type == CUSTOM:
                            self.custom_validator(field_name, data[field_name], validate_value)

            return self.errors

    def required_validator(self, field_name, field_value, validate_value):
        if validate_value and (field_value is None or None == re.compile(Validators.VALID_NOT_EMPTY).search(field_value)):
            self.invalidate(field_name, REQUIRED)
        return

    def custom_validator(self, field_name, field_value, validate_value):
        if field_value and not validate_value:
            self.invalidate(field_name, CUSTOM)

    def email_validator(self, field_name, field_value, validate_value):
        if field_value and validate_value and None == re.search(Validators.VALID_EMAIL, field_value):
            self.invalidate(field_name, EMAIL)
        return

    def alphabet_digits_validator(self, field_name, field_value, validate_value):
        if field_value and validate_value and None == re.search(Validators.VALID_ALPHABET_DIGITS, field_value):
            self.invalidate(field_name, ALPHABET_DIGITS)
        return

    def number_validator(self, field_name, field_value, validate_value):
        if field_value and validate_value and None == re.search(Validators.VALID_NUMBER, field_value):
            self.invalidate(field_name, NUMBER)
        return

    def url_validator(self, field_name, field_value, validate_value):
        if field_value and validate_value and None == re.search(Validators.VALID_URL, field_value):
            self.invalidate(field_name, URL)
        return

    def dateiso_validator(self, field_name, field_value, validate_value):
        if field_value and validate_value and None == re.search(Validators.VALID_DATEISO, field_value):
            self.invalidate(field_name, DATEISO)
        return

    def digits_validator(self, field_name, field_value, validate_value):
        if field_value and validate_value and None == re.search(Validators.VALID_DIGITS, field_value):
            self.invalidate(field_name, DIGITS)
        return

    def equalto_validator(self, field_name, field_value, validate_value):
        if field_value != validate_value:
            self.invalidate(field_name, EQUALTO)

    def maxlength_validator(self, field_name, field_value, validate_value):
        if field_value and len(field_value) > validate_value:
            self.invalidate(field_name, MAXLENGTH)

    def minlength_validator(self, field_name, field_value, validate_value):
        if field_value and len(field_value) < validate_value:
            self.invalidate(field_name, MINLENGTH)

    def rangelength_validator(self, field_name, field_value, validate_value):
        if field_value and (len(field_value) < int(validate_value[0]) or len(field_value) > int(validate_value[1])):
            self.invalidate(field_name, RANGELENGTH)

    def range_validator(self, field_name, field_value, validate_value):
        if field_value and (int(field_value) < int(validate_value[0]) or int(field_value) > int(validate_value[1])):
            self.invalidate(field_name, RANGE)

    def max_validator(self, field_name, field_value, validate_value):
        if field_value is not None and int(field_value) > int(validate_value):
            self.invalidate(field_name, MAX)
        return

    def min_validator(self, field_name, field_value, validate_value):
        if field_value is not None and int(field_value) < int(validate_value):
            self.invalidate(field_name, MIN)
        return