from jinja2 import Markup
from pyramid.view import view_config

from seeweb.models.auth import Role
from seeweb.models.access import get_team, team_access_role
from seeweb.models.edit import create_team

from .tools import view_init, tabs


@view_config(route_name='user_view_teams', renderer='templates/user/view_teams.jinja2')
def index(request):
    user, current_uid, allow_edit = view_init(request)

    if 'new_team' in request.params:
        tid = request.params.get('team_id', "")
        if len(tid) == 0:
            request.session.flash("Enter a team id first", 'warning')
        else:
            tid = tid.lower().strip()
            if " " in tid:
                request.session.flash("Team id ('%s') cannot have space" % tid, 'warning')
            else:
                team = get_team(tid)
                if team is not None:
                    team_url = request.route_url('team_view_home', tid=tid)
                    msg = "Team <a href='%s'>'%s'</a> already exists" % (team_url, tid)
                    request.session.flash(Markup(msg), 'warning')
                else:
                    # create new team
                    team = create_team(tid)
                    team.add_auth(Role.edit, user=user)
                    request.session.flash("New team %s created" % tid, 'success')

    teams = []
    for actor in user.teams:
        team = get_team(actor.team)
        role = team_access_role(team, current_uid)
        if role != Role.denied:
            teams.append((role, team))

    return {"user": user,
            "tabs": tabs,
            "tab": 'teams',
            "allow_edit": allow_edit,
            "teams": teams}
