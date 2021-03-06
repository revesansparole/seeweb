from pyramid.view import view_config

from seeweb.models import DBSession

from .commons import view_init


@view_config(route_name='ro_view_links',
             renderer='templates/ro/view_links.jinja2')
def view(request):
    session = DBSession()
    ro, view_params = view_init(request, session, 'links')

    links = []
    for link in ro.out_links:
        links.append(("self", link.type, link.target))
    for link in ro.in_links:
        links.append((link.source, link.type, "self"))

    view_params["links"] = links

    return view_params
