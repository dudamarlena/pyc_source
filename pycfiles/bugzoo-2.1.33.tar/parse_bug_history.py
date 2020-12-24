# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\bzETL\parse_bug_history.py
# Compiled at: 2013-12-18 17:03:15
import re, math
from bzETL.util import struct, strings
from bzETL.util.struct import nvl
from bzETL.util.multiset import Multiset
from transform_bugzilla import normalize, NUMERIC_FIELDS, MULTI_FIELDS
from bzETL.util.cnv import CNV
from bzETL.util.logs import Log
from bzETL.util.queries import Q
from bzETL.util.struct import Struct, Null
from bzETL.util.files import File
from bzETL.util.maths import Math
FLAG_PATTERN = re.compile('^(.*)([?+-])(\\([^)]*\\))?$')
DEBUG_CHANGES = False
DEBUG_STATUS = False
TRUNC_FIELDS = [
 'cc', 'blocked', 'dependson', 'keywords']
KNOWN_MISSING_KEYWORDS = {
 'dogfood', 'beta1', 'nsbeta1', 'nsbeta2', 'nsbeta3', 'patch', 'mozilla1.0', 'correctness',
 'mozilla0.9', 'mozilla0.9.9+', 'nscatfood', 'mozilla0.9.3', 'fcc508', 'nsbeta1+', 'mostfreq'}
STOP_BUG = 999999999
MAX_TIME = 9999999999000

