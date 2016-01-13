import os
import sys
import transaction
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from sqlalchemy import engine_from_config
from ..models import Base, DBSession
from seeweb.models.project import Project
from seeweb.models.user import User


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)

    config_uri = argv[1]
    options = parse_vars(argv[2:])

    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        session = DBSession()

        users = []

        for i in range(4):
            username = "user%d" % i
            user = User(username=username,
                        email="%s@gmail.com" % username,
                        name="toto %s" % username,
                        public_profile=False)
            session.add(user)
            users.append(user)

        user = users[0]
        user.public_profile = True
        session.add(user)

        projects = []

        for i in range(5):
            name = "pjt%d" % i
            project = Project(name=name,
                              owner="user%d" % (i % 4),
                              public=False)
            session.add(project)
            projects.append(project)

            users[i % 4].projects.append(project)

        projects[0].public = True
        session.add(projects[0])

        for user in users:
            session.add(user)
