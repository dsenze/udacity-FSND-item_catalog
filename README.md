# udacity-FSND-item_catalog

### Overview

Item Catalog is a RESTful web applicaiton using Flask with CRUD operations to a SQL Database with oauth authentication.

*Python, OAUTH, CRUD, Flask Framework, Bootstrap, PSQL,grunt*

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

### API DOC

https://github.com/dsenze/udacity-FSND-item_catalog/blob/master/api-doc.md

### Files in project
* model.py
	- contains the database model for the application
* add_data.py
    - adds some dummy data to database.
* application.py
    - contains the application. 
* UPLOAD
    - used to temporary store uploaded files, app crash if this folders does not exist.
* Templates
    - contains all html templates for the project
* static
    - contains compressed CSS and Images
* fb_clients_secrets.json
    - contains appid/secret to your application in facebook developer account (Must be updated with your Application, see install instructions)
* sourcefiles
    - can be ignored. used for cleanup operations with grunt.
* Tester.py
    - run this program to test all endpoints and get a summary of broken URLs.

![Image of tester.py](https://github.com/dsenze/udacity-FSND-item_catalog/blob/master/static/images/blob/tester.PNG)





### How to Install

### Prerequriements