class BugHistoryParser:

    def __init__(self, settings, output_queue):
        self.aliases = Null
        self.startNewBug(struct.wrap({'bug_id': 0, 'modified_ts': 0, '_merge_order': 1}))
        self.prevActivityID = Null
        self.prev_row = Null
        self.settings = settings
        self.output = output_queue
        self.initializeAliases()

    def processRow(self, row_in):
        if len(row_in.items()) == 0:
            return
        else:
            try:
                try:
                    self.currBugID = row_in.bug_id
                    if self.settings.debug:
                        Log.note('process row: {{row}}', {'row': row_in})
                    if self.prevBugID < self.currBugID:
                        if self.prevBugID > 0:
                            if DEBUG_STATUS:
                                Log.note('Emitting intermediate versions for {{bug_id}}', {'bug_id': self.prevBugID})
                            self.populateIntermediateVersionObjects()
                        if row_in.bug_id == STOP_BUG:
                            return
                        self.startNewBug(row_in)
                    if row_in.field_name in TRUNC_FIELDS:
                        added = CNV.value2string(row_in.new_value)
                        removed = CNV.value2string(row_in.old_value)
                        uncertain = False
                        if added in ('? ?', '?'):
                            uncertain = True
                            Log.note('PROBLEM Encountered uncertain added value.  Skipping.')
                            row_in.new_value = Null
                        elif added != None and added.startswith('? '):
                            uncertain = True
                            row_in.new_value = added[2:]
                        if removed in ('? ?', '?'):
                            uncertain = True
                            Log.note('PROBLEM Encountered uncertain removed value.  Skipping.')
                            row_in.old_value = Null
                        elif removed != None and removed.startswith('? '):
                            uncertain = True
                            row_in.old_value = removed[2:]
                        if uncertain and self.currBugState.uncertain == None:
                            Log.note('PROBLEM Setting this bug to be uncertain.')
                            self.processBugsActivitiesTableItem(struct.wrap({'modified_ts': row_in.modified_ts, 
                               'modified_by': row_in.modified_by, 
                               'field_name': 'uncertain', 
                               'new_value': Null, 
                               'old_value': '1', 
                               'attach_id': Null}))
                            if row_in.new_value == None and row_in.old_value == None:
                                Log.note('Nothing added or removed. Skipping update.')
                                return
                    new_value = CNV.value2int(row_in.new_value) if row_in.field_name.endswith('_ts') else row_in.new_value
                    if row_in._merge_order == 1:
                        self.processSingleValueTableItem(row_in.field_name, new_value)
                    elif row_in._merge_order == 2:
                        self.processMultiValueTableItem(row_in.field_name, new_value)
                    elif row_in._merge_order == 7:
                        self.processAttachmentsTableItem(row_in)
                    elif row_in._merge_order == 8:
                        self.processFlagsTableItem(row_in)
                    elif row_in._merge_order == 9:
                        self.processBugsActivitiesTableItem(row_in)
                    else:
                        Log.warning("Unhandled merge_order: '" + row_in._merge_order + "'")
                except Exception as e:
                    Log.warning('Problem processing row: {{row}}', {'row': row_in}, e)

            finally:
                if row_in._merge_order > 1 and self.currBugState.created_ts == None:
                    Log.note('PROBLEM expecting a created_ts (did you install the timezone database into your MySQL instance?)')
                for b in self.currBugState.blocked:
                    if isinstance(b, basestring):
                        Log.note('PROBLEM error')

                self.prev_row = row_in

            return

    @staticmethod
    def uid(bug_id, modified_ts):
        if modified_ts == None:
            Log.error('modified_ts can not be Null')
        return unicode(bug_id) + '_' + unicode(modified_ts)[0:-3]

    def startNewBug(self, row_in):
        self.prevBugID = row_in.bug_id
        self.bugVersions = []
        self.bugVersionsMap = Struct()
        self.currActivity = Struct()
        self.currBugAttachmentsMap = Struct()
        self.currBugState = Struct(_id=BugHistoryParser.uid(row_in.bug_id, row_in.modified_ts), bug_id=row_in.bug_id, modified_ts=row_in.modified_ts, modified_by=row_in.modified_by, reported_by=row_in.modified_by, attachments=[])
        for f in MULTI_FIELDS:
            self.currBugState[f] = set([])

        self.currBugState.flags = []
        if row_in._merge_order != 1:
            Log.warning('Current bugs table record not found for bug_id: {{bug_id}}  (merge order should have been 1, but was {{start_time}})', row_in)

    def processSingleValueTableItem(self, field_name, new_value):
        self.currBugState[field_name] = new_value

    def processMultiValueTableItem(self, field_name, new_value):
        if field_name in NUMERIC_FIELDS:
            new_value = int(new_value)
        try:
            self.currBugState[field_name].add(new_value)
            return Null
        except Exception as e:
            Log.warning('Unable to push {{value}} to array field {{start_time}} on bug {{curr_value}} current value: {{curr_value}}', {'value': new_value, 
               'field': field_name, 
               'bug_id': self.currBugID, 
               'curr_value': self.currBugState[field_name]}, e)

    def processAttachmentsTableItem(self, row_in):
        currActivityID = BugHistoryParser.uid(self.currBugID, row_in.modified_ts)
        if currActivityID != self.prevActivityID:
            self.prevActivityID = currActivityID
            self.currActivity = Struct(_id=currActivityID, modified_ts=row_in.modified_ts, modified_by=row_in.modified_by, changes=[
             {'field_name': 'attachment_added', 
                'attach_id': row_in.attach_id}])
            self.bugVersions.append(self.currActivity)
            self.bugVersionsMap[currActivityID] = self.currActivity
        att = self.currBugAttachmentsMap[unicode(row_in.attach_id)]
        if att == None:
            att = {'attach_id': row_in.attach_id, 'modified_ts': row_in.modified_ts, 
               'created_ts': row_in.created_ts, 
               'modified_by': row_in.modified_by, 
               'flags': []}
            self.currBugAttachmentsMap[unicode(row_in.attach_id)] = att
        att['created_ts'] = Math.min([row_in.modified_ts, att['created_ts']])
        if row_in.field_name == 'created_ts' and row_in.new_value == None:
            pass
        else:
            att[row_in.field_name] = row_in.new_value
        return

    def processFlagsTableItem(self, row_in):
        flag = self.makeFlag(row_in.new_value, row_in.modified_ts, row_in.modified_by)
        if row_in.attach_id != None:
            if self.currBugAttachmentsMap[unicode(row_in.attach_id)] == None:
                Log.note('Unable to find attachment {{attach_id}} for bug_id {{bug_id}}', {'attach_id': row_in.attach_id, 
                   'bug_id': self.currBugID})
            else:
                if self.currBugAttachmentsMap[unicode(row_in.attach_id)].flags == None:
                    Log.error('should never happen')
                self.currBugAttachmentsMap[unicode(row_in.attach_id)].flags.append(flag)
        else:
            self.currBugState.flags.append(flag)
        return

    def processBugsActivitiesTableItem(self, row_in):
        if self.currBugState.created_ts == None:
            Log.error('must have created_ts')
        if row_in.field_name == 'flagtypes_name':
            row_in.field_name = 'flags'
        multi_field_new_value = self.getMultiFieldValue(row_in.field_name, row_in.new_value)
        multi_field_old_value = self.getMultiFieldValue(row_in.field_name, row_in.old_value)
        currActivityID = BugHistoryParser.uid(self.currBugID, row_in.modified_ts)
        if currActivityID != self.prevActivityID:
            self.currActivity = self.bugVersionsMap[currActivityID]
            if self.currActivity == None:
                self.currActivity = Struct(_id=currActivityID, modified_ts=row_in.modified_ts, modified_by=row_in.modified_by, changes=[])
                self.bugVersions.append(self.currActivity)
            self.prevActivityID = currActivityID
        if row_in.attach_id != None:
            attachment = self.currBugAttachmentsMap[unicode(row_in.attach_id)]
            if attachment == None:
                Log.note('PROBLEM Unable to find attachment {{attach_id}} for bug_id {{start_time}}: {{start_time}}', {'attach_id': row_in.attach_id, 
                   'bug_id': self.currBugID, 
                   'attachments': self.currBugAttachmentsMap})
                self.currActivity.changes.append({'field_name': row_in.field_name, 
                   'new_value': row_in.new_value, 
                   'old_value': row_in.old_value, 
                   'attach_id': row_in.attach_id})
            elif row_in.field_name in MULTI_FIELDS:
                total = attachment[row_in.field_name]
                total = self.removeValues(total, multi_field_new_value, 'added', row_in.field_name, 'attachment', attachment, row_in.modified_ts)
                total = self.addValues(total, multi_field_old_value, 'removed attachment', row_in.field_name, attachment)
                attachment[row_in.field_name] = total
            else:
                attachment[row_in.field_name] = row_in.old_value
                self.currActivity.changes.append({'field_name': row_in.field_name, 
                   'new_value': row_in.new_value, 
                   'old_value': row_in.old_value, 
                   'attach_id': row_in.attach_id})
        elif row_in.field_name in MULTI_FIELDS:
            total = self.currBugState[row_in.field_name]
            total = self.removeValues(total, multi_field_new_value, 'added', row_in.field_name, 'currBugState', self.currBugState, row_in.modified_ts)
            total = self.addValues(total, multi_field_old_value, 'removed bug', row_in.field_name, self.currBugState)
            self.currBugState[row_in.field_name] = total
        else:
            self.currBugState[row_in.field_name] = row_in.old_value
            self.currActivity.changes.append({'field_name': row_in.field_name, 
               'new_value': row_in.new_value, 
               'old_value': row_in.old_value, 
               'attach_id': row_in.attach_id})
        return

    def populateIntermediateVersionObjects(self):
        self.bugVersions = Q.sort(self.bugVersions, [{'field': 'modified_ts', 'sort': -1}])
        prevValues = {}
        currVersion = Null
        nextVersion = Struct(_id=self.currBugState._id, changes=[])
        flagMap = {}
        self.bug_version_num = 1
        while self.bugVersions or nextVersion != None:
            try:
                currVersion = nextVersion
                if self.bugVersions:
                    try:
                        nextVersion = self.bugVersions.pop()
                    except Exception as e:
                        Log.error('problem', e)

                else:
                    nextVersion = Null
                if DEBUG_STATUS:
                    Log.note('Populating JSON for version {{id}}', {'id': currVersion._id})
                mergeBugVersion = False
                if nextVersion != None and currVersion._id == nextVersion._id:
                    if DEBUG_STATUS:
                        Log.note('Merge mode: activated ' + self.currBugState._id)
                    mergeBugVersion = True
                if nextVersion != None:
                    if DEBUG_STATUS:
                        Log.note('We have a nextVersion: {{timestamp}} (ver {{next_version}})', {'timestamp': nextVersion.modified_ts, 
                           'next_version': self.bug_version_num + 1})
                    self.currBugState.expires_on = nextVersion.modified_ts
                else:
                    if DEBUG_STATUS:
                        Log.note('Last bug_version_num = {{version}}', {'version': self.bug_version_num})
                    self.currBugState.expires_on = MAX_TIME
                for propName, propValue in currVersion.items():
                    self.currBugState[propName] = propValue

                changes = Q.sort(currVersion.changes, ['attach_id', 'field_name', {'field': 'old_value', 'sort': -1}, 'new_value'])
                currVersion.changes = changes
                self.currBugState.changes = changes
                for c, change in enumerate(changes):
                    if c + 1 < len(changes):
                        next = changes[(c + 1)]
                        if change.attach_id == next.attach_id and change.field_name == next.field_name and change.old_value != None and next.old_value == None:
                            next.old_value = change.old_value
                            changes[c] = Null
                            continue
                        if change.new_value == None and change.old_value == None and change.field_name != 'attachment_added':
                            changes[c] = Null
                            continue
                    if DEBUG_CHANGES:
                        'Processing change: ' + CNV.object2JSON(change)
                    target = self.currBugState
                    targetName = 'currBugState'
                    attach_id = change.attach_id
                    if attach_id != None:
                        if change.field_name == 'attachment_added':
                            att = self.currBugAttachmentsMap[unicode(attach_id)]
                            self.currBugState.attachments.append(att)
                            continue
                        else:
                            target = self.currBugAttachmentsMap[unicode(attach_id)]
                            targetName = 'attachment'
                            if target == None:
                                Log.warning('Encountered a change to missing attachment for bug {{bug_id}}: {{change}}', {'bug_id': self.currBugState['bug_id'], 
                                   'change': change})
                                target = self.currBugState
                                targetName = 'currBugState'
                    if change.field_name == 'flags':
                        self.processFlagChange(target, change, currVersion.modified_ts, currVersion.modified_by)
                    elif change.field_name in MULTI_FIELDS:
                        a = target[change.field_name]
                        multi_field_value = BugHistoryParser.getMultiFieldValue(change.field_name, change.new_value)
                        multi_field_value_removed = BugHistoryParser.getMultiFieldValue(change.field_name, change.old_value)
                        a = self.removeValues(a, multi_field_value_removed, 'removed', change.field_name, targetName, target, currVersion.modified_ts)
                        a = self.addValues(a, multi_field_value, 'added', change.field_name, target)
                        target[change.field_name] = a
                    else:
                        if target[change.field_name] != change.new_value:
                            self.setPrevious(target, change.field_name, target[change.field_name], currVersion.modified_ts)
                        target[change.field_name] = change.new_value

                self.currBugState.bug_version_num = self.bug_version_num
                if not mergeBugVersion:
                    self.bug_version_num += 1
                    if self.currBugState.expires_on >= self.settings.start_time:
                        state = normalize(self.currBugState)
                        if state.blocked != None and len(state.blocked) == 1 and 'Null' in state.blocked:
                            Log.note("ERROR: state.blocked has 'Null'!  Programming error!")
                        if DEBUG_STATUS:
                            Log.note('Bug {{bug_state.bug_id}} v{{bug_state.bug_version_num}} (id = {{bug_state.id}})', {'bug_state': state})
                        self.output.add({'id': state.id, 'value': state})
                    elif DEBUG_STATUS:
                        Log.note('Not outputting {{_id}} - it is before self.start_time ({{start_time|datetime}})', {'_id': self.currBugState._id, 
                           'start_time': self.settings.start_time})
                elif DEBUG_STATUS:
                    Log.note('Merging a change with the same timestamp = {{bug_state._id}}: {{bug_state}}', {'bug_state': currVersion})
            finally:
                if self.currBugState.blocked == None:
                    Log.note('expecting a created_ts')

        return

    def findFlag(self, flag_list, flag):
        for f in flag_list:
            if f.value == flag.value:
                return f
            if f.request_type == flag.request_type and f.request_status == flag.request_status and self.alias(f.requestee) == self.alias(flag.requestee):
                Log.note("Using bzAliases to match change '" + flag.value + "' to '" + f.value + "'")
                return f

        return Null

    def processFlagChange(self, target, change, modified_ts, modified_by, reverse=False):
        if target.flags == None:
            Log.note("PROBLEM  processFlagChange called with unset 'flags'")
            target.flags = []
        addedFlags = BugHistoryParser.getMultiFieldValue('flags', change.new_value)
        removedFlags = BugHistoryParser.getMultiFieldValue('flags', change.old_value)
        if reverse:
            addedFlags, removedFlags = removedFlags, addedFlags
        for flagStr in removedFlags:
            if flagStr == '':
                continue
            removed_flag = BugHistoryParser.makeFlag(flagStr, modified_ts, modified_by)
            existingFlag = self.findFlag(target.flags, removed_flag)
            if existingFlag != None:
                existingFlag['previous_modified_ts'] = existingFlag['modified_ts']
                existingFlag['modified_ts'] = modified_ts
                if existingFlag['modified_by'] != modified_by:
                    existingFlag['previous_modified_by'] = existingFlag['modified_by']
                    existingFlag['modified_by'] = modified_by
                existingFlag['previous_status'] = removed_flag['request_status']
                existingFlag['request_status'] = 'd'
                existingFlag['previous_value'] = flagStr
                existingFlag['value'] = Null
                duration_ms = existingFlag['modified_ts'] - existingFlag['previous_modified_ts']
                existingFlag['duration_days'] = math.floor(duration_ms / 86400000.0)
            else:
                Log.warning('Did not find a corresponding flag for removed value {{removed}} in {{existing}}', {'removed': flagStr, 
                   'existing': target.flags})

        for flagStr in addedFlags:
            if flagStr == '':
                continue
            added_flag = self.makeFlag(flagStr, modified_ts, modified_by)
            candidates = [ element for element in target.flags if element['value'] == None and added_flag['request_type'] == element['request_type'] and added_flag['request_status'] != element['previous_status']
                         ]
            if not candidates:
                target.flags.append(added_flag)
                continue
            chosen_one = candidates[0]
            if len(candidates) > 1:
                if DEBUG_STATUS:
                    Log.note('Matched added flag {{flag}} to multiple removed flags {{candidates}}.  Using the best.', {'flag': added_flag, 
                       'candidates': candidates})
                matched_ts = [ element for element in candidates if added_flag.modified_ts == element.modified_ts
                             ]
                if len(matched_ts) == 1:
                    Log.note('Matching on modified_ts fixed it')
                    chosen_one = matched_ts[0]
                else:
                    Log.note('Matching on modified_ts left us with {{num}} matches', {'num': len(matched_ts)})
                    matched_req = [ element for element in candidates if element['requestee'] != None and added_flag['modified_by'].lower() == element['requestee'].lower()
                                  ]
                    if len(matched_req) == 1:
                        Log.note('Matching on requestee fixed it')
                        chosen_one = matched_req[0]
                    else:
                        Log.warning('Matching on requestee left us with {{num}} matches. Skipping match.', {'num': len(matched_req)})
                        chosen_one = Null
            elif DEBUG_STATUS:
                Log.note('Matched added flag {{added}} to removed flag {{removed}}', {'added': added_flag, 
                   'removed': chosen_one})
            if chosen_one != None:
                for f in ['value', 'request_status', 'requestee']:
                    chosen_one[f] = nvl(added_flag[f], chosen_one[f])

        return

    def setPrevious(self, dest, aFieldName, aValue, aChangeAway):
        if dest['previous_values'] == None:
            dest['previous_values'] = {}
        pv = dest['previous_values']
        vField = aFieldName + '_value'
        caField = aFieldName + '_change_away_ts'
        ctField = aFieldName + '_change_to_ts'
        ddField = aFieldName + '_duration_days'
        pv[vField] = aValue
        if pv[caField] != None:
            pv[ctField] = pv[caField]
        else:
            pv[ctField] = dest['created_ts']
        pv[caField] = aChangeAway
        try:
            duration_ms = pv[caField] - pv[ctField]
        except Exception as e:
            Log.error('', e)

        pv[ddField] = math.floor(duration_ms / 86400000.0)
        return

    @staticmethod
    def makeFlag(flag, modified_ts, modified_by):
        flagParts = Struct(modified_ts=modified_ts, modified_by=modified_by, value=flag)
        matches = FLAG_PATTERN.match(flag)
        if matches:
            flagParts.request_type = matches.group(1)
            flagParts.request_status = matches.group(2)
            if matches.start(3) != -1 and len(matches.group(3)) > 2:
                flagParts.requestee = matches.group(3)[1:-1]
        return flagParts

    def addValues(self, total, add, valueType, field_name, target):
        if not add:
            return total
        else:
            if field_name == 'flags':
                for v in add:
                    total.append(BugHistoryParser.makeFlag(v, target.modified_ts, target.modified_by))

                if valueType != 'added':
                    self.currActivity.changes.append({'field_name': field_name, 
                       'new_value': Null, 
                       'old_value': (', ').join(Q.sort(add)), 
                       'attach_id': target.attach_id})
                else:
                    Log.error('programming error')
                return total
            diff = add - total
            removed = total & add
            if removed:
                Log.note('PROBLEM: Found {{type}}({{bug_id}}).{{field_name}} value: (Removing {{removed}} can not result in {{existing}})', {'bug_id': target.bug_id, 
                   'type': valueType, 
                   'field_name': field_name, 
                   'removed': removed, 
                   'existing': target[field_name]})
            if valueType != 'added' and diff:
                self.currActivity.changes.append({'field_name': field_name, 
                   'new_value': Null, 
                   'old_value': (', ').join(map(unicode, Q.sort(diff))), 
                   'attach_id': target.attach_id})
            return total | add

    def removeValues(self, total, remove, valueType, field_name, arrayDesc, target, timestamp):
        if field_name == 'flags':
            removeMe = []
            for v in remove:
                flag = BugHistoryParser.makeFlag(v, 0, 0)
                found = self.findFlag(total, flag)
                if found != None:
                    removeMe.append(found.value)
                else:
                    Log.note('PROBLEM Unable to find {{type}} FLAG: {{object}}.{{field_name}}: (All {{missing}}' + ' not in : {{existing}})', {'type': valueType, 
                       'object': arrayDesc, 
                       'field_name': field_name, 
                       'missing': v, 
                       'existing': total})

            total = [ a for a in total if a.value not in removeMe ]
            if valueType == 'added' and removeMe:
                try:
                    self.currActivity.changes.append({'field_name': field_name, 
                       'new_value': (', ').join(Q.sort(removeMe)), 
                       'old_value': Null, 
                       'attach_id': target.attach_id})
                except Exception as email:
                    Log.error('problem', email)

            return total
        if field_name == 'keywords':
            diff = remove - total
            output = total - remove
            if valueType == 'added' and remove:
                self.currActivity.changes.append({'field_name': field_name, 
                   'new_value': (', ').join(map(unicode, Q.sort(remove))), 
                   'old_value': Null, 
                   'attach_id': target.attach_id})
            if diff - KNOWN_MISSING_KEYWORDS:
                Log.note('PROBLEM Unable to find {{type}} KEYWORD {{object}}({{bug_id}}) (adding anyway): (All {{missing}}' + ' not in : {{existing}})', {'bug_id': target.bug_id, 
                   'type': valueType, 
                   'object': arrayDesc, 
                   'field_name': field_name, 
                   'missing': diff, 
                   'existing': total})
                for d in diff:
                    KNOWN_MISSING_KEYWORDS.add(d)

            return output
        if field_name == 'cc':
            map_total = struct.inverse({t:self.alias(t) for t in total})
            map_remove = struct.inverse({r:self.alias(r) for r in remove})
            c_total = set(map_total.keys())
            c_remove = set(map_remove.keys())
            removed = c_total & c_remove
            diff = c_remove - c_total
            output = c_total - c_remove
            if not target.uncertain:
                if diff:
                    Log.note('PROBLEM: Unable to find CC:\n{{missing|indent}}\nnot in:\n{{existing|indent}}\nalias info:\n{{candidates|indent}}', {'type': valueType, 
                       'object': arrayDesc, 
                       'field_name': field_name, 
                       'missing': Q.sort(Q.map(diff, map_remove)), 
                       'existing': Q.sort(total), 
                       'candidates': {d:self.aliases.get(d, None) for d in diff}})
            else:
                for lost in diff:
                    best_score = 0.3
                    best = Null
                    for found in output:
                        score = Math.min([
                         strings.edit_distance(found, lost),
                         strings.edit_distance(found.split('@')[0], lost.split('@')[0]),
                         strings.edit_distance(map_total[found][0], lost),
                         strings.edit_distance(map_total[found][0].split('@')[0], lost.split('@')[0])])
                        if score < best_score:
                            best = found

                    if best != Null:
                        Log.note('UNCERTAIN ALIAS FOUND: {{lost}} == {{found}}', {'lost': lost, 
                           'found': best})
                        removed.add(best)
                        output.discard(best)
                    else:
                        Log.note('PROBLEM Unable to pattern match {{type}} value: {{object}}.{{field_name}}: ({{missing}}' + ' not in : {{existing}})', {'type': valueType, 
                           'object': arrayDesc, 
                           'field_name': field_name, 
                           'missing': lost, 
                           'existing': total})

            if valueType == 'added':
                try:
                    if removed - set(map_total.keys()):
                        Log.error('problem with alias finding:\n' + 'map_total={{map_total}}\n' + 'map_remove={{map_remove}}\n' + 'c_total={{c_total}}\n' + 'c_remove={{c_remove}}\n' + 'removed={{removed}}\n' + 'diff={{diff}}\n' + 'output={{output}}\n', {'map_total': map_total, 
                           'c_total': c_total, 
                           'map_remove': map_remove, 
                           'c_remove': c_remove, 
                           'removed': removed, 
                           'diff': diff, 
                           'output': output})
                    final_removed = Q.map(removed, map_total)
                    if final_removed:
                        self.currActivity.changes.append({'field_name': field_name, 
                           'new_value': (', ').join(map(unicode, Q.sort(final_removed))), 
                           'old_value': Null, 
                           'attach_id': target.attach_id})
                except Exception as email:
                    Log.error('issues', email)

            return Q.map(output, map_total)
        else:
            removed = total & remove
            diff = remove - total
            output = total - remove
            if valueType == 'added' and removed:
                self.currActivity.changes.append({'field_name': field_name, 
                   'new_value': (', ').join(map(unicode, Q.sort(removed))), 
                   'old_value': Null, 
                   'attach_id': target.attach_id})
            if diff:
                Log.note('PROBLEM Unable to find {{type}} value in {{bug_id}}: {{object}}.{{field_name}}: (All {{missing}}' + ' not in : {{existing}})', {'bug_id': target.bug_id, 
                   'type': valueType, 
                   'object': arrayDesc, 
                   'field_name': field_name, 
                   'missing': diff, 
                   'existing': total})
            return output
            return

    @staticmethod
    def getMultiFieldValue(name, value):
        if value == None:
            return set()
        else:
            if name in MULTI_FIELDS:
                if name in NUMERIC_FIELDS:
                    return set([ int(s.strip()) for s in value.split(',') if s.strip() != '' ])
                return set([ s.strip() for s in value.split(',') if s.strip() != '' ])
            return {
             value}

    def alias(self, name):
        if name == None:
            return Null
        else:
            return nvl(self.aliases.get(name, Null).canonical, name)

    def initializeAliases(self):
        try:
            try:
                alias_json = File(self.settings.alias_file).read()
            except Exception as e:
                alias_json = '{}'

            self.aliases = {k:struct.wrap(v) for k, v in CNV.JSON2object(alias_json).items()}
            Log.note('{{num}} aliases loaded', {'num': len(self.aliases.keys())})
        except Exception as e:
            Log.error('Can not init aliases', e)