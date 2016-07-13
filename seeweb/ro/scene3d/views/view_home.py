from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.views.ro.commons import view_init_min


route_name = 'ro_scene3d_view_home'
route_url = 'ro_scene3d/{uid}/home'


@view_config(route_name=route_name,
             renderer='../templates/view_home.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = view_init_min(request, session)

    view_params['scene'] = ro.scene

    return view_params