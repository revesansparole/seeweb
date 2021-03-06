from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models import DBSession

from seeweb.views.ro.commons import view_init_min

route_name = 'ro_data_view_home'
route_url = 'ro_data/{uid}/home'


@view_config(route_name=route_name,
             renderer='../templates/view_home.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = view_init_min(request, session)

    view_params['description'] = Markup(ro.html_description())

    value = ""
    for i in range(10):
        value += ro.value[(i * 50):((i + 1) * 50)]
        value += "\n"

    if len(ro.value) > 500:
        value += "\n ..."

    view_params['value'] = value

    return view_params
