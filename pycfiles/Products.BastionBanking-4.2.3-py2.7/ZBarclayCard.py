# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/Merchants/BarclayCard/ZBarclayCard.py
# Compiled at: 2015-07-18 19:38:10
import os, AccessControl
from AccessControl import ClassSecurityInfo
from App.ImageFile import ImageFile
from Shared.DC.Scripts.Script import defaultBindings
from Shared.DC.Scripts.Signature import FuncCode
from Products.PythonScripts.PythonScript import PythonScript
from Products.BastionBanking.interfaces.BastionMerchantInterface import IBastionMerchant
from OFS.ObjectManager import ObjectManager
from OFS.PropertyManager import PropertyManager
from OFS.SimpleItem import SimpleItem
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
import returncode
from Products.BastionBanking.ZCurrency import CURRENCIES
from Products.BastionBanking.ZCreditCard import ZCreditCard
from Products.BastionBanking.BastionPayment import BastionPayment
from zope.interface import implements
try:
    from Products.PerlExternalMethod import PerlExtMethod, FuncCode

    class MPIAgent(PerlExtMethod):
        """
        we've invoked a perl module to take care of the https connection
        because httplib doesn't seem very well behaved.  We could possibly use
        something like cryptlib to keep this pure Python ..   
        """
        id = title = meta_type = 'MPIAgent'

        def __init__(self):
            self.module = 'MPI'
            self.function = 'send'
            self.func_code = FuncCode(open(os.path.join(os.path.dirname(__file__), 'MPI.pm')).read())


    mpi_send = MPIAgent()
except ImportError:
    mpi_send = None

preauth = '<EngineDocList xmlns:tal="http://xml.zope.org/namespaces/tal">\n <DocVersion>1.0</DocVersion>\n <EngineDoc>\n  <ContentType>OrderFormDoc</ContentType>\n  <User>\n   <Name tal:content="here/username"/>\n   <Password tal:content="here/password"/>\n   <ClientId DataType="S32"><span tal:replace="here/clientid"/></ClientId>\n  </User>\n  <Instructions>\n   <Pipeline>PaymentNoFraud</Pipeline>\n  </Instructions>\n  <OrderFormDoc>\n   <Mode>P</Mode>\n   <Comments/>\n   <Consumer>\n    <Email/>\n    <PaymentMech>\n     <CreditCard>\n      <Number tal:content="request/card">4111111111111111</Number>\n      <Expires DataType="ExpirationDate" Locale="826">\n        <span tal:replace="request/expiry_mm"/>/<span tal:replace="request/expiry_yy"/>\n      </Expires>\n     </CreditCard>\n    </PaymentMech>\n   </Consumer>\n   <Transaction>\n    <Type>Auth</Type>\n    <CurrentTotals>\n     <Totals>\n      <Total DataType="Money" ZCurrency="826"\n             tal:attributes="currency here/currencycode">\n       <span tal:replace="python: float(request[\'amount\']) * 100">removed (implied) decimal place...</span>\n      </Total>\n     </Totals>\n    </CurrentTotals>\n   </Transaction>\n  </OrderFormDoc>\n </EngineDoc>\n</EngineDocList>'
form = '\n<img src="" height="35" width="80" valign="bottom"\n     tal:attributes="src string:${request/BASEPATH1}/${container/icon}"/>&nbsp;&nbsp;\n<select name="type">\n   <option tal:repeat="type python: (\'VISA\', \'Delta\', \'Mastercard\', \'JCB\')"\n           tal:content="type"/>\n</select>\n<span class="form-label">Number</span>&nbsp;\n<input type="text" size="16" name="card">&nbsp;&nbsp;\n<span class="form-label">Expires</span>&nbsp;\n<strong>&nbsp;/&nbsp;</strong>\n<select name="expiry:list:int" tal:define="year python: DateTime().year()">\n    <option tal:repeat="yy python: range(0, 4)" tal:content="python: year + yy"/>\n</select>\n<select name="expiry:list:int">\n    <option tal:repeat="mm python: range(1, 13)" tal:content="python: \'%02d\' % mm"/>\n</select>\n<input type="hidden" name="expiry:list:int" value="1"/>\n'

