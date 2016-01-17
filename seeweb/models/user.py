# import hashlib
from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import relationship
from models import Base

user_to_projects = Table('asso_user_projects',
                         Base.metadata,
                         Column('user_id', String(255),
                                ForeignKey('users.id'),
                                primary_key=True),
                         Column('project_id', String(255),
                                ForeignKey('projects.id'),
                                primary_key=True),
                         )

user_to_teams = Table('asso_user_teams',
                      Base.metadata,
                      Column('user_id', String(255),
                             ForeignKey('users.id'),
                             primary_key=True),
                      Column('team_id', String(255),
                             ForeignKey('teams.id'),
                             primary_key=True),
                      )


class User(Base):
    __tablename__ = 'users'

    id = Column(String(255), unique=True, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    description = Column(Text, default="")

    projects = relationship("Project", secondary=user_to_projects)
    teams = relationship("Team", secondary=user_to_teams)

    def __repr__(self):
        return "<User(id='%s', name='%s', email='%s')>" % (self.id,
                                                           self.name,
                                                           self.email)

    # def md5(self):
    #     return hashlib.md5(self.email.strip().lower()).hexdigest()

    def is_member(self, tid):
        """Check if user is a member of the given team
        """
        for team in self.teams:
            if team.id == tid:
                return True

        return False
