import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

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

    advertisements = relationship("Advertisement", back_populates="owner")
    tokens = relationship("Token", back_populates="user")
    groups = relationship("Group", secondary="user_groups", back_populates="user")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(
        Integer,
        primary_key=True,
    )
    token = Column(
        String,
        server_default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
        index=True,
    )
    expires = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tokens")


class Group(Base):
    __tablename__ = "groups"
    region = Column(String)
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    user = relationship("User", secondary="user_groups", back_populates="groups")


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True)
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))


class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=True)
    body = Column(String(10000), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    state = Column(String(10))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    owner = relationship("User", back_populates="advertisements")
