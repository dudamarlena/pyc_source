# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/lbdrabbit-project/lbdrabbit/example/handlers/auth.py
# Compiled at: 2019-10-06 19:09:58
# Size of source mod 2**32: 9624 bytes
import re
from lbdrabbit import LbdFuncConfig
__lbd_func_config__ = LbdFuncConfig()
__lbd_func_config__.apigw_resource_yes = False
__lbd_func_config__.apigw_method_yes = False

def handler(event, context):
    print('Client token: ' + event['authorizationToken'])
    print('Method ARN: ' + event['methodArn'])
    principalId = 'my-organization'
    tmp = event['methodArn'].split(':')
    apiGatewayArnTmp = tmp[5].split('/')
    awsAccountId = tmp[4]
    policy = AuthPolicy(principalId, awsAccountId)
    policy.restApiId = apiGatewayArnTmp[0]
    policy.region = tmp[3]
    policy.stage = apiGatewayArnTmp[1]
    if event['authorizationToken'] == 'allow':
        policy.allowAllMethods()
    else:
        policy.denyAllMethods()
    authResponse = policy.build()
    context = {'key':'value', 
     'number':1, 
     'bool':True}
    authResponse['context'] = context
    return authResponse


handler.__lbd_func_config__ = LbdFuncConfig()
handler.__lbd_func_config__.apigw_authorizer_yes = True

class HttpVerb:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    HEAD = 'HEAD'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'
    ALL = '*'


class AuthPolicy(object):
    awsAccountId = ''
    principalId = ''
    version = '2012-10-17'
    pathRegex = '^[/.a-zA-Z0-9-\\*]+$'
    allowMethods = []
    denyMethods = []
    restApiId = '*'
    region = '*'
    stage = '*'

    def __init__(self, principal, awsAccountId):
        self.awsAccountId = awsAccountId
        self.principalId = principal
        self.allowMethods = []
        self.denyMethods = []

    def _addMethod(self, effect, verb, resource, conditions):
        """Adds a method to the internal lists of allowed or denied methods. Each object in
        the internal list contains a resource ARN and a condition statement. The condition
        statement can be null."""
        if verb != '*':
            if not hasattr(HttpVerb, verb):
                raise NameError('Invalid HTTP verb ' + verb + '. Allowed verbs in HttpVerb class')
            resourcePattern = re.compile(self.pathRegex)
            if not resourcePattern.match(resource):
                raise NameError('Invalid resource path: ' + resource + '. Path should match ' + self.pathRegex)
            if resource[:1] == '/':
                resource = resource[1:]
        else:
            resourceArn = 'arn:aws:execute-api:{}:{}:{}/{}/{}/{}'.format(self.region, self.awsAccountId, self.restApiId, self.stage, verb, resource)
            if effect.lower() == 'allow':
                self.allowMethods.append({'resourceArn':resourceArn, 
                 'conditions':conditions})
            elif effect.lower() == 'deny':
                self.denyMethods.append({'resourceArn':resourceArn, 
                 'conditions':conditions})

    def _getEmptyStatement(self, effect):
        """Returns an empty statement object prepopulated with the correct action and the
        desired effect."""
        statement = {'Action':'execute-api:Invoke', 
         'Effect':effect[:1].upper() + effect[1:].lower(), 
         'Resource':[]}
        return statement

    def _getStatementForEffect(self, effect, methods):
        """This function loops over an array of objects containing a resourceArn and
        conditions statement and generates the array of statements for the policy."""
        statements = []
        if len(methods) > 0:
            statement = self._getEmptyStatement(effect)
            for curMethod in methods:
                if curMethod['conditions'] is None or len(curMethod['conditions']) == 0:
                    statement['Resource'].append(curMethod['resourceArn'])
                else:
                    conditionalStatement = self._getEmptyStatement(effect)
                    conditionalStatement['Resource'].append(curMethod['resourceArn'])
                    conditionalStatement['Condition'] = curMethod['conditions']
                    statements.append(conditionalStatement)

            if statement['Resource']:
                statements.append(statement)
        return statements

    def allowAllMethods(self):
        """Adds a '*' allow to the policy to authorize access to all methods of an API"""
        self._addMethod('Allow', HttpVerb.ALL, '*', [])

    def denyAllMethods(self):
        """Adds a '*' allow to the policy to deny access to all methods of an API"""
        self._addMethod('Deny', HttpVerb.ALL, '*', [])

    def allowMethod(self, verb, resource):
        """Adds an API Gateway method (Http verb + Resource path) to the list of allowed
        methods for the policy"""
        self._addMethod('Allow', verb, resource, [])

    def denyMethod(self, verb, resource):
        """Adds an API Gateway method (Http verb + Resource path) to the list of denied
        methods for the policy"""
        self._addMethod('Deny', verb, resource, [])

    def allowMethodWithConditions(self, verb, resource, conditions):
        """Adds an API Gateway method (Http verb + Resource path) to the list of allowed
        methods and includes a condition for the policy statement. More on AWS policy
        conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition"""
        self._addMethod('Allow', verb, resource, conditions)

    def denyMethodWithConditions(self, verb, resource, conditions):
        """Adds an API Gateway method (Http verb + Resource path) to the list of denied
        methods and includes a condition for the policy statement. More on AWS policy
        conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition"""
        self._addMethod('Deny', verb, resource, conditions)

    def build(self):
        """Generates the policy document based on the internal lists of allowed and denied
        conditions. This will generate a policy with two main statements for the effect:
        one statement for Allow and one statement for Deny.
        Methods that includes conditions will have their own statement in the policy."""
        if self.allowMethods is None or len(self.allowMethods) == 0:
            if self.denyMethods is None or len(self.denyMethods) == 0:
                raise NameError('No statements defined for the policy')
        policy = {'principalId':self.principalId,  'policyDocument':{'Version':self.version, 
          'Statement':[]}}
        policy['policyDocument']['Statement'].extend(self._getStatementForEffect('Allow', self.allowMethods))
        policy['policyDocument']['Statement'].extend(self._getStatementForEffect('Deny', self.denyMethods))
        return policy


if __name__ == '__main__':
    event = {'type':'TOKEN',  'authorizationToken':'incoming-client-token', 
     'methodArn':'arn:aws:execute-api:us-east-1:123456789012:example/prod/POST/{proxy+}'}
    policy = handler(event, {})
    print(policy)