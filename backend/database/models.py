from .db import db
from sqlalchemy import Column, Integer, String
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class AO3Table(db.Model):
    db.Model.metadata.reflect(db.engine)
    __tablename__ = 'ao3'
    __table_args__ = {
        'autoload': True,
        'schema': 'public',
        'autoload_with': db.engine
    }
    index = Column(Integer, primary_key=True)


class MatrixTable(db.Model):
    db.Model.metadata.reflect(db.engine)
    __tablename__ = 'matrix'
    __table_args__ = {
        'autoload': True,
        'schema': 'public',
        'autoload_with': db.engine
    }
    index = Column(Integer, primary_key=True)


class Word2vecTable(db.Model):
    db.Model.metadata.reflect(db.engine)
    __tablename__ = 'word2vec'
    __table_args__ = {
        'autoload': True,
        'schema': 'public',
        'autoload_with': db.engine
    }
    key = Column(String, primary_key=True)


class AO3Schema(SQLAlchemyAutoSchema):
    class Meta:
        model = AO3Table
        include_relationships = True
        load_instance = True

    