class ZBarclayCard(ObjectManager, PropertyManager, PythonScript):
    """
    Heh - this is kind of complicated - but we want this class to behave like a PythonScript
    because we want to recycle the testing functionality.  But we (i) don't want to edit
    the script - that would breach security; (ii) want to not have to recompile the function
    that is actually file-resident here...

    So, we just trick PythonScript into using the function by setting _v_f ...
    """
    meta_type = 'ZBarclayCard'
    implements(IBastionMerchant)
    _security = ClassSecurityInfo()
    _reserved_names = ('mpi_preauth', )
    icon = 'Merchants/www/barclaycard.gif'
    ePDQ = ImageFile('www/epdq.gif', globals())
    _params = 'card,expiry_yy,expiry_mm,amount'
    manage_options = ({'label': 'Configuration', 'action': 'manage_propertiesForm'}, {'label': 'Advanced', 'action': 'manage_main'}, {'label': 'Test', 'action': 'ZScriptHTML_tryForm'}) + SimpleItem.manage_options
    manage_propertiesForm = PageTemplateFile('zpt/properties', globals())
    _properties = ({'id': 'username', 'type': 'string', 'mode': 'w'}, {'id': 'password', 'type': 'string', 'mode': 'w'}, {'id': 'clientid', 'type': 'string', 'mode': 'w'}, {'id': 'chargetype', 'type': 'string', 'mode': 'w'}, {'id': 'currencycode', 'type': 'string', 'mode': 'w'}, {'id': 'parameters', 'type': 'string', 'mode': 'w'})

    def __setstate__(self, state):
        ZBarclayCard.inheritedAttribute('__setstate__')(self, state)
        self._v_f = self._pay

    def __init__(self, id):
        self.id = id
        self.manage_edit('ZBarclayCard - ePDQ', '', '', '', '', '')
        self.ZBindings_edit(defaultBindings)
        self._setObject('mpi_preauth', ZopePageTemplate('mpi_preauth', preauth))
        self.mpi_preauth.content_type = 'text/xml'
        self._setObject('widget', ZopePageTemplate('widget', form))
        self._v_f = self._pay

    def _generateBastionPayment(self, id, amount, ref, REQUEST):
        """
        this should agree with stuff in our form (excepting amount) ...
        """
        payee = ZCreditCard(REQUEST['card'], DateTime('%s/%s/01' % (REQUEST['expiry'][0], REQUEST['expiry'][1])), REQUEST['type'])
        return BastionPayment(id, payee, amount, ref)

    def _pay(self, payment, REQUEST=None):
        """
        """
        request = {'card': payment.payee.number, 'expiry_yy': payment.payee.expiry.year(), 
           'expiry_mm': payment.payee.expiry.month(), 
           'amount': payment.amount.amount()}
        id, total, rc, severity, msg, content = mpi_send(self.mpi_preauth(request))
        if REQUEST:
            REQUEST.RESPONSE.setHeader('Content-Type', 'text/html')
        try:
            if int(severity) >= 100:
                return returncode.returncode(id, amount, rc, returncode.ERROR, msg, content)
        except:
            pass

        if int(severity) >= 5:
            return returncode.returncode(id, amount, rc, returncode.ERROR, msg, content)
        return returncode.returncode(id, amount, rc, returncode.OK, msg, content)

    def manage_edit(self, title, username, password, clientid, chargetype, currencycode, REQUEST=None):
        """ """
        self.title = title
        self.username = username
        self.password = password
        self.clientid = clientid
        self.chargetype = chargetype
        self.currencycode = currencycode
        if REQUEST:
            REQUEST.set('management_view', 'Properties')
            REQUEST.set('manage_tabs_message', 'Properties Updated')
            return self.manage_propertiesForm(self, REQUEST)

    def manage_test_preauth(self, REQUEST):
        """ just in case something really f**ked is going on with the XML stuff ...
        """
        return self.mpi_preauth(REQUEST)

    def _refund(self, payment, ref, REQUEST=None):
        raise NotYetImplemented

    def supportedCurrencies(self):
        return CURRENCIES


AccessControl.class_init.InitializeClass(ZBarclayCard)