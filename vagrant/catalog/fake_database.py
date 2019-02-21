from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import *
import datetime


engine = create_engine('sqlite:///item_catalog.db')
Base.metadata = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
#delete all table and create new
session.query(User).delete()
session.query(Category).delete()
session.query(Items).delete()

#fake user, category and item
User1 = User(name='Nini Keck', email='nini@hello.com',
                picture='https://cdn.pixabay.com/photo/2015/03/04/22/35/head-659651_960_720.png')
session.add(User1)
session.commit()

Category1 = Category(name='Car', user_id=1)
session.add(Category1)
session.commit()


Item1 = Items(name='Steering', date=datetime.datetime.now(),
description='useful to direct the car :)', picture='https://dummyimage.com/300/09f.png/fff',
category_id=1, user_id=1)
session.add(Item1)
session.commit()


