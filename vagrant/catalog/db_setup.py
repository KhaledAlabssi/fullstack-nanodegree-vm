#  from and import section
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


# user class as User should contain
# id, name, email and picture
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))

# category class as Category with serializetion for json
#With id, name, user_id with foreignkey and user in relation


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref='category')
    
    #serialize
    @property
    def serialize(self):
        return {
            'name':self.name,
            'id':self.id
        }

# items class as Item should contain:
#id, name, date, description, picture, 
#category_id FK, category rel, user_id FK and user rel

class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    date = Column(DateTime, nullable = False)
    description = Column(String(250))
    picture = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category,
    backref = backref('items', cascade = 'all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref = 'items')







    #serialize
    @property
    def serialize(self):
        return {
            'name':self.name,
            'id':self.id,
            'description':self.description,
            'picture':self.picture,
            'category':self.category
        }


#creating the Database
engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.create_all(engine)
