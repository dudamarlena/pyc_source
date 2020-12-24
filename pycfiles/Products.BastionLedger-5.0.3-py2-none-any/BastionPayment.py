# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/BastionPayment.py
# Compiled at: 2015-07-18 19:38:10
import AccessControl, transaction
from Acquisition import aq_base
from AccessControl.Permissions import access_contents_information, view_management_screens
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Permissions import operate_bastionbanking
from PortalContent import PortalContent
from Products.ATContentTypes.content.folder import ATBTreeFolder as BTreeFolder2
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
import ZReturnCode

class BastionPayment(PortalContent):
    """
    Contains a payment request and provides the basis for the Payment
    Workflow Engine
    """
    meta_type = portal_type = 'BastionPayment'
    icon = 'misc_/BastionBanking/payment'
    gateway = ''
    __ac_permissions__ = PortalContent.__ac_permissions__ + (
     (
      view_management_screens, ('manage_payee', )),
     (
      access_contents_information,
      ('getReturnCodes', 'referenceObject', 'getRemoteRef', 'getTransactionRef', 'number')),
     (
      operate_bastionbanking,
      ('manage_changeStatus', 'setReference', 'setReferenceObject', 'setRemoteRef', 'setTransactionRef')))
    _properties = ({'id': 'gateway', 'type': 'string', 'mode': 'r'}, {'id': 'submitted', 'type': 'date', 'mode': 'r'}, {'id': 'amount', 'type': 'currency', 'mode': 'r'}, {'id': 'reference', 'type': 'string', 'mode': 'w'}, {'id': 'remote_ref', 'type': 'tokens', 'mode': 'w'})
    manage_options = ({'label': 'History', 'action': 'manage_main'}, {'label': 'Payee', 'action': 'manage_payee'}) + PortalContent.manage_options
    manage_main = PageTemplateFile('zpt/returncodes', globals())

    def manage_payee(self, REQUEST):
        """
        """
        REQUEST.RESPONSE.redirect('payee/manage_workspace')

    def __init__(self, id, payee, amount, reference=''):
        self.id = id
        self.gateway = ''
        self.submitted = DateTime()
        self.payee = payee
        self.amount = amount
        self.reference = reference
        self.remote_ref = ()
        self.returncodes = BTreeFolder2('returncodes')

    def _setReturnCode(self, rc):
        """ set a returncode for a payment request """
        id = self.returncodes.generateId()
        self.returncodes._setObject(id, ZReturnCode.ZReturnCode(id, rc.reference, rc.amount, rc.returncode, rc.severity, rc.message, rc.response))
        transaction.get().commit()
        return self.returncodes._getOb(id)

    def returncode(self):
        """ the last return code """
        rcs = self.returncodes.objectValues()
        if rcs:
            return rcs[(-1)]
        else:
            return

    def getReturnCodes(self):
        """
        return all return codes (from all remote ops regarding this payment)
        """
        return self.returncodes.objectItems()

    def manage_changeStatus(self, action, wfid='', REQUEST=None):
        """
        do a workflow transition from the ZMI
        """
        wftool = getToolByName(self, 'portal_workflow')
        wftool.doActionFor(self, action, wfid or 'bastionpayment_workflow')
        cat = self.aq_parent
        cat.uncatalog_object(self)
        cat.catalog_object(self)
        if REQUEST:
            return self.manage_main(self, REQUEST)

    def setReference(self, ref):
        """
        Allow post-payment reference setting
        """
        if not self.reference:
            self.reference = ref
        self.reindexObject()

    def setReferenceObject(self, obj):
        """
        set the reference as the path to associated object
        """
        if not self.reference:
            self.reference = ('/').join(obj.getPhysicalPath())
        self.reindexObject()

    def referenceObject(self):
        """
        if the reference is a path, get the object ...
        """
        if self.reference:
            try:
                return self.getPhysicalRoot().unrestrictedTraverse(self.reference)
            except:
                pass

        return

    def setRemoteRef(self, ref):
        """
        append ref to remote references chain (if not already present) and do
        a database commit as this IS very important ...
        """
        if ref in self.remote_ref:
            return
        self._updateProperty('remote_ref', self.remote_ref + (ref,))
        transaction.get().commit()

    def getRemoteRef(self):
        """
        return the last remote ref in the chain (or none)
        """
        rref = self.remote_ref
        if len(rref):
            return rref[(-1)]
        return ''

    def getRemoteInfo(self):
        """
        call the underlying service to get their data about this payment
        """
        return self.aq_parent.service.getTransaction(self)

    def setTransactionRef(self, txn):
        """
        if you've a BLTransaction associated with this, then we can save
        it here
        """
        assert txn.meta_type in ('BLTransaction', 'BLSubsidiaryTransaction'), 'Not a BLTransaction: %s' % txn.meta_type
        self._txn_ref = ('/').join(txn.getPhysicalPath())

    def getTransactionRef(self):
        """
        return any BLTransaction associated with this payment
        """
        ref = getattr(aq_base(self), '_txn_ref', '')
        if ref:
            return self.getPhysicalRoot().unrestrictedTraverse(ref)
        else:
            return

    def manage_beforeDelete(self, item, container):
        """
        uncatalog myself
        """
        cat = self.aq_parent
        for rc in self.returncodes.objectValues():
            cat.uncatalog_object(('/').join(rc.getPhysicalPath()))

        cat.uncatalog_object(('/').join(self.getPhysicalPath()))

    def reconcile(self):
        """
        debug/helper which returns whether or not this payment is reconciled
        """
        return self.aq_parent.service._reconcile(self)

    def number(self):
        """
        indexing
        """
        payee = self.payee
        if payee and payee.number:
            return payee.number
        raise AttributeError, 'number'


AccessControl.class_init.InitializeClass(BastionPayment)