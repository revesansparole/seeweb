from seeweb.models.ro_link import ROLink
from seeweb.ro.container.models.ro_container import ROContainer
from seeweb.rodata.scene3d.models.ro_scene3d import ROScene3d


def main(session, user, container):
    """Create a project that contains different types of data

    Args:
        session (DBSession):
        user (User): owner of created project
        container (ROContainer): top level container

    Returns:
        None
    """
    # default interfaces for openalea
    roc = ROContainer()
    roc.init(session, dict(owner=user.id, name="data"))
    ROLink.connect(session, container.id, roc.id, 'contains')

    with open("seeweb/scripts/scene.json", 'r') as f:
        sc = f.read()

    rosc = ROScene3d()
    rosc.init(session, dict(owner=user.id, name="test scene", scene=sc))

    ROLink.connect(session, roc.id, rosc.id, "contains")
