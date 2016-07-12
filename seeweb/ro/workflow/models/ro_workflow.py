from sqlalchemy import Column, ForeignKey, String

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink


class ROWorkflow(ResearchObject):
    """Research Object that contains node for workflows
    """
    __tablename__ = 'ro_workflows'

    id = Column(String(255), ForeignKey('ros.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'workflow',
    }

    def __repr__(self):
        return "<ROWorkflow(id='%s', name='%s')>" % (self.id,
                                                     self.title)

    @staticmethod
    def get(session, uid):
        """Fetch a given RO in the database.

        Args:
            session: (DBSession)
            uid: (str) RO id

        Returns:
            (ResearchObject) or None if no RO with this id is found
        """
        return get_by_id(session, ROWorkflow, uid)

    def init(self, session, ro_def):
        """Initialize this RO with a set of attributes

        Args:
            session (DBSession):
            ro_def (dict): set of properties to initialize this RO

        Returns:
            None
        """
        ResearchObject.init(self, session, ro_def)

        # link to nodes used by this workflow
        # ports = ro_def.get("inputs", []) + ro_def.get("outputs", [])
        # uids = set(port_def['interface'] for port_def in ports)
        # for uid in uids:
        #     ROLink.connect(session, self.id, uid, 'use')
