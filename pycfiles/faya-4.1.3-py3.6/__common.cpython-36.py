# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/faya/lib/__common.py
# Compiled at: 2018-06-29 04:15:10
# Size of source mod 2**32: 1133 bytes
import hashlib, random, re, click

@click.command()
@click.argument('source')
def md5(source):
    _md5 = hashlib.md5()
    _md5.update(source.encode('utf-8'))
    click.echo(_md5.hexdigest())


@click.command()
@click.argument('data')
def unicodeDecode(data):
    s = data.encode('utf-8')
    click.echo(s.decode('unicode-escape'))


@click.command()
@click.argument('data')
def unicodeEncode(data):
    s = data.encode('unicode-escape')
    click.echo(s.decode('utf-8'))


@click.command()
def roll():
    click.echo(str(random.randint(0, 100)))


@click.command()
def greek():
    l = [chr(x) for x in range(945, 970)]
    click.echo(' '.join(l))


@click.command()
@click.argument('data')
def cal(data):
    cal_reg = re.compile('[\\.\\+\\-\\*\\(\\)\\d/]+')
    in_cal = re.findall(cal_reg, data)
    if in_cal:
        if in_cal[0] != data:
            click.echo('输入不合法')
        else:
            try:
                click.echo(f"{data} = " + str(eval(data)))
            except SyntaxError:
                click.echo('输入算式有误')


if __name__ == '__main__':
    pass