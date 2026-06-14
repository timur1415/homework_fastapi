from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer,String, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String)
    password = Column(String)
    bio = Column(String)
    avatar = Column(String, default='😊')

    posts = relationship('Post', back_populates='user')


class Post(Base):
    __tablename__ = 'posts'


    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = Column(String)
    content = Column(String)
    image = Column(String)

    user = relationship('User', back_populates='posts')
