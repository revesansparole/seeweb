from pyramid.view import view_config

from seeweb.models import DBSession

from .tools import tabs, view_init


@view_config(route_name='team_view_members',
             renderer='templates/team/view_members.jinja2')
def index(request):
    session = DBSession()
    team, current_uid, allow_edit = view_init(request, session)

    members = []
    for actor in team.auth:
        if actor.is_team:
            typ = 'team'
        else:
            typ = 'user'
        members.append((typ, actor.role, actor.user))

    return {"team": team,
            "tabs": tabs,
            "tab": 'members',
            "allow_edit": allow_edit,
            "members": members}
