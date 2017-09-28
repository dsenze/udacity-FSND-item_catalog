## API DOC

### Base Url : http://localhost:5000/catalog/api/v1.0

**Get Item by id**
/item/{itemid}/JSON

returns:

    id
    name
    price
    description
    dateadded
    datemodified
    picture
    owner
    categoryid
    subcategoryid
    itemcategoryid

**Get category by id**
/category/{categoryid}/JSON

returns:

    id
    name
    picture

**Get subcategorys by categoryid**
/category/{categoryid)}/subcategorys/JSON

returns:

    id
    categoryid
    name
    picture

**Get subcategory by id**
/subcategory/{subcategoryid}/JSON

returns:

    id
    name
    picture

**Get itemcategorys by subcategoryid**
/subcategory/{subcategoryid}/itemcategorys/JSON

returns:

    id
    subcategoryid
    name
    picture

**Get itemcategory by id**
/itemcategory/{itemcategoryid}/JSON
returns:

    id
    name
    picture

**Get items by itemcategoryid**
/itemcategory/{itemcategoryid}/items/JSON

    id
    name
    price
    description
    dateadded
    datemodified
    picture
    owner
    categoryid
    subcategoryid
    itemcategoryid
    
## EXAMPLE

GET http://localhost:5000/catalog/api/v1.0/itemcategory/1/items/JSON

Response: 

{
  "ItemCategorys": [
    {
      "categoryid": 1, 
      "dateadded": "Thu, 28 Sep 2017 19:21:45 GMT", 
      "datemodified": "Thu, 28 Sep 2017 19:21:45 GMT", 
      "description": "New Titleist Pro V1 and Pro V1x golfballs offer total performance for every player.", 
      "id": 1, 
      "itemcategoryid": 1, 
      "name": "TITLEIST PRO V1", 
      "owner": 1, 
      "picture": "images/item/1/golfball2.jpg", 
      "price": "60$", 
      "subcategoryid": 1
    }, 
    {
      "categoryid": 1, 
      "dateadded": "Thu, 28 Sep 2017 19:21:45 GMT", 
      "datemodified": "Thu, 28 Sep 2017 19:21:45 GMT", 
      "description": "", 
      "id": 4, 
      "itemcategoryid": 1, 
      "name": "CHROME SOFT GOLF BALLS", 
      "owner": null, 
      "picture": "images/item/5/callaway_golfball.jpg", 
      "price": "39$", 
      "subcategoryid": 1
    }
  ]
}
