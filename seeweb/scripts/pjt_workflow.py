from uuid import uuid1

from seeweb.models.ro_link import ROLink
from seeweb.ro.container.models.ro_container import ROContainer
from seeweb.ro.interface.models.ro_interface import ROInterface


def main(session, user):
    """Create workflow related projects.

    Args:
        session (DBSession):
        user (User): owner of created project

    Returns:
        None
    """
    roc = ROContainer.create(session,
                             uuid1().hex,
                             user.id,
                             "nodelib")

    for iname in ("any", "IStr", "IInt", "IFileStr"):
        roi = ROInterface.create(session,
                                 uuid1().hex,
                                 user.id,
                                 iname)

        ROLink.connect(session, roc.id, roi.id, "contains")
