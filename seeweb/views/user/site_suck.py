from jinja2 import Markup
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from seeweb.avatar import upload_project_avatar
from seeweb.models import DBSession
from seeweb.model_access import get_project
from seeweb.model_edit import add_dependency, clear_dependencies, create_project
from seeweb.project.explore_sources import (fetch_avatar,
                                            fetch_dependencies,
                                            fetch_gallery,
                                            fetch_readme)
from seeweb.project.gallery import add_gallery_image, clear_gallery
from seeweb.project.source import fetch_sources, parse_hostname
from seeweb.project.provider import github_git


@view_config(route_name='site_suck',
             renderer='templates/user/site_suck.jinja2')
def view(request):
    session = DBSession()

    if request.unauthenticated_userid is None:
        request.session.flash("Action not authorized for anonymous users",
                              'warning')
        raise HTTPFound(location=request.route_url('home'))

    view_params = {}

    src_url = request.params.get("src_url", "")
    if len(src_url) == 0:
        return view_params

    view_params["src_url"] = src_url

    hostname = parse_hostname(src_url)
    if hostname != 'github':
        request.session.flash("Unrecognized host name: %s" % hostname,
                              'warning')
        return view_params

    owner, project_name = github_git.parse_url(src_url)
    if owner is None:
        request.session.flash("Unrecognized url, must be https://github.com/owner/project.git", 'warning')
        return view_params

    if "project_name" in request.params:
        project_name = request.params["project_name"]

    pid = project_name.lower().strip()
    if " " in pid:
        request.session.flash("Project names can not contains spaces", 'warning')
        return view_params

    project = get_project(session, pid)
    if project is not None:
        if project.public:
            project_url = request.route_url('project_view_home',
                                            pid=pid)
            msg = "Project <a href='%s'>'%s'</a> already exists" % (project_url, pid)
            request.session.flash(Markup(msg), 'warning')
        else:
            msg = "Project '%s' already exists (private)" % pid
            request.session.flash(msg, 'warning')

        view_params["project_name"] = pid
        return view_params

    # create project
    project = create_project(session,
                             request.unauthenticated_userid,
                             pid,
                             public=True)
    project.src_url = src_url

    if not fetch_sources(project):
        request.session.flash("Unable to fetch sources", 'warning')
    else:
        clear_dependencies(session, project)
        for name, ver in fetch_dependencies(project.id):
            add_dependency(session, project, name, ver)

        # fetch avatar
        try:
            img = fetch_avatar(project.id)
            if img is None:
                request.session.flash("No avatar found in sources", 'warning')
            else:
                upload_project_avatar(img, project)
        except IOError:
            request.session.flash("Unable to read image", 'warning')

        # fetch gallery
        clear_gallery(project)
        imgs = fetch_gallery(project.id)
        if len(imgs) > 0:
            for img, name in imgs:
                add_gallery_image(project, img, name)

        # fetch readme
        try:
            txt = fetch_readme(project.id)
            project.store_description(txt)
        except IOError:
            request.session.flash("Unable to find suitable readme file",
                                  'warning')

    loc = request.route_url('project_view_home', pid=pid)
    return HTTPFound(location=loc)
