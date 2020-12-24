# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/btform/rules.py
# Compiled at: 2015-09-16 04:15:41
import btform
not_null = btform.notnull
is_not_empty = btform.regexp('.+', '不允许为空')
is_date = btform.regexp('(\\d{4})-(\\d{2}-(\\d\\d))', '日期格式:yyyy-MM-dd')
is_email = btform.regexp('[\\w-]+(\\.[\\w-]+)*@[\\w-]+(\\.[\\w-]+)+$', 'email格式,比如name@domain.com')
is_chars = btform.regexp('^[A-Za-z]+$', '必须是英文字符串')
is_alphanum = lambda x: btform.regexp('^[A-Za-z0-9]{%s}$' % x, '必须是长度为%s的数字字母组合' % x)
is_alphanum2 = lambda x, y: btform.regexp('^[A-Za-z0-9]{%s,%s}$' % (x, y), '必须是长度为%s到%s的数字字母组合' % (x, y))
is_number = btform.regexp('^[0-9]*$', '必须是数字')
is_number2 = btform.regexp('^[1-9]\\d*$', '必须是大于0的正整数')
is_number3 = btform.regexp('^(([1-9]\\d*)|0)(\\.\\d{1,3})?$', '支持包含(最大3位)小数点 xx.xxxxx')
is_numberOboveZore = btform.regexp('^\\d+$', '必须为大于等于0的整数')
is_cn = btform.regexp('^[\\u4e00-\\u9fa5],{0,}$', '必须是汉字')
is_url = btform.regexp('[a-zA-z]+://[^\\s]*', 'url格式 xxxx://xxx')
is_phone = btform.regexp('^(\\(\\d{3,4}\\)|\\d{3,4}-)?\\d{7,8}$', '固定电话号码格式：0000-00000000')
is_idcard = btform.regexp('^\\d{15}$|^\\d{18}$|^\\d{17}[Xx]$', '身份证号码格式')
is_ip = btform.regexp('(^$)|\\d+\\.\\d+\\.\\d+\\.\\d+', 'ip格式：xxx.xxx.xxx.xxx')
is_mac = btform.regexp('[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}$', 'MAC地址格式 xx:xx:xx:xx:xx:xx')
is_rmb = btform.regexp('^(([1-9]\\d*)|0)(\\.\\d{1,2})?$', '人民币金额 xx.xx')
len_of = lambda x, y: btform.regexp('[\\s\\S]{%s,%s}$' % (x, y), '长度必须为%s到%s' % (x, y))
is_alphanum3 = lambda x, y: btform.regexp('^[A-Za-z0-9\\_\\-]{%s,%s}$' % (x, y), '必须是长度为%s到%s的数字字母与下划线组合' % (x, y))
is_period = btform.regexp('(^$)|^([01][0-9]|2[0-3]):[0-5][0-9]-([01][0-9]|2[0-3]):[0-5][0-9]$', '时间段，hh:mm-hh:mm,支持跨天，如 19:00-09:20')
is_telephone = btform.regexp('^1[0-9]{10}$', '必须是手机号码')
is_time = btform.regexp('(\\d{4})-(\\d{2}-(\\d\\d))\\s([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]', '时间格式:yyyy-MM-dd hh:mm:ss')
is_time_hm = btform.regexp('^([01][0-9]|2[0-3]):[0-5][0-9]$', '时间格式: hh:mm')
input_style = {'class': 'form-control'}
button_style = {'class': 'btn btn-primary'}
button_style_block = {'class': 'btn btn-block'}
if __name__ == '__main__':
    print is_mac.valid('00:0C:29:E3:5F:39')