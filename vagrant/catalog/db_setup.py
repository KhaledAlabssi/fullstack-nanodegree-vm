#  from and import section





# user class as User should contain
#id, name, email and picture
class User(Base):
    __tablename__ = 'user'










# category class as Category with serializetion for json
#With id, name, user_id with foreignkey and user in relation


class Category(Base):
    __tablename__ = 'category'





    #serialize
    @property











# items class as Item should contain:
#id, name, date, description, picture, 
#category_id FK, category rel, user_id FK and user rel

class Items(Base):
    __tablename__ = 'items'







    #serialize
    @property




#creating the Database








