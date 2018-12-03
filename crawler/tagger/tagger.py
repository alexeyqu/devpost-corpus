import os, logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.engine.url import URL

import nltk
from nltk.tokenize.treebank import TreebankWordTokenizer

from schema.tables import Project, Token, DeclarativeBase

logger = logging.getLogger(__name__)

class Tagger(object):
    def __init__(self, settings):
        self.database = settings.get('DATABASE')
        nltk.download('punkt')
        self.sent_tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
        self.word_tokenizer = TreebankWordTokenizer()
        
    def make_tagging(self):
        engine = create_engine(URL(**self.database), poolclass=NullPool)
        session = sessionmaker(bind=engine)()
        
        DeclarativeBase.metadata.create_all(engine, checkfirst=True)
        
        logger.warn('clearing tokens table')
        session.query(Token).delete() # remove old tokens # .filter(Token.project_id == project.id)
        projects = session.query(Project.id, Project.text).all()
        tokens = []
        
        BATCH_SIZE = 2000
        batch_row = 1
        for project in projects:
            if project.text is None:
                logger.warn('project #{} has empty descritpion, unable to tokenize'.format(project.id))
                continue
            old_tagged = len(tokens)
            sents_coords = self.sent_tokenizer.span_tokenize(project.text)
            for i in range(len(sents_coords) - 1):
                tokens.append(Token(project_id=project.id, start=sents_coords[i][1], end=sents_coords[i+1][0], pos='<EOS>'))
            if len(sents_coords) > 0:
                tokens.append(Token(project_id=project.id, start=sents_coords[-1][1], end=len(project.text), pos='<EOS>'))
            
            for sent_coords in sents_coords:
                sent = project.text[sent_coords[0]:sent_coords[1]]
                # TreebankWordTokenizer doesn't support span_tokenize yet.
                # The work is on the way, but currently we can only implement it by ourselves
                words = self.word_tokenizer.tokenize(sent)
                i = 0
                for word, pos in nltk.pos_tag(words):
                    i = sent.find(word, i)
                    if i >= 0:
                        tokens.append(Token(project_id=project.id, pos=pos,
                            start=(sent_coords[0] + i), end=(sent_coords[0] + i + len(word))))
            
            logger.warn('tagged {} tokens for project #{}'.format(len(tokens) - old_tagged, project.id))
            if batch_row % BATCH_SIZE == 0:
                logger.warn('committing batch')
                session.add_all(tokens)
                session.commit()
                tokens = []
            batch_row += 1

        
        logger.warn('committing the last batch')
        session.add_all(tokens)
        session.commit()
        session.close()

