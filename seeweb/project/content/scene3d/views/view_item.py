from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.views.project.commons import content_init


@view_config(route_name='project_content_scene3d_view_item',
             renderer='../templates/view_item.jinja2')
def view(request):
    session = DBSession()
    project, scene, scene_def, view_params = content_init(request, session)

    return view_params