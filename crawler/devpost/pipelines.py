# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os, logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from scrapy.exceptions import DropItem
from scrapy import signals
from devpost.items import ProjectItem

logger = logging.getLogger(__name__)

DeclarativeBase = declarative_base()

class Project(DeclarativeBase):
	__tablename__ = 'projects'

	url = Column('url', String, primary_key=True)
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


class SqlitePipeline(object):
	def __init__(self, settings):
		self.database = settings.get('DATABASE')
		self.sessions = {}

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls(crawler.settings)
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def create_engine(self):
		engine = create_engine(URL(**self.database), poolclass=NullPool)
		return engine

	def create_tables(self, engine):
		DeclarativeBase.metadata.create_all(engine, checkfirst=True)

	def create_session(self, engine):
		session = sessionmaker(bind=engine)()
		return session

	def spider_opened(self, spider):
		engine = self.create_engine()
		self.create_tables(engine)
		session = self.create_session(engine)
		self.sessions[spider] = session

	def spider_closed(self, spider):
		session = self.sessions.pop(spider)
		session.close()

	def process_item(self, item, spider):
		session = self.sessions[spider]
		project = Project(**item)
		link_exists = session.query(Project).filter_by(url=item['url']).first() is not None

		if link_exists:
			logger.info('Item {} is in db'.format(project))
			return item

		try:
			session.add(project)
			session.commit()
			logger.info('Item {} stored in db'.format(project))
		except:
			logger.info('Failed to add {} to db'.format(project))
			session.rollback()
			raise

		return item