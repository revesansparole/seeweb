from itertools import chain
from sqlalchemy import Column, ForeignKey, String

from seeweb.models.models import get_by_id
from seeweb.models.research_object import ResearchObject
from seeweb.models.ro_link import ROLink


class ROWorkflowProv(ResearchObject):
    """Research Object that contains execution provenance of a workflow
    """
    __tablename__ = 'ro_workflow_provs'

    id = Column(String(255), ForeignKey('ros.id'), primary_key=True)
    workflow = Column(String(255), ForeignKey('ro_workflows.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'workflow_prov',
    }

    def __repr__(self):
        return "<ROWorkflowProv(id='%s', name='%s')>" % (self.id,
                                                         self.name)

    @staticmethod
    def get(session, uid):
        """Fetch a given RO in the database.

        Args:
            session: (DBSession)
            uid: (str) RO id

        Returns:
            (ResearchObject) or None if no RO with this id is found
        """
        return get_by_id(session, ROWorkflowProv, uid)

    def init(self, session, ro_def):
        """Initialize this RO with a set of attributes

        Args:
            session (DBSession):
            ro_def (dict): set of properties to initialize this RO

        Returns:
            None
        """
        loc_def = dict(ro_def)
        wkf = loc_def.pop('workflow')

        ResearchObject.init(self, session, loc_def)
        self.workflow = wkf

        # link to workflow associated to this provenance
        ROLink.connect(session, self.id, wkf, 'use')

        # link to workflow nodes associated with each process?

        # link to data produced

    def repr_json(self, full=False):
        """Create a json representation of this object

        Args:
            full (bool): if True, also add all properties stored in definition
                         default False

        Returns:
            dict
        """
        d = ResearchObject.repr_json(self, full=full)

        if full:
            d['workflow'] = self.workflow

        return d
