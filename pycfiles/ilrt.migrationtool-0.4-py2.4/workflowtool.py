# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ilrt/migrationtool/browser/workflowtool.py
# Compiled at: 2009-04-17 18:09:26
from zope.interface import implements
from zope.component import getUtility
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from ilrt.migrationtool.browser.interfaces import IWorkflowMigrationView

class WorkflowMigrationView(BrowserView):
    """
    Migrates content from one workflow to another via a manually
    tailored mapping implemented as an adjunct to the site migration tool
    """
    __module__ = __name__
    implements(IWorkflowMigrationView)
    _template = ViewPageTemplateFile('templates/manage_workflow.pt')
    _workflows = None
    _mapping = {}

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal = getUtility(ISiteRoot)
        self.workflow_tool = getToolByName(self.portal, 'portal_workflow')
        self.aok = 0
        self.tok = 0
        self.fok = 0

    def __call__(self):
        """ Handle the zmi manage form actions -
            set migration,
            set mapping
            or run migration
        """
        wf_from = self.request.get('wf_from', None)
        wf_to = self.request.get('wf_to', None)
        if wf_from or wf_to:
            out = self.setWorkflowMigration(wf_from, wf_to)
            if out:
                self.request['out'] = out
        states = self.request.get('state', [])
        if states:
            for record in states:
                self._mapping[record['from']] = record['to']

        if self.request.get('run_migration', ''):
            self.resetMsgCounters()
            msg = self.transferObjectsState(wf_from, wf_to, self.getLocale())
            if msg:
                self.request['out'] = msg
            else:
                self.request['out'] = self.migrateMsg(wf_from, wf_to)
        return xhtml_compress(self._template())

    def resetMsgCounters(self):
        """ Reset the counters to zero """
        self.aok = 0
        self.tok = 0
        self.fok = 0

    def migrateMsg(self, wf_from, wf_to):
        """ Generate the message of what the migration has done """
        msg = 'You have migrated %s to %s' % (wf_from, wf_to)
        msg += ' with %s successful transitions,' % str(self.tok)
        msg += ' %s failed transitions' % str(self.fok)
        msg += ' and %s objects already in the right state' % str(self.aok)
        return msg

    def getLocale(self):
        """ Return a folder from a relative path
            Default to the whole portal
        """
        path = self.request.get('locale', '/')
        obj = self.portal
        for part in path.split('/'):
            if part and hasattr(obj, part):
                obj = getattr(obj, part)

        return obj

    @memoize
    def listWorkflows(self):
        """ Return a vocab of id,title dictionarys for the workflows available
        """
        vocab = []
        for wf in self.workflow_tool.items():
            vocab.append({'id': wf[0], 'title': getattr(wf[1], 'title', wf[0])})

        return vocab

    @memoize
    def setWorkflowMigration(self, wf_from, wf_to):
        """
        Set the worflows for the migration
        """
        out = 'The workflows have been selected for mapping.'
        if not wf_from or not wf_to:
            return "<h4>You must select a workflow from each dropdown</h4>                     <p>Please select from the 'from workflow' and 'to workflow'                     dropdowns and resubmit</p>"
        if wf_from == wf_to:
            return "<h4>You do not need to migrate a workflow to itself</h4>                     <p>Please change either the 'from workflow' or                     the 'to workflow' dropdown and resubmit"
        self._workflows = [
         None, None]
        for wf in self.workflow_tool.items():
            if wf_from == wf[0]:
                self._workflows[0] = wf[1]
            elif wf_to == wf[0]:
                self._workflows[1] = wf[1]

        if not self._workflows[0]:
            self._workflows = None
        return

    @memoize
    def getStates(self, wf, id='return vocab'):
        """ Return the states for a workflow as a vocab -
            or if given a state id then that state as a dictionary
        """
        workflow_folder = getattr(self.workflow_tool, wf, None)
        vocab = []
        if workflow_folder:
            state_folder = getattr(workflow_folder, 'states', None)
            if state_folder is not None:
                for state in state_folder.objectValues():
                    if state.id == id:
                        return {'id': state.id, 'title': state.title}
                    vocab.append({'id': state.id, 'title': state.title})

        if id == 'return vocab':
            return vocab
        else:
            return
        return

    @memoize
    def getTransitionStateMap(self, wf):
        """ Return a dictionary mapping the lists of transistions
            required for any possible change from one state to another
            for the supplied worflow id.
        """
        workflow_folder = getattr(self.workflow_tool, wf, None)
        from_trans = {}
        to_trans = {}
        transpath = {}
        if workflow_folder:
            trans_folder = getattr(workflow_folder, 'transitions', None)
            if trans_folder is not None:
                for trans in trans_folder.objectValues():
                    to_state = getattr(trans, 'new_state_id', '')
                    if to_trans.has_key(to_state):
                        to_trans[to_state].add(trans.getId())
                    else:
                        to_trans[to_state] = set([trans.getId()])

                state_folder = getattr(workflow_folder, 'states', None)
                states = []
                for state in state_folder.objectValues():
                    from_trans[state.getId()] = set(getattr(state, 'transitions', []))
                    states.append(state.getId())

                orderedstates = states

                def findStateTrans(end):
                    """ Find a state and transistion that arrives at this
                        end state - ordered states has the from_state first
                        - Use to traverse down transitions needed
                    """
                    for start in orderedstates:
                        intersect = from_trans[start] & to_trans[end]
                        if intersect:
                            return [
                             start, intersect.pop()]

                    return [
                     None, None]

                for from_state in states:
                    orderedstates.remove(from_state)
                    orderedstates.insert(0, from_state)
                    for to_state in states:
                        if from_state != to_state:
                            fromto = from_state + '>' + to_state
                            common = from_trans[from_state] & to_trans[to_state]
                            if common:
                                transpath[fromto] = [
                                 common.pop()]
                            else:
                                end = to_state
                                start = ''
                                depth = 0
                                transpath[fromto] = []
                                while from_state != start:
                                    depth += 1
                                    (start, trans) = findStateTrans(end)
                                    if not start or depth > 10:
                                        raise 'The workflow %wf is broken in that                                                it has states that cannot be transitioned                                                between from any other states' % wf
                                    transpath[fromto].append(trans)
                                    end = start

                                transpath[fromto].reverse()

        return transpath

    @memoize
    def getWorkflowMigration(self):
        """ Return the workflow [from,to] list """
        return self._workflows

    @memoize
    def getStateMapping(self):
        """ Return the mapping of states """
        return self._mapping

    def _runTransfer(self, wf_from, wf_to, mapping, container=None):
        """ Run a transfer directly rather than via the zmi manage forms """
        self._mapping = mapping
        if not container:
            container = self.portal
        msg = self.setWorkflowMigration(wf_from, wf_to)
        if not msg:
            self.resetMsgCounters()
            msg = self.transferObjectsState(wf_from, wf_to, container)
        if not msg:
            msg = self.migrateMsg(wf_from, wf_to)
        return msg

    def transferObjectsState--- This code section failed: ---

 L. 230         0  LOAD_FAST             3  'container'
                3  LOAD_ATTR             1  'objectValues'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            6  'objs'

 L. 231        12  LOAD_FAST             0  'self'
               15  LOAD_ATTR             4  'workflow_tool'
               18  LOAD_ATTR             5  'getWorkflowById'
               21  LOAD_FAST             2  'wf_to'
               24  CALL_FUNCTION_1       1  None
               27  STORE_FAST            8  'workflow'

 L. 232        30  LOAD_CONST               'ilrt.migrationtool migrated state from %s to %s'
               33  LOAD_FAST             1  'wf_from'
               36  LOAD_FAST             2  'wf_to'
               39  BUILD_TUPLE_2         2 
               42  BINARY_MODULO    
               43  STORE_FAST            4  'comment'

 L. 234        46  LOAD_FAST             0  'self'
               49  LOAD_ATTR            10  'getTransitionStateMap'
               52  LOAD_FAST             2  'wf_to'
               55  CALL_FUNCTION_1       1  None
               58  STORE_FAST           10  'transmap'

 L. 235        61  LOAD_FAST            10  'transmap'
               64  JUMP_IF_TRUE          8  'to 75'
             67_0  THEN                     76
               67  POP_TOP          

 L. 236        68  LOAD_CONST               'This workflow has no transitions so must be single state'
               71  RETURN_VALUE     
               72  JUMP_FORWARD          1  'to 76'
             75_0  COME_FROM            64  '64'
               75  POP_TOP          
             76_0  COME_FROM            72  '72'

 L. 237        76  SETUP_LOOP          345  'to 424'
               79  LOAD_FAST             6  'objs'
               82  GET_ITER         
               83  FOR_ITER            337  'to 423'
               86  STORE_FAST           11  'obj'

 L. 238        89  LOAD_FAST             0  'self'
               92  LOAD_ATTR             4  'workflow_tool'
               95  LOAD_ATTR            13  'getInfoFor'
               98  LOAD_FAST            11  'obj'

 L. 239       101  LOAD_CONST               'review_state'
              104  LOAD_CONST               'wf_id'
              107  LOAD_FAST             1  'wf_from'
              110  CALL_FUNCTION_258   258  None
              113  STORE_FAST            5  'from_state'

 L. 240       116  LOAD_FAST             5  'from_state'
              119  JUMP_IF_FALSE       264  'to 386'
              122  POP_TOP          

 L. 241       123  LOAD_FAST             0  'self'
              126  LOAD_ATTR            15  '_mapping'
              129  LOAD_ATTR            16  'get'
              132  LOAD_FAST             5  'from_state'
              135  LOAD_CONST               None
              138  CALL_FUNCTION_2       2  None
              141  STORE_FAST            7  'to_state'

 L. 242       144  LOAD_FAST             7  'to_state'
              147  JUMP_IF_FALSE       232  'to 382'
              150  POP_TOP          

 L. 243       151  LOAD_FAST             0  'self'
              154  LOAD_ATTR             4  'workflow_tool'
              157  LOAD_ATTR            13  'getInfoFor'
              160  LOAD_FAST            11  'obj'

 L. 244       163  LOAD_CONST               'review_state'
              166  LOAD_CONST               'wf_id'
              169  LOAD_FAST             2  'wf_to'
              172  CALL_FUNCTION_258   258  None
              175  STORE_FAST            9  'current_state'

 L. 245       178  LOAD_FAST             9  'current_state'
              181  LOAD_FAST             7  'to_state'
              184  COMPARE_OP            3  !=
              187  JUMP_IF_FALSE       173  'to 363'
              190  POP_TOP          

 L. 246       191  SETUP_LOOP          185  'to 379'
              194  LOAD_FAST            10  'transmap'
              197  LOAD_FAST             9  'current_state'
              200  LOAD_CONST               '>'
              203  BINARY_ADD       
              204  LOAD_FAST             7  'to_state'
              207  BINARY_ADD       
              208  BINARY_SUBSCR    
              209  GET_ITER         
              210  FOR_ITER            146  'to 359'
              213  STORE_FAST           12  'trans'

 L. 247       216  LOAD_FAST             0  'self'
              219  LOAD_ATTR            21  '_tryTransition'
              222  LOAD_CONST               'workflow'
              225  LOAD_FAST             8  'workflow'

 L. 248       228  LOAD_CONST               'obj'
              231  LOAD_FAST            11  'obj'

 L. 249       234  LOAD_CONST               'transition'
              237  LOAD_FAST            12  'trans'

 L. 250       240  LOAD_CONST               'comment'
              243  LOAD_FAST             4  'comment'
              246  CALL_FUNCTION_1024  1024  None
              249  JUMP_IF_FALSE        19  'to 271'
              252  POP_TOP          

 L. 251       253  LOAD_FAST             0  'self'
              256  DUP_TOP          
              257  LOAD_ATTR            22  'tok'
              260  LOAD_CONST               1
              263  INPLACE_ADD      
              264  ROT_TWO          
              265  STORE_ATTR           22  'tok'
              268  JUMP_FORWARD         16  'to 287'
            271_0  COME_FROM           249  '249'
              271  POP_TOP          

 L. 253       272  LOAD_FAST             0  'self'
              275  DUP_TOP          
              276  LOAD_ATTR            23  'fok'
              279  LOAD_CONST               1
              282  INPLACE_ADD      
              283  ROT_TWO          
              284  STORE_ATTR           23  'fok'
            287_0  COME_FROM           268  '268'

 L. 254       287  LOAD_FAST             0  'self'
              290  LOAD_ATTR             4  'workflow_tool'
              293  LOAD_ATTR            13  'getInfoFor'
              296  LOAD_FAST            11  'obj'

 L. 255       299  LOAD_CONST               'review_state'
              302  LOAD_CONST               'wf_id'
              305  LOAD_FAST             2  'wf_to'
              308  CALL_FUNCTION_258   258  None
              311  LOAD_FAST             9  'current_state'
              314  COMPARE_OP            2  ==
              317  JUMP_IF_FALSE        35  'to 355'
              320  POP_TOP          

 L. 256       321  LOAD_CONST               'Unable to translate %s to %s'
              324  LOAD_CONST               '/'
              327  LOAD_ATTR            24  'join'
              330  LOAD_FAST            11  'obj'
              333  LOAD_ATTR            25  'getPhysicalPath'
              336  CALL_FUNCTION_0       0  None
              339  CALL_FUNCTION_1       1  None
              342  LOAD_FAST             7  'to_state'
              345  BUILD_TUPLE_2         2 
              348  BINARY_MODULO    
              349  RAISE_VARARGS_1       1  None
              352  JUMP_BACK           210  'to 210'
            355_0  COME_FROM           317  '317'
              355  POP_TOP          
              356  JUMP_BACK           210  'to 210'
              359  POP_BLOCK        
              360  JUMP_ABSOLUTE       383  'to 383'
            363_0  COME_FROM           187  '187'
              363  POP_TOP          

 L. 259       364  LOAD_FAST             0  'self'
              367  DUP_TOP          
              368  LOAD_ATTR            26  'aok'
              371  LOAD_CONST               1
              374  INPLACE_ADD      
              375  ROT_TWO          
              376  STORE_ATTR           26  'aok'
            379_0  COME_FROM           191  '191'
              379  JUMP_ABSOLUTE       387  'to 387'
            382_0  COME_FROM           147  '147'
              382  POP_TOP          
              383  JUMP_FORWARD          1  'to 387'
            386_0  COME_FROM           119  '119'
              386  POP_TOP          
            387_0  COME_FROM           383  '383'

 L. 260       387  LOAD_FAST            11  'obj'
              390  LOAD_ATTR            27  'isPrincipiaFolderish'
              393  JUMP_IF_FALSE        23  'to 419'
              396  POP_TOP          

 L. 261       397  LOAD_FAST             0  'self'
              400  LOAD_ATTR            28  'transferObjectsState'
              403  LOAD_FAST             1  'wf_from'
              406  LOAD_FAST             2  'wf_to'
              409  LOAD_FAST            11  'obj'
              412  CALL_FUNCTION_3       3  None
              415  POP_TOP          
              416  JUMP_BACK            83  'to 83'
            419_0  COME_FROM           393  '393'
              419  POP_TOP          
              420  JUMP_BACK            83  'to 83'
              423  POP_BLOCK        
            424_0  COME_FROM            76  '76'

 L. 262       424  LOAD_CONST               None
              427  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 379

    def _tryTransition(self, workflow, obj, transition, comment):
        """Try to perform a workflow transition on the object,
           returns true on success
        """
        if workflow:
            tdef = workflow.transitions.get(transition, None)
            if tdef:
                try:
                    workflow._executeTransition(obj, tdef=tdef, kwargs={'comment': comment})
                    catalog = getToolByName(self.portal, 'portal_catalog')
                    catalog.reindexObject(obj, idxs=['review_state', 'allowedRolesAndUsers'])
                    return True
                except:
                    return False

        return False