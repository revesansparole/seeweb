from .auth import Role
from .comment import Comment
from .models import DBSession
from .project import Project
from .team import Team
from .user import User


def get_project(pid):
    """Fetch a given project in the database
    """
    session = DBSession()

    projects = session.query(Project).filter(Project.id == pid).all()
    if len(projects) == 0:
        return None

    project, = projects

    return project


def get_team(tid):
    """Fetch a given team from the database
    """
    session = DBSession()
    teams = session.query(Team).filter(Team.id == tid).all()
    if len(teams) == 0:
        return None

    team, = teams

    return team


def get_user(uid):
    """Fetch a given user from the database
    """
    session = DBSession()
    users = session.query(User).filter(User.id == uid).all()
    if len(users) == 0:
        return None

    user, = users

    return user


def fetch_comments(pid, limit=None):
    """Fectch all comments associated to a project.
    """
    session = DBSession()

    query = session.query(Comment).filter(Comment.project == pid).order_by(Comment.rating.desc())
    if limit is not None:
        query = query.limit(limit)

    comments = query.all()

    return comments


def project_access_role(project, uid):
    """Check the type of access granted to a user for a given project.

    args:
     - project (Project): project to check
     - uid (str): id of user willing to access project

    return:
     - role (Role): type of access granted to user
    """
    # user own project
    if project.owner == uid:
        return Role.edit

    # check project auth for this user
    for actor in project.auth:
        if actor.user == uid:
            return actor.role

    # project is public
    if project.public:
        return Role.read
    else:
        return Role.denied


def team_access_role(team, uid):
    """Check the type of access granted to a user for a given team.

    args:
     - team (Team): team to check
     - uid (str): id of user willing to access team

    return:
     - role (Role): type of access granted to user
    """
    role = Role.read

    # check team auth for this user
    i, actor = team.get_actor(uid)
    if actor is not None:
        role = actor.role
        if role == Role.denied:  # actually will never occur since denied
                                 # user are removed from the list
            return role

    # check team auth
    user = get_user(uid)
    for actor in team.auth_team:
        if user.is_member(actor.team):
            role = max(role, actor.role)

    # teams are public by default
    return role
