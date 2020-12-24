# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cfautodoc/autodoc.py
# Compiled at: 2016-03-04 11:56:21
import datetime, json

def heading(string, level=2):
    """
    Takes a string and wraps it with a heading.
    """
    return ('\n{0} {1}\n').format('#' * level, string)


def autodoc(template, documentation, timestamp=False, insert=False):
    try:
        with open(template) as (t):
            data = json.load(t)
    except Exception as exc:
        raise exc

    towrite = []
    if 'Description' in data:
        towrite.append(heading('Description'))
        towrite.append(data['Description'])
    if insert:
        try:
            with open(insert) as (insertf):
                for line in insertf:
                    towrite.append(line)

        except Exception as exc:
            raise exc

    if 'Metadata' in data:
        towrite.append(heading('Metadata', level=4))
        for key, value in sorted(data['Metadata'].iteritems()):
            towrite.append((' * **{0}**: {1}').format(key, value))

    if 'Parameters' in data:
        towrite.append(heading('Parameters'))
        for key, value in sorted(data['Parameters'].iteritems()):
            towrite.append((' * **{0}** - {1}').format(key, value['Description']))
            if 'Default' in value:
                towrite.append(('  * Default: `{0}`').format(value['Default']))
            if 'ConstraintDescription' in value:
                towrite.append(('  * Constraint: `{0}`').format(value['ConstraintDescription']))

    if 'Conditions' in data:
        towrite.append(heading('Conditions'))
        for key, value in sorted(data['Conditions'].iteritems()):
            towrite.append((' * **{0}** - `{1}`').format(key, value))

    if 'Mappings' in data:
        towrite.append(heading('Mappings'))
        for key, value in sorted(data['Mappings'].iteritems()):
            towrite.append((' * **{0}**:').format(key))
            for key in value.iteritems():
                towrite.append(('  * `{0}`').format(key))

    if 'Resources' in data:
        towrite.append(heading('Resources'))
        for key, value in sorted(data['Resources'].iteritems()):
            towrite.append((' * **{0}** - `{1}`').format(key, value['Type']))

    if 'Outputs' in data:
        towrite.append(heading('Outputs'))
        for key, value in sorted(data['Outputs'].iteritems()):
            towrite.append((' * **{0}** - `{1}`').format(key, value['Value']))

    if timestamp:
        time = str(datetime.datetime.now())
        towrite.append(('\n**Last Updated:** {0}').format(time))
    return ('\n').join(towrite)


if __name__ == '__main__':
    pass