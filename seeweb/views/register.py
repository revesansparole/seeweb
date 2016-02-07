from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.models import DBSession
from seeweb.model_access import get_team, get_user
from seeweb.model_edit import create_user

from seeweb.security import (is_good_email,
                             is_good_id,
                             is_good_name,
                             log_user_in)


@view_config(route_name='user_register', renderer='templates/register.jinja2')
def view(request):
    if request.unauthenticated_userid is not None:
        request.session.flash("Already logged in, log out first", 'warning')
        return HTTPFound(location=request.route_url('home'))

    if "ok" in request.params:
        session = DBSession()

        # check all fields are correct
        uid = request.params["user_id"]
        if len(uid) == 0 or not is_good_id(uid):
            request.session.flash("User id is not a valid id", 'warning')
            return HTTPFound(location=request.current_route_url())

        name = request.params["user_name"]
        if len(name) == 0 or not is_good_name(name):
            request.session.flash("Name given is not valid", 'warning')
            return HTTPFound(location=request.current_route_url())

        email = request.params["user_email"]
        if len(email) == 0 or not is_good_email(email):
            request.session.flash("Email given is not valid", 'warning')
            return HTTPFound(location=request.current_route_url())

        # check user does not exist already
        # as a user
        user = get_user(session, uid)
        if user is not None:
            request.session.flash("User %s already exists" % uid, 'warning')
            return HTTPFound(location=request.current_route_url())

        # as a team
        team = get_team(session, uid)
        if team is not None:
            msg = "User %s already exists as a team name" % uid
            request.session.flash(msg, 'warning')
            return HTTPFound(location=request.current_route_url())

        # register new user
        create_user(session, uid, name, email)
        return log_user_in(request, uid, True)

    else:
        return {}
