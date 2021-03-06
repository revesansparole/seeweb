from base64 import b64encode
import json

from seeweb.models.ro_link import ROLink
from seeweb.ro.container.models.ro_container import ROContainer
from seeweb.ro.data.models.ro_data import ROData
from seeweb.rodata.image.models.ro_image import ROImage
from seeweb.ro.interface.models.ro_interface import any_uid, ROInterface
from seeweb.rodata.scene3d.models.ro_scene3d import ROScene3d


def cvt_schema(obj_def):
    """Convert an object definition into a jsonschema

    Args:
        obj_def (dict): json schema in dict form

    Returns:
        (str): the serialized version of json schema
    """
    obj_def["$schema"] = "http://json-schema.org/schema#"
    return json.dumps(obj_def, sort_keys=True)


def main(session, user, container):
    """Create a project that contains different types of data

    Args:
        session (DBSession):
        user (User): owner of created project
        container (ROContainer): top level container

    Returns:
        None
    """
    # register common data interfaces
    roc = ROContainer()
    roc.init(session, dict(id="81c69a8558a311e6afb6d4bed973e64a",
                           owner=user.id, name="interfaces", public=True,
                           description="Store commonly used interfaces"))

    roi = ROInterface()
    roi.init(session, dict(id=ROData.implements,
                           owner=user.id, name="any", public=True,
                           description="Interface used for data that don't "
                                       "have a specific interface"))
    ROLink.connect(session, roc.id, roi.id, 'contains')

    ropy = ROInterface()
    ropy.init(session, dict(id="dc5b10c858a611e6afb6d4bed973e64a",
                            owner=user.id, name="pyobj", public=True))
    ROLink.connect(session, roc.id, ropy.id, 'contains')

    schema = dict(title="Interface for data of type 'string'",
                  description="Just a simple chain of characters",
                  type="string")

    roi = ROInterface()
    roi.init(session, dict(id="006bca4c58a311e6afb6d4bed973e64a",
                           owner=user.id, name="string", public=True,
                           schema=cvt_schema(schema), ancestors=[ropy.id]))
    ROLink.connect(session, roc.id, roi.id, 'contains')

    sid = roi.id
    for name in ("code", "path", "ref", "text"):
        roi = ROInterface()
        roi.init(session, dict(owner=user.id, name=name, public=True,
                               ancestors=[sid]))
        ROLink.connect(session, roc.id, roi.id, 'contains')

    schema = dict(title="Interface for data of type 'number'",
                  description="Just a simple number",
                  type="number")

    roi = ROInterface()
    roi.init(session, dict(id="c7f6a30a58a511e6afb6d4bed973e64a",
                           owner=user.id, name="number", public=True,
                           schema=cvt_schema(schema), ancestors=[ropy.id]))
    ROLink.connect(session, roc.id, roi.id, 'contains')

    sid = roi.id
    for name in ("complex", "int", "float"):
        roi = ROInterface()
        roi.init(session, dict(owner=user.id, name=name, public=True,
                               ancestors=[sid]))
        ROLink.connect(session, roc.id, roi.id, 'contains')

    rgba_schema = dict(title="Interface for color of type rgba",
                       description="Just a simple array of rgba quadruplets",
                       type="array",
                       minLength=4,
                       maxLength=4,
                       items=dict(type="int"))

    roi = ROInterface()
    roi.init(session, dict(id="256203e058b911e6afb6d4bed973e64a",
                           owner=user.id, name="rgba", public=True,
                           schema=cvt_schema(rgba_schema), ancestors=[]))
    ROLink.connect(session, roc.id, roi.id, 'contains')

    schema = dict(title="Interface for data of type 2D images",
                  description="Just a simple 2d array of rgba quadruplets",
                  type="array",
                  minLength=1,
                  items=dict(type="array",
                             minLength=1,
                             items=rgba_schema))

    roi = ROInterface()
    roi.init(session, dict(id=ROImage.implements,
                           owner=user.id, name="image", public=True,
                           schema=cvt_schema(schema), ancestors=[]))
    ROLink.connect(session, roc.id, roi.id, 'contains')

    schema = dict(title="Interface for data of type 3D scenes",
                  description="Json description of a 3D scene",
                  type="array",
                  minLength=1,
                  items=dict(type="array",
                             minLength=1,
                             items=rgba_schema))

    roi = ROInterface()
    roi.init(session, dict(id=ROScene3d.implements,
                           owner=user.id, name="scene3d", public=True,
                           schema=cvt_schema(schema), ancestors=[]))
    ROLink.connect(session, roc.id, roi.id, 'contains')

    # create a sample project with some common data examples
    roc = ROContainer()
    roc.init(session, dict(id="0a73ad11596111e6a3a6d4bed973e64a",
                           owner=user.id, name="data", ctype="project"))
    ROLink.connect(session, container.id, roc.id, 'contains')

    # raw data
    rod = ROData()
    rod.init(session, dict(owner=user.id, name="test number", value=3.14159))
    ROLink.connect(session, roc.id, rod.id, "contains")

    with open("seeweb/ro/data/static/default_avatar.png", 'rb') as f:
        value = b64encode(f.read())

    rod = ROData()
    rod.init(session, dict(owner=user.id, name="test data", value=value))
    ROLink.connect(session, roc.id, rod.id, "contains")

    # image
    with open("seeweb/ro/data/static/default_avatar.png", 'rb') as f:
        value = b64encode(f.read())

    roi = ROImage()
    roi.init(session, dict(id="03faa88158bb11e6afb6d4bed973e64a",
                           owner=user.id, name="test image", value=value,
                           description="Sample image for testing purpose"))
    ROLink.connect(session, roc.id, roi.id, "contains")

    # scene3D
    with open("seeweb/scripts/scene.json", 'r') as f:
        sc = json.load(f)

    rosc = ROScene3d()
    rosc.init(session, dict(owner=user.id, name="test scene", value=sc))
    ROLink.connect(session, roc.id, rosc.id, "contains")
