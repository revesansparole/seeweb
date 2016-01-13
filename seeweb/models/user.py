# import hashlib
from sqlalchemy import Boolean, Column, ForeignKey, String, Table
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


class User(Base):
    __tablename__ = 'users'

    id = Column(String(255), unique=True, primary_key=True)

    public_profile = Column(Boolean)

    projects = relationship("Project", secondary=user_to_projects)

    def __repr__(self):
        return "<User(id='%s')>" % self.id

    # def md5(self):
    #     return hashlib.md5(self.email.strip().lower()).hexdigest()
