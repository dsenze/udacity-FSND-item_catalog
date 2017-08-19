from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User,Category,SubCategory,ItemCategory,Items,Base

engine = create_engine('sqlite:///items.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create user
User1 = User(name="Tommy Vadman", email="tommy.vadman@outlook.com",
             picture='https://media.licdn.com/mpr/mpr/shrinknp_200_200/p/7/005/04f/110/03f078d.jpg', role="admin")
session.add(User1)
session.commit()

# create Category
category = Category(name="Sport",id=1,picture="category/1/Sport.png")
session.add(category)
session.commit()

category2 = Category(name="Health",id=2,picture="category/2/Health.png")
session.add(category2)
session.commit()

# create SubCategory
subcategory = SubCategory(name="Golf",categoryid=1,picture="subcategory/1/Golf.png")

session.add(subcategory)
session.commit()

subcategory2 = SubCategory(name="Yoga",categoryid=2,picture="subcategory/2/Yoga.png")

session.add(subcategory2)
session.commit()

subcategory3 = SubCategory(name="Fotbool",categoryid=1,picture="subcategory/2/Yoga.png")

session.add(subcategory3)
session.commit()

# create ItemCategory
itemcategory = ItemCategory(name="Balls",subcategoryid=1,picture="itemcategory/2/balls.png")

session.add(itemcategory)
session.commit()

itemcategory2 = ItemCategory(name="Videos",subcategoryid=2,picture="itemcategory/2/Yoga.png")

session.add(itemcategory2)
session.commit()

itemcategory3 = ItemCategory(name="Woods",subcategoryid=1,picture="itemcategory/2/Yoga.png")

session.add(itemcategory3)
session.commit()
# create Item
item = Items(id=1,name="TITLEIST PRO V1",price="60$",description="Best ball",
picture="http://www.lannasport.se/images/2.1335053/titleist-pro-v1.jpeg",
categoryid=1,subcategoryid=1,itemcategoryid=1)

session.add(item)
session.commit()

item = Items(id=2,name="Yoga for Beginners: Boxed Se",price="20$",description="AM-PM Yoga for Beginners",
picture="https://images-na.ssl-images-amazon.com/images/I/71V8MVS8t5L._SX522_.jpg",
categoryid=2,subcategoryid=2,itemcategoryid=2)

session.add(item)
session.commit()

print "added items!"