# udacity-FSND-item_catalog

### Overview

Item Catalog is a RESTful web application using Flask with CRUD operations to a SQL Database with oauth authentication.

*Python, OAUTH, CRUD, Flask Framework, Bootstrap, PSQL, grunt*

![Image of app](https://github.com/dsenze/udacity-FSND-item_catalog/blob/master/static/images/blob/startpage.PNG)

### Features:
* CRUD Operations
* Facebook user registration 
* User permissions for ADD/CREATE/EDIT
    - public user can view all items including query public API.
	- registered FB users can create and update own items.
	- admins can modify all items including add new categorys/subcategorys/itemcategorys.
* Registered users have possibility to request Admin Access in settings menu
* Registered users have personalised 'my items view' to see all items that can be edited.
* Upload and change pictures	
* Public API

### PRE Requirements
Vagrant, Virtualbox and Udacity vagrant VM preconfigured machine.

- https://www.vagrantup.com/
- https://www.virtualbox.org/wiki/Downloads
- https://github.com/udacity/fullstack-nanodegree-vm

### API DOC

Follow url to API Documentation:

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
1. Install all prereqs.

2. git clone https://github.com/udacity/fullstack-nanodegree-vm
3. git clone https://github.com/dsenze/udacity-FSND-item_catalog.git

4. copy all from udacity-FSND-item-catalog to fullstack-nanodegree-vm/vagrant/catalog
5. update fb_client_secrets.json with Facebook APPID and Secret
	- you have to create an facebook app (https://developers.facebook.com/docs/apps/register/)
	- add site URL (http://localhost:5000/) under https://developers.facebook.com/apps/{yourappid}/settings/ . **Select (+add platform / website)** 

##### Start VagrantVM and deploy APP.
*TYPE in terminal*
6. cd fullstack-nanodegree-vm/vagrant/
7. vagrant up
8. vagrant ssh
9. cd /vagrant/catalog

##### Setup DB, ADD Data and start Application (must be runned in specified sequence.)

*TYPE in terminal*
10. python model.py
11. python add_data.py
12. python application.py

go web browser : https://localhost:5000 and have some fun! :)



