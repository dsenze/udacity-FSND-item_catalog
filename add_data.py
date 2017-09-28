from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import User, Category, SubCategory, ItemCategory, Items, Base

# Add some contents to DB for fist use.

engine = create_engine('sqlite:///items.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create user endpoint tester for future endpoint tests tester.py
User1 = User(name="endpointtester", username="endpointtester@outlook.com",
             picture="", role="admin")
session.add(User1)
session.commit()

# create Category
category = Category(
    name="Sport",
    id=1,
    picture="images/category/1/golf_tiger.jpg")
session.add(category)
session.commit()

category2 = Category(name="Health", id=2, picture="images/category/2/yoha.jpg")
session.add(category2)
session.commit()

# create SubCategory
subcategory = SubCategory(
    name="Golf",
    categoryid=1,
    picture="images/category/1/golf_tiger.jpg")

session.add(subcategory)
session.commit()

subcategory2 = SubCategory(
    name="Yoga",
    categoryid=2,
    picture="images/category/2/yoha.jpg")

session.add(subcategory2)
session.commit()

subcategory3 = SubCategory(
    name="Fotboll",
    categoryid=1,
    picture="images/category/3/fotballs2.jpg")

session.add(subcategory3)
session.commit()

subcategory4 = SubCategory(
    name="Food",
    categoryid=2,
    picture="images/subcategory/4/food.jpg")

session.add(subcategory4)
session.commit()

# create ItemCategory
itemcategory = ItemCategory(
    name="Balls",
    subcategoryid=1,
    picture="images/itemcategory/1/fotball1.jpg")

session.add(itemcategory)
session.commit()

itemcategory2 = ItemCategory(
    name="Videos",
    subcategoryid=2,
    picture=(
        "images/category/2/Untitled_" +
        "81092d59-de4e-47f0-b678-764956c045fc.png"
    )
    )

session.add(itemcategory2)
session.commit()

itemcategory3 = ItemCategory(
    name="Drivers",
    subcategoryid=1,
    picture="images/category/3/golf_driver.jpg")

session.add(itemcategory3)
session.commit()

itemcategory4 = ItemCategory(
    name="vegan",
    subcategoryid=4,
    picture="images/itemcategory/4/veganfood.jpg")

session.add(itemcategory4)
session.commit()

itemcategory5 = ItemCategory(
    name="Balls",
    subcategoryid=3,
    picture="images/category/5/fotball1.jpg")

session.add(itemcategory5)
session.commit()
# create Item
item = Items(id=1, name="TITLEIST PRO V1", price="60$", description=(
    "New Titleist Pro V1 and Pro V1x golf" +
    "balls offer total performance for every player."
    ),
             picture="images/item/1/golfball2.jpg",
             categoryid=1, subcategoryid=1, itemcategoryid=1, owner=1)

session.add(item)
session.commit()

item2 = Items(
    name="Yoga for Beginners: Boxed Se", price="20$",
    description="AM-PM Yoga for Beginners",
    picture="images/item/2/Untitled_81092d59-de4e-47f0-b678-764956c045fc.png",
    categoryid=2, subcategoryid=2, itemcategoryid=2
    )
session.add(item2)
session.commit()

item3 = Items(name="carrot", price="20$", description=(
    "he carrot (Daucus carota subsp. sativus) is a root vegetable," +
    "usually orange in colour, though purple, black, red, white, " +
    "and yellow cultivars exist. Carrots are a domesticated form of" +
    "the wild carrot, Daucus carota, native to Europe and southwestern" +
    "Asia. The plant probably originated in Persia and was originally" +
    "cultivated for its leaves and seeds. The most commonly eaten part" +
    "of the plant is the taproot, although the greens are sometimes" +
    "eaten as well.The domestic carrot has been selectively bred" +
    "for its greatly enlarged," +
    "more palatable, less woody-textured taproot."
), picture="images/item/3/carrot.jpg", categoryid=2,
    subcategoryid=4, itemcategoryid=4)
session.add(item3)
session.commit()

item4 = Items(name="CHROME SOFT GOLF BALLS", price="39$", description="",
              picture="images/item/5/callaway_golfball.jpg",
              categoryid=1, subcategoryid=1, itemcategoryid=1)

session.add(item4)
session.commit()

item5 = Items(name="Wilson driver", price="20$", description=(
    "best club in the world."
    ),
              picture="images/item/4/wilson_driver.jpg",
              categoryid=1, subcategoryid=1, itemcategoryid=3)

session.add(item5)
session.commit()

item6 = Items(name="Nike PRO ball", price="20$", description=(
    "best ball in the world."
    ),
              picture="images/item/6/fotball1.jpg",
              categoryid=1, subcategoryid=3, itemcategoryid=5)

session.add(item6)
session.commit()

item7 = Items(name="", price="20$", description="",
              picture="images/item/3/carrot.jp",
              categoryid=2, subcategoryid=4, itemcategoryid=4)

session.add(item7)
session.commit()


print "added items!"
