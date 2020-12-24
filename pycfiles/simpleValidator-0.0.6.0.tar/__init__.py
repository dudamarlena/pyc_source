# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kenmartel/Development/Python/simpleValidator/simplevalidator/__init__.py
# Compiled at: 2014-02-10 04:23:54
""" 
    Simple Validator class with default validation rules, inspired by laravel

"""
__version__ = '0.0.5.9'
from . import rules as rulefactory
from . import i18n

class Validator:

    def __init__(self, **kwargs):
        self.rulefactory = rulefactory
        self.error_messages = []
        self.error_rules = []
        if 'fields' in kwargs and 'rules' in kwargs:
            self.make(fields=kwargs.get('fields'), rules=kwargs.get('rules'), messages=kwargs.get('messages'))

    def make(self, **kwargs):
        fields = kwargs.get('fields')
        rules = kwargs.get('rules')
        messages = kwargs.get('messages')
        if not isinstance(fields, dict):
            raise TypeError('fields data must be a dict')
        if not isinstance(rules, dict):
            raise TypeError('rules data must be a dict')
        if messages is not None and not isinstance(messages, dict):
            raise TypeError('custom error messages must be contained in a dict')
        self.fields = fields
        self.rules = rules
        if messages:
            self.rulefactory.messages.update(messages)
            self.messages_temp = messages
        else:
            self.messages_temp = None
        self.verify_fields()
        self.__validate()
        return

    def extend(self, customrule):
        if not isinstance(customrule, dict):
            raise TypeError('custom rule must be a dict')
        for rule in customrule:
            if not hasattr(customrule[rule], '__call__'):
                raise TypeError('custom rule is not a callable')
            setattr(self.rulefactory, rule, customrule[rule])

    def __call_rule(self, rule, **kwargs):
        return getattr(self.rulefactory, rule)(**kwargs)

    def validate(self, what, how):
        errors = []
        failed_rules = []
        rulelist = how.split('|')
        for rule in rulelist:
            if ':' in rule:
                rulevalue = rule.split(':')
                callback = self.__call_rule(rule=rulevalue[0], value=what, constraint=rulevalue[1])
            else:
                rulevalue = [
                 rule]
                callback = self.__call_rule(rule=rule, value=what)
            if not callback:
                if len(rulevalue) == 2:
                    errors.append(self.set_errors(rulevalue[0], field=what, constraint=rulevalue[1]))
                else:
                    errors.append(self.set_errors(rulevalue[0], field=what, constraint=''))
                failed_rules.append({what: rule})

        self.error_messages = errors
        self.error_rules = failed_rules

    def __validate(self):
        errors = []
        failed_rules = []
        for field in self.rules:
            rules = self.rules[field]
            rulelist = rules.split('|')
            for rule in rulelist:
                if ':' in rule:
                    rulevalue = rule.split(':')
                    callback = self.__call_rule(rule=rulevalue[0], value=self.fields[field], constraint=rulevalue[1])
                else:
                    rulevalue = [
                     rule]
                    callback = self.__call_rule(rule=rule, value=self.fields[field])
                if not callback:
                    if len(rulevalue) == 2:
                        errors.append(self.set_errors(rulevalue[0], field=field, constraint=rulevalue[1]))
                    else:
                        errors.append(self.set_errors(rulevalue[0], field=field, constraint=''))
                    failed_rules.append({field: rule})

        self.error_messages = errors
        self.error_rules = failed_rules

    def set_errors(self, rule, **kwargs):
        try:
            _ = i18n.defaultlang.ugettext
        except AttributeError:
            _ = i18n.defaultlang.gettext

        constraint = kwargs['constraint']
        field = kwargs['field']
        try:
            field_value = self.fields[field]
        except AttributeError:
            field_value = field

        if isinstance(self.rulefactory.messages[rule], dict):
            if self.rulefactory.is_number(field_value):
                rule_text = self.rulefactory.messages[rule]['numeric']
            else:
                rule_text = self.rulefactory.messages[rule]['string']
        else:
            rule_text = self.rulefactory.messages[rule]
        if ',' in constraint:
            boundaries = constraint.split(',')
            return _(rule_text).format(field, *boundaries)
        return _(rule_text).format(field, constraint)

    def fails(self):
        return len(self.error_messages) > 0

    def failed(self):
        return self.error_rules

    def errors(self):
        return self.error_messages

    def verify_fields(self):
        """ 
            As rules can be optional (ie not explicitely enforced)
            We check that the rules exist in the field dict 
        """
        for rule in self.rules:
            if rule not in self.fields:
                raise ValueError('fields do not correspond to rules')

        if self.messages_temp is not None:
            error = 0
            for d_rule in self.rules:
                for rule in self.messages_temp:
                    if rule not in self.rules[d_rule]:
                        error += 1
                    else:
                        error = 0

            if error > 0:
                raise ValueError('custom validation messages do not correspond to rule list')
        return