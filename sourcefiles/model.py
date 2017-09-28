import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import random, string


Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    picture = Column(String(250))
    role = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)

    # for json
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'username': self.username,
            'picture': self.picture,
            'role': self.role,
            'name': self.name
        }

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    picture = Column(String(250), nullable=False)
    # for json
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'picture': self.picture,
            'id': self.id
        }

class SubCategory(Base):
    __tablename__ = 'subcategory'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    categoryid = Column(Integer, ForeignKey('category.id'))
    picture = Column(String(250), nullable=False)
    # for json
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'picture': self.picture,
            'id': self.id,
            'categoryid': self.categoryid
        }
class ItemCategory(Base):
    __tablename__ = 'itemcategory'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    subcategoryid = Column(Integer, ForeignKey('subcategory.id'))
    picture = Column(String(250), nullable=False)
    # for json
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'picture': self.picture,
            'id': self.id,
            'subcategoryid': self.subcategoryid
        }

class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    price = Column(String(250))
    description = Column(String(250))
    dateadded = Column(DateTime, default=datetime.datetime.utcnow)
    datemodified = Column(DateTime, default=datetime.datetime.utcnow)
    picture = Column(String(250), nullable=False)
    owner = Column(Integer, ForeignKey('user.id'))
    categoryid = Column(Integer, ForeignKey('category.id'))
    subcategoryid = Column(Integer, ForeignKey('subcategory.id'))
    itemcategoryid = Column(Integer, ForeignKey('itemcategory.id'))
        # for json
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'dateadded': self.dateadded,
            'datemodified': self.datemodified,
            'picture': self.picture,
            'owner': self.owner,
            'categoryid': self.categoryid,
            'subcategoryid': self.subcategoryid,
            'itemcategoryid': self.itemcategoryid
        }
engine = create_engine('sqlite:///items.db')


Base.metadata.create_all(engine)