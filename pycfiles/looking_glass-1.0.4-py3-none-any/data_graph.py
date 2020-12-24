# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/TimHe/OneDrive/Programming/LookingGlass/looking_glass/lib/data_graph.py
# Compiled at: 2019-02-26 10:02:03
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_
import boto3, os.path, sys, datetime
from .tables import ChangeLog, Node, AdditionalNodeData, Edge, User, Workspace, AuthorizedWorkspaceUser, setup_tables

class DataGraph:

    def __init__(self):
        self.engine = create_engine('sqlite:///looking_glass.db', isolation_level='SERIALIZABLE')
        self.Session = scoped_session(sessionmaker(bind=self.engine, autocommit=False))
        setup_tables(self.engine)

    def create_session(self):
        return self.Session()

    def close_session(self):
        self.Session.remove()

    def load_user(self, user_id):
        return self.create_session().query(User).filter_by(id=user_id).first()

    def create_user(self, username, password):
        session = self.create_session()
        new_user = User(username, password)
        session.add(new_user)
        session.commit()

    def node_as_dict_with_additional_data(self, session, node):
        additional_node_data_list = session.query(AdditionalNodeData).filter_by(node_id=node.id).all()
        node_data = node.serializable_dict()
        for additional_node_data in additional_node_data_list:
            node_data[additional_node_data.data_key] = additional_node_data.data_value

        return node_data

    def create_workspace(self, user_id, workspace_name, default=False):
        session = self.create_session()
        if session.query(Workspace).filter_by(active=True, owning_user=user_id, name=workspace_name).first() is not None:
            return
        else:
            new_workspace = Workspace(owning_user=user_id, name=workspace_name, default=default, active=True)
            session.add(new_workspace)
            session.commit()
            return new_workspace

    def delete_workspace(self, user_id, workspace_id):
        session = self.create_session()
        workspace = session.query(Workspace).filter_by(active=True, owning_user=user_id, id=workspace_id).first()
        if workspace is None:
            return False
        else:
            workspace.active = False
            session.add(workspace)
            session.commit()
            return True

    def grant_workspace_access(self, owning_user_id, workspace_id, authorized_user_id):
        session = self.create_session()
        if session.query(User).filter_by(id=authorized_user_id).first() is None:
            return False
        else:
            if session.query(Workspace).filter_by(active=True, owning_user=owning_user_id, id=workspace_id).first() is None:
                return False
            session.add(AuthorizedWorkspaceUser(workspace_id=workspace_id, authorized_user=authorized_user_id))
            session.commit()
            return True

    def revoke_workspace_access(self, owning_user_id, workspace_id, unauthorized_user_id):
        session = self.create_session()
        user_authorization = session.query(AuthorizedWorkspaceUser).filter_by(workspace_id=workspace_id, authorized_user=unauthorized_user_id).first()
        if user_authorization is None:
            return False
        else:
            session.delete(user_authorization)
            session.commit()
            return True

    def can_user_access_workspace(self, session, username, workspace_id):
        access_allowed = False
        owned_workspace = session.query(Workspace).filter_by(active=True, owning_user=username, id=workspace_id).first()
        if owned_workspace is None:
            authorized_workspace = session.query(AuthorizedWorkspaceUser).filter_by(workspace_id=workspace_id, authorized_user=username).first()
            if authorized_workspace is not None:
                access_allowed = True
        else:
            access_allowed = True
        return access_allowed

    def workspaces_for_user(self, username):
        session = self.create_session()
        owned_workspaces = session.query(Workspace).filter_by(active=True, owning_user=username).all()
        authorizations = session.query(AuthorizedWorkspaceUser).filter_by(authorized_user=username).all()
        authorized_workspace_ids = [ a.workspace_id for a in authorizations ]
        authorized_workspaces = session.query(Workspace).filter(and_(Workspace.id.in_(authorized_workspace_ids), Workspace.active == True)).all()
        return owned_workspaces + authorized_workspaces

    def default_workspace_for_user(self, username):
        session = self.create_session()
        return session.query(Workspace).filter_by(owning_user=username, default=True).first()

    def current_graph_json(self, username, workspace_id):
        session = self.create_session()
        if not self.can_user_access_workspace(session, username, workspace_id):
            return None
        else:
            nodes = session.query(Node).filter_by(active=True, workspace_id=workspace_id).all()
            current_version_number = ChangeLog.curr_version_number(session)
            nodes_by_id = {}
            for node in nodes:
                node_data = self.node_as_dict_with_additional_data(session, node)
                nodes_by_id[node.id] = node_data

            for edge in session.query(Edge).filter_by(active=True, workspace_id=workspace_id).all():
                if 'connections' in nodes_by_id[edge.source_node_id]:
                    nodes_by_id[edge.source_node_id]['connections'].append(edge.destination_node_id)
                else:
                    nodes_by_id[edge.source_node_id]['connections'] = [
                     edge.destination_node_id]

            return {'current_version_number': current_version_number, 'nodes': list(nodes_by_id.values())}

    def get_node_by_ip(self, node_ip, username, workspace_id):
        session = self.create_session()
        if not self.can_user_access_workspace(session, username, workspace_id):
            return None
        else:
            node = session.query(Node).filter_by(active=True, ip=node_ip, workspace_id=workspace_id).first()
            if node:
                node = self.node_as_dict_with_additional_data(session, node)
            return node

    def upsert_node(self, node_dict, username, workspace_id):
        session = self.create_session()
        if not self.can_user_access_workspace(session, username, workspace_id):
            return
        else:
            if 'id' in node_dict:
                for n in session.query(Node).filter_by(active=True, id=node_dict['id'], workspace_id=workspace_id).all():
                    n.active = False
                    session.add(n)

            node_obj_dict = {}
            additional_node_data = {}
            for key in node_dict:
                if key in Node.__table__.columns:
                    node_obj_dict[key] = node_dict[key]
                else:
                    additional_node_data[key] = node_dict[key]

            current_version_number = ChangeLog.curr_version_number(session)
            new_version_number = current_version_number + 1
            new_changelog_row = ChangeLog(version_number=new_version_number, date_time=datetime.datetime.utcnow())
            new_node = Node.from_dict(node_obj_dict, workspace_id)
            new_node.version_number = new_version_number
            session.add(new_node)
            session.add(new_changelog_row)
            for key in additional_node_data:
                session.add(AdditionalNodeData(node_id=new_node.id, data_key=key, data_value=str(additional_node_data[key])))

            session.commit()
            return

    def add_edge(self, edge, username, workspace_id):
        session = self.create_session()
        if not self.can_user_access_workspace(session, username, workspace_id):
            return
        else:
            current_version_number = ChangeLog.curr_version_number(session)
            from_node_id = edge['from']
            source_node = session.query(Node).filter_by(active=True, id=from_node_id, workspace_id=workspace_id).first()
            if not source_node:
                session.rollback()
                raise 'Unable to create edge; from node with ID of %s does not exist' % from_node_id
            new_version_number = current_version_number + 1
            new_changelog_row = ChangeLog(version_number=new_version_number, date_time=datetime.datetime.utcnow())
            new_edge = Edge(source_node_id=edge['from'], destination_node_id=edge['to'], version_number=new_version_number, workspace_id=workspace_id, active=True)
            session.add(new_edge)
            session.add(new_changelog_row)
            session.commit()
            return

    def remove_node(self, node_id, username, workspace_id):
        session = self.create_session()
        if not self.can_user_access_workspace(session, username, workspace_id):
            return
        else:
            current_version_number = ChangeLog.curr_version_number(session)
            new_changelog_row = ChangeLog(version_number=current_version_number + 1, date_time=datetime.datetime.utcnow())
            session.add(new_changelog_row)
            edges_from_node = session.query(Edge).filter_by(active=True, source_node_id=node_id, workspace_id=workspace_id).all()
            for edge in edges_from_node:
                edge.active = False

            session.add_all(edges_from_node)
            node = session.query(Node).filter_by(active=True, id=node_id, workspace_id=workspace_id).first()
            node.active = False
            session.add(node)
            session.commit()
            return

    def remove_edge(self, from_node_id, to_node_id, username, workspace_id):
        session = self.create_session()
        if not self.can_user_access_workspace(session, username, workspace_id):
            return
        else:
            current_version_number = ChangeLog.curr_version_number(session)
            new_changelog_row = ChangeLog(version_number=current_version_number + 1, date_time=datetime.datetime.utcnow())
            session.add(new_changelog_row)
            edge = session.query(Edge).filter_by(active=True, source_node_id=from_node_id, destination_node_id=to_node_id, workspace_id=workspace_id).first()
            edge.active = False
            session.add(edge)
            session.commit()
            return

    def does_edge_exist(self, src_ip, dst_ip, username, workspace_id):
        session = self.create_session()
        if not self.can_user_access_workspace(session, username, workspace_id):
            return False
        else:
            src_node = session.query(Node).filter_by(active=True, ip=src_ip, workspace_id=workspace_id).first()
            dst_node = session.query(Node).filter_by(active=True, ip=dst_ip, workspace_id=workspace_id).first()
            if not (src_node and dst_node):
                return False
            edge = session.query(Edge).filter_by(active=True, source_node_id=src_node.id, destination_node_id=dst_node.id, workspace_id=workspace_id).first()
            return edge is not None