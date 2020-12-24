# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/dlaxalde/src/cw/cubes/localperms/cubicweb_localperms/views.py
# Compiled at: 2019-03-13 06:54:25
# Size of source mod 2**32: 8057 bytes
__doc__ = 'cubicweb-localperms views/forms/actions/components for web ui'
__docformat__ = 'restructuredtext en'
from cubicweb import _
from logilab.mtconverter import xml_escape
from cubicweb.predicates import one_line_rset, non_final_entity, is_instance, match_user_groups, relation_possible
import cubicweb.web as wdgs
from cubicweb.web.views import uicfg
from cubicweb.web.formfields import guess_field
from cubicweb.web.views import ibreadcrumbs, actions, management, cwuser, tableview
_AFS = uicfg.autoform_section
_AFS.tag_subject_of(('CWPermission', 'require_group', '*'), 'main', 'attributes')
_AFS.tag_subject_of(('CWPermission', 'require_group', '*'), 'muledit', 'attributes')
_AFS.tag_subject_of(('*', 'granted_permission', '*'), 'main', 'hidden')
_AFS.tag_subject_of(('*', 'require_permission', '*'), 'main', 'hidden')
_ADDMENU = uicfg.actionbox_appearsin_addmenu
_ADDMENU.tag_subject_of(('*', 'granted_permission', '*'), False)
_ADDMENU.tag_subject_of(('*', 'require_permission', '*'), False)
_PVS = uicfg.primaryview_section
_PVS.tag_subject_of(('*', 'granted_permission', '*'), 'hidden')
_PVS.tag_object_of(('*', 'granted_permission', '*'), 'hidden')
_PVS.tag_subject_of(('*', 'require_permission', '*'), 'hidden')
_PVS.tag_object_of(('*', 'require_permission', '*'), 'hidden')

class CWPermissionIBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    __select__ = is_instance('CWPermission')

    def parent_entity(self):
        permissionof = getattr(self.entity, 'reverse_granted_permission', ())
        if len(permissionof) == 1:
            return permissionof[0]
        permissionof = getattr(self.entity, 'reverse_require_permission', ())
        if len(permissionof) == 1:
            return permissionof[0]


class SecurityManagementView(management.SecurityManagementView):
    """SecurityManagementView"""
    __select__ = management.SecurityManagementView.__select__ & relation_possible('require_permission', 'subject')

    def entity_call(self, entity):
        super(SecurityManagementView, self).entity_call(entity)
        if hasattr(entity, 'granted_permission'):
            self.w('<h3>%s</h3>' % self._cw._('Local permissions'))
            perms = entity.granted_permission
            self.existing_permissions(entity, 'granted_permission', perms)
            rschema = self._cw.vreg.schema.rschema('granted_permission')
            if rschema.has_perm((self._cw), 'add', fromeid=(entity.eid)):
                self.granted_permission_edit_form(entity)
            perms = set((x.eid for x in entity.granted_permission))
        else:
            perms = ()
        iperms = [x for x in entity.require_permission if x.eid not in perms]
        if iperms:
            self.w('<h3>%s</h3>' % self._cw._('Inherited permissions'))
            self.existing_permissions(entity, 'require_permission', iperms)

    def existing_permissions(self, entity, rtype, perms):
        w = self.w
        _ = self._cw._
        rschema = self._cw.vreg.schema.rschema(rtype)
        if rschema.has_perm((self._cw), 'delete', fromeid=(entity.eid)):
            delurl = self._cw.build_url('edit', __redirectvid='security', __redirectpath=(entity.rest_path()))
            delurl = delurl.replace('%', '%%')
            delurl += '&__delete=%s:%s:%%s' % (entity.eid, rtype)
            dellinktempl = '[<a href="%s" title="%s">-</a>]&#160;' % (
             xml_escape(delurl), _('delete this permission'))
        else:
            dellinktempl = None
        w('<table class="listing schemaInfo">')
        w('<tr><th>%s</th><th>%s</th></tr>' % (_('permission'),
         _('granted to groups')))
        for cwperm in perms:
            w('<tr><td>')
            if dellinktempl:
                w(dellinktempl % cwperm.eid + ' ')
            w('%s</td>' % cwperm.view('oneline'))
            w('<td>%s</td>' % self._cw.view('csv', cwperm.related('require_group'), 'null'))
            w('</tr>\n')

        w('</table>')

    def granted_permission_edit_form(self, entity):
        divid = 'addNewPerm%s' % entity.eid
        self.w('<br/><a class="addButton" href="javascript:toggleVisibility(\'%s\')">%s</a>' % (
         divid, self._cw._('New CWPermission')))
        self.w('<div id="%s" class="hidden">' % divid)
        newperm = self._cw.vreg['etypes'].etype_class('CWPermission')(self._cw)
        newperm.eid = self._cw.varmaker.next()
        form = self._cw.vreg['forms'].select('base',
          (self._cw), entity=newperm, form_buttons=[
         wdgs.SubmitButton()],
          domid=('reqperm%s' % entity.eid),
          __redirectvid='security',
          __redirectpath=(entity.rest_path()))
        form.add_hidden('granted_permission', (entity.eid), role='object', eidparam=True)
        permnames = getattr(entity, '__permissions__', None)
        cwpermschema = newperm.e_schema
        if permnames is not None:
            field = guess_field(cwpermschema, (self._cw.vreg.schema.rschema('name')), widget=(wdgs.Select({'size': 1})),
              choices=permnames)
        else:
            field = guess_field(cwpermschema, self._cw.vreg.schema.rschema('name'))
        form.append_field(field)
        field = guess_field(cwpermschema, self._cw.vreg.schema.rschema('label'))
        form.append_field(field)
        field = guess_field(cwpermschema, self._cw.vreg.schema.rschema('require_group'))
        form.append_field(field)
        renderer = self._cw.vreg['formrenderers'].select('htable',
          (self._cw), rset=None, display_progress_div=False)
        form.render(w=(self.w), renderer=renderer)
        self.w('</div>')


actions.ManagePermissionsAction.__select__ = one_line_rset() & non_final_entity() & (match_user_groups('managers') | relation_possible('granted_permission', 'subject', 'CWPermission', action='add'))

class CWGroupsTable(cwuser.CWGroupsTable):
    """CWGroupsTable"""

    def local_permissions_cell(w, entity):
        perms = []
        for perm in entity.reverse_require_group:
            if perm.__regid__ != 'CWPermission':
                continue
            for something in perm.reverse_granted_permission:
                perms.append('%s [%s]' % (something.view('oneline'), perm.name))

        w(', '.join(perms))

    columns = cwuser.CWGroupsTable.columns + [_('local_permissions')]
    cwuser.CWGroupsTable.column_renderers['local_permissions'] = tableview.EntityTableColRenderer(renderfunc=local_permissions_cell,
      header=(_('local_permissions')))


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, (CWGroupsTable,))
    vreg.register_and_replace(CWGroupsTable, cwuser.CWGroupsTable)