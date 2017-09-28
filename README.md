# udacity-FSND-item_catalog

### Overview

Item Catalog is a RESTful web applicaiton using Flask with CRUD operations to a SQL Database with oauth authentication.

*Python, OAUTH, CRUD, Flask Framework, Bootstrap, PSQL*

![Image of app](https://github.com/dsenze/udacity-FSND-item_catalog/blob/master/static/images/blob/startpage.PNG)

### Features:
	* CRUD Operations
	* Facebook user registration 
	* User permissions for ADD/CREATE/EDIT
		- public user can view all items including query public API.
		- registred FB users can create and update own items.
		- admins can modify all items including add new categorys/subcategorys/itemcategorys.
	* Registred users have possibility to request Admin Access in settings menu
	* Registred users have personalised 'my items view' to see all items that can be edited.
	* Upload and change pictures
	* Public API

### API

#### Base Url : http://localhost:5000/catalog/api/v1.0

**Get Item by id**
/item/{itemid(int)}/JSON

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

**Get Item by id**
/category/{categoryid(int)}/JSON
**/category/{categoryid(int)}/subcategorys/JSON**
**/subcategory/{subcategoryid(int)}/JSON**
**/subcategory/{subcategoryid(int)}/itemcategorys/JSON**
**/itemcategory/{itemcategoryid(int)}/JSON**
**/itemcategory/{itemcategoryid(int)}/items/JSON**

### Files in project

#### Tester.py:
run this program to test all endpoints and get a summary of broken URLs.

![Image of tester.py](https://github.com/dsenze/udacity-FSND-item_catalog/blob/master/static/images/blob/tester.PNG)





### How to Install

### Prerequriements

