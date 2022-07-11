from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import datetime
# from db.database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    ads = relationship("Ad", back_populates="owner")
    drafts = relationship("Draft", back_populates="owner")
    groups = relationship('Group', secondary='user_groups', back_populates='users')


class Group(Base):
    __tablename__ = "groups"
    region = Column(String)
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    users = relationship('User', secondary='user_groups', back_populates='groups')


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))


class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=True)
    body = Column(String(10000), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    state = Column(String(10), index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="ads")


class Draft(Base):
    __tablename__ = "drafts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=True)
    body = Column(String(10000), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    state = Column(String(10), index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="drafts")


if __name__ == "__main__":

    SQLALCHEMY_DATABASE_URL = "postgresql://marat:1q2w3e4r5t@localhost/fastapi"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )

    from datetime import datetime
    with Session(bind=engine) as session:

        # user = User(email='fgfffffffffgfgffffffff')
        user = session.query(User).get(2)
        user.email ='11kд1д8k;сhgпкk17'

        # group = session.query(Group).get(1)
        # user.groups = [group]
        session.add(user)
        session.commit()
