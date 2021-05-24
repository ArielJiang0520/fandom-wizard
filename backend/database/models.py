from .db import db
from sqlalchemy import Column, Integer
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class AO3(db.Model):
    db.Model.metadata.reflect(db.engine)
    __tablename__ = 'ao3'
    __table_args__ = {
        'autoload': True,
        'schema': 'public',
        'autoload_with': db.engine
    }
    index = Column(Integer, primary_key=True)


class VECTOR(db.Model):
    db.Model.metadata.reflect(db.engine)
    __tablename__ = 'vector'
    __table_args__ = {
        'autoload': True,
        'schema': 'public',
        'autoload_with': db.engine
    }
    index = Column(Integer, primary_key=True)


class WORD2VEC(db.Model):
    db.Model.metadata.reflect(db.engine)
    __tablename__ = 'word2vec'
    __table_args__ = {
        'autoload': True,
        'schema': 'public',
        'autoload_with': db.engine
    }
    index = Column(Integer, primary_key=True)


class AO3Schema(SQLAlchemyAutoSchema):
    class Meta:
        model = AO3
        include_relationships = True
        load_instance = True

    
