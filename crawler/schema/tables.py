from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey

DeclarativeBase = declarative_base()

class Project(DeclarativeBase):
    __tablename__ = 'projects'

    id = Column('id', Integer, primary_key=True)
    url = Column('url', String, unique=True, nullable=False)
    title = Column('title', String)
    headline = Column('headline', Integer)
    hackathon = Column('hackathon', String)
    text = Column('text', String)
    builtwith = Column('builtwith', String)
    likes = Column('likes', Integer)
    winner = Column('winner', String)
    # developers = Column('developers', String)
    # created_by = Column('created_by', String)

    def __repr__(self):
        return "<Project({0})>".format(self.title)

    

class Token(DeclarativeBase):
    __tablename__ = 'tokens'
    
    id = Column('id', Integer, primary_key=True)
    project_id = Column('project_id', Integer, ForeignKey(Project.id), nullable=False)
    start = Column('begin', Integer, nullable=False)
    end = Column('end', Integer, nullable=False)
    pos = Column('pos', String)


