from pyramid.httpexceptions import HTTPFound
import transaction

from seeweb.models.auth import Role
from seeweb.models.research_object import ResearchObject


tabs = [('Home', 'home'),
        ('Actors', 'actors'),
        ('Links', 'links')]


def fetch_ro(request, session):
    """Retrieve RO whose id is in URL.

    Args:
        request: (Request)
        session: (DBSession)

    Returns:
        (str, ResearchObject): uid, ro
    """
    uid = request.matchdict['uid']
    ro = ResearchObject.get(session, uid)
    if ro is None:
        request.session.flash("RO %s does not exists" % uid, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    return uid, ro


def view_init_min(request, session):
    """Common init for all 'view' parts.

    Args:
        request: (Request)
        session: (DBSession)

    Returns:
        (ResearchObject, dict of (str: any)): ro, view_params
    """
    uid, ro = fetch_ro(request, session)

    current_uid = request.unauthenticated_userid

    role = ro.access_role(session, current_uid)
    if role == Role.denied:
        request.session.flash("Access to %s not granted for you" % uid,
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    # allow edition
    allow_edit = (current_uid is not None and role == Role.edit)

    view_params = {"ro": ro,
                   "allow_edit": allow_edit,
                   "minimized": True}

    return ro, view_params


def view_init(request, session, tab):
    """Extended init adding tabs.

    Args:
        request: (Request)
        session: (DBSession)
        tab: (str) current tab in view

    Returns:
        (ResearchObject, dict of (str: any)): ro, view_params
    """
    ro, view_params = view_init_min(request, session)

    view_params["tabs"] = tabs
    view_params["tab"] = tab
    view_params["sections"] = []

    return ro, view_params


def edit_init(request, session, tab):
    """Common init for all 'edit' views.

    Args:
        request: (Request)
        session: (DBSession)
        tab: (str) current tab in view

    Returns:
        (ResearchObject, dict of (str: any)): ro, view_params
    """
    ro, view_params = view_init(request, session, tab)

    if not view_params["allow_edit"]:
        msg = "Access to %s edition not granted for you" % ro.id
        request.session.flash(msg, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    if 'back' in request.params:
        # request.session.flash("Edition stopped", 'success')
        loc = request.route_url('ro_view_%s' % tab, uid=ro.id)
        raise HTTPFound(location=loc)

    if "confirm_delete" in request.params:
        if ResearchObject.remove(session, ro):
            transaction.commit()
            request.session.flash("RO '%s' deleted" % ro.id, 'success')
        else:
            request.session.flash("Failed to delete '%s'" % ro.id, 'warning')
        raise HTTPFound(location=request.route_url('home'))

    return ro, view_params
